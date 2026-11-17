import json, math, random
F="/Users/danielstroebel/Projekte/sofortsichtbar/src/entwicklung/storyboard/story7/assets/fonts"
faces="".join(f'@font-face{{font-family:"{fam}";font-weight:{w};src:url("file://{F}/{d}-latin-{w}-normal.woff2")}}' for fam,d,w in [("Inter","inter",400),("Inter","inter",500),("Inter","inter",600),("Inter Tight","inter-tight",700)])
# Szenen: (start, ende, Satz, Unterzeile)
SZ=[(0.3,5,"Du willst mehr Kunden aus deinen Zielgruppen.","Zum Beispiel private Bauherren in deiner Region."),
    (5,10,"Vom Marketing der Zentrale kommt wenig.","Ideen hängen monatelang in der Abstimmung."),
    (10,17,"sofort sichtbar liefert fertige Vertriebsstrecken.","Je Zielgruppe: Landingpage, Postings, Mailing – im Look deiner Agentur."),
    (17,25,"Die Postings bringen dich vor die Bauherren deiner Region.","Regelmäßig, auf LinkedIn, Facebook und Instagram."),
    (25,31,"Wer reagiert, wird zum Gesprächsanlass.","Familie K. lädt die Checkliste Hausbau."),
    (31,38,"Dein Vertrieb macht daraus einen Termin.","Rückruf, Beratung, Abschluss – wie immer, nur mit mehr Anlässen."),
    (38,44,"Und du bleibst im Bestand präsent.","Deine Inhalte erreichen auch deine Kunden. Der nächste Anlass kommt."),
    (44,50.5,"Selbst machen oder machen lassen?","Die Strecken liefern wir immer. Das Betreiben übernehmen wir auf Wunsch."),
    (50.5,55,"","")]
def an(name,dauer,start,extra="both"):
    return f"{name} {dauer}s {start}s {extra}"
def sichtbar(a,b,ein="ein",aus="aus"):
    return f"animation:{an(ein,.6,a)},{an(aus,.45,b-.45,'forwards')};"
