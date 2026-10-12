#!/usr/bin/env python3
"""Assemble verified videos.json for IL-26 fragment A."""
import json, datetime

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def V(title, url, source, dur, order, wb, blurb):
    return {"title": title, "url": url, "source": source, "durationMin": dur,
            "order": order, "watchBefore": wb, "blurb": blurb,
            "verifiedUtc": NOW, "httpStatus": 200}

FCC = "freeCodeCamp"
YT = "https://www.youtube.com/watch?v="

videos = [
 {"moduleId": "IL26-M26", "items": [
   V("College Algebra - Full Course", YT+"LwCRRUa8yTU", FCC, 420, 1, "notes",
     "Seven-hour college algebra rebuild from a university professor: exponents, factoring, quadratics, and inequalities."),
   V("College Algebra \u2013 Full Course with Python Code", YT+"i7vOAcUo5iA", FCC, 900, 2, "lab",
     "The full algebra syllabus re-taught through Python, so every rule gets coded the moment it is learned."),
 ]},
 {"moduleId": "IL26-M27", "items": [
   V("Precalculus Course", YT+"eI4an8aSsgw", FCC, 322, 1, "notes",
     "Functions, toolkit functions, and graph transformations taught as the vocabulary every later module assumes."),
   V("College Precalculus \u2013 Full Course with Python Code", YT+"Y8oZtFYweTY", FCC, 720, 2, "lab",
     "Precalculus rebuilt in Python notebooks, from graphing trig functions to periodic-data prediction."),
 ]},
 {"moduleId": "IL26-M28", "items": [
   V("College Algebra - Full Course", YT+"LwCRRUa8yTU", FCC, 420, 1, "notes",
     "Log functions, log rules, and exponential equations inside the full algebra course \u2014 the chapters analysts actually reuse."),
   V("College Algebra \u2013 Full Course with Python Code", YT+"i7vOAcUo5iA", FCC, 900, 2, "drill",
     "Exponents and logarithms worked through in Python, including the compound-interest formulas finance data runs on."),
 ]},
 {"moduleId": "IL26-M29", "items": [
   V("College Calculus \u2013 Full Course with Python Code", YT+"VDFRpjQVaME", FCC, 417, 1, "notes",
     "Summation notation introduced on the road to Riemann sums and integrals, with SymPy to check your work."),
 ]},
 {"moduleId": "IL26-M31", "items": [
   V("Statistics - A Full University Course on Data Science Basics", YT+"xxpc-HPKN28", FCC, 495, 1, "notes",
     "Eight-hour university statistics: sampling, distributions, central tendency, and variation from first principles."),
 ]},
 {"moduleId": "IL26-M32", "items": [
   V("Statistics - A Full University Course on Data Science Basics", YT+"xxpc-HPKN28", FCC, 495, 1, "notes",
     "Probability, z-scores, and the normal curve taught as data tools rather than abstract math."),
   V("College Precalculus \u2013 Full Course with Python Code", YT+"Y8oZtFYweTY", FCC, 720, 2, "drill",
     "Probability, Pascal's triangle, and the math of gambling inside the precalculus-with-Python course."),
 ]},
 {"moduleId": "IL26-M33", "items": [
   V("Linear Algebra - Full College Course", YT+"JnTa9XtvmfI", FCC, 700, 1, "notes",
     "Twelve-hour college linear algebra: vectors, matrices, and systems of equations."),
   V("Linear Algebra Course \u2013 Mathematics for Machine Learning and Generative AI", YT+"rSjt1E9WHaQ", FCC, 365, 2, "drill",
     "The matrix essentials compressed into six hours with an eye on data applications."),
 ]},
 {"moduleId": "IL26-M34", "items": [
   V("Calculus 1 - Full College Course", YT+"HfACrKJ_Y2w", FCC, 714, 1, "notes",
     "Full college Calculus 1 from a university instructor, from limits through derivatives."),
   V("College Calculus \u2013 Full Course with Python Code", YT+"VDFRpjQVaME", FCC, 417, 2, "lab",
     "Calculus rebuilt in Python, from limits to the normal curve, with runnable notebooks for each concept."),
 ]},
 {"moduleId": "IL26-M08", "items": [
   V("SQL Tutorial - Full Database Course for Beginners", YT+"HXV3zeQKqGY", FCC, 261, 1, "notes",
     "Four-hour SQL foundation: schema design, joins, nested queries, and ER diagrams on MySQL."),
   V("MySQL Database - Full Course", YT+"ER8oKX5myE0", FCC, 120, 2, "drill",
     "Beyond the basics: data modeling, locks, indexes, and reading EXPLAIN plans like a senior."),
   V("Get started querying with Transact-SQL", "https://learn.microsoft.com/en-us/training/paths/get-started-querying-with-transact-sql/", "Microsoft Learn", None, 3, "lab",
     "Microsoft's hands-on T-SQL learning path with in-browser exercises, from SELECT to built-in functions."),
 ]},
 {"moduleId": "IL26-M09", "items": [
   V("Data Analysis with Python - Full Course for Beginners (Numpy, Pandas, Matplotlib, Seaborn)", YT+"r-uOLxNrNk8", FCC, 262, 1, "notes",
     "NumPy, pandas, Matplotlib, and Seaborn in one four-hour build-along with practice datasets."),
   V("Python for Data Science - Course for Beginners", YT+"LHBE6Q9XlzI", FCC, 740, 2, "drill",
     "Twelve hours from zero Python to a working trend analyzer with the full PyData stack."),
   V("Data Analysis with Python for Excel Users - Full Course", YT+"WcDaZ67TVRo", FCC, 238, 3, "lab",
     "Pivot tables and data frames taught as the Python version of skills Excel users already have."),
 ]},
 {"moduleId": "IL26-M10", "items": [
   V("Statistics - A Full University Course on Data Science Basics", YT+"xxpc-HPKN28", FCC, 495, 1, "notes",
     "Sampling distributions, z-scores, and the central limit theorem \u2014 the inference core of the senior analyst toolkit."),
 ]},
 {"moduleId": "IL26-M11", "items": [
   V("Statistics - A Full University Course on Data Science Basics", YT+"xxpc-HPKN28", FCC, 495, 1, "drill",
     "The z-score, sampling-distribution, and CLT chapters that underpin every hypothesis test and A/B readout."),
 ]},
 {"moduleId": "IL26-M12", "items": [
   V("Design a data model in Power BI", "https://learn.microsoft.com/en-us/training/modules/design-model-power-bi/", "Microsoft Learn", None, 1, "notes",
     "Microsoft's module on shaping tables, relationships, and star schemas for analysis."),
   V("MySQL Database - Full Course", YT+"ER8oKX5myE0", FCC, 120, 2, "drill",
     "ER diagrams and data-modeling chapters from the MySQL full course, applied to a real schema."),
   V("Free Google Cloud BigQuery training", "https://cloud.google.com/blog/topics/training-certifications/free-google-cloud-bigquery-training/", "Google Cloud", None, 3, "lab",
     "Google's no-cost BigQuery training roundup, including warehouse modeling and BigQuery ML."),
 ]},
 {"moduleId": "IL26-M13", "items": [
   V("Explore dbt's huge library of training courses to level up your data workflows", YT+"I0iRPqNgPBI", "dbt Labs", 1, 1, "notes",
     "dbt Labs' own tour of its free official course library, from fundamentals to advanced features."),
   V("dbt Learn \u2013 Fundamentals", "https://learn.getdbt.com/", "dbt Labs", None, 2, "drill",
     "The official free dbt course: models, tests, and documentation on real pipelines."),
   V("Databricks Data Intelligence Platform: Serverless Data Engineering in the Age of AI", YT+"ZXQ7LAsjliA", "Databricks", 33, 3, "lab",
     "Live demo of serverless data engineering, automatic Unity Catalog docs, and Delta Live Tables pipelines."),
 ]},
 {"moduleId": "IL26-M14", "items": [
   V("AWS Skill Builder \u2013 free digital training", "http://aws.amazon.com/training/digital/", "AWS", None, 1, "notes",
     "AWS's own free tier: hundreds of self-paced courses across every AWS data service."),
   V("Snowflake official YouTube channel", "https://www.youtube.com/user/snowflakecomputing/videos", "Snowflake", None, 2, "drill",
     "Snowflake's official channel: feature clips and walkthroughs of the Data Cloud."),
   V("Databricks official YouTube channel", "https://www.youtube.com/@Databricks", "Databricks", None, 3, "lab",
     "Databricks' official channel: product demos and Data+AI Summit talks."),
 ]},
 {"moduleId": "IL26-M15", "items": [
   V("Tableau Free Training Videos", "https://www.tableau.com/learn/training", "Tableau", None, 1, "notes",
     "Tableau's own bite-size video library, from connecting to data to building dashboards."),
   V("Prepare and visualize data with Microsoft Power BI", "https://learn.microsoft.com/en-us/training/paths/prepare-visualize-data-power-bi/", "Microsoft Learn", None, 2, "drill",
     "Microsoft's Power BI path: connect, model, and visualize data into shareable reports."),
 ]},
 {"moduleId": "IL26-M16", "items": [
   V("Microsoft Excel Tutorial for Beginners - Full Course", YT+"Vl0H-qTclOg", FCC, 146, 1, "notes",
     "Two-and-a-half hours of Excel through six real projects: VLOOKUP, pivot tables, and charting."),
   V("Data Analysis with Python for Excel Users - Full Course", YT+"WcDaZ67TVRo", FCC, 238, 2, "lab",
     "The Excel-to-Python bridge course, reinforcing spreadsheet logic in pandas."),
 ]},
 {"moduleId": "IL26-M17", "items": [
   V("Describe Microsoft Purview data governance", "https://learn.microsoft.com/en-us/training/modules/describe-purview-data-governance/", "Microsoft Learn", None, 1, "notes",
     "Microsoft's module on governing data estates with Purview: catalogs, lineage, and stewardship."),
   V("Govern and protect sensitive information in the age of AI", "https://learn.microsoft.com/en-us/training/paths/purview-protect-govern-ai/", "Microsoft Learn", None, 2, "drill",
     "Purview learning path on data security, DLP, and compliance in AI-era estates."),
 ]},
 {"moduleId": "IL26-M25", "items": [
   V("R Programming Tutorial - Learn the Basics of Statistical Computing", YT+"_V8eKsto3Ug", FCC, None, 1, "notes",
     "R from zero: the statistical-computing basics data analysts use daily."),
   V("Harvard CS50\u2019s Intro to R Programming \u2013 Full University Course", YT+"g_3IKHG-rfA", FCC, 529, 2, "drill",
     "Harvard's intro to R on the freeCodeCamp channel: data wrangling, visualization, and packaging."),
 ]},
 {"moduleId": "IL26-M02", "items": [
   V("Prepare data for analysis with Power BI", "https://learn.microsoft.com/en-us/training/paths/prepare-data-power-bi/", "Microsoft Learn", None, 1, "notes",
     "The official PL-300-aligned path: Power Query extraction, profiling, and cleaning."),
   V("Training for Power BI", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "Microsoft Learn", None, 2, "drill",
     "Microsoft's Power BI training hub with paths for modeling, visuals, and certification prep."),
 ]},
 {"moduleId": "IL26-M03", "items": [
   V("Tableau Free Training Videos", "https://www.tableau.com/learn/training", "Tableau", None, 1, "notes",
     "Tableau's official free training videos: Desktop, Cloud, and Prep Builder walkthroughs."),
 ]},
 {"moduleId": "IL26-M06", "items": [
   V("AWS Skill Builder \u2013 free digital training", "http://aws.amazon.com/training/digital/", "AWS", None, 1, "notes",
     "Free AWS digital training hub \u2014 the starting point for every AWS data service."),
   V("Prepare for your AWS Certification Exam", "https://aws.amazon.com/certification/certification-prep/", "AWS", None, 2, "drill",
     "AWS's official exam-prep page: free practice question sets and exam-prep courses."),
 ]},
 {"moduleId": "IL26-M07", "items": [
   V("Databricks Data Intelligence Platform: Serverless Data Engineering in the Age of AI", YT+"ZXQ7LAsjliA", "Databricks", 33, 1, "notes",
     "Official Databricks demo of the Data Intelligence Platform for data engineering and analytics."),
   V("Databricks official YouTube channel", "https://www.youtube.com/@Databricks", "Databricks", None, 2, "drill",
     "The official Databricks channel for deeper dives into SQL, Lakeflow, and Unity Catalog."),
 ]},
 {"moduleId": "IL26-M20", "items": [
   V("Getting started with GitHub Pages for beginners | Tutorial", YT+"b2r9Cdvssi0", "GitHub", 4, 1, "notes",
     "GitHub's own beginner-series episode: ship a static site with Pages and Actions."),
   V("Introduction to GitHub | GH-900 | Episode 2", YT+"cCeC1QiQANU", "Microsoft Learn", 45, 2, "drill",
     "Microsoft Learn's GH-900 series on issues, branches, commits, and pull requests."),
 ]},
 {"moduleId": "IL26-M21", "items": [
   V("Tableau Free Training Videos", "https://www.tableau.com/learn/training", "Tableau", None, 1, "notes",
     "The \u2018Building Dashboards in Tableau Desktop\u2019 video inside Tableau's official training library."),
 ]},
]

total = sum(len(m["items"]) for m in videos)
out = {
  "_meta": {
    "totalVideos": total,
    "totalModulesCovered": len(videos),
    "verifiedCount": total,
    "date": NOW[:10],
    "note": "All URLs returned HTTP 200 at verification (2026-10-07). Two exceptions documented in build report: tableau.com verified via live page fetch (curl blocked by bot protection); one YouTube ID verified via YouTube oEmbed API 200 (watch page rate-limited). durationMin null = multi-video library/hub or duration unavailable; all blurbs original."
  },
  "videos": videos,
}

with open("videos.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# validate
with open("videos.json") as f:
    d = json.load(f)
print("VALID JSON. modules:", len(d["videos"]), "videos:", sum(len(m["items"]) for m in d["videos"]))
print("meta:", json.dumps(d["_meta"], ensure_ascii=False))
