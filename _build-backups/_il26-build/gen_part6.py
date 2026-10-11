# Part 6: multicloudLabs (AWS/Azure/GCP) + installSteps
import json

MULTICLOUD_LABS = [
  {
    "id": "IL26-MC-AWS-01",
    "title": "AWS: S3 + Athena Query on the Sample Orders CSV",
    "cloud": "aws",
    "brief": "Run one real analytics workload on AWS's free tier: upload the fictional ecom_orders CSV to S3, query it with Athena's serverless SQL engine (pay-per-query, no servers), then tear everything down. You will touch a bucket, a table definition, and a query — and leave no billable residue.",
    "steps": [
      "Sign in to the AWS console and choose a region close to you (e.g. us-east-1); do ALL work in this one region so resources are easy to find at cleanup",
      "Create an S3 bucket with a globally unique name (e.g. il26-lab-<yourname>-<date>); keep Block Public Access ON and versioning OFF",
      "Upload data/raw/ecom_orders.csv to the bucket under s3://<bucket>/raw/ecom_orders.csv",
      "Open Athena, run the one-time setup: set the query-result location to s3://<bucket>/athena-results/ (Athena needs a place to write results)",
      "In the Athena query editor, create the table: CREATE EXTERNAL TABLE orders (order_id string, order_date string, customer_id string, region string, channel string, product_category string, amount double, discount_code string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION 's3://<bucket>/raw/' TBLPROPERTIES ('skip.header.line.count'='1')",
      "Run the workload query: SELECT region, COUNT(*) AS orders, ROUND(SUM(amount),2) AS revenue FROM orders GROUP BY region ORDER BY revenue DESC — confirm it matches your local DuckDB totals",
      "Check the Athena query history panel: note the 'Data scanned' amount for your queries (this is what Athena bills on — small CSV means fractions of a cent)"
    ],
    "workload": "Athena serverless SQL over the S3-hosted ecom_orders CSV: revenue and order counts by region, reconciled against the local DuckDB totals from TL-02. The workload demonstrates decoupled storage (S3) and serverless compute (Athena) — the core cloud analytics pattern.",
    "costGuardrails": [
      "Athena's free tier covers a small monthly query-data allowance; a 15-row CSV scans kilobytes — stay on tiny files and this lab costs essentially nothing",
      "S3 free tier covers a small amount of storage and requests monthly; one CSV plus query results is far below it — do not upload large datasets",
      "Keep everything in ONE region; cross-region data movement is where surprise charges come from",
      "Do not enable S3 versioning, replication, or intelligent-tiering on the lab bucket — all add cost for zero lab benefit",
      "Set a billing alert (e.g. $1) in the Billing console before starting — the habit matters more than the threshold"
    ],
    "cleanup": [
      "Athena: no persistent compute to delete (serverless), but note your query history for the report",
      "S3: delete s3://<bucket>/athena-results/ contents, then s3://<bucket>/raw/ecom_orders.csv, then delete the bucket itself",
      "Verify: S3 console shows zero buckets matching il26-lab-*; Billing dashboard shows no active resources",
      "Record the final 'Data scanned' totals and confirm the month-to-date bill is $0.00 before closing the lab"
    ],
    "checkpoint": "Athena query results match local DuckDB region totals exactly; lab bucket deleted; billing dashboard shows $0.00; 'Data scanned' recorded."
  },
  {
    "id": "IL26-MC-AZURE-01",
    "title": "Azure: Storage + Synapse Serverless SQL on the Sample Orders CSV",
    "cloud": "azure",
    "brief": "Run the same workload on Azure: land the fictional ecom_orders CSV in Azure Storage and query it with Synapse's serverless SQL pool (pay per terabyte scanned, no cluster to manage). Free-account framing throughout, full teardown at the end.",
    "steps": [
      "Sign in to the Azure portal; confirm you are on a free account/trial subscription and note its expiry date before creating anything",
      "Create a resource group named il26-lab-rg in a region near you — everything goes here so cleanup is one deletion",
      "Create a Storage account (standard performance, LRS redundancy — the cheapest options) inside il26-lab-rg",
      "In the storage account, create a container named raw and upload data/raw/ecom_orders.csv",
      "Open Synapse Studio, create a serverless SQL pool workspace (or use an existing one), and run: SELECT region, COUNT(*) AS orders, ROUND(SUM(CAST(amount AS FLOAT)),2) AS revenue FROM OPENROWSET(BULK 'https://<account>.blob.core.windows.net/raw/ecom_orders.csv', FORMAT='CSV', PARSER_VERSION='2.0', HEADER_ROW=TRUE) AS o GROUP BY region ORDER BY revenue DESC",
      "Reconcile the results against your local DuckDB totals — same numbers, different cloud",
      "Check the Synapse monitoring view: note the data processed by the query (this is the billing meter)"
    ],
    "workload": "Synapse serverless SQL over the Storage-hosted ecom_orders CSV via OPENROWSET: revenue and order counts by region, reconciled against local DuckDB totals. Demonstrates Azure's decoupled storage-plus-serverless-query pattern, the direct analog of the AWS lab.",
    "costGuardrails": [
      "Serverless SQL pools bill per terabyte of data processed; a 15-row CSV processes megabytes — keep files tiny and queries few",
      "Free accounts include limited monthly credits: this lab uses a negligible fraction, but never run ad-hoc exploratory queries against large files on a free account",
      "Use the cheapest storage options (standard, LRS) — premium tiers and geo-redundancy multiply cost for no lab benefit",
      "Do NOT provision a dedicated SQL pool or Spark pool — those bill per hour while running and are unnecessary for this workload",
      "Put everything in the single il26-lab-rg resource group so nothing billable hides outside it"
    ],
    "cleanup": [
      "Delete the entire resource group il26-lab-rg (this removes the storage account, container, and any Synapse artifacts in one action)",
      "Verify: portal search for il26-lab-rg returns nothing; storage accounts list shows no lab account",
      "Check Cost Management: confirm the subscription shows no ongoing charges from the lab resources",
      "Record the data-processed totals from Synapse monitoring for your lab report"
    ],
    "checkpoint": "Query results match local DuckDB totals; resource group il26-lab-rg deleted and verified gone; Cost Management shows no ongoing lab charges."
  },
  {
    "id": "IL26-MC-GCP-01",
    "title": "GCP: BigQuery Sandbox Query on the Sample Orders Dataset",
    "cloud": "gcp",
    "brief": "Run the workload on Google Cloud's BigQuery sandbox — which lets you query without even adding a billing account. Load the fictional ecom_orders CSV, run the regional revenue analysis, and clean up the dataset. The sandbox's limits ARE the guardrails here.",
    "steps": [
      "Sign in to the Google Cloud console and create/select a project named il26-lab; open BigQuery Studio",
      "Confirm you are in sandbox mode (no billing account attached — the console labels it); note the sandbox's table expiration behavior before loading data",
      "Create a dataset named lab_orders in a US region; upload data/raw/ecom_orders.csv as a table named orders (auto-detect schema, header row = 1)",
      "Run the workload query: SELECT region, COUNT(*) AS orders, ROUND(SUM(amount),2) AS revenue FROM `il26-lab.lab_orders.orders` GROUP BY region ORDER BY revenue DESC",
      "Reconcile against local DuckDB totals; then run one variant: monthly revenue trend with DATE_TRUNC(order_date, MONTH)",
      "Open the query job details: note bytes processed and slot time — this is what BigQuery meters"
    ],
    "workload": "BigQuery SQL over the uploaded ecom_orders table: regional revenue/orders plus a monthly trend, reconciled against local DuckDB totals. Demonstrates the warehouse-native pattern (data loaded INTO the engine) as contrast to the S3/Storage query-in-place pattern of the other two labs.",
    "costGuardrails": [
      "The BigQuery sandbox requires no billing account and grants a monthly free query allowance — but sandbox tables EXPIRE (default 60 days) and some features are restricted; know these limits before relying on sandbox data",
      "With billing enabled later, BigQuery's free tier covers a monthly query-data allowance — the 15-row table processes kilobytes; never point ad-hoc queries at multi-terabyte public datasets on a free tier without checking bytes-processed first",
      "Always check the query validator's 'bytes processed' estimate BEFORE running — it is displayed in the editor and is your pre-flight cost check",
      "Keep the lab to the two queries specified; exploratory querying against large tables is the classic free-tier-burn mistake"
    ],
    "cleanup": [
      "Delete the lab_orders dataset (deleting the dataset removes the orders table with it)",
      "Verify: BigQuery explorer shows no lab_orders dataset under il26-lab",
      "Optionally delete the il26-lab project itself for a fully clean slate",
      "Record bytes-processed totals from both query jobs for your lab report"
    ],
    "checkpoint": "Both queries' results match local DuckDB totals; lab_orders dataset deleted and verified gone; bytes-processed recorded for both jobs."
  }
]

