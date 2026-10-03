"""音声取得+文字起こし (F-03, F-04)

play_url から動画をDL → ffmpegで音声抽出 → Gemini で文字起こし。
原語のまま保存する(翻訳しない)。処理後に音声・動画ファイルは削除する。
transcripts/<video_id>.json が既にあればスキップ (冪等性、コスト直結)。

必要な環境変数: GOOGLE_API_KEY

使い方:
    python3 collector/transcribe.py <handle> [--limit 5]
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

PROMPT = (
    "この音声を一字一句、話された言語のまま文字起こししてください。翻訳しないでください。"
    "BGMや効果音は無視し、話者の発話のみを書き起こします。"
    "内容はビジネス・起業・経営の話です。同音異義語は文脈に合う表記を選んでください"
    "（例:「こうりぎょう」は氷業ではなく小売業、「こうり」は高利ではなく小売など）。"
    '次のJSONだけを返してください: {"language": "ISO 639-1コード", "text": "文字起こし全文"} '
    "発話が全く無い場合は text を空文字にしてください。"
)


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as res, open(dest, "wb") as f:
        f.write(res.read())


def extract_audio(video: Path, audio: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
         "-b:a", "48k", str(audio)],
        check=True, capture_output=True,
    )


def gemini_transcribe(audio: Path, retries: int = 3) -> dict:
    b64 = base64.b64encode(audio.read_bytes()).decode()
    body = json.dumps({
        "contents": [{"parts": [
            {"text": PROMPT},
            {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
        ]}],
        "generationConfig": {"response_mime_type": "application/json", "temperature": 0},
    }).encode()
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{GEMINI_MODEL}:generateContent?key={GOOGLE_API_KEY}")
    for i in range(retries):
        try:
            req = urllib.request.Request(url, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as res:
                j = json.load(res)
            text = j["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)
        except Exception as e:
            if i == retries - 1:
                raise
            print(f"[retry {i+1}/{retries}] {e}", file=sys.stderr)
            time.sleep(5 * (i + 1))
    raise RuntimeError("unreachable")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("handle")
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()

    if not GOOGLE_API_KEY:
        sys.exit("GOOGLE_API_KEY が未設定です")

    base = DATA_DIR / args.handle
    videos = json.loads((base / "videos.json").read_text())[: args.limit]
    tdir = base / "transcripts"
    tdir.mkdir(exist_ok=True)

    done = skipped = failed = 0
    for i, v in enumerate(videos, 1):
        out = tdir / f"{v['video_id']}.json"
        if out.exists():
            skipped += 1
            continue
        label = f"[{i}/{len(videos)}] {v['video_id']} ({v['duration_sec']}s)"
        try:
            with tempfile.TemporaryDirectory() as tmp:
                mp4 = Path(tmp) / "v.mp4"
                mp3 = Path(tmp) / "a.mp3"
                download(v["play_url"], mp4)
                extract_audio(mp4, mp3)
                result = gemini_transcribe(mp3)
            out.write_text(json.dumps({
                "video_id": v["video_id"],
                "language": result.get("language"),
                "text": result.get("text", ""),
                "model": GEMINI_MODEL,
            }, ensure_ascii=False, indent=2))
            done += 1
            print(f"{label} OK lang={result.get('language')} chars={len(result.get('text', ''))}")
        except Exception as e:
            failed += 1
            print(f"{label} FAILED: {e}", file=sys.stderr)
        time.sleep(1)

    print(f"完了 {done} / スキップ {skipped} / 失敗 {failed}")


if __name__ == "__main__":
    main()
