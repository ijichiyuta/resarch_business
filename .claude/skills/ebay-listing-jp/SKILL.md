---
name: ebay-listing-jp
description: 日本からeBay（主に米国）へバイク純正部品を出品するときの手順と安全ルール。出品文の作成、出品前の最終確認（仕入れ値・在庫・競合価格・米国価格）、ebay-mcp での下書き作成と公開に使う。「出品して」「出品文を作って」「この品番を出したい」「eBayに載せて」と言われたとき、または research/ebay/listings/ のファイルを扱うときに使う。
---

# eBay出品（日本→米国、バイク純正部品）

調査の結論と実データは `research/ebay/`（README.md、genres/report.html、listings/month1.md・month1.json）にある。数字を思い出で書かず、必ずファイルか実測から取る。

## 絶対に守ること

1. **ユーザーが「公開して」と言うまで `ebay_publish_offer` / `ebay_bulk_publish_offer` / `ebay_create_listing`（Trading）を呼ばない。** 下書き（inventory item と offer）までは作ってよい。公開直前に、タイトル・価格・送料・発送日数・写真の枚数を一覧で見せて承認をもらう
2. **写真は自分で撮ったものだけ。** 仕入れ先（モノタロウ・楽天）、競合の出品、メーカーのサイトの画像を使わない。eBayの規約違反で、画像の無断転載で逮捕された例もある。写真がない品は公開しない
3. **推測で商品の仕様を埋めない。** 原産国・取り付け位置・適合年式は、パッケージか公式の部品リスト（Partzilla の Product Fitment など）で確かめたものだけを書く
4. **仕入れ先から買い手へ直送しない。** 必ず自分か発送代行が受け取って検品してから送る（eBayのドロップシッピング規約）
5. **本名・勤務先を出品文や店名に出さない**（本業に副業を知られないため）

## 出品前の最終確認（その日のうちに、1品ずつ）

| 確認 | 方法 | 不合格なら |
|---|---|---|
| 仕入れ値と在庫 | 仕入番の verify モジュール（`research/ebay/tools/supplier_check.mts`、EC_saas/verify で実行） | 在庫なし→出品しない。値上がり→利益を計算し直す |
| 日本の競合の最安値 | eBayのSold・出品中の検索（発送元=日本） | 最安値より高いなら値付けを見直す |
| 全世界の出品 | 同じ品番を国の絞り込みなしで検索（中国・インドネシア・米国の安い出品を見る） | 同じ純正品がずっと安く出ているなら外す |
| 米国の部品店 | Partzilla の価格と在庫（Playwrightで開き、ポップアップを消してから Product Fitment タブ） | 米国で在庫があって自分より安いなら外すか値下げ |
| 個数 | 競合の出品ページの「Number in Pack」「Quantity」 | セット売りなら仕入れ値を個数倍にする |
| 利益 | 売値 −（落札13.6%＋国際1.65%＋為替2%）− $0.40 − 国際送料2,300円 − 梱包100円 − 仕入れ÷1.1 | 利益2,500円未満か利益率20%未満なら出さない |

米国の関税は、DDPで買い手がチェックアウト時に払う（ebay.co.jp/tariffs）。利益から引かない。

## ebay-mcp での手順（REST Inventory モデルに統一）

1. 初回だけ: `ebay_opt_in_to_program`（ビジネスポリシー）→ 支払い・返品（30日、返送料はセラー負担）・送料（SpeedPAK Economy、送料無料、発送日数は手元にあれば3日・無在庫なら10日）のポリシーを作る → `ebay_create_inventory_location`（日本の住所。公開される範囲に注意）
2. `ebay_get_category_suggestions` → `ebay_get_item_aspects_for_category` で必須の仕様を確かめる
3. `ebay_create_or_replace_inventory_item`（SKU＝品番、状態 NEW、数量1、仕様、適合車種）
4. 写真: `ebay_attach_media_to_inventory_item`（`EBAY_MCP_MEDIA_DIRS` に自分で撮った写真のフォルダだけを許可する）
5. `ebay_create_offer`（価格はドル、ポリシーID、location）→ `ebay_get_listing_fees` で手数料を見せる
6. **ユーザーの承認** → `ebay_publish_offer`

新規アカウントは出品上限（月10品・$500）がある。合計額を超えないか、公開前に足し算して見せる。

## 出品したあと

- 仕入れ先URLを仕入番（shiireban.com）に登録して、在庫切れと値上げを監視する
- 在庫切れになったら、すぐに eBay の在庫を0にする（キャンセルは新規アカウントに致命的）
- 売れたら: `ebay_get_orders` → 仕入れ → 検品・撮影記録 → 発送 → `ebay_create_shipping_fulfillment`（追跡番号）
