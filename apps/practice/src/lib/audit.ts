export type Finding = { name: string; decision: string; state: "Held" | "Partial" | "Gap" };

export const findings: Finding[] = [
  { name: "Pace", decision: "Self-paced. No deadlines, no cohort calendar.", state: "Held" },
  { name: "Assistant", decision: "Noah drafts, plans, remembers, and keeps goals on this device. Assistant turns try the frontier model first. Noah does not send mail, spend money, browse after the turn, or connect to Meta’s apps.", state: "Partial" },
  { name: "Open weight first", decision: "Ollama, then Hugging Face, then a frontier model only if those are unset.", state: "Partial" },
  { name: "Voice", decision: "The browser speaks. Frontier speech is the fallback, not the product.", state: "Partial" },
  { name: "Exceed Muse", decision: "The harness is inspectable and local. The avatar is not a filmed character, and an open 7B weight is not a larger model by default.", state: "Partial" },
  { name: "Own editor", decision: "SQL on one table, a Java shape check, an HTML preview. No JetBrains, Eclipse, VS Code, or JDK.", state: "Held" },
  { name: "Exams", decision: "Original practice only. Vendor items are not stored.", state: "Held" },
  { name: "Math", decision: "Eight adaptive items, then a band.", state: "Held" },
  { name: "School", decision: "Webucator and Per Scholas are the topic map. Manuals are MDN, Node, Postgres, Ansible.", state: "Held" },
  { name: "Works and academy", decision: "Engineering labs and the build, field, return. Both open shelves linked, not rehosted.", state: "Held" },
  { name: "Data", decision: "Analyst grain, chart, and model. Tableau and Power BI are catalogs. Superset, DuckDB, Vega-Lite, pandas, scikit-learn, dbt are the tools.", state: "Held" },
  { name: "Orchestration", decision: "Jev routes refuse, memory, goal, one SQL statement, teach, or assist. TypeSafe’s hosted Jev is not called. LangGraph stays unused.", state: "Held" },
  { name: "Public site", decision: "The Learning OS and this server share one map. /practice/ on the static host is the wing: placement and the bench. Noah’s frontier turn cannot run inside that static page.", state: "Partial" },
  { name: "Host", decision: "Tomorrow, at the machine. Windows stays the host. The secondary disk is not erased from here.", state: "Gap" },
];
