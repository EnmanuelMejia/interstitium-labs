/* IL 2026-10-01: remove poisoned offline state unconditionally. The service worker is retired; this clears any registered worker and every cache, then the page loads 100% fresh from network. Extracted to an external file so pages with a strict script-src CSP can run it. */
(function(){try{
if("serviceWorker" in navigator){navigator.serviceWorker.getRegistrations().then(function(rs){for(var i=0;i<rs.length;i++){try{rs[i].unregister()}catch(e){}}}).catch(function(){})}
if("caches" in window){caches.keys().then(function(ks){for(var i=0;i<ks.length;i++){try{caches.delete(ks[i])}catch(e){}}}).catch(function(){})}
}catch(e){}})();
