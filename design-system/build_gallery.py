#!/usr/bin/env python3
import json, os, re, sys

SRC = '/Users/rob/Desktop/_XrossWorld/site/index.html'
OUT = ['/Users/rob/Desktop/_XrossWorld/site/gallery.html', '/tmp/xw-site/gallery.html',
       '/Users/rob/Desktop/_XrossWorld/orbital/index.html', '/tmp/orbital/index.html']
ORDER = ['foundations', 'campaign', 'carousel', 'cards', 'motion', 'chat', 'heroes']
WIDE = re.compile(r'(hero|grid|mission|console|stage|globe|emitter|deck|thread|feed|lattice|price tag|ticker|wordmark)', re.I)

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

html = open(SRC).read()
baseCSS    = html.split('<style>',1)[1].split('</style>',1)[0]
orbitalCSS = html.split('<style id="orbital">',1)[1].split('</style>',1)[0]
script     = html.split('<script>',1)[1].split('</script>',1)[0]
# strip only the page-router (everything before `function toast(` is the routing block)
i1 = script.index('function toast(')
driverJS = script[i1:]
# genericize brand strings that live in the driver JS (carousel card lockup)
driverJS = driverJS.replace('XW · Stable', 'ORBITAL · Stable')
driverJS = driverJS.replace(
    '<path d="M3 3L21 21M21 3L3 21" stroke="#020617" stroke-width="3" stroke-linecap="round"/>',
    '<ellipse cx="12" cy="12" rx="10" ry="3.6" transform="rotate(32 12 12)" stroke="#020617" stroke-width="2"/><circle cx="12" cy="12" r="2.6" fill="#020617"/>')

CHROME = """
/* ===== gallery chrome ===== */
.dsx-top{position:sticky;top:0;z-index:60;display:flex;align-items:center;gap:12px;padding:13px 22px;background:rgba(2,6,23,.88);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(203,213,225,.16)}
.dsx-top svg{width:22px;height:22px;flex:none;display:block}
.dsx-top h1{font-size:14px;letter-spacing:.16em;margin:0;color:#fff;font-weight:600}
.dsx-top .sub{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#64748B;margin-left:auto}
@media(max-width:560px){.dsx-top .sub{display:none}}
.dsx-wrap{display:grid;grid-template-columns:212px 1fr;align-items:start}
.dsx-nav{position:sticky;top:50px;align-self:start;padding:22px 14px;border-right:1px solid rgba(203,213,225,.12);min-height:calc(100dvh - 50px)}
.dsx-nav a{display:block;padding:9px 12px;border-radius:2px;color:#94A3B8;font-size:12px;letter-spacing:.05em;text-decoration:none;text-transform:uppercase;transition:color .15s,background .15s}
.dsx-nav a:hover{color:#fff;background:rgba(255,255,255,.05)}
.dsx-nav a.on{color:#020617;background:#E6FF00;font-weight:600}
.dsx-main{padding:30px 28px 140px;min-width:0}
.dsx-intro{border:1px solid rgba(203,213,225,.16);background:#070C1A;padding:26px 24px;margin-bottom:30px}
.dsx-intro h2{color:#fff;font-size:clamp(24px,3.4vw,34px);letter-spacing:-.03em;margin:0 0 8px}
.dsx-intro p{color:#94A3B8;font-size:13px;max-width:74ch;margin:0}
.dsx-sec{scroll-margin-top:66px;padding:26px 0 6px}
.dsx-sec>h2{font-size:clamp(21px,3vw,29px);letter-spacing:-.03em;color:#fff;margin:0;display:flex;align-items:baseline;gap:12px}
.dsx-sec>h2::before{content:"";width:9px;height:9px;background:#E6FF00;display:inline-block}
.dsx-sec>.bl{color:#64748B;font-size:13px;margin:9px 0 22px;max-width:72ch}
.dsx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:20px;align-items:start}
.dsx-frame{border:1px solid rgba(203,213,225,.16);background:#070C1A;overflow:hidden}
.dsx-frame.wide{grid-column:1/-1}
.dsx-cap{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;padding:11px 14px;border-bottom:1px solid rgba(203,213,225,.12);background:rgba(255,255,255,.02)}
.dsx-cap b{color:#fff;font-size:12px;letter-spacing:.03em;font-weight:600}
.dsx-cap .st{color:#0F172A;background:#E6FF00;font-size:9px;letter-spacing:.12em;text-transform:uppercase;padding:2px 7px;font-weight:600}
.dsx-cap .bl{flex-basis:100%;color:#64748B;font-size:11px;line-height:1.55;margin-top:2px}
.dsx-stage{padding:22px;display:flex;flex-direction:column;gap:16px}
.dsx-stage .btn-navy{outline:1px solid rgba(230,255,0,.22)}
.dsx-row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
@media(max-width:860px){
  .dsx-wrap{grid-template-columns:1fr}
  .dsx-nav{position:static;min-height:0;border-right:none;border-bottom:1px solid rgba(203,213,225,.12);display:flex;gap:6px;overflow-x:auto;padding:11px}
  .dsx-nav a{white-space:nowrap}
  .dsx-main{padding:20px 15px 100px}
  .dsx-grid{grid-template-columns:1fr}
}
"""

