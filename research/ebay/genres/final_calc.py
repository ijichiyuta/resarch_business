import json,statistics,collections
FX=157.4
I=json.load(open('moto_v2.json')); M=json.load(open('monotaro_prices.json'))
RATIO={'honda':0.884,'yamaha':1.002,'kawasaki':1.216,'suzuki':1.0}  # モノタロウ÷定価（sourcing_desk.md 実測中央値）
def profit(P,cost,ship):
    fees=P*(0.136+0.0165+0.02)+0.40*FX
    dom=550 if cost<3500 else 0
    return P-fees-ship-100-cost-dom
by=collections.defaultdict(list)
for i in I:
    if i.get('pn'): by[i['pn']].append(i)
brand={}
for pn,v in by.items(): brand[pn]=v[0].get('brand')
base=[]
for pn,v in by.items():
    m=M.get(pn)
    if not(m and 'price_in' in m): continue
    b=brand[pn]; teika=m['price_in']/RATIO.get(b,1.0)
    P=statistics.median(x['price'] for x in v)
    base.append(dict(pn=pn,brand=b,n=len(v),P=P,mono=m['price_in'],teika=round(teika),lead=m.get('lead'),title=v[0]['title'],sellers=len({x['seller'] for x in v})))
print('priced',len(base),'of',len(by), collections.Counter(r['brand'] for r in base))
SC={
 '最悪: 定価で仕入れ・還付なし':lambda r:r['teika'],
 '今のまま: モノタロウ税込・還付なし':lambda r:r['mono'],
 '現実: メーカー別最安(ホンダ=モノタロウ,他=定価)+還付':lambda r:min(r['mono'],r['teika'])/1.1,
 '現実+: 定価の9掛け+還付':lambda r:min(r['mono'],r['teika']*0.9)/1.1,
 'ベスト: 定価の85%+還付':lambda r:min(r['mono'],r['teika']*0.85)/1.1,
}
res={}
for name,f in SC.items():
  for ship in (2300,3300):
    R=[(r,profit(r['P'],f(r),ship)) for r in base]
    ok=[(r,p) for r,p in R if p>=3000 and p/r['P']>=0.10]
    res[f'{name}|{ship}']=dict(n=len(R),ok=len(ok),rate=round(len(ok)/len(R)*100,1),loss=sum(p<0 for r,p in R),med=round(statistics.median(p for r,p in R)),okmed=round(statistics.median(p for r,p in ok)) if ok else 0)
    print(f'{name} ship{ship}: 合格 {len(ok)}/{len(R)} ({len(ok)/len(R):.1%}) 赤字{res[f"{name}|{ship}"]["loss"]} 利益中央値{res[f"{name}|{ship}"]["med"]} 合格品の利益中央値{res[f"{name}|{ship}"]["okmed"]}')
# realistic list
f=SC['現実: メーカー別最安(ホンダ=モノタロウ,他=定価)+還付']
rows=[]
for r in base:
    c=f(r); p=profit(r['P'],c,2300)
    rows.append(dict(r,cost=round(c),profit=round(p),margin=round(p/r['P']*100,1)))
rows.sort(key=lambda r:-r['profit'])
json.dump(dict(res=res,rows=rows),open('final_results.json','w'),ensure_ascii=False)
ok=[r for r in rows if r['profit']>=3000 and r['margin']>=10]
print('brand of ok',collections.Counter(r['brand'] for r in ok))
print('ok with n>=2',sum(1 for r in ok if r['n']>=2))
for r in ok[:15]: print(r['pn'],r['brand'],r['n'],r['P'],r['cost'],r['profit'],r['margin'],r['title'][:50])
