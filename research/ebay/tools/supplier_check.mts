/**
 * 仕入番（EC_saas/verify）の取得・抽出モジュールで、品番ごとの仕入れ値と在庫を確かめる。
 * EC_saas 側のファイルは変更しない（読み込むだけ）。
 * 使い方: npx tsx supplier_check.ts pns.json out.json
 */
import { readFileSync, writeFileSync } from "node:fs";
import * as cheerio from "/Users/ijichiyuuta/.superset/projects/EC_saas/verify/node_modules/cheerio/dist/esm/index.js";
import { fetchStatic, politeWait } from "/Users/ijichiyuuta/.superset/projects/EC_saas/verify/src/fetch.ts";
import { extractStructured } from "/Users/ijichiyuuta/.superset/projects/EC_saas/verify/src/structured.ts";
import { applyRules } from "/Users/ijichiyuuta/.superset/projects/EC_saas/verify/src/apply.ts";
import type { SelectorRules } from "/Users/ijichiyuuta/.superset/projects/EC_saas/verify/src/types.ts";

// モノタロウ商品ページ用（2026-09-23、/g/01475546/ の実HTMLから作成）
const MONOTARO: SelectorRules = {
  price_selector: '[class*="TaxIncludedPrice-module"][class*="Price--Normal"]',
  price_attr: null,
  in_stock_rule: { type: "text_contains", selector: "button", text: "バスケットに入れる" } as any,
  out_of_stock_rule: { type: "text_contains", selector: "body", text: "取扱い終了" } as any,
  title_selector: "h1",
  image_selector: null, image_attr: null, confidence: 0.8,
  notes: "価格は税込セル。在庫あり=カート投入ボタン、在庫なし=取扱い終了表記。どちらも無ければunknown",
};

const norm = (s: string) => s.toUpperCase().replace(/[-\s]/g, "");
const pns: string[] = JSON.parse(readFileSync(process.argv[2], "utf8"));
const out: Record<string, any> = {};

for (const pn of pns) {
  const r: any = { monotaro: null, rakuten: [] };
  // --- モノタロウ
  try {
    await politeWait("www.monotaro.com", 3500);
    const s = await fetchStatic(`https://www.monotaro.com/s/?q=${encodeURIComponent(pn)}`, 25000);
    const links = [...new Set([...(s.html ?? "").matchAll(/href="(\/g\/\d+\/)"/g)].map((m) => m[1]))].slice(0, 3);
    for (const l of links) {
      await politeWait("www.monotaro.com", 3500);
      const p = await fetchStatic("https://www.monotaro.com" + l, 25000);
      if (!p.html) continue;
      const ex = applyRules(p.html, MONOTARO);
      if (!ex.title || !norm(ex.title).includes(norm(pn))) continue;
      const lead = cheerio.load(p.html)("body").text().match(/(\d+日以内出荷|当日出荷|翌日出荷|お取り寄せ)/)?.[1] ?? null;
      r.monotaro = { url: "https://www.monotaro.com" + l, price: ex.priceJpy, stock: ex.stock, lead, title: ex.title };
      break;
    }
  } catch (e) { r.monotaroErr = String(e); }
  // --- 楽天
  try {
    await politeWait("search.rakuten.co.jp", 3500);
    const s = await fetchStatic(`https://search.rakuten.co.jp/search/mall/${encodeURIComponent(pn)}/`, 25000);
    const all = [...new Set([...(s.html ?? "").matchAll(/https:\/\/item\.rakuten\.co\.jp\/[\w-]+\/[\w%.-]+\/?/g)].map((m) => m[0]))];
    const key = norm(pn);
    const items = [...all.filter((u) => norm(u).includes(key)), ...all.filter((u) => !norm(u).includes(key))].slice(0, 6);
    for (const u of items) {
      await politeWait("item.rakuten.co.jp", 3500);
      const p = await fetchStatic(u, 25000);
      if (!p.html) continue;
      const sd = extractStructured(p.html);
      const pageText = cheerio.load(p.html)("body").text();
      // 品番はハイフン付きで完全一致、かつメーカー名か「純正」が載っていること（商品番号の数字列との偶然の一致を除く）
      const exact = new RegExp("(^|[^0-9A-Z])" + pn.replace(/[-]/g, "[-‐－]") + "([^0-9A-Z]|$)", "i");
      if (!exact.test(pageText) || !/カワサキ|kawasaki|ホンダ|honda|ヤマハ|yamaha|スズキ|suzuki|純正/i.test(pageText)) continue;
      r.rakuten.push({ url: u, price: sd.priceJpy, stock: sd.stock, title: sd.title });
    }
  } catch (e) { r.rakutenErr = String(e); }
  out[pn] = r;
  console.log(pn, JSON.stringify({ m: r.monotaro && [r.monotaro.price, r.monotaro.stock, r.monotaro.lead], rk: r.rakuten.map((x: any) => [x.price, x.stock]) }));
  writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
}
