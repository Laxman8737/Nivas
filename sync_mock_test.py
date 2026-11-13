from playwright.sync_api import sync_playwright
MOCK="""window.DB={};const mk=p=>({get:async()=>({exists:p in DB,data:()=>DB[p]}),set:async v=>{DB[p]=v},update:async v=>{DB[p]={...DB[p],...v}},delete:async()=>{delete DB[p]}});
window.firebase={firestore:Object.assign(()=>({collection:c=>({doc:i=>{const r=mk(c+'/'+i);r.p=c+'/'+i;return r}}),runTransaction:async f=>f({get:async r=>({exists:r.p in DB,data:()=>DB[r.p]}),set:(r,v)=>{DB[r.p]=v},update:(r,v)=>{DB[r.p]={...DB[r.p],...v}}})}),{FieldValue:{serverTimestamp:()=>1}})};"""
res=[]
def T(n,ok):res.append((n,ok));print(('PASS ' if ok else 'FAIL ')+n)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();e=[];pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('file:///home/claude/out/nivas-hostel-app/nivas-demo.html');pg.wait_for_timeout(300);pg.evaluate(MOCK)
    pg.evaluate("user={uid:'u1',email:'a@b.c',emailVerified:true};cloudSync()");pg.wait_for_timeout(300)
    T('first sync uploads local data (migration), rev 1',pg.evaluate("DB['owners/u1']&&DB['owners/u1'].rev==1&&JSON.parse(DB['owners/u1'].data).res.length==D.res.length"))
    n0=pg.evaluate("D.res.length");pg.evaluate("save()");T('local copy still present after migration',pg.evaluate("JSON.parse(localStorage.getItem(KEY())).res.length")==n0)
    pg.evaluate("D.res.pop();save()");pg.wait_for_timeout(2200)
    T('edit is pushed, rev 2, dirty flag cleared',pg.evaluate("DB['owners/u1'].rev==2&&!localStorage.getItem(DKy())"))
    other=pg.evaluate("(()=>{const o=JSON.parse(DB['owners/u1'].data);o.res=o.res.slice(0,1);DB['owners/u1']={...DB['owners/u1'],data:JSON.stringify(o),rev:5};return o.res.length})()")
    pg.evaluate("cloudSync()");pg.wait_for_timeout(300)
    T('newer cloud copy is adopted when device has no unsynced edits',pg.evaluate("D.res.length")==other)
    T('previous local data saved as backup before adopting',pg.evaluate("Object.keys(localStorage).some(k=>k.startsWith('nivas-backup:u1:local'))"))
    pg.evaluate("D.hostels[0].name='Edited offline';save()");pg.evaluate("clearTimeout(_qt)")
    pg.evaluate("DB['owners/u1']={...DB['owners/u1'],rev:9}");pg.evaluate("cloudSync()");pg.wait_for_timeout(300)
    T('conflict shows a choice dialog, nothing overwritten silently',pg.evaluate("al.open&&al.innerText.includes('Choose which one')")&pg.evaluate("D.hostels[0].name=='Edited offline'&&DB['owners/u1'].rev==9"))
    pg.click('#alc');pg.wait_for_timeout(400)
    T('Keep this device: cloud saved as backup, device data pushed rev 10',pg.evaluate("DB['owners/u1'].rev==10&&JSON.parse(DB['owners/u1'].data).hostels[0].name=='Edited offline'&&Object.keys(localStorage).some(k=>k.startsWith('nivas-backup:u1:cloud'))"))
    pg.evaluate("window.firebase.firestore=()=>({collection:()=>({doc:()=>({get:async()=>{throw new Error('net')}})})})");pg.evaluate("FS=null;cloudSync()");pg.wait_for_timeout(300)
    T('network failure shows an error status, no crash',pg.evaluate("$('#syn').dataset.s")in('err','off') and not e)
    print(e)
