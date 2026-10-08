#!/usr/bin/env python3
"""HTTP-check every supplemental URL in IL-01..IL-15 using urllib (no subprocess).
Follows redirects, requires final 200. Writes results JSON."""
import json, glob, os, urllib.request, urllib.error, concurrent.futures, ssl, socket

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
OUT = os.path.expanduser("~/workspace/apex-audit/.work/url-check-results.json")

def collect():
    recs = []
    for f in sorted(glob.glob(os.path.join(BASE, "il-0[1-9]-*.json")) + glob.glob(os.path.join(BASE, "il-1[0-5]-*.json"))):
        d = json.load(open(f))
        code = d.get("code")
        for m in d.get("modules", []):
            for v in (m.get("videos") or []):
                if isinstance(v, dict) and v.get("url"):
                    recs.append(dict(course=code, where=f"module:{m.get('id')}", label=v.get("title", ""), url=v["url"]))
        for sl in (d.get("sourceLinks") or []):
            if sl.get("url"):
                recs.append(dict(course=code, where="sourceLinks", label=sl.get("name", ""), url=sl["url"]))
        for jm in (d.get("jdMatrix") or []):
            if jm.get("postingUrl"):
                recs.append(dict(course=code, where="jdMatrix", label=jm.get("postingTitle", ""), url=jm["postingUrl"]))
        if d.get("dossierUrl"):
            recs.append(dict(course=code, where="dossier", label="", url=d["dossierUrl"]))
    seen, uniq = {}, []
    for r in recs:
        if r["url"] not in seen:
            seen[r["url"]] = r
            uniq.append(r)
    return uniq

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def check(rec):
    url = rec["url"]
    final, code = url, None
    try:
        # manual redirect loop (max 8) so we can record the final URL
        for _ in range(8):
            req = urllib.request.Request(final, method="HEAD",
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
            try:
                resp = urllib.request.urlopen(req, timeout=20)
                code = resp.getcode(); final = resp.geturl(); resp.close()
                break
            except urllib.error.HTTPError as e:
                code = e.code
                if code in (301, 302, 303, 307, 308):
                    loc = e.headers.get("Location")
                    if not loc:
                        break
                    final = urllib.parse.urljoin(final, loc)
                    continue
                break
        # some servers reject HEAD; retry with GET on 4xx/5xx (not redirects)
        if code and code >= 400:
            try:
                req = urllib.request.Request(final, method="GET",
                    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36", "Range": "bytes=0-0"})
                resp = urllib.request.urlopen(req, timeout=20)
                code = resp.getcode(); final = resp.geturl(); resp.close()
            except urllib.error.HTTPError as e:
                code = e.code
            except Exception:
                pass
        ok = code == 200
        return dict(rec, http=str(code), final_url=final, ok=ok, err="" if ok else f"final status {code}")
    except Exception as e:
        return dict(rec, http="ERR", final_url=final, ok=False, err=repr(e)[:200])

recs = collect()
print(f"checking {len(recs)} unique urls", flush=True)
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(check, r): r for r in recs}
    for i, fut in enumerate(concurrent.futures.as_completed(futs)):
        results.append(fut.result())
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(recs)} done", flush=True)
json.dump(results, open(OUT, "w"), indent=1)
bad = [r for r in results if not r["ok"]]
print(f"DONE: {len(results)} checked, {len(bad)} non-200")
for r in bad:
    print(f"  [{r['http']}] {r['course']} {r['where']} :: {r['label'][:60]} :: {r['url'][:110]} :: {r['err'][:80]}")
print("wrote", OUT)