INSTALL_STEPS = [
  {"id": "IL26-INST-01", "title": "Python analytics environment",
   "summary": "Python 3.11+, a virtualenv, and pip packages: pandas, duckdb, polars, pyarrow. The base for TL-01, TL-02, TL-08.",
   "commands": ["python3 --version  # need 3.11+", "python3 -m venv ~/venv/il26 && source ~/venv/il26/bin/activate", "pip install pandas duckdb polars pyarrow"]},
  {"id": "IL26-INST-02", "title": "dbt Core + DuckDB adapter",
   "summary": "dbt-core with dbt-duckdb and a profiles.yml pointing at the TL-02 analytics.duckdb. Needed for TL-03.",
   "commands": ["pip install dbt-core dbt-duckdb", "mkdir -p ~/.dbt  # profiles.yml with duckdb adapter, path to analytics.duckdb", "dbt --version"]},
  {"id": "IL26-INST-03", "title": "Tableau access",
   "summary": "Tableau Desktop (trial) or the free Tableau Public for TL-04. No CLI install; sign up and install the desktop app.",
   "commands": ["# Install Tableau Desktop trial or Tableau Public from the official Tableau site", "# Verify: open app, connect to a CSV"]},
  {"id": "IL26-INST-04", "title": "Power BI Desktop",
   "summary": "Power BI Desktop (Windows; free) for TL-05. Mac/Linux learners use a Windows VM or lab machine.",
   "commands": ["# Install Power BI Desktop from the official Microsoft site", "# Verify: Get Data -> CSV loads"]},
  {"id": "IL26-INST-05", "title": "Excel or Google Sheets",
   "summary": "Any modern Excel or a Google account with Sheets for TL-06. No install beyond what you have.",
   "commands": ["# Verify: open a CSV, build a pivot table"]},
  {"id": "IL26-INST-06", "title": "Streamlit and Marimo",
   "summary": "pip packages streamlit and marimo for TL-07 (Module 45). Install into the IL26 venv.",
   "commands": ["source ~/venv/il26/bin/activate", "pip install streamlit marimo", "streamlit --version && marimo --version"]},
  {"id": "IL26-INST-07", "title": "AWS account + CLI (free tier)",
   "summary": "AWS account with a $1 billing alert set; AWS CLI configured. Needed for the AWS multicloud lab.",
   "commands": ["aws --version", "aws sts get-caller-identity  # verify credentials", "# Console: Billing -> create $1 billing alert BEFORE any lab"]},
  {"id": "IL26-INST-08", "title": "Azure account (free)",
   "summary": "Azure free account; note the trial expiry date. Needed for the Azure multicloud lab.",
   "commands": ["# Portal: portal.azure.com -> verify subscription is the free/trial one", "# Note the expiry date somewhere visible"]},
  {"id": "IL26-INST-09", "title": "GCP account (BigQuery sandbox)",
   "summary": "Google Cloud account; BigQuery sandbox needs no billing account. Needed for the GCP multicloud lab.",
   "commands": ["# Console: console.cloud.google.com -> create project il26-lab", "# BigQuery Studio: confirm sandbox mode (no billing attached)"]}
]

with open('/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/part6_cloud.json', 'w') as f:
    json.dump({'multicloudLabs': MULTICLOUD_LABS, 'installSteps': INSTALL_STEPS}, f, indent=2)
print('part6 written:', len(MULTICLOUD_LABS), 'cloud labs,', len(INSTALL_STEPS), 'install steps')
