SRC='/Users/rob/Desktop/_XrossWorld/site/index.html'
html=open(SRC).read()
baseCSS=html.split('<style>',1)[1].split('</style>',1)[0]
orbitalCSS=html.split('<style id="orbital">',1)[1].split('</style>',1)[0]

LOGO=('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
 '<ellipse cx="12" cy="12" rx="10.4" ry="3.8" transform="rotate(32 12 12)" stroke="#E6FF00" stroke-width="1.4"/>'
 '<ellipse cx="12" cy="12" rx="10.4" ry="3.8" transform="rotate(-32 12 12)" stroke="#CBD5E1" stroke-width="1.1" opacity=".5"/>'
 '<circle cx="12" cy="12" r="2.6" fill="#E6FF00"/></svg>')

OGCSS="""
html,body{width:1200px;height:630px;overflow:hidden}
.ogwrap{width:1200px;height:630px;box-sizing:border-box;padding:60px 68px;
  display:flex;flex-direction:column;justify-content:space-between;position:relative;z-index:1}
.ogtop{display:flex;align-items:center;gap:15px}
.ogtop svg{width:42px;height:42px;display:block}
.ogtop .nm{font-size:34px;font-weight:600;letter-spacing:.14em;color:#fff;line-height:1}
.ogtop .sub{font-size:13px;letter-spacing:.24em;color:#64748B;text-transform:uppercase;margin-left:6px}
.oghero{margin:6px 0}
.oghero .qc-bar{margin:0;border-radius:10px;padding:30px 34px;box-shadow:0 24px 60px -12px rgba(230,255,0,.25)}
.oghero .qc-bar .cap{font-size:15px}
.oghero .qc-bar .prt{font-size:12px}
.oghero .qs label{font-size:13px}
.oghero .qc-status{font-size:13px}
.ogfoot{display:flex;justify-content:space-between;align-items:flex-end}
.ogfoot .tag{font-size:30px;color:#fff;font-weight:500;letter-spacing:-.025em;line-height:1.15;max-width:22ch}
.ogfoot .tag em{font-style:normal;color:#E6FF00}
.ogfoot .url{font-size:15px;color:#E6FF00;letter-spacing:.12em;white-space:nowrap}
"""

BAR=('<div class="qc-bar">'
 '<div class="cap"><span>NETWORK MACROS — LIVE</span><span class="prt">TRX 02</span></div>'
 '<div class="qc-sliders">'
 '<div class="qs"><label>PACE <b>62%</b></label><input type="range" min="0" max="100" value="62"></div>'
 '<div class="qs"><label>RISK <b>34%</b></label><input type="range" min="0" max="100" value="34"></div>'
 '<div class="qs"><label>REACH <b>71%</b></label><input type="range" min="0" max="100" value="71"></div>'
 '</div>'
 '<div class="qc-status">ALL POSITIONS NOMINAL. HOLDING.</div></div>')

doc=f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<style>{baseCSS}</style><style id="orbital">{orbitalCSS}</style><style>{OGCSS}</style></head>
<body><div class="ogwrap">
  <div class="ogtop">{LOGO}<span class="nm">ORBITAL</span><span class="sub">Design System</span></div>
  <div class="oghero">{BAR}</div>
  <div class="ogfoot"><div class="tag">High-contrast components.<br>One <em>electric</em> accent.</div><div class="url">orbital-eta-six.vercel.app</div></div>
</div></body></html>"""
open('/tmp/orbital/og.html','w').write(doc)
print('og.html written')
