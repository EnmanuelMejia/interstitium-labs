"""IL-15 retrofit: shard-h.json paths.

For each of the 5 IL-15 paths ensures:
- topics: string list drawn from the path's own module coverage
- sources: [{name, url, note}] reusing ONLY URLs already in the repo
  (from docs/university/data/catalog/shard-h-sources.json 'used_in' mapping)
- il_provides: 2-3 sentence instructor-voice blurb
Preserves every existing field.
"""
import json
import os

SHARD = os.path.expanduser("~/workspace/apex-audit/docs/university/data/catalog/shard-h.json")
SRC = os.path.expanduser("~/workspace/apex-audit/docs/university/data/catalog/shard-h-sources.json")

BANNED = ["aleks", "brilliant", "khan academy", "coursera", "udemy", "edx", "palantir"]

TOPICS = {
    "data-eng-interview-prep": [
        "Advanced SQL: window functions, CTEs, join patterns",
        "Aggregation at the right grain",
        "Python data wrangling with pandas",
        "Chunked processing for data bigger than memory",
        "Batch pipeline design: extraction, orchestration, backfills",
        "Apache Airflow: DAGs, sensors, retries",
        "Apache Spark: partitions, shuffles, skew",
        "Streaming systems: event time, Kafka, delivery semantics",
        "Data modeling: star schemas, SCDs, medallion layers",
        "Data-quality gates and pipeline debugging",
        "Timed mock circuits with scoring rubrics",
    ],
    "data-science-interview-prep": [
        "Probability distributions: normal, binomial, Poisson",
        "Expectation, variance, and the central limit theorem",
        "Confidence intervals and honest p-value interpretation",
        "Exploratory analysis with pandas",
        "Merge safety and leakage prevention",
        "Regression, classification, and metric selection",
        "Overfitting, regularization, validation discipline",
        "A/B testing: randomization, power, sample size",
        "Experiment sins: peeking, multiple testing, interference",
        "Case-study framing and narrative",
        "Timed DS mock loops with rubrics",
    ],
    "data-analyst-interview-prep": [
        "SQL foundations: joins, GROUP BY, subqueries, EXISTS",
        "COUNT(*) vs COUNT(column) and NULL semantics",
        "Spreadsheet lookups, references, and pivot tables",
        "Formula-based, auditable data cleaning",
        "Chart selection and honest axes",
        "Dashboards that drive decisions",
        "North Star and input metrics",
        "Funnels, cohorts, and retention curves",
        "Segmentation and the metric-moved drill",
        "Recommendation memos and stakeholder walkthroughs",
        "Timed analyst mock loops with rubrics",
    ],
    "ml-interview-prep": [
        "Bias-variance tradeoff and regularization",
        "Maximum likelihood and loss-function intuition",
        "Gradient descent variants and failure modes",
        "Backprop, activations, and initialization",
        "CNNs, RNNs, LSTMs, and the attention handoff",
        "Training-curve diagnosis",
        "ML system design: framing, skew, feature stores",
        "Monitoring: drift, retraining triggers, champion/challenger",
        "From-scratch coding: k-means, gradient descent, tree splits",
        "Experiment tracking, ablations, model cards",
        "Timed ML mock loops with rubrics",
    ],
    "sql-analytics-drills": [
        "Join fluency: inner, outer, anti-joins, self-joins",
        "EXISTS vs IN and NULL-safe patterns",
        "Window functions: ranking, LAG/LEAD, frames",
        "Top-N per group and running totals",
        "CTEs as query architecture",
        "Recursive CTEs: hierarchies and date spines",
        "Funnel queries in SQL",
        "Cohort and retention queries",
        "Sessionization with window functions",
        "Portable pivoting via conditional aggregation",
        "Timed mixed-pattern circuits",
    ],
}

IL_PROVIDES = {
    "data-eng-interview-prep": (
        "I'm your instructor for this path, and I'll take you from SQL fluency through pipeline "
        "system design to full mock circuits. You'll whiteboard batch and streaming pipelines end to end, "
        "defend every modeling choice aloud, and finish with a capstone pipeline you can walk an "
        "interviewer through line by line."
    ),
    "data-science-interview-prep": (
        "I'm your instructor for this path, and we'll build the complete DS interview stack: the "
        "probability floor, live pandas analysis, modeling judgment, and experimentation design. You'll "
        "rehearse each round's shape — stats, analysis, experiment whiteboard, case — until the method, "
        "not just the answer, is what you bring into the room."
    ),
    "data-analyst-interview-prep": (
        "I'm your instructor for this path, and we'll turn you into the analyst who answers 'how many "
        "users did X' without breaking a sweat. SQL foundations, spreadsheet craft, honest visualization, "
        "and the metrics judgment to diagnose a moved metric like a detective — closed out with a "
        "portfolio project and full mock loops."
    ),
    "ml-interview-prep": (
        "I'm your instructor for this path, and we'll go from ML theory derived on the board to system "
        "design for production. You'll implement algorithms from scratch in vectorized NumPy, design "
        "monitored ML systems with honest complexity, and run full mock loops scored the way hiring "
        "committees score them."
    ),
    "sql-analytics-drills": (
        "I'm your instructor for this circuit, and this is where SQL becomes reflex. Five drill modules — "
        "joins, windows, CTEs, analytics patterns — then full timed mixed circuits with narration and "
        "recovery practice. You'll leave recognizing the pattern in the question before you start writing."
    ),
}


def main():
    with open(SHARD) as f:
        shard = json.load(f)
    with open(SRC) as f:
        srcs = json.load(f)["sources"]

    by_path = {}
    for s in srcs:
        for pid in s.get("used_in", []):
            by_path.setdefault(pid, []).append(
                {"name": s["name"], "url": s["url"], "note": s.get("description", "")}
            )

    for p in shard["paths"]:
        pid = p["id"]
        p["topics"] = TOPICS[pid]
        p["sources"] = by_path.get(pid, [])
        p["il_provides"] = IL_PROVIDES[pid]
        blob = p["il_provides"] + " ".join(p["topics"])
        for b in BANNED:
            if b in blob.lower():
                raise ValueError("banned term %r in path %s" % (b, pid))
        if not (2 <= p["il_provides"].count(".") + p["il_provides"].count("!") <= 4):
            print("warn: sentence count check for", pid)

    tmp = SHARD + ".tmp"
    with open(tmp, "w") as f:
        json.dump(shard, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(tmp) as f:
        check = json.load(f)
    assert len(check["paths"]) == 5
    for p in check["paths"]:
        assert isinstance(p["topics"], list) and all(isinstance(t, str) for t in p["topics"])
        assert isinstance(p["sources"], list) and all(
            set(s.keys()) == {"name", "url", "note"} for s in p["sources"]
        )
        assert isinstance(p["il_provides"], str) and len(p["il_provides"]) > 50
    os.replace(tmp, SHARD)
    print("shard-h: 5 paths retrofitted (topics/sources/il_provides); file re-validated")
    for p in check["paths"]:
        print("  %s: topics=%d sources=%d" % (p["id"], len(p["topics"]), len(p["sources"])))


if __name__ == "__main__":
    main()
