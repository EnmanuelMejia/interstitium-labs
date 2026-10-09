import re, html, json, sys, os
from html.parser import HTMLParser
from urllib.parse import urljoin

PAGES = {
    "home": "https://interstitiumlabs.dev/",
    "univ": "https://interstitiumlabs.dev/university/",
    "il29": "https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery",
    "academy": "https://interstitiumlabs.dev/university/academy.html",
    "tlboot": "https://interstitiumlabs.dev/bootcamps/tl-interview/",
    "tlprep": "https://interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/",
    "enroll": "https://interstitiumlabs.dev/enroll.html",
    "portfolio": "https://enmanueldmejia.com/",
    "app": "https://app.interstitiumlabs.dev/",
}

DATA_DIR = "/home/hatch/workspace/apex-audit/.work/asset-scratch"

class Extractor(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.assets = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("href"):
            rel = (a.get("rel") or "").lower()
            self.assets.append((urljoin(self.base, a["href"]), "link[%s]" % rel, "link"))
        if tag == "script" and a.get("src"):
            self.assets.append((urljoin(self.base, a["src"]), "script", "script"))
        if tag == "img" and a.get("src"):
            self.assets.append((urljoin(self.base, a["src"]), "img", "img"))
        for t in ("img", "source"):
            if tag == t and a.get("srcset"):
                for part in a["srcset"].split(","):
                    u = part.strip().split(" ")[0]
                    if u:
                        self.assets.append((urljoin(self.base, u), "%s[srcset]" % t, t))
        if tag in ("video", "audio", "source", "embed", "track"):
            for k in ("src", "data-src"):
                if a.get(k):
                    self.assets.append((urljoin(self.base, a[k]), "%s[%s]" % (tag, k), tag))
        if tag == "meta":
            prop = (a.get("property") or a.get("name") or "").lower()
            if prop in ("og:image", "og:image:secure_url", "twitter:image") and a.get("content"):
                self.assets.append((urljoin(self.base, a["content"]), "meta[%s]" % prop, "meta"))

results = {}
for name, url in PAGES.items():
    path = os.path.join(DATA_DIR, "page_%s.html" % name)
    base_url = url
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        htmltext = f.read()
    m = re.search(r'<base[^>]+href=["\']([^"\']+)["\']', htmltext, re.I)
    if m:
        base_url = urljoin(url, m.group(1))
    ex = Extractor(base_url)
    ex.feed(htmltext)
    for mu in re.findall(r'url\(\s*["\']?([^"\'\)]+)["\']?\s*\)', htmltext):
        mu = mu.strip()
        if mu.startswith("data:"):
            continue
        ex.assets.append((urljoin(base_url, mu), "css-url()", "inline"))
    seen, ded = [], set()
    for u, kind, tag in ex.assets:
        u = html.unescape(u)
        if u.startswith(("data:", "javascript:", "mailto:", "tel:")):
            continue
        key = (u, kind)
        if key not in ded:
            ded.add(key)
            seen.append({"url": u, "kind": kind})
    results[name] = {"page_url": url, "assets": seen}

with open(os.path.join(DATA_DIR, "assets.json"), "w") as f:
    json.dump(results, f, indent=1)

total = sum(len(v["assets"]) for v in results.values())
print("pages=%d total_asset_refs=%d" % (len(results), total))
for name, v in results.items():
    print("  %s: %d" % (name, len(v["assets"])))

# unique url map
url_pages, url_kind = {}, {}
for name, v in results.items():
    for a in v["assets"]:
        url_pages.setdefault(a["url"], []).append(name)
        url_kind.setdefault(a["url"], a["kind"])
json.dump({"url_pages": url_pages, "url_kind": url_kind},
          open(os.path.join(DATA_DIR, "urlmap.json"), "w"))
import re as _re
css = [u for u in url_pages if _re.search(r"\.css(\?|#|$)", u)]
open(os.path.join(DATA_DIR, "csslist.txt"), "w").write("\n".join(css) + "\n")
open(os.path.join(DATA_DIR, "urllist.txt"), "w").write("\n".join(url_pages.keys()) + "\n")
print("unique=%d css=%d" % (len(url_pages), len(css)))
