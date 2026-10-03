"""アカウント統合レポート生成 (F-06)

全動画の抽出結果を prompts/generate_report.md のプロンプトで1枚のMarkdownに統合し、
reports/<handle>.md に保存する。

必要な環境変数: ANTHROPIC_API_KEY

使い方:
    python3 collector/report.py <handle>
"""

import argparse
import json
from pathlib import Path

import anthropic

MODEL = "claude-opus-4-8"
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PROMPTS_DIR = ROOT / "prompts"
REPORTS_DIR = ROOT / "reports"


def load_prompt_block(section: str) -> str:
    text = (PROMPTS_DIR / "generate_report.md").read_text()
    after = text.split(section, 1)[1]
    return after.split("```", 2)[1].strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("handle")
    args = ap.parse_args()

    base = DATA_DIR / args.handle
    account = json.loads((base / "account.json").read_text())
    videos = {v["video_id"]: v for v in json.loads((base / "videos.json").read_text())}

    extractions = []
    for p in sorted((base / "extractions").glob("*.json")):
        e = json.loads(p.read_text())
        v = videos.get(e["video_id"], {})
        extractions.append({
            "video_url": v.get("video_url"),
            "posted_at": v.get("posted_at"),
            "view_count": v.get("view_count"),
            **e["payload"],
        })

    system_prompt = load_prompt_block("## System プロンプト")
    user_msg = load_prompt_block("## User プロンプト（テンプレート）").format(
        handle=account["handle"],
        display_name=account["display_name"],
        follower_count=account["follower_count"],
        bio=account["bio"],
        n=len(extractions),
        extractions_json=json.dumps(extractions, ensure_ascii=False),
    )

    client = anthropic.Anthropic()
    with client.messages.stream(
        model=MODEL,
        max_tokens=32000,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        resp = stream.get_final_message()

    report = next(b.text for b in resp.content if b.type == "text")
    REPORTS_DIR.mkdir(exist_ok=True)
    out = REPORTS_DIR / f"{args.handle}.md"
    out.write_text(report)

    cost = resp.usage.input_tokens / 1e6 * 5 + resp.usage.output_tokens / 1e6 * 25
    print(f"保存: {out}")
    print(f"分析対象 {len(extractions)}本 / トークン in={resp.usage.input_tokens} "
          f"out={resp.usage.output_tokens} / 約{cost*150:.0f}円")


if __name__ == "__main__":
    main()
