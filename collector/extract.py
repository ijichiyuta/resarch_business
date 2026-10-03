"""動画単位のLLM抽出 (F-05)

prompts/extract_video.md のSystemプロンプトを使い、文字起こしを§7スキーマの
JSONに構造化する。出力はClaudeの構造化出力(output_config.format)で保証する。
extractions/<video_id>.json が既にあればスキップ (冪等性)。

必要な環境変数: ANTHROPIC_API_KEY

使い方:
    python3 collector/extract.py <handle> [--limit 5]
"""

import argparse
import json
import sys
from pathlib import Path

import anthropic

MODEL = "claude-opus-4-8"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

# Opus 4.8: $5 / $25 per 1M tokens
PRICE_IN, PRICE_OUT = 5.0, 25.0

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["has_business_content", "source_language", "topic", "business",
                 "numbers", "origin", "requirements", "failures", "claim_vs_fact",
                 "japan_applicability", "confidence"],
    "properties": {
        "has_business_content": {"type": "boolean"},
        "source_language": {"type": "string"},
        "topic": {"type": "string"},
        "business": {
            "type": "object", "additionalProperties": False,
            "required": ["what", "who", "how_much", "revenue_model"],
            "properties": {
                "what": {"type": ["string", "null"]},
                "who": {"type": ["string", "null"]},
                "how_much": {"type": ["string", "null"]},
                "revenue_model": {"type": ["string", "null"]},
            },
        },
        "numbers": {
            "type": "array",
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["label", "value", "is_verifiable"],
                "properties": {
                    "label": {"type": "string"},
                    "value": {"type": "string"},
                    "is_verifiable": {"type": "boolean"},
                },
            },
        },
        "origin": {
            "type": "object", "additionalProperties": False,
            "required": ["motivation", "initial_cost", "time_to_revenue", "prior_skill"],
            "properties": {
                "motivation": {"type": ["string", "null"]},
                "initial_cost": {"type": ["string", "null"]},
                "time_to_revenue": {"type": ["string", "null"]},
                "prior_skill": {"type": ["string", "null"]},
            },
        },
        "requirements": {"type": "array", "items": {"type": "string"}},
        "failures": {"type": "array", "items": {"type": "string"}},
        "claim_vs_fact": {
            "type": "object", "additionalProperties": False,
            "required": ["claims", "facts"],
            "properties": {
                "claims": {"type": "array", "items": {"type": "string"}},
                "facts": {"type": "array", "items": {"type": "string"}},
            },
        },
        "japan_applicability": {
            "anyOf": [
                {
                    "type": "object", "additionalProperties": False,
                    "required": ["score", "reason", "existing_jp_competitors"],
                    "properties": {
                        "score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                        "reason": {"type": "string"},
                        "existing_jp_competitors": {"type": "array", "items": {"type": "string"}},
                    },
                },
                {"type": "null"},
            ]
        },
        "confidence": {"type": "number"},
    },
}


def load_prompt_block(section: str) -> str:
    """prompts/extract_video.md の指定セクション直後のコードフェンス内を返す。"""
    text = (PROMPTS_DIR / "extract_video.md").read_text()
    after = text.split(section, 1)[1]
    return after.split("```", 2)[1].strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("handle")
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()

    base = DATA_DIR / args.handle
    videos = {v["video_id"]: v for v in json.loads((base / "videos.json").read_text())}
    tdir = base / "transcripts"
    edir = base / "extractions"
    edir.mkdir(exist_ok=True)

    system_prompt = load_prompt_block("## System プロンプト")
    user_template = load_prompt_block("## User プロンプト（テンプレート）")

    client = anthropic.Anthropic()
    total_in = total_out = 0
    done = skipped = failed = 0

    transcripts = sorted(tdir.glob("*.json"))[: args.limit]
    for i, tpath in enumerate(transcripts, 1):
        t = json.loads(tpath.read_text())
        v = videos.get(t["video_id"])
        if v is None:
            continue
        out = edir / f"{t['video_id']}.json"
        if out.exists():
            skipped += 1
            continue
        label = f"[{i}/{len(transcripts)}] {t['video_id']}"
        try:
            user_msg = user_template.format(
                video_url=v["video_url"], posted_at=v["posted_at"],
                view_count=v["view_count"], like_count=v["like_count"],
                duration_sec=v["duration_sec"], caption=v["caption"],
                transcript=t["text"],
            )
            resp = client.messages.create(
                model=MODEL,
                max_tokens=16000,
                thinking={"type": "adaptive"},
                system=system_prompt,
                messages=[{"role": "user", "content": user_msg}],
                output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
            )
            text = next(b.text for b in resp.content if b.type == "text")
            payload = json.loads(text)
            out.write_text(json.dumps({
                "video_id": t["video_id"],
                "payload": payload,
                "model": MODEL,
                "usage": {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens},
            }, ensure_ascii=False, indent=2))
            total_in += resp.usage.input_tokens
            total_out += resp.usage.output_tokens
            done += 1
            biz = "business" if payload["has_business_content"] else "非事業"
            print(f"{label} OK ({biz} / confidence={payload['confidence']})")
        except Exception as e:
            failed += 1
            print(f"{label} FAILED: {e}", file=sys.stderr)

    cost_usd = total_in / 1e6 * PRICE_IN + total_out / 1e6 * PRICE_OUT
    print(f"完了 {done} / スキップ {skipped} / 失敗 {failed}")
    print(f"トークン in={total_in} out={total_out} / 概算コスト ${cost_usd:.3f} (約{cost_usd*150:.0f}円)")


if __name__ == "__main__":
    main()
