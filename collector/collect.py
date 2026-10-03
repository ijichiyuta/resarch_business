"""TikTokアカウント収集 (F-01, F-02)

vad-dashboard の lib/tiktok.ts (RapidAPI tiktok-scraper7) をPythonに移植したもの。
プロフィール情報と直近の動画メタデータを取得し、data/<handle>/ にJSONで保存する。

必要な環境変数: RAPIDAPI_KEY (任意: TIKTOK_API_HOST)

使い方:
    python3 collector/collect.py <handle または プロフィールURL> [--limit 100]
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HOST = os.environ.get("TIKTOK_API_HOST", "tiktok-scraper7.p.rapidapi.com")
KEY = os.environ.get("RAPIDAPI_KEY")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def api_get(path: str, params: dict, retries: int = 3, delay: float = 2.0) -> dict:
    url = f"https://{HOST}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "x-rapidapi-key": KEY,
        "x-rapidapi-host": HOST,
    })
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                return json.load(res)
        except Exception as e:  # 5xx/ネットワークはリトライ
            if i == retries - 1:
                raise
            print(f"[retry {i+1}/{retries}] {e}", file=sys.stderr)
            time.sleep(delay * (i + 1))
    raise RuntimeError("unreachable")


def parse_handle(arg: str) -> str:
    m = re.search(r"tiktok\.com/@([\w.\-]+)", arg)
    return (m.group(1) if m else arg).lstrip("@").strip()


def fetch_user(handle: str) -> dict:
    j = api_get("/user/info", {"unique_id": handle})
    if j.get("code") != 0 or not j.get("data"):
        raise RuntimeError(f"user/info failed: {j.get('msg')}")
    u, s = j["data"]["user"], j["data"]["stats"]
    return {
        "platform": "tiktok",
        "handle": u["uniqueId"],
        "profile_url": f"https://www.tiktok.com/@{u['uniqueId']}",
        "display_name": u["nickname"],
        "bio": u.get("signature", ""),
        "follower_count": s.get("followerCount"),
        "video_count": s.get("videoCount"),
        "heart_count": s.get("heartCount"),
        "sec_uid": u.get("secUid"),
        "collected_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def fetch_videos(handle: str, limit: int = 100) -> list[dict]:
    """直近limit本のメタを新しい順に取得。play/music URLは署名付きで短命な点に注意。"""
    videos: list[dict] = []
    cursor = "0"
    pages = 0
    while len(videos) < limit and pages < 50:
        pages += 1
        j = api_get("/user/posts", {"unique_id": handle, "cursor": cursor, "count": 35})
        if j.get("code") != 0 or not j.get("data"):
            print(f"[warn] user/posts code={j.get('code')} msg={j.get('msg')}", file=sys.stderr)
            break
        posts = j["data"].get("videos", [])
        if not posts:
            break
        for p in posts:
            videos.append({
                "video_id": p["video_id"],
                "video_url": f"https://www.tiktok.com/@{handle}/video/{p['video_id']}",
                "caption": p.get("title", ""),
                "posted_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(p["create_time"])),
                "view_count": p.get("play_count"),
                "like_count": p.get("digg_count"),
                "comment_count": p.get("comment_count"),
                "share_count": p.get("share_count"),
                "duration_sec": p.get("duration"),
                "is_top": p.get("is_top"),
                "play_url": p.get("play"),      # 透かしなし動画 (署名付き・数日で失効)
                "music_url": p.get("music"),    # 音声トラック
            })
        if not j["data"].get("hasMore"):
            break
        cursor = str(j["data"]["cursor"])
        time.sleep(0.8)  # レート制限への配慮 (元実装と同じ)

    # ピン留めで順序が乱れるので投稿日降順に整え、重複を除去して上限を適用
    uniq = {v["video_id"]: v for v in videos}
    ordered = sorted(uniq.values(), key=lambda v: v["posted_at"], reverse=True)
    return ordered[:limit]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("account", help="ハンドル名 または プロフィールURL")
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()

    if not KEY:
        sys.exit("RAPIDAPI_KEY が未設定です (vad-dashboard/.env.local から export してください)")

    handle = parse_handle(args.account)
    out = DATA_DIR / handle
    out.mkdir(parents=True, exist_ok=True)

    print(f"[1/2] user/info: @{handle}")
    account = fetch_user(handle)
    (out / "account.json").write_text(json.dumps(account, ensure_ascii=False, indent=2))
    print(f"      {account['display_name']} / followers={account['follower_count']} / videos={account['video_count']}")

    print(f"[2/2] user/posts: 直近{args.limit}本まで")
    videos = fetch_videos(handle, args.limit)
    (out / "videos.json").write_text(json.dumps(videos, ensure_ascii=False, indent=2))
    total_sec = sum(v["duration_sec"] or 0 for v in videos)
    print(f"      取得 {len(videos)}本 / 合計 {total_sec//60}分{total_sec%60}秒 / 保存先 {out}")


if __name__ == "__main__":
    main()
