SRC='/Users/rob/Desktop/_XrossWorld/site/index.html'
html=open(SRC).read()
baseCSS=html.split('<style>',1)[1].split('</style>',1)[0]
orbitalCSS=html.split('<style id="orbital">',1)[1].split('</style>',1)[0]
script=html.split('<script>',1)[1].split('</script>',1)[0]
QC=script[script.index('let qcT=null'):]   # the quantum-core module (consts + functions)

LOGO=('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
 '<ellipse cx="12" cy="12" rx="10.4" ry="3.8" transform="rotate(32 12 12)" stroke="#E6FF00" stroke-width="1.4"/>'
 '<ellipse cx="12" cy="12" rx="10.4" ry="3.8" transform="rotate(-32 12 12)" stroke="#CBD5E1" stroke-width="1.1" opacity=".5"/>'
 '<circle cx="12" cy="12" r="2.6" fill="#E6FF00"/></svg>')

OGCSS="""
html,body{width:1200px;height:630px;overflow:hidden}
.ogwrap{width:1200px;height:630px;box-sizing:border-box;padding:30px 40px 26px;display:flex;flex-direction:column;gap:16px;position:relative;z-index:1}
.ogtop{display:flex;align-items:center;gap:13px;flex:none}
.ogtop svg{width:32px;height:32px;display:block}
.ogtop .nm{font-size:25px;font-weight:600;letter-spacing:.14em;color:#fff;line-height:1}
.ogtop .sub{font-size:11px;letter-spacing:.24em;color:#64748B;text-transform:uppercase;margin-left:4px}
.ogtop .url{margin-left:auto;font-size:13px;color:#E6FF00;letter-spacing:.1em}
.ogdeck{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.ogdeck .qc-shell{width:100%}
.ogdeck .qc{padding:20px}
.ogdeck .qc-top{padding:4px 6px 14px}
.ogdeck .qc-time{font-size:46px}
#qcCanvas{height:96px}
.ogdeck .qc-bar{padding:16px 20px}
"""

QCMARKUP=('<div class="qc-shell"><div class="qc">'
 '<div class="qc-top">'
 '<div><div class="qc-day">CAMPAIGN-Q3 · TRANCHE 2/6</div><div class="qc-time" id="qcClock">09:59<sup id="qcSec">13</sup></div></div>'
 '<div style="text-align:right"><div class="qc-day">NETWORK</div><div style="font-size:18px;font-weight:400">41 LIVE</div></div>'
 '</div>'
 '<div class="qc-grid">'
 '<div class="qc-matrix"><div class="cap">X_CORE // CAMPAIGN_STATE</div><canvas id="qcCanvas"></canvas></div>'
 '<div class="qc-log"><div class="cap">OPERATION LOGS</div><div id="qcLog"></div></div>'
 '</div>'
 '<div class="qc-bar">'
 '<div class="cap"><span>NETWORK MACROS — LIVE</span><span class="prt">TRX 02</span></div>'
 '<div class="qc-sliders">'
 '<div class="qs"><label>PACE <b>14%</b></label><input type="range" min="0" max="100" value="14"></div>'
 '<div class="qs"><label>RISK <b>64%</b></label><input type="range" min="0" max="100" value="64"></div>'
 '<div class="qs"><label>REACH <b>71%</b></label><input type="range" min="0" max="100" value="71"></div>'
 '</div>'
 '<div class="qc-status">ALL POSITIONS NOMINAL. HOLDING.</div>'
 '</div></div></div>')

JS=("const DPR=Math.min(devicePixelRatio||1,2);"
 "function el(h){const d=document.createElement('div');d.innerHTML=h;return d.firstElementChild}"
 + QC +
 "\nstartQC();"
 "setTimeout(function(){qcDraw('LIVE \\u00b7 41');"
 "qcLog('EXECUTING: PACE \\u2192 14%',true);qcLog('NETWORK STABLE. HOLDING.');qcLog('EXECUTING: RISK \\u2192 64%',true);},220);")

doc=f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<style>{baseCSS}</style><style id="orbital">{orbitalCSS}</style><style>{OGCSS}</style></head>
<body><div class="ogwrap">
  <div class="ogtop">{LOGO}<span class="nm">ORBITAL</span><span class="sub">Design System</span><span class="url">orbital-eta-six.vercel.app</span></div>
  <div class="ogdeck">{QCMARKUP}</div>
</div><script>{JS}</script></body></html>"""
open('/tmp/orbital/og2.html','w').write(doc)
print('og2.html written')