css=faces+'''
*{box-sizing:border-box;margin:0}
body{width:1280px;height:720px;overflow:hidden;background:#fff;font-family:Inter;color:#1d1d1f}
.buehne{position:relative;width:1280px;height:720px;overflow:hidden;background:#fff}
@keyframes ein{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes einp{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:none}}
@keyframes aus{from{opacity:1}to{opacity:0}}
@keyframes zeichne{from{stroke-dashoffset:var(--l)}to{stroke-dashoffset:0}}
@keyframes dreh{to{transform:rotate(360deg)}}
@keyframes chip{to{background:linear-gradient(100deg,#0b9fbd,#8613a1);color:#fff;box-shadow:none}}
@keyframes gesehen{to{fill:#e6e6eb;stroke:#8e8e93}}
@keyframes fkfarbe{to{opacity:1}}
@keyframes klingel{0%,100%{transform:rotate(0)}20%{transform:rotate(-12deg)}40%{transform:rotate(10deg)}60%{transform:rotate(-8deg)}80%{transform:rotate(6deg)}}
@keyframes fkzug{to{transform:translate(var(--dx),var(--dy))}}
@keyframes stempel{from{opacity:0;transform:scale(1.6) rotate(-8deg)}to{opacity:1;transform:rotate(-8deg)}}
@keyframes farbe{to{background-position:var(--bp) 0}}
@keyframes flieg1{from{transform:translate(-300px,90px) rotate(-8deg);opacity:0}to{transform:none;opacity:1}}
@keyframes flieg2{from{transform:translate(-300px,-30px) rotate(6deg);opacity:0}to{transform:none;opacity:1}}
@keyframes flieg3{from{transform:translate(-300px,-150px) rotate(-4deg);opacity:0}to{transform:none;opacity:1}}
.satz{position:absolute;left:80px;top:54px;width:1120px}
.satz b{display:block;font-family:"Inter Tight";font-weight:700;font-size:46px;letter-spacing:-.03em;line-height:1.05}
.satz span{display:block;margin-top:12px;color:#6e6e73;font-size:22px;font-weight:500}
.ab{position:absolute}
.karte{position:absolute;border-radius:14px;background:#fff;box-shadow:0 0 0 1.5px #d2d2d7,0 14px 30px rgba(0,0,0,.08)}
.agentur{position:absolute;display:grid;place-items:center;width:150px;height:150px;border-radius:50%;background:#1d1d1f;color:#fff;font-weight:700;font-size:19px;line-height:1.15;text-align:center}
.chip{position:absolute;padding:10px 18px;border-radius:99px;background:#fff;box-shadow:0 0 0 1.5px #d2d2d7;color:#6e6e73;font-weight:600;font-size:18px}
.mini{display:block;height:7px;border-radius:4px;background:#ececf0;margin-top:8px}
.post{position:absolute;width:118px;height:142px;padding:10px;border-radius:12px;background:#fff;box-shadow:0 0 0 1.5px #d2d2d7,0 10px 24px rgba(0,0,0,.08)}
.post i{display:grid;place-items:center;width:20px;height:20px;border-radius:5px;color:#fff;font-size:11px;font-style:normal;font-weight:700}
.post .bild{height:70px;margin-top:8px;border-radius:7px;display:flex;align-items:flex-end;padding:6px;color:#fff;font-family:"Inter Tight";font-weight:700;font-size:12px;line-height:1.05}
.note{position:absolute;display:flex;align-items:center;gap:12px;padding:14px 18px 14px 14px;border-radius:16px;background:#fff;box-shadow:0 0 0 1.5px #d2d2d7,0 14px 30px rgba(0,0,0,.08)}
.note .app{width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#0b9fbd,#8613a1)}
.note b{display:block;font-size:18px}.note small{display:block;color:#6e6e73;font-size:15px}
.stufe{position:absolute;top:0;height:96px;display:grid;align-content:center;padding:0 34px 0 44px;color:#fff;background:#1d1d1f;clip-path:polygon(0 0,calc(100% - 22px) 0,100% 50%,calc(100% - 22px) 100%,0 100%,22px 50%)}
.stufe b{font-family:"Inter Tight";font-weight:700;font-size:26px}.stufe small{font-size:15px;opacity:.75}
.stufe.erste{padding-left:28px;border-radius:18px 0 0 18px;clip-path:polygon(0 0,calc(100% - 22px) 0,100% 50%,calc(100% - 22px) 100%,0 100%)}
.stufe.letzte{border-radius:0 18px 18px 0;clip-path:polygon(0 0,100% 0,100% 100%,0 100%,22px 50%)}
.farbig{background:linear-gradient(100deg,#0b9fbd 0%,#8613a1 100%);background-size:200% 100%}
.wer{position:absolute;top:-44px;font-weight:700;font-size:18px}
'''
h=[]
# Satz-Ebenen
for a,b,s1,s2 in SZ:
    if s1: h.append(f'<div class="satz" style="{sichtbar(a,b)}"><b>{s1}</b><span>{s2}</span></div>')
# Agentur (S1–S7)
h.append(f'<div class="agentur" style="left:960px;top:400px;{sichtbar(.6,44)}">Deine<br>Agentur</div>')
# Bauherren-Punkte (S1–S7)
random.seed(4); P=[]
while len(P)<22:
    x,y=random.uniform(560,860),random.uniform(250,640)
    if all(math.hypot(x-a,y-b)>38 for a,b in P) and math.hypot(x-720,y-470)>40: P.append((x,y))
FK=(720,470)
svg=[f'<svg class="ab" width="1280" height="720" style="left:0;top:0;{sichtbar(.8,44)}"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#0b9fbd"/><stop offset="1" stop-color="#8613a1"/></linearGradient></defs>']
# Linien Posts -> Punkte (S4)
quellen=[(520,320),(520,440),(520,560)]
for i,(x,y) in enumerate(P[:15]):
    q=quellen[i%3]; L=math.hypot(x-q[0],y-q[1])
    svg.append(f'<line x1="{q[0]}" y1="{q[1]}" x2="{x:.0f}" y2="{y:.0f}" stroke="#d2d2d7" stroke-width="1.5" style="stroke-dasharray:{L:.0f};--l:{L:.0f};animation:{an("zeichne",1.2,19.5+i*.08)},{an("aus",.4,38.5,"forwards")}"/>')
