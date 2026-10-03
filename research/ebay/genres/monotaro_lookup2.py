import json,re,html,time,random,subprocess,collections,sys
import os,sys
src=sys.argv[1] if len(sys.argv)>1 else 'moto_v2.json'
I=json.load(open(src))
by=collections.defaultdict(list)
for i in I:
    if i.get('pn') and i.get('price'): by[i['pn']].append(i)
multi=[p for p,v in by.items() if len(v)>=2]
single=[p for p,v in by.items() if len(v)==1]
pns=multi+single
out=json.load(open('monotaro_prices.json')) if os.path.exists('monotaro_prices.json') else {}
pns=[p for p in pns if p not in out]
print('todo',len(pns),flush=True)
for n,pn in enumerate(pns):
    try:
        b=subprocess.run(['curl','-s','-A','Mozilla/5.0','--max-time','20','https://www.monotaro.com/s/?q='+pn],capture_output=True).stdout
        s=b.decode('utf-8','ignore')
        t=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
        t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
        key=pn.replace('-','')
        res=None
        hits=int((re.search(r'([\d,]+)\s*件中',t) or [0,'0'])[1].replace(',','')) if re.search(r'([\d,]+)\s*件中',t) else 0
        for m in re.finditer(r'(?:'+re.escape(pn)+'|'+re.escape(key)+r')\s+([^￥]{0,40}?)\s*(?:\(\d+件のレビュー\)\s+)?￥\s?([\d,]+)\s+税込\s+￥\s?([\d,]+)\s+\S+\s+(\S*出荷|\S*取寄\S*|\S*お問い合わせ\S*)?',t,flags=re.I):
            res={'maker':m.group(1).strip(),'price_ex':int(m.group(2).replace(',','')),'price_in':int(m.group(3).replace(',','')),'lead':m.group(4),'hits':hits}; break
        out[pn]=res
    except Exception as e: out[pn]={'err':str(e)}
    if n%25==0: print(n,len(pns),sum(1 for v in out.values() if v and 'price_in' in v),flush=True); json.dump(out,open('monotaro_prices.json','w'),ensure_ascii=False)
    time.sleep(1.2)
json.dump(out,open('monotaro_prices.json','w'),ensure_ascii=False)
print('done',len(out),sum(1 for v in out.values() if v and 'price_in' in v))
