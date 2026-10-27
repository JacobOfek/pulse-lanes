// Pulse Lanes offline support. The cache name changes on every build.
const CACHE='pulse-lanes-202610271734';
const CORE=['/','/manifest.webmanifest','/icons/pulse-lanes-180.png','/icons/pulse-lanes-192.png','/icons/pulse-lanes-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
  if(u.origin===location.origin){   // network first, so a new version shows up; the cache keeps it working offline
    e.respondWith(fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp))}return res})
      .catch(()=>caches.match(r).then(m=>m||(r.mode==='navigate'?caches.match('/'):Response.error()))));return}
  if(/fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)){   // fonts: cache first
    e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res})))}
});