cats, navlinks, inits = [], [], []
missing = []
for cid in ORDER:
    p = f'/tmp/xw-gallery-{cid}.json'
    if not os.path.exists(p):
        missing.append(cid); continue
    try:
        spec = json.load(open(p))
    except Exception as e:
        missing.append(f'{cid} (bad json: {e})'); continue
    name = spec.get('category', cid.title())
    blurb = spec.get('blurb', '')
    navlinks.append(f'<a href="#sec-{cid}">{name}</a>')
    frames = []
    for c in spec.get('components', []):
        nm = c.get('name', '')
        bl = c.get('blurb', '')
        states = c.get('states', []) or []
        body = c.get('html', '')
        ij = (c.get('initJs') or '').strip()
        if ij:
            inits.append(ij)
        wide = ' wide' if WIDE.search(nm) else ''
        sts = ''.join(f'<span class="st">{esc(s)}</span>' for s in states)
        bln = f'<span class="bl">{esc(bl)}</span>' if bl else ''
        frames.append(
            f'<div class="dsx-frame{wide}"><div class="dsx-cap"><b>{esc(nm)}</b>{sts}{bln}</div>'
            f'<div class="dsx-stage">{body}</div></div>'
        )
    cats.append(
        f'<section class="dsx-sec" id="sec-{cid}"><h2>{esc(name)}</h2>'
        f'<p class="bl">{esc(blurb)}</p><div class="dsx-grid">{"".join(frames)}</div></section>'
    )

# chat thread populate (driver primitives are global) + dedup inits + scrollspy
init_calls = '\n'.join(f'  try{{ {x} }}catch(e){{console.warn("init",e)}}' for x in dict.fromkeys(inits))
INIT = f"""
function dsxBoot(){{
{init_calls}
  // live chat demo
  try{{
    if(document.getElementById('chatlog')){{
      window.agentName='Marlowe';
      meMsg('Sell a product drop');
      note('goal \\u2192 <b>Sell a product drop</b>');
      setTimeout(()=>agentMsg("Good \\u2014 cost per result, not applause. What's the tranche size?",()=>chips(['$25K test','$100K tranche','$250K'])),350);
    }}
  }}catch(e){{console.warn('chat',e)}}
  // scrollspy
  const links=[...document.querySelectorAll('.dsx-nav a')];
  const io=new IntersectionObserver(es=>{{es.forEach(e=>{{if(e.isIntersecting)links.forEach(l=>l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id))}})}},{{rootMargin:'-35% 0px -60% 0px'}});
  document.querySelectorAll('.dsx-sec').forEach(s=>io.observe(s));
}}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(dsxBoot,80));
else setTimeout(dsxBoot,80);
// canvases that measure once (lattice, resonance emitter) need a re-measure after layout settles
setTimeout(()=>window.dispatchEvent(new Event('resize')),260);
setTimeout(()=>window.dispatchEvent(new Event('resize')),900);
"""

LOGO = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<ellipse cx="12" cy="12" rx="10.4" ry="3.8" transform="rotate(32 12 12)" stroke="#E6FF00" stroke-width="1.5"/>'
        '<ellipse cx="12" cy="12" rx="10.4" ry="3.8" transform="rotate(-32 12 12)" stroke="#CBD5E1" stroke-width="1.2" opacity=".5"/>'
        '<circle cx="12" cy="12" r="2.8" fill="#E6FF00"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E"
           "%3Crect width='24' height='24' fill='%23020617'/%3E"
           "%3Cellipse cx='12' cy='12' rx='10' ry='3.6' transform='rotate(32 12 12)' fill='none' stroke='%23E6FF00' stroke-width='1.4'/%3E"
           "%3Ccircle cx='12' cy='12' r='3' fill='%23E6FF00'/%3E%3C/svg%3E")

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#020617">
<title>Orbital — Design System</title>
<meta name="description" content="Orbital — a high-contrast, neon-on-navy interface system. Every component live, in one playground.">
<meta property="og:title" content="Orbital — Design System">
<meta property="og:description" content="A high-contrast, neon-on-navy interface system. Every component live, in one playground.">
<link rel="icon" href="{FAVICON}">
<style>{baseCSS}</style>
<style id="orbital">{orbitalCSS}</style>
<style>{CHROME}</style>
</head>
<body>
<div class="dsx-top">{LOGO}<h1>ORBITAL</h1><span class="sub">Design System</span></div>
<div class="dsx-wrap">
<nav class="dsx-nav">{''.join(navlinks)}</nav>
<main class="dsx-main">
<div class="dsx-intro"><h2>Orbital — the component system</h2><p>A high-contrast, neon-on-navy interface language: flat white surfaces, hard offset shadows, square corners, and one electric accent. Every component here is live — rendered from the system's own CSS and JS — organized by the surfaces it builds: foundations, campaign-management controls, the selection carousel, profile &amp; data cards, animated globes, chat &amp; scoring, and landing heroes. Interact with anything; this is the playground before it ports to Storybook.</p></div>
{''.join(cats)}
</main>
</div>
<div class="toast" id="toast"></div>
<script>{driverJS}</script>
<script>{INIT}</script>
</body>
</html>"""

for o in OUT:
    os.makedirs(os.path.dirname(o), exist_ok=True)
    open(o, 'w').write(doc)

print(f'built gallery: {len(doc)} bytes, {len(cats)} categories, {len(list(dict.fromkeys(inits)))} init calls')
print('categories:', [c.split('id="sec-')[1].split('"')[0] for c in cats])
if missing:
    print('MISSING SPEC FILES:', missing)