L=math.hypot(FK[0]-520,FK[1]-440)
svg.append(f'<line x1="520" y1="440" x2="{FK[0]}" y2="{FK[1]}" stroke="#3d5bd1" stroke-width="2" style="stroke-dasharray:{L:.0f};--l:{L:.0f};animation:{an("zeichne",1,20.5)},{an("aus",.4,38,"forwards")}"/>')
for i,(x,y) in enumerate(P):
    svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#fff" stroke="#c7c7cc" stroke-width="2" style="animation:{an("einp",.4,1+i*.05)},{an("gesehen",.6,20+i*.1,"forwards")},{an("aus",.4,38.5,"forwards")}"/>')
# Faden FK -> Telefon -> Kalender -> Agentur (S6/S7)
faden="M720 470 C 780 470 800 250 880 250 S 980 250 1000 250 M 1110 250 C 1150 250 1150 380 1080 420"
svg.append(f'<path d="{faden}" fill="none" stroke="url(#g)" stroke-width="6" stroke-linecap="round" style="stroke-dasharray:700;--l:700;animation:{an("zeichne",4,31.5)},{an("aus",.4,38.5,"forwards")}"/>')
svg.append('</svg>')
h.append("".join(svg))
# Familie K.
h.append(f'<div class="ab" style="left:{FK[0]-12}px;top:{FK[1]-12}px;width:24px;height:24px;border-radius:50%;background:#fff;box-shadow:inset 0 0 0 2px #c7c7cc;{sichtbar(1.2,38.6)}"></div>')
h.append(f'<div class="ab" style="left:{FK[0]-16}px;top:{FK[1]-16}px;width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#0b9fbd,#8613a1);box-shadow:0 0 0 10px rgba(11,159,189,.15);opacity:0;--dx:{1035-FK[0]-16+16}px;--dy:{560-FK[1]}px;animation:{an("fkfarbe",.5,25.2,"forwards")},{an("fkzug",1.6,38.6,"forwards")},{an("aus",.4,43.6,"forwards")}"></div>')
h.append(f'<div class="note" style="left:{FK[0]-80}px;top:{FK[1]+34}px;{sichtbar(25.6,31)}"><span class="app"></span><div><b>Familie K.</b><small>lädt die Checkliste Hausbau</small></div></div>')
# Zentrale (S2)
h.append(f'<div class="karte" style="left:80px;top:300px;width:400px;padding:24px;{sichtbar(5.4,10)}"><p style="color:#6e6e73;font-size:15px;font-weight:600">Anfrage an die Zentrale</p><p style="margin-top:8px;font-family:Inter Tight;font-weight:700;font-size:26px;color:#8e8e93">Posting-Idee Bauherren</p><p style="margin-top:14px;display:flex;align-items:center;gap:10px;color:#8e8e93;font-weight:600;font-size:18px"><span style="width:20px;height:20px;border-radius:50%;border:3px solid #d2d2d7;border-top-color:#8e8e93;animation:dreh 1s linear infinite"></span>in Abstimmung …</p></div>')
# Zielgruppen-Chips (S3)
for i,(name,x,y) in enumerate((("Junge Familien",80,270),("Private Bauherren",270,270),("Landwirte",80,326),("+ 17 weitere",226,326))):
    extra=f",{an('chip',.4,11.6,'forwards')}" if name=="Private Bauherren" else ""
    h.append(f'<div class="chip" style="left:{x}px;top:{y}px;animation:{an("ein",.5,10.3+i*.12)}{extra},{an("aus",.4,12.8,"forwards")}">{name}</div>')
