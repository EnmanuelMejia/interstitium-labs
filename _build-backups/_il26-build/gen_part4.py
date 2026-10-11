# Part 4: IL26-M48 data contracts, IL26-M49 semantic layers, IL26-M50 XML/XPath/XSLT, IL26-M51 PowerPoint storytelling
import json

M48 = {
  "id": "IL26-M48",
  "code": "IL-26",
  "title": "Data Contracts",
  "summary": "A data contract is an explicit agreement between data producers and consumers: schema, semantics, freshness, and ownership — written down and enforced. This module teaches contracts as the analyst's defense against silent upstream breakage: how to read them, what to demand in them, and how they connect to dbt tests and SLAs.",
  "objectives": [
    "Define a data contract and its core elements: schema, semantics, freshness/SLA, ownership, change policy",
    "Distinguish schema contracts from semantic contracts and explain why both matter",
    "Read a contract and translate it into concrete dbt tests and monitoring checks",
    "Negotiate contract terms with a producer team: what to ask for and what to concede",
    "Describe how contracts prevent the 'silent breakage' class of pipeline failures"
  ],
  "notes": [
    {
      "title": "What a data contract is (and isn't)",
      "body": "- A data contract is a documented, versioned agreement: 'the orders feed will contain these columns with these types and meanings, refreshed by 6 AM daily, owned by the checkout team, with 7 days notice before breaking changes.'\n- It is NOT just a schema file. Schema says 'column amount is NUMERIC'; the contract adds semantics ('amount is in USD, refunds excluded'), freshness ('by 6 AM ET'), and ownership ('checkout-team@').\n- Without a contract, every upstream change is a surprise: a renamed column breaks your mart at 7 AM and you find out from the stakeholder, not the producer.\n- With a contract, breaking changes are announced, versioned, and migration-planned — the failure mode shifts from 'silent breakage' to 'scheduled migration'.\n\n```yaml\n# contract: orders feed v3 (example structure, adapt to your org's format)\ncontract: orders-feed\nversion: 3\nowner: checkout-team@\nschema:\n  - {name: order_id, type: string, required: true}\n  - {name: amount, type: numeric, required: true,\n     semantics: 'USD, refunds excluded; see refunds table'}\n  - {name: order_date, type: date, required: true}\nfreshness: {sla: '06:00 ET daily', late_policy: 'page owner after 30 min'}\nchange_policy: {breaking_notice_days: 7, channel: '#data-contracts'}\n```"
    },
    {
      "title": "Schema vs semantics: the two halves",
      "body": "- Schema contract: names, types, nullability, allowed values. Machine-checkable — this is what becomes dbt tests and pipeline assertions.\n- Semantic contract: what the fields MEAN. 'amount' excluding refunds vs including them is a semantic difference no type checker catches — and it's the difference between a right and wrong revenue number.\n- The analyst's job: when a number looks off, check semantics first ('did the definition of active_user change?'), schema second.\n- Document semantics where the data is consumed (dbt column descriptions, semantic layer definitions) — a contract nobody can find is decoration.\n\n```yaml\n# The same schema, two different semantics -> two different revenues\ncolumns:\n  - name: amount\n    tests: [not_null]\n    description: >-\n      SEMANTICS (contract v3): USD gross merchandise value at order time,\n      refunds EXCLUDED (see refunds table), tax included. Changed 2026-09-01:\n      previously included refunds. Historical comparison must note the break.\n```\n\n```sql\n-- A semantic change the schema can't catch: definition of 'active'\n-- Contract v2: active = logged in within 30d. Contract v3: within 7d.\n-- Your dashboard drops 40% overnight with zero schema change.\n-- Fix: version the metric definition, annotate the break, never silently splice.\n```"
    },
    {
      "title": "From contract to enforcement: tests and monitors",
      "body": "- Every contract clause becomes something executable: schema -> dbt generic tests (unique, not_null, accepted_values); freshness SLA -> a recency monitor ('max(order_date) older than 26h -> alert'); change policy -> CI check that diffs the contract file.\n- Consumer-side: your staging models assert the contract on ingest — fail fast at the boundary instead of propagating bad data into marts.\n- Versioning: contracts are versioned (v3), and consumers pin to a version. The producer supports v2 and v3 during the migration window, then retires v2 per the notice policy.\n- Escalation path in the contract: who gets paged, in what channel, with what severity — agreed BEFORE the 6 AM failure, not during it.\n\n```sql\n-- tests/freshness_orders.sql: contract SLA as a singular test (0 rows = fresh)\nSELECT MAX(order_date) AS latest\nFROM {{ source('raw', 'orders') }}\nHAVING MAX(order_date) < CURRENT_DATE - INTERVAL '1 day'\n-- Violation rows -> the 06:00 ET SLA from the contract is breached.\n```"
    },
    {
      "title": "Negotiating a contract: what analysts should demand",
      "body": "- Ask for: explicit nullability per column, allowed-value sets for codes/statuses, the freshness SLA in writing, a named owner (team + channel), and the breaking-change notice period.\n- Concede gracefully: you can't demand real-time from a batch source; negotiate the SLA you actually need ('6 AM is fine; what I need is the page when it's late').\n- Bring evidence: 'last quarter, three silent schema changes cost us two dashboard incidents' beats 'contracts are best practice'.\n- Review cadence: contracts rot. Reconfirm semantics quarterly for your top-5 critical feeds — definitions drift even when schemas don't.\n\n```text\nAnalyst's contract request (template):\n1. Schema: column names/types/nullability + allowed values for codes.\n2. Semantics: one-line definition per business-critical field.\n3. Freshness: SLA timestamp + late-notification channel.\n4. Ownership: team + on-call channel.\n5. Change policy: notice period for breaking vs additive changes.\n6. Versioning: contract version pinned by consumers; migration window.\nSend this to the producer team; track the response like any dependency.\n```"
    }
  ],
  "cards": [
    {"front": "Data contract in one sentence", "back": "A documented, versioned agreement on schema, semantics, freshness, ownership, and change policy between data producers and consumers."},
    {"front": "Schema vs semantic contract", "back": "Schema: names/types/nullability (machine-checkable). Semantics: what fields MEAN (refunds excluded? active = 7d or 30d?) — no type checker catches this."},
    {"front": "Silent breakage", "back": "Upstream changes with no notice that break downstream silently — the failure class contracts convert into scheduled migrations."},
    {"front": "Contract clause -> enforcement mapping", "back": "Schema -> dbt tests; freshness SLA -> recency monitor; change policy -> CI diff on the contract file."},
    {"front": "Fail fast at the boundary", "back": "Assert the contract in staging models on ingest — bad data fails there, never propagates into marts."},
    {"front": "Contract versioning", "back": "Contracts are versioned; consumers pin a version; producers support old+new during the migration window, then retire per notice policy."},
    {"front": "What to demand in negotiation", "back": "Nullability, allowed values, freshness SLA in writing, named owner + channel, breaking-change notice period."},
    {"front": "Why contracts rot", "back": "Definitions drift even when schemas don't — reconfirm semantics quarterly for top critical feeds."}
  ],
  "quiz": [
    {"q": "Your revenue dashboard breaks at 7 AM after the checkout team renames amount to total_amount with no notice. The contract concept that prevents recurrence:", "choices": ["A data contract with schema + 7-day breaking-change notice + named owner, so renames are announced and migration-planned", "A bigger dashboard", "Checking the dashboard more often", "Blaming the checkout team"], "answer": 0, "explain": "Contracts convert silent breakage into scheduled, announced migrations. (Module 48)"},
    {"q": "amount is NUMERIC and not null, but revenue is wrong because refunds are now included. Which contract half failed?", "choices": ["The semantic contract — the MEANING of amount changed with no schema change", "The schema contract", "The freshness SLA", "The change policy"], "answer": 0, "explain": "Semantics (what fields mean) is invisible to type checks — the classic silent break. (Module 48)"},
    {"q": "The contract promises freshness by 06:00 ET daily. How do you enforce it?", "choices": ["A recency check (e.g. singular test: max(order_date) older than 1 day -> violation rows -> alert)", "Hope", "Refresh the dashboard manually at 6", "Email the owner daily asking if it's fresh"], "answer": 0, "explain": "SLA clauses become executable monitors; violations become alerts. (Module 48)"},
    {"q": "Producer announces contract v4 with a renamed column, supporting v3 for 30 days. You should:", "choices": ["Pin v3, plan the migration to v4 inside the window, test, then cut over — per the change policy", "Ignore it until v3 breaks", "Migrate overnight with no testing", "Fork the feed yourself"], "answer": 0, "explain": "Versioned contracts + migration windows are the designed path — use them. (Module 48)"},
    {"q": "Where should field semantics ('amount excludes refunds') be documented so analysts actually find it?", "choices": ["Where data is consumed: dbt column descriptions / semantic layer definitions — a contract nobody can find is decoration", "In someone's head", "In a chat thread from March", "Nowhere — it's obvious"], "answer": 0, "explain": "Semantics must live at the point of consumption, not in an unread wiki. (Module 48)"},
    {"q": "Your 'active users' metric drops 40% overnight with zero schema change. First hypothesis:", "choices": ["A semantic change upstream (e.g. active redefined from 30d to 7d) — check semantics before schema", "The database is down", "Users actually left", "The dashboard is broken"], "answer": 0, "explain": "Definition drift with stable schema is the signature of a semantic break. (Module 48)"},
    {"q": "In negotiation, the producer says real-time is impossible; the feed is batch. Your move:", "choices": ["Concede real-time; negotiate what you actually need: a written 6 AM SLA plus a page when it's late", "Demand real-time anyway", "Walk away from the data", "Build your own pipeline secretly"], "answer": 0, "explain": "Negotiate the SLA you need and the escalation path — not an impossible architecture. (Module 48)"},
    {"q": "Why do staging models assert the contract on ingest instead of checking in marts?", "choices": ["Fail fast at the boundary: bad data stops at staging instead of propagating into every downstream mart", "Staging is faster", "Marts don't support tests", "It's traditional"], "answer": 0, "explain": "Boundary assertions contain the blast radius to one layer. (Module 48)"}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL26-M49", "IL26-M44", "IL26-TL-03"]
}

M49 = {
  "id": "IL26-M49",
  "code": "IL-26",
  "title": "Semantic Layers",
  "summary": "A semantic layer defines business metrics once — 'revenue', 'active user', 'churn' — so every dashboard, notebook, and AI query computes them identically. This module teaches metric definition, dimensions vs measures, the single-source-of-truth payoff, and the governance discipline that keeps metric sprawl from returning.",
  "objectives": [
    "Define a semantic layer and explain the metric-sprawl problem it solves",
    "Distinguish dimensions, measures, and metric definitions with correct grain",
    "Write a metric definition (YAML-style) with aggregation, filters, and time grain",
    "Explain how a semantic layer serves BI tools, notebooks, and AI assistants consistently",
    "Apply governance: naming, ownership, certification, and deprecation of metrics"
  ],
  "notes": [
    {
      "title": "The metric-sprawl problem",
      "body": "- Without a semantic layer: Sales defines revenue as 'bookings including tax', Finance as 'recognized excluding refunds', and the exec dashboard shows a third number — three 'revenues', zero trust.\n- Root cause: metric logic lives inside individual dashboards and notebooks, copied and subtly mutated each time.\n- A semantic layer centralizes definitions: each metric is defined ONCE (name, logic, grain, owner) and every consumer — dashboard, notebook, AI assistant — queries the definition, not a copy.\n- The payoff is trust: 'revenue' means the same everywhere, and when the definition changes, it changes everywhere at once, with an owner and a changelog.\n\n```yaml\n# metrics/revenue.yml — defined once, consumed everywhere\nmetric: revenue\ndefinition:\n  measure: order_amount_sum        # SUM(amount) over the orders mart\n  filters: [amount >= 0]           # refunds excluded, per contract v3\n  time_grain: day\n  dimensions: [region, channel, product_category]\nowner: finance-analytics\ndescription: 'USD gross merchandise value, refunds excluded, tax included.'\nstatus: certified\n```"
    },
    {
      "title": "Dimensions, measures, metrics: the vocabulary",
      "body": "- Dimension: an attribute you slice by — region, channel, date. Answers 'by what?'.\n- Measure: an aggregation over a fact — SUM(amount), COUNT(orders). Answers 'how much?' — but a raw measure has no business rules yet.\n- Metric: a measure + business logic + governance — filters (exclude refunds), grain (daily), definition, owner, certification status. 'Revenue' is a metric; SUM(amount) is a measure.\n- Grain discipline: a metric must declare its grain ('one row per day per region'). Comparing a daily metric to a monthly one without alignment is the classic apples-to-oranges error.\n\n```yaml\n# measure vs metric: the business logic is what makes it a metric\nmeasures:\n  - name: order_amount_sum\n    agg: sum\n    expr: amount            # raw aggregation, no rules\n\nmetrics:\n  - name: revenue\n    measure: order_amount_sum\n    filters: [amount >= 0]  # the business rule lives HERE\n    # grain: day  (declared, so consumers can't mis-aggregate)\n```\n\n```sql\n-- What the layer compiles 'revenue by region, last 30d' into:\nSELECT region, DATE_TRUNC('day', order_date) AS day, SUM(amount) AS revenue\nFROM marts.orders\nWHERE amount >= 0 AND order_date >= CURRENT_DATE - INTERVAL '30 days'\nGROUP BY region, day\n```"
    },
    {
      "title": "One definition, many consumers",
      "body": "- The same metric definition serves: BI dashboards (the tool queries the layer, not raw tables), notebooks (analysts import certified metrics instead of rewriting logic), and AI assistants (the AI grounds 'revenue' in the defined metric instead of guessing SQL).\n- This is the AI-safety payoff from Module 47: an AI that answers 'what was revenue?' through the semantic layer can't invent its own definition — it inherits the certified one.\n- Consistency check: pick any metric, query it from two consumers, compare. Divergence means someone bypassed the layer — treat it as an incident, not a curiosity.\n- Migration path: don't boil the ocean. Start with your 5 most-disputed metrics, certify them, point the exec dashboard at the layer, expand.\n\n```python\n# notebook consumer: certified metric, not rewritten logic\nfrom semantic_layer import metrics\nrev = metrics.query('revenue',\n                    dimensions=['region'],\n                    date_range='last_30d')\n# rev is computed from the certified definition — identical to the dashboard's.\n```"
    },
    {
      "title": "Governance: certification, ownership, deprecation",
      "body": "- Every metric has an owner (team/person) and a status: draft, certified, deprecated. Only certified metrics appear in the exec layer.\n- Certification bar: definition reviewed, logic tested (dbt-style tests on the underlying model), semantics documented, stakeholder sign-off.\n- Deprecation, not deletion: when 'revenue_v1' is replaced, mark it deprecated with a pointer to v2 and a sunset date — dashboards migrate on a schedule, nothing vanishes overnight.\n- Naming discipline: one name, one meaning. 'Revenue' can't also mean 'net revenue' somewhere else — that's net_revenue, a different certified metric.\n\n```yaml\n# lifecycle in the metric registry\nmetric: revenue_v1\nstatus: deprecated\nreplaced_by: revenue_v2\nsunset_date: 2027-01-31\nmigration_note: 'v2 excludes tax per Finance sign-off 2026-11-15.'\n# dashboards on v1 get a migration ticket, not a surprise.\n```"
    }
  ],
  "cards": [
    {"front": "Semantic layer in one sentence", "back": "Business metrics defined once (name, logic, grain, owner) and consumed identically by every dashboard, notebook, and AI query."},
    {"front": "Metric sprawl", "back": "The same metric defined differently in each dashboard/notebook — three 'revenues', zero trust. The problem the layer solves."},
    {"front": "Dimension vs measure vs metric", "back": "Dimension: slice-by attribute. Measure: raw aggregation. Metric: measure + business rules + grain + owner + certification."},
    {"front": "Why grain must be declared", "back": "Comparing a daily metric to a monthly one without alignment is apples-to-oranges; declared grain prevents mis-aggregation."},
    {"front": "AI-safety payoff of a semantic layer", "back": "An AI answering through the layer inherits the certified metric definition instead of inventing its own SQL logic."},
    {"front": "Metric statuses (3)", "back": "draft, certified (exec-ready), deprecated (with replacement pointer + sunset date)."},
    {"front": "Certification bar", "back": "Definition reviewed, logic tested, semantics documented, stakeholder sign-off — only certified metrics reach executives."},
    {"front": "Deprecation rule", "back": "Deprecate with pointer + sunset date and migration tickets — never silently delete a metric dashboards use."}
  ],
  "quiz": [
    {"q": "Three dashboards show three different 'revenue' numbers. The semantic-layer fix is:", "choices": ["Define revenue once (logic, grain, owner, certified) and point all consumers at the definition", "Pick the biggest number", "Average the three", "Delete two dashboards"], "answer": 0, "explain": "Single definition, many consumers — the sprawl cure. (Module 49)"},
    {"q": "Which is a METRIC rather than a mere measure?", "choices": ["SUM(amount) with the business rule 'refunds excluded', daily grain, owner, and certified status", "SUM(amount)", "COUNT(*)", "A column named amount"], "answer": 0, "explain": "Business rules + grain + governance turn a measure into a metric. (Module 49)"},
    {"q": "An AI assistant answers 'revenue last quarter' using the semantic layer. The safety benefit:", "choices": ["It inherits the certified definition instead of generating its own possibly-wrong SQL", "It's faster", "It uses more tokens", "It doesn't need data"], "answer": 0, "explain": "Grounding AI in certified definitions prevents invented metric logic. (Module 49)"},
    {"q": "'Revenue' is used for both gross and net figures in different reports. Governance fix:", "choices": ["One name, one meaning: keep revenue for the certified gross definition; create net_revenue as a separate certified metric", "Let context decide", "Rename both randomly", "It's fine"], "answer": 0, "explain": "Naming discipline: distinct meanings get distinct certified names. (Module 49)"},
    {"q": "Finance changes the revenue definition (now excludes tax). Rollout discipline:", "choices": ["Version it (revenue_v2), certify, deprecate v1 with sunset date + migration tickets — never silent replacement", "Overwrite the definition in place", "Tell no one", "Change it back next week"], "answer": 0, "explain": "Definition changes are versioned migrations, not silent edits. (Module 49)"},
    {"q": "A notebook computes revenue with hand-written SQL that differs from the dashboard. You should:", "choices": ["Treat the bypass as an incident: point the notebook at the certified metric and reconcile the difference", "Ignore it", "Change the dashboard to match the notebook", "Delete the notebook"], "answer": 0, "explain": "Divergence from the layer means someone bypassed it — investigate, don't normalize. (Module 49)"},
    {"q": "Starting a semantic layer from zero, the pragmatic first step is:", "choices": ["Certify the 5 most-disputed metrics, point the exec dashboard at them, then expand", "Define all 500 metrics at once", "Buy software first", "Write a 100-page spec"], "answer": 0, "explain": "Start where the pain is: disputed metrics, visible win, then expand. (Module 49)"},
    {"q": "A metric's grain is declared as 'day'. An analyst sums its daily values into a monthly total. This is:", "choices": ["Valid only if the metric is additive at that grain — non-additive metrics (ratios, distinct counts) need re-aggregation from base facts", "Always valid", "Always invalid", "Valid on weekends"], "answer": 0, "explain": "Grain discipline: additive measures sum safely; ratios and distinct counts don't. (Module 49)"}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL26-M48", "IL26-M15", "IL26-TL-04", "IL26-TL-05"]
}

M50 = {
  "id": "IL26-M50",
  "code": "IL-26",
  "title": "XML, XPath, and XSLT for Data Analysts",
  "summary": "XML still runs banking feeds, government filings, healthcare HL7, and legacy enterprise integrations — analysts who can't parse it are locked out. This module teaches XML structure, XPath navigation, XSLT transformation, and the Python workflow that turns XML payloads into tidy tables.",
  "objectives": [
    "Read XML documents: elements, attributes, namespaces, and well-formedness rules",
    "Write XPath expressions to select nodes, filter by predicates, and extract values",
    "Apply XSLT to transform XML into another XML shape or flat text/CSV",
    "Parse XML in Python (ElementTree/lxml) into pandas-ready records",
    "Handle namespaces and malformed XML without silent data loss"
  ],
  "notes": [
    {
      "title": "XML anatomy: elements, attributes, namespaces",
      "body": "- XML is a tree: elements nest (`<order><id>1</id></order>`), attributes annotate (`<order priority=\"high\">`), one root element per document.\n- Well-formed (syntax: tags closed, nested properly) vs valid (conforms to a schema like XSD) — a file can be well-formed but invalid; parsing needs the first, contracts need the second.\n- Namespaces (`xmlns:inv=\"...\"`) prevent tag collisions when documents mix vocabularies — `<inv:total>` vs `<tax:total>`. They are the #1 reason XPath queries 'return nothing'.\n- Analyst rule: always inspect the raw XML (first 50 lines) before writing any extraction — structure surprises (nested vs flat, attributes vs elements) are the norm.\n\n```xml\n<!-- orders.xml: elements carry data, attributes annotate -->\n<orders xmlns=\"urn:il26:orders\">\n  <order id=\"1001\" priority=\"high\">\n    <customer>Acme Corp</customer>\n    <total currency=\"USD\">250.00</total>\n  </order>\n  <order id=\"1002\" priority=\"normal\">\n    <customer>Globex</customer>\n    <total currency=\"USD\">89.50</total>\n  </order>\n</orders>\n```"
    },
    {
      "title": "XPath: SQL for trees",
      "body": "- XPath selects nodes: `//order` (all order elements anywhere), `/orders/order[1]` (first child), `//order[@priority='high']` (predicate filter), `//total/text()` (the text content).\n- Axes you'll actually use: child (default), attribute (`@id`), descendant (`//`), parent (`..`).\n- Predicates do the WHERE work: `//order[total > 100]`, `//order[position() <= 10]`, `//customer[contains(., 'Acme')]`.\n- Namespace trap: with a default xmlns, `//order` matches NOTHING — you must bind a prefix (`//o:order`) even though the source uses no prefix. This burns everyone once.\n\n```text\nSample XPaths against orders.xml (with prefix o bound to the namespace):\n  //o:order                     -> both order elements\n  //o:order[@priority='high']   -> order 1001 only\n  //o:order[o:total > 100]/o:customer/text()  -> 'Acme Corp'\n  count(//o:order)               -> 2\n  //o:total/@currency            -> 'USD', 'USD' (attribute axis)\nThink: // is SELECT, [@x='y'] is WHERE, /text() is the column.\n```"
    },
    {
      "title": "XSLT: transform XML into something usable",
      "body": "- XSLT is a template language that transforms XML -> XML, HTML, or plain text (including CSV). Legacy pipelines use it to reshape feeds before analysts ever see them.\n- You won't write stylesheets daily, but you must READ them: when a feed arrives 'wrong', the XSLT in the middle is often the culprit.\n- Core: `<xsl:template match=\"...\">` (which nodes), `<xsl:for-each>` (loop), `<xsl:value-of select=\"...\"/>` (extract).\n- Modern analyst move: skip XSLT when you can — parse the XML directly in Python (next note). Reach for XSLT when the transform must live in the pipeline, not your script.\n\n```xml\n<!-- orders-to-csv.xsl: flatten orders to CSV lines -->\n<xsl:stylesheet version=\"1.0\"\n  xmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\"\n  xmlns:o=\"urn:il26:orders\">\n  <xsl:output method=\"text\"/>\n  <xsl:template match=\"/\">\n    <xsl:text>order_id,customer,total&#10;</xsl:text>\n    <xsl:for-each select=\"//o:order\">\n      <xsl:value-of select=\"@id\"/><xsl:text>,</xsl:text>\n      <xsl:value-of select=\"o:customer\"/><xsl:text>,</xsl:text>\n      <xsl:value-of select=\"o:total\"/><xsl:text>&#10;</xsl:text>\n    </xsl:for-each>\n  </xsl:template>\n</xsl:stylesheet>\n<!-- output: order_id,customer,total / 1001,Acme Corp,250.00 / ... -->\n```"
    },
    {
      "title": "Python: XML to dataframe without silent loss",
      "body": "- ElementTree (stdlib) handles most feeds; lxml when you need full XPath or broken-HTML tolerance.\n- Pattern: iterate record elements, extract fields with namespace-aware finds, build a list of dicts, DataFrame it.\n- Namespace handling in ElementTree: use the Clark notation `{urn:il26:orders}order` or register a prefix map — pick one and be consistent.\n- Malformed XML: parse defensively — catch ParseError, log the offending file, quarantine it. A parser that silently skips records is worse than one that loudly fails.\n\n```python\nimport xml.etree.ElementTree as ET\nimport pandas as pd\n\nNS = {'o': 'urn:il26:orders'}\nrecords = []\ntry:\n    root = ET.parse('orders.xml').getroot()\n    for o in root.findall('o:order', NS):\n        records.append({\n            'order_id': o.get('id'),                       # attribute\n            'priority': o.get('priority', 'normal'),       # default if missing\n            'customer': o.findtext('o:customer', '', NS),   # element text\n            'total': float(o.findtext('o:total', '0', NS)),\n            'currency': o.find('o:total', NS).get('currency'),\n        })\nexcept ET.ParseError as e:\n    raise SystemExit(f'QUARANTINE orders.xml: malformed ({e}) — fix source, do not silently skip')\n\ndf = pd.DataFrame(records)\nprint(df, df['total'].sum())\n```"
    }
  ],
  "cards": [
    {"front": "Well-formed vs valid XML", "back": "Well-formed: syntax correct (tags closed/nested). Valid: conforms to a schema (XSD). Parsing needs well-formed; contracts need valid."},
    {"front": "XPath //o:order[@priority='high']", "back": "All order elements anywhere in the doc with priority attribute = 'high'. // is descendant, [@..] is the predicate filter."},
    {"front": "The namespace trap", "back": "With a default xmlns, //order matches NOTHING — bind a prefix (//o:order) even though the source uses no prefix."},
    {"front": "XPath mental model", "back": "// is SELECT (find nodes), [@x='y'] is WHERE (predicates), /text() is the column (extract content)."},
    {"front": "XSLT in one sentence", "back": "A template language transforming XML into other XML, HTML, or text/CSV — read it to debug legacy feed pipelines."},
    {"front": "xsl:value-of vs xsl:for-each", "back": "value-of extracts a value (select=...); for-each loops over a node set. template match=... picks which nodes."},
    {"front": "ElementTree namespace handling", "back": "Use a prefix map (findall('o:order', NS)) or Clark notation {uri}tag — be consistent, or finds return nothing."},
    {"front": "Malformed XML rule", "back": "Catch ParseError, log + quarantine the file. Loud failure beats silent record-skipping."}
  ],
  "quiz": [
    {"q": "Your XPath //order returns nothing against a document with a default xmlns. The cause and fix:", "choices": ["The namespace trap: bind a prefix to the namespace URI and query //o:order", "The file is empty", "XPath is case-sensitive about 'order' vs 'Order' only", "Use single slashes"], "answer": 0, "explain": "Default namespaces require a bound prefix in XPath — the classic gotcha. (Module 50)"},
    {"q": "Select the customer names of high-priority orders with totals over 100. Best XPath:", "choices": ["//o:order[@priority='high'][o:total > 100]/o:customer/text()", "//customer", "//o:order/text()", "/orders"], "answer": 0, "explain": "Predicates filter (@attr and child element comparisons), then navigate to the text. (Module 50)"},
    {"q": "A legacy pipeline delivers a feed in the wrong shape and the XSLT in the middle is suspect. Your first move:", "choices": ["Read the stylesheet: check template match patterns and value-of selects against the actual XML", "Rewrite the pipeline", "Blame the vendor", "Parse it harder"], "answer": 0, "explain": "XSLT literacy means reading transforms to find the reshape bug. (Module 50)"},
    {"q": "ElementTree findall('order') returns [] but the file clearly has orders. Likely cause:", "choices": ["Undeclared namespace: use findall('o:order', NS) with the namespace map", "The file is JSON", "Python is broken", "Orders are invisible"], "answer": 0, "explain": "Same namespace trap in Python: unprefixed finds miss namespaced elements. (Module 50)"},
    {"q": "o.get('priority', 'normal') in the parsing code is an example of:", "choices": ["Defensive extraction: defaulting a missing attribute instead of crashing or inserting None silently", "A bug", "Namespace handling", "Type coercion"], "answer": 0, "explain": "Explicit defaults document assumptions; silent Nones corrupt downstream logic. (Module 50)"},
    {"q": "The XML file fails to parse halfway through a 10,000-record feed. Correct handling:", "choices": ["Quarantine the file, log the error, fix the source — never silently process the 5,000 that parsed", "Process the 5,000 and hope", "Delete the file", "Manually edit the XML"], "answer": 0, "explain": "Partial silent processing is the worst outcome; loud quarantine preserves integrity. (Module 50)"},
    {"q": "When should you reach for XSLT instead of Python parsing?", "choices": ["When the transform must live in the pipeline (reusable, language-neutral) rather than in your one-off script", "Always — XSLT is faster", "Never", "When you feel like it"], "answer": 0, "explain": "XSLT's value is pipeline-resident, reusable transforms; Python wins for analysis-time parsing. (Module 50)"},
    {"q": "Well-formed but invalid XML means:", "choices": ["Syntax is fine but it violates the agreed schema (XSD) — parsing works, contract validation fails", "It cannot be parsed", "It is JSON", "It is perfect"], "answer": 0, "explain": "Well-formed = parseable; valid = schema-conformant. Both matter, differently. (Module 50)"}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL26-M09", "IL26-TL-01"]
}

M51 = {
  "id": "IL26-M51",
  "code": "IL-26",
  "title": "PowerPoint Data Storytelling",
  "summary": "Analysis that can't be presented doesn't ship. This module teaches the analyst's presentation craft: narrative structure (situation-complication-resolution), one-message-per-slide, honest chart design, and the delivery habits that turn a findings deck into decisions.",
  "objectives": [
    "Structure a findings deck with a narrative arc: situation, complication, resolution, recommendation",
    "Apply one-message-per-slide: headline as the takeaway, visual as the evidence",
    "Design honest charts: proper baselines, labeled axes, no truncated or dual-axis deception",
    "Tailor the deck to the audience: executive summary up front, appendix for the deep dive",
    "Deliver with the decision in mind: recommendation, tradeoffs, ask, and next steps on the final slides"
  ],
  "notes": [
    {
      "title": "Narrative arc: SCR (Situation-Complication-Resolution)",
      "body": "- Situation: shared context everyone agrees on ('Q3 revenue was $4.2M, up 8%').\n- Complication: the tension that demands a decision ('...but churn in the West region doubled, erasing the gain').\n- Resolution: your recommendation ('Reallocate $200K of acquisition spend to West retention; projected +$600K net').\n- The arc turns a data dump into a story with stakes. Executives decide; they don't explore — your deck must arrive at the decision, not invite wandering.\n- Test: cover the slide headlines only — they should read as a coherent paragraph. If they don't, the story is broken.\n\n```text\nHeadline-only test (the deck's story in 5 lines):\n1. Q3 revenue grew 8% to $4.2M           (situation)\n2. But West-region churn doubled, erasing the gain  (complication)\n3. Churn concentrates in customers acquired via discount codes (insight)\n4. We recommend shifting $200K to West retention   (resolution)\n5. Projected net: +$600K; decision needed by Friday (ask)\n```"
    },
    {
      "title": "One message per slide: headline = takeaway",
      "body": "- Rule: the slide title states the CONCLUSION ('West churn doubled in Q3'), not the topic ('Churn analysis'). The visual below is the evidence.\n- One chart per slide, one takeaway per chart. Two messages = two slides.\n- Annotate the chart: circle the spike, label the key value, add the 'so what' in a caption. Never make the audience hunt for the point.\n- Data-ink discipline: remove gridlines, 3D effects, and decoration that doesn't encode information. If removing an element changes nothing, remove it.\n\n```text\nBEFORE (topic title):  \"Churn by region\"  + busy 3D bar chart\nAFTER (takeaway title): \"West churn doubled in Q3, erasing the revenue gain\"\n                        + flat bars, West bar highlighted, annotation:\n                          \"2.1% -> 4.3% (n=1,204)\"\nThe audience gets the message in 3 seconds, with or without you talking.\n```"
    },
    {
      "title": "Honest charts: the integrity checklist",
      "body": "- Baselines: bar charts start at zero — truncated bars exaggerate differences. (Line charts may zoom, but say so.)\n- No dual axes with different scales unless you label both loudly — they manufacture correlations.\n- Label directly: put values on the bars/points, not just on an axis the audience must interpolate.\n- Show uncertainty: error bars or 'n=' counts where the data is thin. A 50% lift on n=12 is noise wearing a costume.\n- Sourcing: every chart gets a source + date footnote ('orders mart, 2026-10-06'). Unsourced charts are rumors.\n- The Module 47 rule applies: every number traces to a validated query.\n\n```text\nChart integrity checklist (run per visual):\n[ ] Bars start at zero (or zoom is disclosed)\n[ ] No sneaky dual axes\n[ ] Values labeled directly on the visual\n[ ] n= shown; uncertainty visible where thin\n[ ] Source + as-of date in the footnote\n[ ] Number traces to a validated query (Module 47 ladder)\n```"
    },
    {
      "title": "Audience tailoring and the close",
      "body": "- Executives: BLUF — Bottom Line Up Front. Recommendation on slide 2, supporting evidence after, deep dive in the appendix. Never make them wait 20 slides for the point.\n- Peers/technical: methodology earns slides — assumptions, grain, validation. They'll challenge the logic; arm them.\n- The close: recommendation (one sentence), tradeoffs (what we give up), the ask (decision/resource/date), next steps with owners.\n- Leave-behind: the deck must stand alone — headlines carry the story, appendix holds the proof, notes hold the narration you gave live.\n\n```text\nClosing slide template:\n  RECOMMENDATION: Shift $200K acquisition -> West retention (Q4).\n  TRADEOFF:      East acquisition growth slows ~3%.\n  ASK:           Approve by Friday to hit the Q4 window.\n  NEXT STEPS:    Ana: retention offer design (10/14) | Ben: spend reallocation (10/15)\n  APPENDIX:      methodology, query logic, sensitivity analysis\n```"
    }
  ],
  "cards": [
    {"front": "SCR narrative arc", "back": "Situation (shared context) -> Complication (tension demanding a decision) -> Resolution (recommendation). Turns data dumps into decisions."},
    {"front": "The headline-only test", "back": "Read just the slide headlines: they must form a coherent paragraph. If not, the story is broken."},
    {"front": "One message per slide", "back": "Title states the CONCLUSION ('West churn doubled'), not the topic ('Churn analysis'); one chart, one takeaway; annotate the point."},
    {"front": "BLUF", "back": "Bottom Line Up Front: recommendation on slide 2 for executives; evidence after; deep dive in the appendix."},
    {"front": "Bar chart baseline rule", "back": "Bars start at zero — truncated bars exaggerate. Line charts may zoom but must disclose it."},
    {"front": "Dual-axis rule", "back": "Avoid dual axes with different scales — they manufacture correlations. If used, label both scales loudly."},
    {"front": "Chart footnote requirement", "back": "Every chart: source + as-of date. Unsourced charts are rumors."},
    {"front": "Closing slide contents", "back": "Recommendation (one sentence), tradeoffs, the ask (decision/date), next steps with owners, appendix pointer."}
  ],
  "quiz": [
    {"q": "Your deck has 20 slides of exploration and the recommendation appears on slide 19. The fix:", "choices": ["BLUF: recommendation on slide 2, evidence after, deep dive in appendix", "Add 10 more slides", "Make the recommendation smaller", "It's fine"], "answer": 0, "explain": "Executives decide; don't make them wait 20 slides for the point. (Module 51)"},
    {"q": "A bar chart shows 4.1% vs 4.3% as dramatically different bar heights. The integrity violation:", "choices": ["Truncated baseline exaggerating a tiny difference — bars must start at zero", "The colors are wrong", "Bars should be 3D", "Percentages shouldn't be charted"], "answer": 0, "explain": "Non-zero baselines manufacture drama; disclose any zoom. (Module 51)"},
    {"q": "Slide title reads 'Q3 numbers'. Better title:", "choices": ["'Q3 revenue grew 8%, but West churn erased the gain' — the takeaway, not the topic", "'Q3 numbers (final)'", "'Data'", "'Misc'"], "answer": 0, "explain": "Headline = conclusion; the visual is the evidence. (Module 51)"},
    {"q": "A chart shows a 50% lift with n=12 and no uncertainty shown. You should:", "choices": ["Show the n and uncertainty — thin data dressed as a finding is noise in a costume", "Celebrate the 50%", "Hide the n", "Remove the chart"], "answer": 0, "explain": "Integrity: thin data must show its thinness. (Module 51)"},
    {"q": "The headline-only test fails — headlines don't form a coherent story. This means:", "choices": ["The narrative arc is broken; restructure around Situation-Complication-Resolution", "The font is wrong", "Add transitions", "Nothing — headlines don't matter"], "answer": 0, "explain": "Headlines carry the story; incoherence there means incoherence everywhere. (Module 51)"},
    {"q": "Presenting to engineers who will challenge your methodology, you should:", "choices": ["Give methodology real slides: assumptions, grain, validation — arm them to challenge the logic", "Hide the methodology", "Same deck as for executives", "Skip Q&A"], "answer": 0, "explain": "Technical audiences need the logic trail; executives need BLUF. Tailor. (Module 51)"},
    {"q": "Every number in the deck must:", "choices": ["Trace to a validated query (Module 47 ladder) with source + as-of date footnoted", "Look plausible", "Come from the AI draft", "Be rounded nicely"], "answer": 0, "explain": "Traceability is the integrity backbone of the whole deck. (Module 51)"},
    {"q": "The deck must stand alone as a leave-behind. This requires:", "choices": ["Headlines carrying the story, appendix with proof, speaker notes with narration — readable without you", "More animations", "Your presence forever", "A verbal-only story"], "answer": 0, "explain": "Leave-behinds get forwarded; they must survive without the presenter. (Module 51)"}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL26-M18", "IL26-TL-08", "IL26-M21"]
}

with open('/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/part4_modules.json', 'w') as f:
    json.dump([M48, M49, M50, M51], f, indent=2)
print('part4 written')
