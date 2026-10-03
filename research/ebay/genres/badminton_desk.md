# eBay輸出ジャンル調査: バドミントン用品（ヨネックス日本版中心）— 机上調査

調査日: 2026-09-23 / 方法: ログイン不要の公開情報のみ（WebSearch・WebFetch・curl）。ブラウザ操作・Terapeakは未使用。

## 結論

**判定: 新品の現行モデルはNO。中古の名機・日本限定色（BP）に絞るなら条件付きだが、合格型番が30種類に届く見込みは低い（推測）。**

- 米国向けは、手数料（約17%）＋関税（12.5%）で売価の約30%が消え、さらにラケット1本あたり送料と梱包で8,000〜9,000円かかる。損益分岐となる仕入れ値は「売価×0.70−8,600円」
- 米国の定価は日本の実売より約1.4〜1.5倍高い（100ZZ: 米$295≒46,400円、日本の最安30,800円）。それでも上の費用を吸収しきれず、主要な新品7型番はすべて赤字か、利益0〜2,000円にとどまった
- eBayに出ている日本発の「JP版」の出品価格は、米国発の出品より**安い**（NF1000Z: 日本発の中央値$273.5、日本以外$289.99）。JP版にプレミアムが付いている形跡は見つからなかった
- 米国宛てのラケットはSpeedPAK Economyが使えない（米国宛ては長さ66cmが上限。ラケットは約68cm）。そのためクーリエかEMSに頼ることになり、送料が高止まりする
- 利益が出そうなのは、**中古の旧名機（Duora Z-Strike、Voltric Z-Force IIなど）とBP限定色**だけ。ただしeBay側の価格は出品価格で、売れた価格ではない。Terapeakでの確認が必須

## 1. 日本版（JP版）の需要と海外版との違い