# Stapel: Mailing, Posting, Landingpage (S3), bleibt bis S4-Beginn sichtbar
h.append(f'<div class="karte" style="left:96px;top:300px;width:260px;height:180px;transform:rotate(-8deg);{sichtbar(13,44)}"><svg width="260" height="180"><path d="M40 40 h180 v100 h-180 z M40 40 l90 60 l90-60" fill="none" stroke="#8e8e93" stroke-width="2"/></svg></div>')
h.append(f'<div class="post" style="left:300px;top:286px;transform:rotate(7deg);{sichtbar(13.2,44)}"><i style="background:#0a66c2">in</i><div class="bild" style="background:#ececf0"></div><span class="mini"></span></div>')
lp=('<p style="display:flex;gap:6px;padding:10px 14px;border-bottom:1px solid #ececf0"><i style="width:9px;height:9px;border-radius:50%;background:#d2d2d7"></i><i style="width:9px;height:9px;border-radius:50%;background:#d2d2d7"></i><i style="width:9px;height:9px;border-radius:50%;background:#d2d2d7"></i></p>'
    '<div style="display:grid;grid-template-columns:1fr 92px;gap:12px;padding:16px 18px"><div><p style="font-weight:700;color:#3d5bd1;font-size:14px">Deine Agentur</p>'
    '<p style="margin-top:6px;font-family:Inter Tight;font-weight:700;font-size:22px;line-height:1.05">Gut abgesichert ins eigene Zuhause.</p><span style="display:inline-block;margin-top:12px;padding:7px 14px;border-radius:99px;background:#3d5bd1;color:#fff;font-size:13px;font-weight:600">Checkliste Hausbau</span></div>'
    '<div style="border-radius:10px;background:#ececf0;display:grid;place-items:center"><svg width="44" height="44" viewBox="0 0 24 24"><path d="M3.5 11L12 4l8.5 7 M6 9.5V20h12V9.5 M10 20v-5h4v5" fill="none" stroke="#8e8e93" stroke-width="1.6"/></svg></div></div>')
h.append(f'<div class="karte" style="left:80px;top:330px;width:330px;height:220px;overflow:hidden;{sichtbar(13.6,44)}">{lp}</div>')
h.append(f'<div class="ab" style="left:300px;top:510px;padding:6px 14px;border:3px solid #3d5bd1;border-radius:10px;color:#3d5bd1;font-weight:700;font-size:16px;background:#fff;animation:{an("stempel",.35,14.8)},{an("aus",.4,16.8,"forwards")}">im Look deiner Agentur</div>')
# Postings fliegen aus (S4)
for i,(y,k,c,bg,t) in enumerate(((260,"in","#0a66c2","linear-gradient(160deg,#0b9fbd,#3d5bd1)","Bauen ist teuer genug."),(380,"f","#1877f2","linear-gradient(160deg,#3d5bd1,#8613a1)","Rohbau versichert?"),(500,"ig","linear-gradient(135deg,#f58529,#dd2a7b,#8134af)","#1d1d1f","Checkliste Hausbau"))):
    h.append(f'<div class="post" style="left:420px;top:{y-12}px;animation:{an(f"flieg{i+1}",.9,17.4+i*.25)},{an("aus",.4,43.4,"forwards")}"><i style="background:{c}">{k}</i><div class="bild" style="background:{bg}">{t}</div><span class="mini"></span></div>')
# Telefon, Kalender (S6)
h.append(f'<div class="ab" style="left:845px;top:215px;width:70px;height:70px;border-radius:50%;background:#1d1d1f;display:grid;place-items:center;{sichtbar(32.2,38.4,"einp")}"><svg width="34" height="34" viewBox="0 0 24 24" style="animation:klingel .8s 32.8s 3 both"><path d="M6 3.5h3l1.8 4.5-2.3 1.5a11 11 0 0 0 6 6l1.5-2.3 4.5 1.8v3a2 2 0 0 1-2 2A16 16 0 0 1 4 5.5a2 2 0 0 1 2-2z" fill="#fff"/></svg></div>')
h.append(f'<div class="ab" style="left:828px;top:296px;width:110px;text-align:center;font-weight:600;font-size:16px;{sichtbar(32.4,38.4)}">Rückruf</div>')
h.append(f'<div class="karte" style="left:1000px;top:200px;width:110px;overflow:hidden;{sichtbar(33.4,38.4,"einp")}"><p style="background:#1d1d1f;color:#fff;text-align:center;font-weight:700;font-size:15px;padding:5px">Di</p><p style="text-align:center;font-family:Inter Tight;font-weight:700;font-size:30px;padding:8px 0 0">17:00</p><p style="text-align:center;font-weight:600;font-size:14px;color:#6e6e73;padding:2px 0 10px">Beratung</p></div>')
# Kundenkreis (S7)
cx,cy,r=1035,475,140
h.append(f'<div class="ab" style="left:{cx-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px;border-radius:50%;box-shadow:inset 0 0 0 2px #d2d2d7;{sichtbar(38.4,44)}"></div>')
for k in range(8):
    if k==5: continue
    a=math.radians(-90+k*45); x=cx+r*math.cos(a); y=cy+r*math.sin(a)
    h.append(f'<div class="ab" style="left:{x-13:.0f}px;top:{y-13:.0f}px;width:26px;height:26px;border-radius:50%;background:#fff;box-shadow:inset 0 0 0 2px #8e8e93;{sichtbar(38.6+k*.06,44,"einp")}"></div>')
