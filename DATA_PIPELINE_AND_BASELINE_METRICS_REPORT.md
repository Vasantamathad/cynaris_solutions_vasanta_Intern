# TradeSight Export Analytics: Repeatable Data Pipeline & Baseline Metrics Report
**Cynaris Solutions Learning Path | Capstone Project (Data Analyst Intern)**  
**Submission Artifact: Data Engineering Pipeline, Baseline Metrics & Version Control**

---

## 1. Executive Summary

This deliverable fulfills the core requirements for the **Data Engineering & Baseline Analytics Milestone** of the **TradeSight Export Analytics** platform:
1. **Repeatable Data Pipeline (Python & SQL):** A modular, automated ETL architecture that handles raw data extraction, feature engineering (38 attributes), automated data quality validation (9/9 tests passed), and idempotent loading into a production SQLite Star Schema data warehouse (`tradesight.db`).
2. **Computed Baseline Metrics:** Complete mathematical calculation and persistence of the 10 core C-Suite baseline KPIs, 12-country export performance breakdown, client profitability rankings, transit lead times, and compliance exception distributions.
3. **Execution Traceability & Version Control:** Version-controlled git repository with conventional commits, a live Jupyter Notebook ([`tradesight_data_pipeline_and_baseline_metrics.ipynb`](file:///c:/CYNARIS%20PROJECT/tradesight_data_pipeline_and_baseline_metrics.ipynb)), a master runner ([`run_pipeline.py`](file:///c:/CYNARIS%20PROJECT/run_pipeline.py)), and an interactive BI dashboard ([`index.html`](file:///c:/CYNARIS%20PROJECT/index.html)).

---

## 2. Pipeline Architecture & Modular Design

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

### Module Responsibilities

| Pipeline Stage | Module File | Description & Execution Logic |
|---|---|---|
| **Pipeline Runner** | [`run_pipeline.py`](file:///c:/CYNARIS%20PROJECT/run_pipeline.py) | Master CLI entry point; triggers extraction, transformation, validation, loading, and metric rollups sequentially. |
| **Extraction** | [`pipeline/extract.py`](file:///c:/CYNARIS%20PROJECT/pipeline/extract.py) | Ingests 1,250 raw order records, 50 client profiles, and 25 product catalogue entries with schema type checking. |
| **Transformation** | [`pipeline/transform.py`](file:///c:/CYNARIS%20PROJECT/pipeline/transform.py) | Standardizes dates, handles null values in active pipeline shipments, and engineers 8+ derived features (`transit_delay_days`, `fx_drift_pct`, `fx_exposure_tier`, `margin_tier`, `compliance_risk_level`). Saves cleaned datasets to `data/processed/`. |
| **Data Quality Validation** | [`pipeline/validate.py`](file:///c:/CYNARIS%20PROJECT/pipeline/validate.py) | Executes an automated 9-test data quality suite (PK uniqueness, FK referential integrity, chronological sanity, positive currency/quantities, domain whitelists). |
| **Star Schema Loader** | [`pipeline/load.py`](file:///c:/CYNARIS%20PROJECT/pipeline/load.py) | Connects to `tradesight.db`, creates normalized dimensions (`dim_customers`, `dim_products`, `dim_countries`) and fact table (`fct_export_orders`), and builds analytical views. |
| **Metrics Engine** | [`pipeline/metrics.py`](file:///c:/CYNARIS%20PROJECT/pipeline/metrics.py) | Calculates C-Suite KPIs, persists benchmark metrics to `agg_baseline_metrics`, and generates Markdown/JSON reports. |

---

## 3. Computed Baseline Metrics (Official C-Suite Benchmarks)

All metrics below have been dynamically computed from the 1,250 B2B export shipments and persisted in the SQLite warehouse table `agg_baseline_metrics`:

### 3.1 Executive C-Suite KPI Rollup

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

* **Gross Revenue Booked:** ₹1,725,370,544.36 (Contracted value at order booking).
* **Realized Revenue in INR:** ₹1,724,140,493.69 (Realized value upon payment settlement).
* **Net Realized FX Variance:** -₹1,230,050.67 (Unhedged currency drift across 10 global settlement currencies).
* **Total Landed Costs:** ₹1,229,409,605.95 (COGS: 78.4%, Shipping Freight: 19.8%, Customs Handling: 1.8%).
* **Gross Profit:** ₹494,730,887.74 (Realized margin: **28.69%**).
* **On-Time Delivery Rate (OTD%):** **35.14%** (Air Cargo: 34.5% OTD vs Sea Freight: 35.3% OTD).
* **Average Transit Lead Time:** **22.5 Days** (Air Cargo: 7.0 days vs Sea Freight: 25.8 days).
* **Compliance Exception Frequency:** **15.84%** (198 of 1,250 shipments faced regulatory holds, adding an average delay of +7.6 days).

---

### 3.2 12-Country Performance & Currency (FX) Volatility

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
| **Total / Overall** | **10 Currencies** | **1,250** | **₹1,724,140,493.69** | **₹494,730,887.74** | **28.69%** | **-₹1,230,050.67** | **-0.071%** |

---

### 3.3 Top 10 Most Profitable B2B Clients

| Rank | Client Company Name | Country | Client Tier | Orders | Realized Revenue | Gross Profit (INR) | Margin % |
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

### 3.4 Compliance Exception Risk Register

| Compliance Flag Category | Severity Level | Flagged Orders | Share of Total | Avg Delay Days | Cost Impact (INR) |
|---|:---:|:---:|:---:|:---:|---:|
| **None (Compliant)** | Compliant | 1,052 | 84.16% | 0.0 days | Baseline |
| **Customs Inspection Hold** | Critical | 40 | 3.20% | 8.3 days | +₹6,000 / shipment |
| **HS Code Discrepancy** | Moderate | 37 | 2.96% | 7.4 days | +₹6,000 / shipment |
| **Fumigation / Phytosanitary Delay** | Moderate | 34 | 2.72% | 7.3 days | +₹6,000 / shipment |
| **Documentation Incomplete** | High | 32 | 2.56% | 8.1 days | +₹6,000 / shipment |
| **Tariff Rate Query** | Low | 30 | 2.40% | 6.8 days | +₹6,000 / shipment |
| **Country Sanctions Screening** | Critical | 25 | 2.00% | 7.8 days | +₹6,000 / shipment |
| **Total Flagged Exceptions** | **Action Required** | **198** | **15.84%** | **7.6 days avg** | **₹1,188,000 extra** |

---

## 4. How to Execute the Pipeline

### Method A: Execute Master Pipeline via CLI
Run the following in the repository root:
```bash
python run_pipeline.py
```
**Terminal Output:**
```text
===========================================================================
TRADESIGHT EXPORT ANALYTICS - REPEATABLE DATA PIPELINE
Cynaris Solutions Learning Path | Capstone Project
===========================================================================
  [EXTRACT] Reading raw CSV data packs...
    - Customers: 50 records (12 columns)
    - Products:  25 records (9 columns)
    - Orders:    1250 records (31 columns)
  [TRANSFORM] Executing data cleaning and feature engineering...
    - Cleaned orders enriched: 1250 records (38 features)
    - Cleaned datasets saved to: ./data/processed
  [VALIDATE] Running automated data quality test suite...
    - Test Results: 9/9 passed. Status: SUCCESS (All Passed)
  [LOAD] Connecting to database: ./tradesight.db...
    - Star Schema DDL and Analytical Views initialized.
    - Loaded dim_countries: 12 records
    - Loaded dim_customers: 50 records
    - Loaded dim_products:  25 records
    - Loaded fct_export_orders: 1250 records
  [METRICS] Calculating and persisting baseline trade metrics...
    - Baseline metrics persisted to table: agg_baseline_metrics
    - Reports generated: baseline_metrics_report.json, baseline_metrics_summary.md
===========================================================================
PIPELINE EXECUTION COMPLETED SUCCESSFULLY IN 0.34s
===========================================================================
```

### Method B: View Interactive Jupyter Notebook
Open [`tradesight_data_pipeline_and_baseline_metrics.ipynb`](file:///c:/CYNARIS%20PROJECT/tradesight_data_pipeline_and_baseline_metrics.ipynb) in VS Code, JupyterLab, or GitHub to inspect the code cells, data validation reports, and SQL queries with live execution outputs.

### Method C: Execute Pure SQL Pipeline
Execute [`sql/repeatable_pipeline.sql`](file:///c:/CYNARIS%20PROJECT/sql/repeatable_pipeline.sql) in any SQL client (e.g., DB Browser for SQLite):
```bash
sqlite3 tradesight.db < sql/repeatable_pipeline.sql
```

---

## 5. Version Control & Git Commit History

The repository has been structured with clean semantic commits tracking all pipeline components:

```bash
$ git log --oneline --graph --decorate
* 220863a (HEAD -> main, origin/main) feat(deploy): add vercel deployment batch script
* 68518a4 feat(deploy): add vercel configuration for static deployment
* 0cdb3e8 chore: ignore local sqlite database binaries
* 3be5147 feat(metrics): automated baseline metric calculation engine and execution documentation
* 7c25f96 feat(pipeline): modular ETL pipeline, star schema DDL, and data quality validator
* f3b1362 feat(checkpoint-1): stakeholder brief, data inventory, and initial profiling
```

* **Remote Repository URL:** [https://github.com/Vasantamathad/CYNARIS-PROJECT](https://github.com/Vasantamathad/CYNARIS-PROJECT)
* **Branch:** `main` (clean working tree, fully synced).