| 論点 | 分かったこと | 出典 |
|---|---|---|
| 製造国 | 上位のPro系はMade in Japan（NF800 Proの公式ページに「日本製」と明記）。Tour/Gameは台湾製、Playは中国製 | [yonexshop.jp NF-800P](https://yonexshop.jp/item/detail/1_1_NF-800P_1/269)、[badmintonhouse.ca](https://badmintonhouse.ca/blogs/news/yonex-made-in-japan-vs-china-tiers) |
| JP版とSP版（国際版）の差 | BadmintonCentralの議論では、違いは塗装の艶程度で差はわずかという見方。ヨネックスは日本国内でJP品を割高に売っており、輸入されたJP品も他コードより高値で売られる | [BadmintonCentral「Yonex JP vs SP」](http://www.badmintoncentral.com/forums/index.php?threads%2Fyonex-jp-vs-sp.86868%2F=) |
| 地域コード | 「JP」は日本向けを示すコード。ただしコードだけで性能が上とはいえない | [badmintonhouse.ca](https://badmintonhouse.ca/blogs/news/how-to-spot-fake-badminton-racket) |
| 重量展開 | 日本版は4U・3Uの両方を展開（NF800 Pro公式） | 同上 公式 |
| 日本限定色 | **BP＝日本バドミントン専門店会の限定カラー**（ARC11 BP、AX88D Pro BP、AX99 BPなど）。国内でしか手に入らない | [アリモトスポーツ](https://arimoto-sp.com/12593/)、[badminton-psu.com](https://www.badminton-psu.com/wp/arimoto/?p=44) |
| 日本先行発売 | 裏付けは取れなかった（未確認） | — |
| 日米の価格差 | Japan Trulyの比較では日本が9〜13%安い（AX88D Pro: 日本$280・米国$320） | [Japan Truly](https://shop.japantruly.com/blogs/product-review/is-yonex-cheaper-in-japan) |

Redditはcurlでもブロック（403）され、r/badmintonの評判は取得できなかった。

## 2. 海外の販売者と価格帯（eBayは出品価格。売れた価格ではない）

eBayの検索結果と商品ページは、WebFetch・curlとも403かCAPTCHAで取得できなかった。以下は検索結果の抜粋と、eBayの出品を集約するpicclick.comから拾った値。

| 型番 | 日本発の出品価格 | 日本以外の出品価格 | 出典 |
|---|---|---|---|
| NF1000Z 新品 | 中央値 $273.5（$150〜430の幅） | 中央値 $289.99 | [picclick](https://picclick.com/?q=yonex+nanoflare+1000z) |
| ARC11 Pro 新品 | $260 | 中央値 $269.99 | [picclick](https://picclick.com/?q=yonex+arcsaber+11+pro) |
| AX100ZZ 新品 | $270（Kurenai） | $269.99〜$325.99 | [picclick](https://picclick.com/?q=yonex+astrox+100zz) |
| AX99 Pro 4U5 | $268.05 | — | [eBay 276790558381](https://www.ebay.com/itm/276790558381) |
| NF800 Pro 新品 | $250 | — | [picclick](https://picclick.com/?q=yonex+badminton+japan) |
| Duora Z-Strike 中古 | $149〜283 | — | 検索結果の抜粋 |
| VT-ZF2 中古 | $118〜370 | — | 検索結果の抜粋 |
| ARC11 Pro BP 未使用 | $1,026＋送料$240（強気の出品） | — | [eBay 406374015604](https://www.ebay.com/itm/406374015604) |
| AX88D Pro BP 5本セット | $4,424 | — | [picclick](https://picclick.com/Popular/yonex-astrox-88d-pro) |

日本人セラーは熊本・東京・岐阜・大阪などに複数いて、送料込みのDDP出品やSpeedPAK Expedited（送料$58）が見られた。米国内には「US-Versand am selben Tag（米国から即日発送）」をうたう業者もいて、同じ型番で競合している。

## 3. 偽物・VeRO・規制

- 偽物: 過去にeBayで買われたヨネックスの約90%が偽物だったという報告がある（NS8000/9000など、$40〜90）。見分け方は、シリアルがレーザー刻印か、ホログラムシールが爪で剥がれるか。[Counterfeit Report](https://thecounterfeitreport.com/product/306/Badminton-Racquets.html)、[Yonex USA](https://us.yonex.com/pages/spotting-counterfeits)
- 保証: Yonex USAは、正規店以外や個人間で買った品を保証しない（同上）。売る側は「日本の正規店で購入」「刻印シリアルの写真」「JPシール」を見せることが信頼の決め手になる
- VeRO: eBayの公開VeROプロフィール一覧（Yの項）には**Yonexも、一覧全体でMizunoも載っていなかった**（curlで取得し全文を検索）。ただし一覧は参加者の全員を載せているわけではない。公式画像の転用は避けること。[VeRO profiles](https://www.ebay.com/sellercenter/resources/verified-rights-owner-profiles)
- 中古を仕入れるなら古物商許可が要る（既存README参照）

## 4. 国内の仕入れ相場（ヤフオク過去180日＋価格.com）

| 型番 | ヤフオク件数・平均 | 新品・未使用 | 中古 | 国内新品の最安 |
|---|---|---|---|---|
| AX99 Pro | 平均20,602円 | 15,000〜25,400円 | 11,000〜20,000円 | 25,575円（価格.com） |
| AX100ZZ | 215件・平均39,102円 | 35,000〜40,000円 | 22,000〜34,500円 | 30,800円（価格.com） |
| NF800 Pro | 33件・平均22,327円 | 19,500〜31,800円 | 5,000〜20,600円 | 18,810〜24,750円（公式36,300円） |
| NF1000Z | 51件・平均25,528円 | 25,000〜30,000円 | 19,800〜23,000円 | — |
| ARC11 Pro | 89件・平均30,283円 | 28,000〜31,000円 | 20,000〜27,200円 | 28,253円（定価37,400円） |
| AX88D Pro | 92件・平均33,365円 | 22,000〜28,000円 | 14,000〜21,000円 | — |
| AX88S Pro | 60件・平均22,785円 | 20,000〜40,000円 | 15,000〜20,000円 | 25,213円 |
| AX77 Pro | 93件・平均22,757円 | 15,000〜20,000円 | — | 27,115円 |
| NF700 Pro | 37件・平均22,123円 | 19,500〜32,000円 | — | 25,500円 |
| Duora Z-Strike | 21件・平均17,744円 | 26,000〜30,000円 | 9,000〜20,000円 | 廃番 |
| VT-ZF2 | 14件・平均21,821円 | 14,850〜25,000円 | 15,000〜25,000円 | 廃番 |
| Nanoray Z-Speed | 24件・平均14,228円 | 約20,000円 | 11,000〜20,500円 | 廃番 |
| BP限定色 | 8件・平均55,427円 | 22,700〜100,100円 | — | 専門店のみ |
| ガット200mロール | 273件・平均17,831円 | BG80: 19,000円 | — | — |
| PC65Z（シューズ） | 89件・平均7,519円 | — | 5,000〜12,000円 | 14,025円（スリム） |
| ミズノのラケット | 277件・平均8,729円 | Fortius 12,000〜17,500円 | — | — |

出典: `https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=<型番>`（各型番で取得）、[価格.com](https://search.kakaku.com/ヨネックス%20バドミントンラケット/)、[価格.com AX100ZZ](https://kakaku.com/item/S0000901408/)

## 5. 海外の販売価格

| 地域 | 例 | 円換算（157.4円/USD） | 出典 |
|---|---|---|---|
| 米国の公式 | 100ZZ $295、99 Pro $290、88S Pro $290、1000Z $285、800 Pro $275、77 Pro $260 | 約41,000〜46,000円 | [Yonex USA](https://us.yonex.com/collections/badminton-racquets) |
| 英国 | 99 Pro £207.99（定価£280）、1000Z £207.94、ARC11 Pro £199.99 | 約40,000円 | [TennisNuts](https://www.tennisnuts.com/shop/badminton/badminton-rackets/yonex-badminton-rackets/made-in-japan.html) |
| ドイツ | 99 Pro €161（アウトレット、定価€260） | 約27,000円 | [badminton-shop.com](https://badminton-shop.com/product/yonex-astrox-99-pro-cherry-sunburst/) |
| マレーシア | 100ZZ RM859〜900 | 約32,000円（推測換算） | [vsmash](https://vsmash.com/product/yonex-astrox-100zz-kurenai) ほか |
| インド | 1000Z ₹15,990〜17,999（MRP ₹30,290） | 約28,000〜32,000円（推測換算） | [racquets4u](https://www.racquets4u.com/yonex-nanoflare-1000-z-badminton-racquet-unstrung.html) |

東南アジアとインドは日本と同じ価格帯なので、狙えない。価格差があるのは米国と英国だけ。

## 6. 送料

- 梱包サイズ: 約72×25×6cm、実重量1.0〜1.3kg（推測）。容積重量は÷5000で2.16kg、÷6000で1.8kg
- **SpeedPAK Economy（米国）: 長さ66cmまで、55.88cmを超えると2,475円の追加料金。ラケットは引き受け対象外**。英国宛ては120cmまで送れる。容積重量は÷8000で、2kgまで5,245円 [料金表PDF（2026/3/25発効）](https://static.orangeconnex.com/capricorn/selfQuery/1141130239112384512.pdf)
- EMS（米国＝第4地帯）: 1.0kg 5,300円、1.5kg 6,600円、2.0kg 7,900円。最長辺1.5mまで。容積重量は取らない [日本郵便](https://www.post.japanpost.jp/send/oversea/charge/list-ems/all.html)。米国宛ては2026/4/14に引き受けを再開し、販売品は指定局での差し出しとZonosでの関税の事前払い（DDP）が必須 [日本郵便](https://www.post.japanpost.jp/service/send/oversea/information/2026/0714_01.html)
- FedEx/DHL（eLogi・CPaSS）: 料金表は公開されていない。請求重量2.5kgで**1本6,000〜9,000円程度（推測）**。eBay上の日本人セラーは送料$58〜60で出している
- 2本同梱（72×25×10cm）は請求重量3.6kgになり、1本あたりの送料は下がる（推測）
- シューズとガットはSpeedPAK Economyで送れる（シューズの送料$14.99の出品例あり）

## 7. 米国の関税（2026年9月時点）

- HTS 9506.59.40.40（バドミントンのラケットとフレーム）: MFN税率5.6% [wove](https://tariffs.wove.com/us/tariff/9506.59.40/fleet-badminton-racket)
- IEEPA関税は2026/2/24に終了。2026/7/24からは強制労働をめぐるSection 301の関税が加わり、日本製品は「MFN税率と合わせて12.5%」が上限になる。**ラケットは5.6%＋6.9%＝合計12.5%** [USTR](https://ustr.gov/about/policy-offices/press-office/press-releases/2026/july/ustr-takes-action-forced-labor-section-301-investigations)、[Zonos](https://zonos.com/docs/guides/us-tariff-changes)
- シューズ（6404.11）はMFN税率がおおむね20%で、上限の12.5%を超えるため追加関税はかからない。関税は20%のまま（税率は推測で、要確認）
- デミニミス（少額免税）は2025/8/29から停止。郵便物は$2,500以下なら関税の事前払い（DDP）が必須

## 8. 利益の試算（米国DDP、1本発送）

前提: 1ドル157.4円（2026/9/22終値）。eBay手数料は落札手数料13.6%＋国際手数料1.65%＋Payoneer約2%＋$0.40。関税12.5%。送料7,500円。梱包と国内送料1,000円。消費税還付は含めない。

| 型番 | 売価（日本発の出品） | 仕入れ | 利益 | 率 | 判定 |
|---|---|---|---|---|---|
| NF1000Z 新品 | $270 | 26,000円 | −4,700円 | — | ✕ |
| AX100ZZ 新品 | $285 | 30,800円 | −7,900円 | — | ✕ |
| AX99 Pro 新品 | $268 | 19,000円（ヤフオク） | +2,000円 | 5% | ✕ |
| NF800 Pro 新品 | $250 | 18,810円 | +300円 | 1% | ✕ |
| ARC11 Pro 新品 | $260 | 28,253円 | −8,100円 | — | ✕ |
| AX88D Pro 新品 | $270 | 22,000円 | −700円 | — | ✕ |
| VT-ZF2 中古美品 | $300 | 18,000円 | +6,600円 | 14% | △ 売価の確認が要る |
| Duora Z-Strike 中古 | $220 | 12,000円 | +3,700円 | 11% | △ |
| PC65Z シューズ | $140 | 14,025円 | −4,100円 | — | ✕（関税20%） |
| BG80 200m | $149 | 19,000円 | −4,800円 | — | ✕ |

国内の正規店で新品を買えば消費税還付で仕入れの約9%が戻る（NF800 Proで+1,700円）。それでも新品で合格ラインを超える型番はなかった。

## 9. 総合判断・リスク・勝ち筋

**30型番の基準: 新品の現行品ではほぼ0型番。中古の旧名機とBP限定色を足しても10〜15型番程度と見る（推測）。ジャンル全体としてはNO寄りの条件付き。**

リスク
- 利益の薄さ: 売価の30%に加え、1本あたり8,500円の固定費がかかる
- 米国での競合: 公式のセール価格（B&Tの100ZZが$269.99）や米国発の即日発送業者が同じ値段帯にいる
- 偽物への警戒: 中古は特に疑われる。シリアル刻印の写真と正規店の購入証明が要る
- 中古は割れやヒビのクレームが多い。発送中の破損リスクもある

勝ち筋（Terapeakで要検証）
1. **BP限定色（日本専門店会の限定）**: 日本でしか買えず、eBayでは$700〜1,000台の強気な出品がある。国内の落札は2.3万〜10万円
2. **廃番の名機の中古美品・未使用品**: VT-ZF2、Duora Z-Strike、Nanoray Z-Speed、ARC10、Voltric Z-Forceなど。米国の公式で買えないので価格比較されにくい
3. **2〜5本のセット**: 送料を薄められる。セット出品も実在する
4. **米国以外**: 英国とオーストラリアはSpeedPAK Economyで長さ120cm・105cmまで送れる。ただし英国は£135まで、ドイツは€150までという上限があり、ラケットの価格帯では使いにくい

次の一手: Terapeak（Item location: Japan、90日）で「BP」「Voltric Z-Force II」「Duora Z-Strike」「Nanoray Z-Speed」「Arcsaber 10」「Armortec 900」「Nanospeed 9900」「100ZZ 3U」を確認し、販売数と平均の売れた価格を取る。