h.append(f'<div class="post" style="left:{cx-59}px;top:{cy-r-190}px;transform:scale(.8);{sichtbar(41,44)}"><i style="background:#0a66c2">in</i><div class="bild" style="background:linear-gradient(160deg,#3d5bd1,#8613a1)">Nachwuchs unterwegs?</div><span class="mini"></span></div>')
h.append(f'<svg class="ab" width="1280" height="720" style="left:0;top:0;{sichtbar(41.3,44)}"><path d="M{cx} {cy-r-55} V {cy-r-14}" stroke="#3d5bd1" stroke-width="2" stroke-dasharray="4 5" fill="none"/></svg>')
h.append(f'<div class="note" style="left:760px;top:600px;{sichtbar(42,44)}"><span class="app"></span><div><b>Neuer Anlass</b><small>Familie K. · Zweitwagen</small></div></div>')
# Stufenbalken (S8)
X0,BW=110,265
stufen=[("Auswählen","Fertige Strecken"),("Betreiben","Posten, vernetzen"),("Vertrieb","Ansprechen, beraten"),("Betreuen","Bestand halten")]
h.append(f'<div class="ab" style="left:0;top:380px;width:1280px;height:120px;{sichtbar(44.4,50.4)}">')
for i,(n,u) in enumerate(stufen):
    cls="stufe"+(" erste" if i==0 else "")+(" letzte" if i==3 else "")
    stil=f"left:{X0+i*(BW+8)}px;width:{BW}px;"
    if i==0: cls+=" farbig"; stil+="background-position:0 0;"
    if i==1: stil+=f"background:linear-gradient(100deg,#0b9fbd 0%,#8613a1 100%);background-size:200% 100%;background-position:100% 0;"
    h.append(f'<div class="{cls}" style="{stil}"><b>{n}</b><small>{u}</small></div>')
# Betreiben zunächst schwarz überdeckt, wird bei 47.6 farbig (Überdeckung blendet aus)
h.append(f'<div class="stufe" style="left:{X0+BW+8}px;width:{BW}px;animation:{an("aus",.6,47.6,"forwards")}"><b>Betreiben</b><small>Posten, vernetzen</small></div>')
h.append(f'<p class="wer" style="left:{X0}px;color:#0b9fbd;animation:{an("ein",.5,45)},{an("aus",.3,47.4,"forwards")}">Selbst machen: Wir liefern</p>')
h.append(f'<p class="wer" style="left:{X0+BW+8}px;color:#1d1d1f;animation:{an("ein",.5,45.3)},{an("aus",.3,47.4,"forwards")}">Dein Team betreibt</p>')
h.append(f'<p class="wer" style="left:{X0}px;color:#8613a1;animation:{an("ein",.5,47.8)}">Machen lassen: Wir liefern und betreiben</p>')
h.append('</div>')
# Endkarte (S9)
h.append(f'<div class="ab" style="left:0;top:0;width:1280px;height:720px;display:grid;place-items:center;text-align:center;animation:{an("ein",.8,50.8)}"><div><p style="font-family:Inter Tight;font-weight:700;font-size:64px;letter-spacing:-.03em">sofort sichtbar</p><p style="margin-top:14px;color:#6e6e73;font-size:24px;font-weight:500">Fertige Vertriebsstrecken für Versicherungsagenturen und Maklerbüros</p><p style="display:inline-block;margin-top:34px;padding:16px 30px;border-radius:99px;background:#1d1d1f;color:#fff;font-weight:600;font-size:22px">Termin auswählen · sofortsichtbar.de</p></div></div>')
open('film.html','w').write(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="buehne">{"".join(h)}</div></body></html>')
json.dump({"dauer":55,"szenen":SZ},open('szenen.json','w'),ensure_ascii=False)
print("ok")
