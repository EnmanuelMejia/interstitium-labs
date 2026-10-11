#!/usr/bin/env python3
"""Verify candidate video URLs: HTTP status, YouTube oEmbed author/title, duration."""
import json, re, time, urllib.request, urllib.parse

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}

CANDS = [
    # (key, url)
    ("i7vOAcUo5iA", "https://www.youtube.com/watch?v=i7vOAcUo5iA"),
    ("eI4an8aSsgw", "https://www.youtube.com/watch?v=eI4an8aSsgw"),
    ("LwCRRUa8yTU", "https://www.youtube.com/watch?v=LwCRRUa8yTU"),
    ("Y8oZtFYweTY", "https://www.youtube.com/watch?v=Y8oZtFYweTY"),
    ("VDFRpjQVaME", "https://www.youtube.com/watch?v=VDFRpjQVaME"),
    ("HfACrKJ_Y2w", "https://www.youtube.com/watch?v=HfACrKJ_Y2w"),
    ("JnTa9XtvmfI", "https://www.youtube.com/watch?v=JnTa9XtvmfI"),
    ("rSjt1E9WHaQ", "https://www.youtube.com/watch?v=rSjt1E9WHaQ"),
    ("xxpc-HPKN28", "https://www.youtube.com/watch?v=xxpc-HPKN28"),
    ("HXV3zeQKqGY", "https://www.youtube.com/watch?v=HXV3zeQKqGY"),
    ("ER8oKX5myE0", "https://www.youtube.com/watch?v=ER8oKX5myE0"),
    ("SpfIwlAYaKk", "https://www.youtube.com/watch?v=SpfIwlAYaKk"),
    ("r-uOLxNrNk8", "https://www.youtube.com/watch?v=r-uOLxNrNk8"),
    ("LHBE6Q9XlzI", "https://www.youtube.com/watch?v=LHBE6Q9XlzI"),
    ("WcDaZ67TVRo", "https://www.youtube.com/watch?v=WcDaZ67TVRo"),
    ("Vl0H-qTclOg", "https://www.youtube.com/watch?v=Vl0H-qTclOg"),
    ("_V8eKsto3Ug", "https://www.youtube.com/watch?v=_V8eKsto3Ug"),
    ("g_3IKHG-rfA", "https://www.youtube.com/watch?v=g_3IKHG-rfA"),
    ("b2r9Cdvssi0", "https://www.youtube.com/watch?v=b2r9Cdvssi0"),
    ("cCeC1QiQANU", "https://www.youtube.com/watch?v=cCeC1QiQANU"),
    ("I0iRPqNgPBI", "https://www.youtube.com/watch?v=I0iRPqNgPBI"),
    ("ZXQ7LAsjliA", "https://www.youtube.com/watch?v=ZXQ7LAsjliA"),
    ("learn-tsql-path", "https://learn.microsoft.com/en-us/training/paths/get-started-querying-with-transact-sql/"),
    ("learn-tsql-module", "https://learn.microsoft.com/en-us/training/modules/introduction-to-transact-sql/"),
    ("learn-tsql-shows", "https://learn.microsoft.com/en-us/shows/programming-databases-with-t-sql-for-beginners/"),
    ("learn-pbi-prep", "https://learn.microsoft.com/en-us/training/paths/prepare-data-power-bi/"),
    ("learn-pbi-hub", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"),
    ("learn-pbi-viz", "https://learn.microsoft.com/en-us/training/paths/prepare-visualize-data-power-bi/"),
    ("learn-pbi-model", "https://learn.microsoft.com/en-us/training/modules/design-model-power-bi/"),
    ("learn-purview-path", "https://learn.microsoft.com/en-us/training/paths/purview-protect-govern-ai/"),
    ("learn-purview-module", "https://learn.microsoft.com/en-us/training/modules/describe-purview-data-governance/"),
    ("tableau-training", "https://www.tableau.com/learn/training?playlist=438452"),
    ("tableau-training-gb", "https://www.tableau.com/en-gb/learn/training"),
    ("aws-skillbuilder", "http://aws.amazon.com/training/digital/"),
    ("aws-certprep", "https://aws.amazon.com/certification/certification-prep/"),
    ("dbt-learn", "https://learn.getdbt.com/"),
    ("snowflake-channel", "https://www.youtube.com/user/snowflakecomputing/videos"),
    ("databricks-channel", "https://www.youtube.com/@Databricks"),
    ("gcp-bigquery-blog", "https://cloud.google.com/blog/topics/training-certifications/free-google-cloud-bigquery-training/"),
]

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(400000)
            return r.status, r.url, body
    except Exception as e:
        return None, None, str(e)

def oembed(watch_url):
    q = urllib.parse.urlencode({"url": watch_url, "format": "json"})
    try:
        req = urllib.request.Request("https://www.youtube.com/oembed?" + q, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:
        return None, str(e)

results = {}
for key, url in CANDS:
    st, final, body = fetch(url)
    rec = {"url": url, "http": st, "final": final}
    if st == 200 and isinstance(body, bytes):
        txt = body.decode("utf-8", "replace")
        m = re.search(r'"lengthSeconds":"(\d+)"', txt)
        if m:
            rec["lengthSeconds"] = int(m.group(1))
        # microsoft learn duration hints
        mm = re.search(r'"timeToComplete":"([^"]+)"', txt)
        if mm:
            rec["timeToComplete"] = mm.group(1)
        mm2 = re.findall(r'(\d+)\s*min\b', txt[:20000])
        if mm2 and "learn.microsoft" in url:
            rec["minMentions"] = mm2[:5]
        if "watch?v=" in url:
            ost, odata = oembed(url)
            rec["oembed_status"] = ost
            if isinstance(odata, dict):
                rec["oembed_title"] = odata.get("title")
                rec["oembed_author"] = odata.get("author_name")
    results[key] = rec
    print(json.dumps({key: {k: v for k, v in rec.items() if k != "final"}}, ensure_ascii=False))
    time.sleep(0.4)

with open("/tmp/verify_results.json", "w") as f:
    json.dump(results, f, indent=1, ensure_ascii=False)
print("SAVED", len(results))
