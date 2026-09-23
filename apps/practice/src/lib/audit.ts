export type Finding = { name: string; decision: string; state: "Held" | "Partial" | "Gap" };

export const findings: Finding[] = [
  { name: "Pace", decision: "Self-paced. No deadlines, no cohort calendar.", state: "Held" },
  { name: "Tutor name", decision: "Noah, in the Dee, Hypatia, Agrippa, or Lovelace office. Not Meta Muse.", state: "Held" },
  { name: "Open weight first", decision: "Ollama, then Hugging Face, then a frontier model only if those are unset.", state: "Partial" },
  { name: "Voice", decision: "The browser speaks. Frontier speech is the fallback, not the product.", state: "Partial" },
  { name: "Exceed Muse", decision: "The harness is inspectable and local. The avatar is not a filmed character, and an open 7B weight is not a larger model by default.", state: "Partial" },
  { name: "Own editor", decision: "SQL on one table, a Java shape check, an HTML preview. No JetBrains, Eclipse, VS Code, or JDK.", state: "Held" },
  { name: "Exams", decision: "Original practice only. Vendor items are not stored.", state: "Held" },
  { name: "Math", decision: "Eight adaptive items, then a band.", state: "Held" },
  { name: "School", decision: "Webucator and Per Scholas are the topic map. Manuals are MDN, Node, Postgres, Ansible.", state: "Held" },
  { name: "Works and academy", decision: "Engineering labs and the build, field, return. Both open shelves linked, not rehosted.", state: "Held" },
  { name: "Data", decision: "Analyst grain, chart, and model. Tableau and Power BI are catalogs. Superset, DuckDB, Vega-Lite, pandas, scikit-learn, dbt are the tools.", state: "Held" },
  { name: "Orchestration", decision: "Jev here is a local scorer: refuse, one SQL statement, or teach. TypeSafe’s hosted Jev is closed, so it is not called. LangGraph stays unused.", state: "Held" },
  { name: "Public site", decision: "This practice is the source tree. The static public site is not this server, so the tutor is not folded into those pages.", state: "Gap" },
  { name: "Host", decision: "The ThinkStation walkthrough was deferred.", state: "Gap" },
];
