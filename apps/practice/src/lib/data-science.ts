export const dataSwaps = [
  { theirs: "Tableau Desktop and Tableau Cloud", ours: "Apache Superset, plus Vega-Lite for a chart you can read", href: "https://superset.apache.org/" },
  { theirs: "Tableau certification exams", ours: "Their catalog. The questions are not stored here", href: "https://www.tableau.com/learn/certification" },
  { theirs: "Power BI and PL-300", ours: "The same open chart. Microsoft’s exam stays on Learn", href: "https://learn.microsoft.com/credentials/certifications/data-analyst-associate/" },
  { theirs: "Excel as the analyst’s only grid", ours: "DuckDB, and the SQL bench already on this site", href: "https://duckdb.org/docs/" },
  { theirs: "A vendor notebook", ours: "Jupyter and pandas, or Polars when the frame is large", href: "https://pandas.pydata.org/docs/" },
  { theirs: "A hosted AutoML console", ours: "scikit-learn’s user guide, and a hold-out you do not tune on", href: "https://scikit-learn.org/stable/user_guide.html" },
  { theirs: "Looker or a semantic-layer product", ours: "dbt for the transform, documented by dbt", href: "https://docs.getdbt.com/" },
  { theirs: "CompTIA Data+", ours: "Their outline. Practice is the grain, the chart, and the bench", href: "https://www.comptia.org/certifications/data" },
];

export const dataModules = [
  {
    name: "Grain",
    units: ["Say what one row is before you aggregate it.", "A chart of the wrong grain is a lie with a legend."],
    check: {
      q: "The grain of a row is",
      choices: ["what one row represents", "the color of the bar", "the certification level", "the tool vendor"],
      why: "Aggregation without a grain invents a number.",
    },
  },
  {
    name: "Chart",
    units: ["Compare rates with a bar, not a pie of identifiers.", "The open mark is Vega-Lite or Superset. Tableau is the catalog, not the file format we ship."],
    check: {
      q: "A pie chart of row ids fails because",
      choices: ["the ids are not the measure", "pies are open source", "Tableau forbids bars", "SQL cannot count"],
      why: "The measure is rate or errors. The id is a name.",
    },
  },
  {
    name: "Model",
    units: ["A feature that includes the future is leakage.", "The hold-out is touched once."],
    check: {
      q: "Leakage is",
      choices: ["a feature that contains the answer", "a missing license", "a slow chart", "a failed certificate"],
      why: "The model looks perfect and does not generalize.",
    },
  },
];
