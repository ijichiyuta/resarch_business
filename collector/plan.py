"""参入プラン生成

1アカウントの生データ（全文文字起こし）を根拠に、利用者本人が
その事業モデルを日本で実行するための具体的な参入プランを生成する。
出力: reports/<handle>_plan.md

必要な環境変数: ANTHROPIC_API_KEY

使い方:
    python3 collector/plan.py <handle> [--profile "利用者の特徴"]
"""

import argparse
import json
from pathlib import Path

import anthropic

MODEL = "claude-opus-4-8"
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"

DEFAULT_PROFILE = (
    "個人でWebサービス・アプリを一人で開発できるエンジニア（Next.js等でのサイト/SaaS開発経験が豊富）。"
    "コンテンツサイトの運営経験あり。TikTokでの発信は本人としては未実績。"
    "営業職の経験はない。初期資本は小さく始めたい。業種へのこだわりはなく、稼げるなら何でもやる方針。"
)

SYSTEM = """あなたは事業立ち上げの参謀です。あるTikTok経営者の全動画の文字起こし（生データ）と、
依頼者本人のプロフィールを渡します。この経営者のモデルを素材に、依頼者が実際に始めるための
参入プランを作ってください。

厳守事項:
1. すべての提案は生データ内の具体的な根拠（発言・数字）に紐づける。出典の動画URLを付ける。
   発信者の数字は本人申告で未検証であることを常に明示し、鵜呑みにした計画を立てない。
2. 依頼者のプロフィールに合わせる。発信者の強み（営業力・不動産経験）と依頼者の強み（開発力）は
   違う。発信者の構造のうち依頼者に移植可能な部品と、移植できない部品を明確に分ける。
3. プランは3案。それぞれに以下を必ず含める:
   - 何をやるか（1文で）
   - なぜこの人のデータがその根拠になるか
   - 初期投資と月次固定費の見積もり（発信者の実数を基準に）
   - 収益モデルと6ヶ月後の現実的な目標数字（強気ではなく、発信者の実績の下限を基準に）
   - 最初の30日でやることの具体的な手順
   - 撤退基準（発信者の「キャッシュがなくなったら失敗」論を数値化して適用）
   - 法規制・リスク
4. 3案の比較表を作り、最後に1案を推奨して理由を述べる。
5. 「実行前に必ず自分で検証すべき未確認事項」の章を設ける。発信者の主張に依存している前提を列挙する。
6. 誇大な期待を作らない。この経営者のデータから言えないことは「言えない」と書く。

Markdownで出力する。"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("handle")
    ap.add_argument("--profile", default=DEFAULT_PROFILE)
    args = ap.parse_args()

    base = DATA_DIR / args.handle
    account = json.loads((base / "account.json").read_text())
    videos = json.loads((base / "videos.json").read_text())
    tdir = base / "transcripts"
    videos.sort(key=lambda v: v["posted_at"])

    blocks = []
    for v in videos:
        tpath = tdir / f"{v['video_id']}.json"
        if not tpath.exists():
            continue
        t = json.loads(tpath.read_text())
        blocks.append(
            f"### 動画 {v['video_id']}\n"
            f"- URL: {v['video_url']} / 投稿日: {v['posted_at']} / 再生数: {v['view_count']}\n"
            f"- キャプション: {v['caption']}\n"
            f"- 文字起こし:\n{t['text']}\n"
        )

    user_msg = (
        f"## 依頼者プロフィール\n{args.profile}\n\n"
        f"## 分析対象の発信者\n"
        f"- @{account['handle']}（{account['display_name']}） / フォロワー {account['follower_count']}\n"
        f"- bio: {account['bio']}\n\n"
        f"## 全動画データ（{len(blocks)}本 / 古い順）\n\n" + "\n".join(blocks)
    )

    client = anthropic.Anthropic()
    with client.messages.stream(
        model=MODEL,
        max_tokens=64000,
        thinking={"type": "adaptive"},
        system=SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        resp = stream.get_final_message()

    plan = next(b.text for b in resp.content if b.type == "text")
    REPORTS_DIR.mkdir(exist_ok=True)
    out = REPORTS_DIR / f"{args.handle}_plan.md"
    out.write_text(plan)

    cost = resp.usage.input_tokens / 1e6 * 5 + resp.usage.output_tokens / 1e6 * 25
    print(f"保存: {out} / in={resp.usage.input_tokens} out={resp.usage.output_tokens} "
          f"/ 約{cost*150:.0f}円 / stop={resp.stop_reason}")


if __name__ == "__main__":
    main()
