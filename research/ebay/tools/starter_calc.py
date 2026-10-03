import json,statistics,sys
FX=157.4
def fees(P): return P*(0.136+0.0165+0.02)+0.40*FX
def best_cost(sup):
    opts=[]
    m=sup.get('monotaro')
    if m and m.get('price') and m.get('stock')!='out_of_stock':
        p=m['price']; ship=0 if p/1.1>=3500 else 500
        opts.append(('モノタロウ',p+ship,p,m.get('stock'),m.get('lead'),m.get('url')))
    for r in sup.get('rakuten',[]):
        if r.get('price') and r.get('stock')=='in_stock':
            opts.append(('楽天:'+r['url'].split('/')[3],r['price']+800,r['price'],r['stock'],None,r['url']))
    return min(opts,key=lambda o:o[1]) if opts else None
def calc(verify,supplier,ship_intl=2300,refund=True):
    out=[]
    for pn,v in verify.items():
        if pn.startswith('__'): continue
        s=supplier.get(pn)
        if not s: continue
        bc=best_cost(s)
        sold=v['soldJPprices']
        med=statistics.median(sold) if sold else None
        cands=[x for x in (v['activeJPmin'],med) if x]
        if not cands or not bc: 
            out.append(dict(pn=pn,skip='価格か仕入れ先なし',v=v,s=s)); continue
        P=min(cands)
        cost=bc[1]/1.1 if refund else bc[1]   # 還付は商品＋送料の消費税分
        prof=P-fees(P)-ship_intl-100-cost
        out.append(dict(pn=pn,P=round(P),src=bc[0],cost_in=bc[1],item=bc[2],stock=bc[3],lead=bc[4],url=bc[5],profit=round(prof),margin=round(prof/P*100,1),soldAll=v['soldAll'],soldJP=v['soldJP'],activeJP=v['activeJP'],activeJPmin=v['activeJPmin'],lastSold=v['lastSold'],title=v['titleEx']))
    return out
if __name__=='__main__':
    V=json.load(open(sys.argv[1])); V=json.loads(V) if isinstance(V,str) else V
    S=json.load(open(sys.argv[2]))
    R=calc(V,S)
    json.dump(R,open(sys.argv[3],'w'),ensure_ascii=False,indent=1)
    R2=[r for r in R if 'skip' not in r]; R2.sort(key=lambda r:-r['margin'])
    for r in R2: print(r['pn'],'売',r['P'],'仕',r['cost_in'],r['src'],r['stock'],r['lead'] or '','利',r['profit'],str(r['margin'])+'%','| 売れ',r['soldAll'],'日本',r['soldJP'],'競合',r['activeJP'],'|',(r['title'] or '')[:45])
    for r in R:
        if 'skip' in r: print('SKIP',r['pn'],r['skip'])
