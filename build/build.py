#!/usr/bin/env python3
"""Builds the standalone Pulse Lanes site (pulse-lanes.pages.dev) from the game's artifact file.

usage: python3 build/build.py SOURCE.html [ICON_OPTION]
  SOURCE.html  the game as published in Claude (body-only, or the full artifact page with its frame)
  ICON_OPTION  a|b|c (see build/icons.py), default a

Writes site/index.html, site/manifest.webmanifest, site/sw.js and site/icons/*.
Every run bumps the service-worker cache name so phones pick up the new version.
"""
import json, os, re, sys, subprocess, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
src = open(sys.argv[1], encoding='utf-8').read()
icon = sys.argv[2] if len(sys.argv) > 2 else 'a'

# the artifact frame (if the source still has it): keep only what's inside <body>
if src.lower().count('<!doctype') >= 1:
    m = re.search(r'<body[^>]*>(.*)</body>', src, re.S | re.I)
    body = m.group(1) if m else src
else:
    body = src

# the same reset the Claude frame gives the page, so it looks exactly as in Claude:
# full-bleed, with room for the iPhone status bar and home indicator
HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#140f22;color:#f4effc}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style>
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" href="/icons/pulse-lanes-192.png">
<link rel="apple-touch-icon" href="/icons/pulse-lanes-180.png">
</head>
<body>
'''
TAIL = '''
<script>if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('/sw.js').catch(()=>{}));</script>
</body>
</html>
'''
os.makedirs(SITE, exist_ok=True)
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(HEAD + body.strip() + TAIL)

json.dump({
    "name": "Pulse Lanes", "short_name": "Pulse Lanes", "start_url": "/", "scope": "/",
    "display": "standalone", "orientation": "any", "background_color": "#140f22", "theme_color": "#140f22",
    "icons": [{"src": "/icons/pulse-lanes-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "/icons/pulse-lanes-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]
}, open(os.path.join(SITE, 'manifest.webmanifest'), 'w'), indent=1)

ver = time.strftime('%Y%m%d%H%M')
SW = '''// Pulse Lanes offline support. The cache name changes on every build.
const CACHE='pulse-lanes-%s';
const CORE=['/','/manifest.webmanifest','/icons/pulse-lanes-180.png','/icons/pulse-lanes-192.png','/icons/pulse-lanes-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
  if(u.origin===location.origin){   // network first, so a new version shows up; the cache keeps it working offline
    e.respondWith(fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp))}return res})
      .catch(()=>caches.match(r).then(m=>m||(r.mode==='navigate'?caches.match('/'):Response.error()))));return}
  if(/fonts\\.(googleapis|gstatic)\\.com$/.test(u.hostname)){   // fonts: cache first
    e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res})))}
});
''' % ver
open(os.path.join(SITE, 'sw.js'), 'w').write(SW)

subprocess.run([sys.executable, os.path.join(ROOT, 'build', 'icons.py'), icon, os.path.join(SITE, 'icons')], check=True)
print('built site/ (cache pulse-lanes-%s, icon %s)' % (ver, icon))
