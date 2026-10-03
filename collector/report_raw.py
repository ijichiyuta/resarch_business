"""生データ（全文文字起こし）ベースの詳細レポート生成

report.py が抽出JSON経由なのに対し、こちらは100本分の文字起こし全文を
そのままコンテキストに投入し、要約で情報を削らない網羅版を生成する。
出力: reports/<handle>_full.md

必要な環境変数: ANTHROPIC_API_KEY

使い方:
    python3 collector/report_raw.py <handle>
"""

import argparse
import json
from pathlib import Path

import anthropic

MODEL = "claude-opus-4-8"
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"

SYSTEM = """あなたは事業リサーチャーです。1人のTikTok発信者（経営者）の全動画の文字起こし（生データ）を渡します。
読者はこのレポートをもとに「この事業モデルを自分が日本でやるか」を判断します。

これは要約レポートではなく【網羅レポート】です。以下を厳守してください。

1. 情報を削らない。事業・収益・数字・手法・経緯に関する情報は、些細でもすべて拾う。
   「代表的なものを挙げる」「など」でまとめて省略することを禁止する。
2. 数字は全件列挙する。金額・期間・人数・率・単価は、語られた全動画分をもれなく表に載せる。
   必ず【主張】（本人申告で検証不能）か【事実】（第三者が確認可能）のラベルを付ける。
3. 本人の重要な発言は「」で原文のまま引用する。言い換えで意味を薄めない。
4. すべての情報に出典の動画URLを付ける。
5. 動画間で数字や説明が食い違う場合は、隠さずすべて矛盾として列挙する。
6. 事業ごとに章を立て、その事業について全動画で語られた内容を時系列で再構成する。
   （例: 賃貸仲介 / TikTok運用 / 小売・氷業 / Amazon物販 / バー・スナック / コンサル / 過去の代行業 / 前職時代）
7. ノウハウ・手法論（集客方法、営業手法、SNS運用術など）も専用の章で全件整理する。
   読者が実行手順として使えるレベルの粒度で書く。
8. 最後に「日本での再現性評価」（可否・法規制・必要リソース・国内競合・参入余地）と
   「信頼性の総括」（検証可能な事実の一覧、誇張の疑いがある箇所の一覧）を置く。

構成は上記を満たす限り自由。長くなることを恐れない。Markdownで出力する。"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("handle")
    args = ap.parse_args()

    base = DATA_DIR / args.handle
    account = json.loads((base / "account.json").read_text())
    videos = json.loads((base / "videos.json").read_text())
    tdir = base / "transcripts"

    # 古い順に並べて時系列を追いやすくする
    videos.sort(key=lambda v: v["posted_at"])

    blocks = []
    for v in videos:
        tpath = tdir / f"{v['video_id']}.json"
        if not tpath.exists():
            continue
        t = json.loads(tpath.read_text())
        blocks.append(
            f"### 動画 {v['video_id']}\n"
            f"- URL: {v['video_url']}\n"
            f"- 投稿日: {v['posted_at']} / 再生数: {v['view_count']} / いいね: {v['like_count']} / {v['duration_sec']}秒\n"
            f"- キャプション: {v['caption']}\n"
            f"- 文字起こし全文:\n{t['text']}\n"
        )

    user_msg = (
        f"## アカウント情報\n"
        f"- ハンドル: @{account['handle']} / 表示名: {account['display_name']}\n"
        f"- フォロワー: {account['follower_count']} / 総投稿: {account['video_count']}本\n"
        f"- bio: {account['bio']}\n\n"
        f"## 全動画データ（{len(blocks)}本 / 投稿日の古い順）\n\n" + "\n".join(blocks)
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

    report = next(b.text for b in resp.content if b.type == "text")
    REPORTS_DIR.mkdir(exist_ok=True)
    out = REPORTS_DIR / f"{args.handle}_full.md"
    out.write_text(report)

    cost = resp.usage.input_tokens / 1e6 * 5 + resp.usage.output_tokens / 1e6 * 25
    print(f"保存: {out}")
    print(f"対象 {len(blocks)}本 / in={resp.usage.input_tokens} out={resp.usage.output_tokens} "
          f"/ 約{cost*150:.0f}円 / stop={resp.stop_reason}")


if __name__ == "__main__":
    main()
