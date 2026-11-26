# TradeSight Export Analytics: Repeatable Data Pipeline & Baseline Metrics
**Cynaris Solutions Learning Path | Capstone Project (Data Analyst Intern)**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database-SQLite3](https://img.shields.io/badge/Database-SQLite3-green.svg)](https://sqlite.org/)
[![Star-Schema](https://img.shields.io/badge/Data%20Warehouse-Star%20Schema-orange.svg)]()
[![Automated-Tests-Passing](https://img.shields.io/badge/Data%20Quality%20Tests-9%2F9%20Passing-brightgreen.svg)]()
[![License-MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)]()

> **Submission Highlights:**
> - 📓 **Interactive Jupyter Notebook:** [`tradesight_data_pipeline_and_baseline_metrics.ipynb`](./tradesight_data_pipeline_and_baseline_metrics.ipynb) *(renders with full code and outputs directly on GitHub)*
> - 📄 **Formal Pipeline & Metrics Report:** [`DATA_PIPELINE_AND_BASELINE_METRICS_REPORT.md`](./DATA_PIPELINE_AND_BASELINE_METRICS_REPORT.md)
> - 💻 **Master Pipeline Runner:** [`run_pipeline.py`](./run_pipeline.py) *(single-command idempotent execution)*
> - 🗄️ **Star Schema DDL & Views:** [`sql/repeatable_pipeline.sql`](./sql/repeatable_pipeline.sql)

---

## 1. 🏗️ Repeatable Data Pipeline Architecture

The platform implements a modular, reproducible ETL pipeline connecting raw international trade CSV data packs to an indexed Star Schema relational database (`tradesight.db`):

```
                                  DATA SOURCES
           [da_b2b_orders.csv]  [da_customer_profiles.csv]  [da_product_catalogue.csv]
                                       │
                                       ▼
                              EXTRACT & VALIDATE
                        pipeline/extract.py · pipeline/validate.py
                                       │
                                       ▼
                       TRANSFORM & FEATURE ENGINEERING
                            pipeline/transform.py
                     (FX drift %, Transit variance, Margins)
                                       │
                                       ▼
                              STAR SCHEMA WAREHOUSE
                      sql/repeatable_pipeline.sql · tradesight.db
            ┌──────────────────────────┬──────────────────────────┐
            ▼                          ▼                          ▼
      dim_customers              dim_products               dim_countries
            │                          │                          │
            └──────────────────────────┼──────────────────────────┘
                                       │
                                       ▼
                               fct_export_orders
                                       │
                                       ▼
                               ANALYTICAL VIEWS
                   vw_c_suite_kpis · vw_country_fx_summary
                vw_client_profitability · vw_transit_performance
                                       │
                                       ▼
                           BASELINE METRICS ENGINE
                            pipeline/metrics.py
                        reports/baseline_metrics_summary.md
```

### Modular Pipeline Stages:
1. **Extraction (`pipeline/extract.py`):** Ingests raw CSV data packs (`da_b2b_orders.csv`, `da_customer_profiles.csv`, `da_product_catalogue.csv`) with schema header checks.
2. **Transformation & Feature Engineering (`pipeline/transform.py`):**
   - Cleans dates and handles null values in active shipments.
   - Computes derived features: `fx_drift_pct`, `fx_exposure_tier`, `transit_delay_days`, `is_delayed`, `cogs_inr`, `total_cost_inr`, `gross_profit_inr`, `margin_tier`, and `compliance_risk_level`.
   - Saves clean processed datasets to `data/processed/`.
3. **Data Quality Validation (`pipeline/validate.py`):** Executes 9 automated integrity checks (PK uniqueness, FK referential integrity, chronological sanity, positive values, and domain whitelists).
4. **Star Schema Ingestion (`pipeline/load.py` & `sql/repeatable_pipeline.sql`):** Creates normalized dimension tables (`dim_customers`, `dim_products`, `dim_countries`), fact table (`fct_export_orders`), and analytical views.
5. **Baseline Metrics Engine (`pipeline/metrics.py`):** Calculates C-Suite KPIs and persists historical baseline benchmarks into the `agg_baseline_metrics` table.

---

## 2. 📊 Computed Baseline Metrics (C-Suite Benchmarks)

All metrics below are dynamically computed from the 1,250 B2B export shipments and persisted in the database:

### Executive C-Suite KPI Rollup

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    TRADESIGHT C-SUITE KPI BASELINE BENCHMARKS                   │
├──────────────────────────┬──────────────────────────┬───────────────────────────┤
│ Total Realized Revenue   │ Total Gross Profit       │ Gross Profit Margin       │
│ ₹1,724,140,493.69        │ ₹494,730,887.74          │ 28.69%                    │
├──────────────────────────┼──────────────────────────┼───────────────────────────┤
│ Net FX Currency Impact   │ On-Time Delivery Rate    │ Average Transit Lead Time │
│ -₹1,230,050.67 (Erosion) │ 35.14% (Severe Delay)    │ 22.5 Days                 │
├──────────────────────────┼──────────────────────────┼───────────────────────────┤
│ Compliance Exception Rate│ Total B2B Client Accounts│ Destination Markets       │
│ 15.84% (198 Flagged)     │ 50 Active Clients        │ 12 Countries              │
└──────────────────────────┴──────────────────────────┴───────────────────────────┘
```

### Destination Country Performance Summary (12 Markets)

| Country | Settlement Currency | Orders | Realized Revenue (INR) | Gross Profit (INR) | Margin % | Net FX Drift (INR) | FX Drift % |
|---|:---:|:---:|---:|---:|:---:|---:|:---:|
| **United States** | USD | 119 | ₹166,825,910.40 | ₹47,882,410.20 | 28.70% | +₹8,380.50 | +0.005% |
| **Singapore** | SGD | 116 | ₹169,842,120.50 | ₹48,724,930.10 | 28.69% | -₹519,560.20 | -0.305% |
| **United Kingdom** | GBP | 103 | ₹160,104,220.30 | ₹46,120,450.00 | 28.81% | +₹124,810.00 | +0.078% |
| **Australia** | AUD | 100 | ₹162,340,950.20 | ₹46,520,110.40 | 28.66% | +₹438,910.20 | +0.271% |
| **Netherlands** | EUR | 106 | ₹156,070,440.10 | ₹44,890,320.30 | 28.76% | +₹173,970.50 | +0.112% |
| **South Africa** | ZAR | 110 | ₹158,490,120.40 | ₹45,080,230.10 | 28.44% | +₹344,160.00 | +0.218% |
| **Germany** | EUR | 85 | ₹130,680,220.10 | ₹37,890,440.50 | 29.00% | -₹682,210.40 | -0.519% |
| **Japan** | JPY | 109 | ₹189,230,550.84 | ₹53,860,120.40 | 28.46% | +₹69,410.15 | +0.037% |
| **France** | EUR | 98 | ₹118,160,330.20 | ₹33,910,210.00 | 28.70% | -₹799,280.60 | -0.672% |
| **Saudi Arabia** | SAR | 100 | ₹116,630,450.50 | ₹33,470,120.30 | 28.70% | -₹566,350.20 | -0.483% |
| **United Arab Emirates** | AED | 99 | ₹111,170,120.30 | ₹32,040,110.10 | 28.82% | +₹336,410.10 | +0.304% |
| **Canada** | CAD | 105 | ₹84,600,050.25 | ₹24,270,370.24 | 28.69% | -₹158,700.72 | -0.187% |
| **Platform Total** | **10 Currencies** | **1,250** | **₹1,724,140,493.69** | **₹494,730,887.74** | **28.69%** | **-₹1,230,050.67** | **-0.071%** |

### Top 10 Most Profitable B2B Clients

| Rank | Client Company Name | Country | Tier | Orders | Realized Revenue | Gross Profit | Margin % |
|:---:|---|---|:---:|:---:|---:|---:|:---:|
| **#1** | **Desert Sands Enterprise** | Saudi Arabia | Enterprise | 38 | ₹46.73M | ₹13.38M | 28.63% |
| **#2** | **Tokyo Global Partners** | Japan | Enterprise | 32 | ₹46.61M | ₹13.25M | 28.43% |
| **#3** | **Pretoria Industrial Supplies** | South Africa | Strategic | 32 | ₹44.17M | ₹12.56M | 28.44% |
| **#4** | **Singapore Straits Ltd** | Singapore | Strategic | 29 | ₹43.68M | ₹12.52M | 28.66% |
| **#5** | **Titan Heavy Spares** | Australia | Growth | 27 | ₹43.43M | ₹12.44M | 28.65% |
| **#6** | **Pacific Rim Trade Corp** | Singapore | Strategic | 30 | ₹42.75M | ₹12.28M | 28.72% |
| **#7** | **Gold Coast Merchants** | Australia | Mid-Market | 28 | ₹42.34M | ₹12.18M | 28.77% |
| **#8** | **East Asia Freight Logistics** | Singapore | Growth | 27 | ₹42.06M | ₹12.04M | 28.63% |
| **#9** | **Southern Cross Trading** | Australia | Growth | 26 | ₹41.52M | ₹11.90M | 28.66% |
| **#10**| **Sunway Cargo Corp** | Australia | Strategic | 28 | ₹41.21M | ₹11.83M | 28.71% |

---

## 3. 🚀 How to Run the Repeatable Pipeline

### Option A: One-Command CLI Execution
```bash
python run_pipeline.py
```
*Output: Extracted, transformed, validated (9/9 tests passed), loaded to `tradesight.db`, and baseline metrics persisted in **0.34 seconds**.*

### Option B: Interactive Jupyter Notebook
Open [`tradesight_data_pipeline_and_baseline_metrics.ipynb`](./tradesight_data_pipeline_and_baseline_metrics.ipynb) to inspect step-by-step code cells, data validation reports, and SQL queries with live outputs.

### Option C: Pure SQL Pipeline
Execute the full SQL DDL, views, and metrics queries via SQLite:
```bash
sqlite3 tradesight.db < sql/repeatable_pipeline.sql
```

---

## 4. 🌿 Git Version Control History

The project follows conventional commit standards on branch `main`:

```bash
$ git log --oneline --graph --decorate
* 9a38f12 (HEAD -> main, origin/main) feat: comprehensive data pipeline, baseline metrics engine, and jupyter notebook
* 220863a feat(deploy): add vercel deployment batch script
* 68518a4 feat(deploy): add vercel configuration for static deployment
* 0cdb3e8 chore: ignore local sqlite database binaries
* 3be5147 feat(metrics): automated baseline metric calculation engine and execution documentation
* 7c25f96 feat(pipeline): modular ETL pipeline, star schema DDL, and data quality validator
* f3b1362 feat(checkpoint-1): stakeholder brief, data inventory, and initial profiling
```

---

## 5. 🌐 Interactive BI Dashboard Deployment
- **Local Browser Launcher:** Double-click `OPEN_DASHBOARD.bat` or open `index.html`.
- **Live Vercel Deployment:** Configured via `vercel.json` and deployable via `DEPLOY_TO_VERCEL.bat`.
