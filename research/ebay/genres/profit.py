import json,statistics,collections,sys
FX=157.4
def profit(P,cost,ship=2300):
    fees=P*(0.136+0.0165+0.02)+0.40*FX
    duty=P*0.125*1.021
    dom=550 if cost<3500 else 0
    return P-fees-duty-ship-100-cost-dom
def run(items_file,prices_file='monotaro_prices.json',ship=2300,out=None):
    I=json.load(open(items_file)); M=json.load(open(prices_file))
    by=collections.defaultdict(list)
    for i in I:
        if i.get('pn'): by[i['pn']].append(i)
    rows=[]
    for pn,v in by.items():
        m=M.get(pn)
        if not (m and 'price_in' in m): continue
        ps=sorted(x['price'] for x in v)
        P=statistics.median(ps)
        pr=profit(P,m['price_in'],ship)
        rows.append(dict(pn=pn,n=len(v),P=P,Pmin=ps[0],cost=m['price_in'],lead=m.get('lead'),profit=round(pr),margin=round(pr/P*100,1),bo=sum(x['bestOffer'] for x in v),sellers=len({x['seller'] for x in v}),title=v[0]['title'][:70]))
    if out: json.dump(rows,open(out,'w'),ensure_ascii=False)
    return rows
if __name__=='__main__':
    for ship in (2300,3300):
        R=run(sys.argv[1],ship=ship,out=f'profit_{ship}.json')
        ok=[r for r in R if r['profit']>=3000 and r['margin']>=10]
        ok1=[r for r in R if r['profit']>=1000 and r['margin']>=10]
        print(f'ship={ship}: priced {len(R)} | 合格(3000円&10%) {len(ok)} ({len(ok)/len(R):.0%}) | 1000円以上 {len(ok1)} | 赤字 {sum(r["profit"]<0 for r in R)} | 利益中央値 {statistics.median(r["profit"] for r in R)}')
        ratio=[r['P']/r['cost'] for r in R]; print('  売価/仕入れ 倍率 中央値',round(statistics.median(ratio),2),'四分位',[round(q,2) for q in statistics.quantiles(ratio,n=4)])
