import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
X='"><img src=x onerror="window.__x=(window.__x||0)+1">'
Y="';window.__x=(window.__x||0)+1;//"
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844});e=[];pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('file://'+f);pg.wait_for_timeout(400)
    pg.evaluate("""([X,Y])=>{for(const h of D.hostels){h.name=X;h.addr=X;h.owner=X;h.area=Y}for(const r of D.res){r.name=X;r.room=Y;r.phone=X}for(const b of D.bills){b.name=X;b.h=X;b.what=Y;b.inv=Y;if(b.r){b.r.u=X;b.r.h=X}}for(const d of D.dues){d.desc=X}D.prof.name=X;D.prof.note=X;if(D.prof.bank)D.prof.bank.upn=X;save()}""",[X,Y])
    for k in ['dash','hostels','res','pay','more','myh','bills','bank','support','scan','onb']:
        try:pg.evaluate(f"go('{k}')")
        except Exception as ex:pass
        pg.wait_for_timeout(120)
    for js in ["viewBill(D.bills[0].inv)","resend(D.bills[0].inv)","collect(D.dues[0].id)","delRes(D.res[0].id)","delHost(D.hostels[0].id)","addRes()","editProf()","exportDlg()","pickLoc()"]:
        try:pg.evaluate(js)
        except Exception:pass
        pg.wait_for_timeout(150);pg.evaluate("for(const d of document.querySelectorAll('dialog[open]'))d.close()")
    print('XSS executions:',pg.evaluate("window.__x||0"),'| pageerrors:',len(e))
