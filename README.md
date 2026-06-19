# pipeline-bike

Databricks Asset Bundle (DABs) project for the bike-share Spark Declarative Pipeline.

## Layout

```
exportedDabs/
├── databricks.yml                        # Bundle entrypoint and target definitions
├── resources/
│   ├── pipelines/pipeline_bike.yml       # SDP pipeline (serverless, SQL sources)
│   └── jobs/init_pipeline_bike.yml       # Job: generate data + trigger pipeline
├── src/
│   ├── pipeline-bike/                    # SQL transformation files
│   │   ├── 01-bronze.sql
│   │   ├── 02-silver.sql
│   │   └── 03-gold.sql
│   └── init-pipeline-bike/              # Job notebook sources
│       ├── 00-global-setup-v2.py
│       └── 01-Bike-Data-generator.py
├── .github/workflows/
│   ├── pr_validate.yml                   # Validate bundle on PRs to main
│   ├── deploy_to_staging.yml             # Deploy to staging on merge to main
│   └── deploy_to_prod.yml               # Deploy to prod on tag push / manual dispatch
├── tests/
│   └── test_unity_catalog.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
databricks bundle validate
```

## Deploying

Production deploys run through CI only — never `databricks bundle deploy -t prod` from a laptop.

| Target | Trigger |
|---|---|
| `dev` | `databricks bundle deploy` from your machine (default target) |
| `staging` | Merge to `main` (GitHub Actions) |
| `prod` | Push a `v*` tag or manual workflow dispatch (requires reviewer approval) |

## Filling in placeholders

Before the first deploy, replace these in `databricks.yml`:

- `https://<dev-workspace-host>.azuredatabricks.net` — your dev workspace URL
- `https://<staging-workspace-host>.azuredatabricks.net` — staging workspace URL
- `https://<prod-workspace-host>.azuredatabricks.net` — prod workspace URL
- `${var.catalog}` default — the Unity Catalog catalog to use (defaults to `dev`)
- `${var.schema}` default — the schema (defaults to `dbdemos_pipeline_bike`)

## GitHub Actions secrets

Configure these in **Settings → Environments** (one set per `staging` / `prod` environment):

| Secret | Description |
|---|---|
| `DATABRICKS_HOST` | Workspace URL matching the target's `workspace_host` |
| `DATABRICKS_CLIENT_ID` | Service principal application (client) ID |
| `DATABRICKS_CLIENT_SECRET` | Service principal client secret |
| `catalog` | Unity Catalog catalog name (maps to `BUNDLE_VAR_catalog`) |
| `schema` | Unity Catalog schema name (maps to `BUNDLE_VAR_schema`) |
| `STAGING_SP_APP_ID` | Service principal client ID used as `run_as` for staging |
| `PROD_SP_APP_ID` | Service principal client ID used as `run_as` for prod |

`DATABRICKS_BUNDLE_ENV` is hardcoded per workflow step and tells the CLI which target to deploy to.
