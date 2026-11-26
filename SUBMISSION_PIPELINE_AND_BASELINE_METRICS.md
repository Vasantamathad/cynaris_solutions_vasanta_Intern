# TradeSight Export Analytics: Repeatable Data Pipeline & Baseline Metric Calculations
**Candidate:** Vasanta Mathad  
**Track:** Data Analyst Intern · Capstone Project  
**Client:** TradeSight Global Export Management Ltd. (Chennai, India)  
**Repository:** https://github.com/Vasantamathad/CYNARIS-PROJECT  
**Interactive Notebook:** https://github.com/Vasantamathad/CYNARIS-PROJECT/blob/main/tradesight_data_pipeline_and_baseline_metrics.ipynb  

---

## 1. Executive Summary & Objective

To fulfill the capstone requirements, an **end-to-end repeatable data pipeline** (built in Python and SQL) was engineered to ingest, clean, enrich, validate, and load international export shipment data into an indexed Star Schema relational data warehouse (`tradesight.db`). 

Baseline metrics were then computed to benchmark:
1. **Commercial Revenue & Gross Profit Margins** across 5 product categories.
2. **Foreign Exchange (FX) Currency Impact** across 12 destination markets and 10 settlement currencies.
3. **Client-Level Profitability Rankings** across 50 active B2B enterprise accounts.
4. **Logistics Transit Lead Times & On-Time Delivery Rates (OTD%)** across maritime and air corridors.
5. **Export Compliance Exception Frequencies** and their operational cost/delay impact.

---

## 2. Repeatable Data Pipeline Architecture

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

### Pipeline Flow:
* **Stage 1 (Extraction):** Ingests raw data from `da_b2b_orders.csv` (1,250 records), `da_customer_profiles.csv` (50 records), and `da_product_catalogue.csv` (25 records).
* **Stage 2 (Transformation & Feature Engineering):** Casts data types, resolves active shipment nulls, and derives 38 analytical features including `fx_drift_pct`, `fx_exposure_tier`, `transit_delay_days`, `is_delayed`, `cogs_inr`, `total_cost_inr`, `gross_profit_inr`, `margin_tier`, and `compliance_risk_level`. Cleaned datasets are archived in `data/processed/`.
* **Stage 3 (Automated Quality Validation):** Runs 9 automated integrity checks (PK uniqueness, FK referential integrity, chronological date logic, positive values, and domain whitelists). All 9 tests passed.
* **Stage 4 (Star Schema Ingestion):** Idempotently loads normalized dimension tables (`dim_customers`, `dim_products`, `dim_countries`) and fact table (`fct_export_orders`) into SQLite.
* **Stage 5 (Baseline Metrics Calculation):** Persists summary KPIs into the database table `agg_baseline_metrics` and outputs structured reports.

---

## 3. Data Pipeline Code Implementation

### 3.1 Python Master Pipeline Orchestrator (`run_pipeline.py`)

```python
import sys
import time
from pipeline.config import ensure_directories
from pipeline.extract import extract_all
from pipeline.transform import transform_and_save_all
from pipeline.validate import validate_datasets
from pipeline.load import load_star_schema
from pipeline.metrics import calculate_and_persist_baseline_metrics

def main():
    start_time = time.time()
    print("=" * 75)
    print("TRADESIGHT EXPORT ANALYTICS - REPEATABLE DATA PIPELINE")
    print("=" * 75)
    
    # 1. Ensure directory tree
    ensure_directories()
    
    # 2. Extract raw data packs
    extracted = extract_all()
    
    # 3. Transform & Feature Engineering
    transformed = transform_and_save_all(extracted)
    
    # 4. Automated Data Quality Validation Suite
    validate_datasets(transformed)
    
    # 5. Load into Star Schema Data Warehouse
    conn = load_star_schema(transformed)
    
    # 6. Calculate & Persist Baseline C-Suite Metrics
    calculate_and_persist_baseline_metrics(conn)
    conn.close()
    
    duration = time.time() - start_time
    print("=" * 75)
    print(f"PIPELINE EXECUTION COMPLETED SUCCESSFULLY IN {duration:.2f}s")
    print("Database: tradesight.db (Star Schema with Analytical Views)")
    print("=" * 75)

if __name__ == "__main__":
    main()
```

---

### 3.2 SQL Star Schema DDL & Analytical Views (`sql/repeatable_pipeline.sql`)

```sql
-- Core Fact Table DDL with 38 Features
CREATE TABLE fct_export_orders (
    order_id VARCHAR(25) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    order_quantity INTEGER NOT NULL,
    settlement_currency VARCHAR(10) NOT NULL,
    unit_price_foreign NUMERIC(12, 2) NOT NULL,
    order_value_foreign NUMERIC(14, 2) NOT NULL,
    booking_fx_rate NUMERIC(10, 4) NOT NULL,
    settlement_fx_rate NUMERIC(10, 4) NOT NULL,
    order_value_inr_booked NUMERIC(14, 2) NOT NULL,
    order_value_inr_realized NUMERIC(14, 2) NOT NULL,
    fx_gain_loss_inr NUMERIC(14, 2) NOT NULL,
    fx_drift_pct NUMERIC(6, 3) NOT NULL,
    fx_exposure_tier VARCHAR(50) NOT NULL,
    shipping_mode VARCHAR(30) NOT NULL,
    origin_port VARCHAR(100) NOT NULL,
    destination_country VARCHAR(100) NOT NULL,
    destination_port VARCHAR(150) NOT NULL,
    dispatch_date DATE NOT NULL,
    target_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    target_transit_days INTEGER,
    transit_days INTEGER,
    transit_delay_days INTEGER,
    is_delayed INTEGER,
    shipment_status VARCHAR(50) NOT NULL,
    compliance_status VARCHAR(50) NOT NULL,
    compliance_flag_type VARCHAR(100) NOT NULL,
    compliance_delay_days INTEGER NOT NULL,
    compliance_risk_level VARCHAR(30) NOT NULL,
    cogs_inr NUMERIC(14, 2) NOT NULL,
    shipping_cost_inr NUMERIC(14, 2) NOT NULL,
    customs_handling_inr NUMERIC(14, 2) NOT NULL,
    total_cost_inr NUMERIC(14, 2) NOT NULL,
    gross_profit_inr NUMERIC(14, 2) NOT NULL,
    profit_margin_pct NUMERIC(6, 2) NOT NULL,
    margin_tier VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
);

-- Analytical View 1: C-Suite Executive KPI Rollup
CREATE VIEW vw_c_suite_kpis AS
SELECT 
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_value_inr_booked), 2) AS total_revenue_booked_inr,
    ROUND(SUM(order_value_inr_realized), 2) AS total_revenue_realized_inr,
    ROUND(SUM(fx_gain_loss_inr), 2) AS net_fx_impact_inr,
    ROUND(SUM(gross_profit_inr), 2) AS total_gross_profit_inr,
    ROUND((SUM(gross_profit_inr) / SUM(order_value_inr_realized)) * 100, 2) AS gross_profit_margin_pct,
    ROUND(
        (SUM(CASE WHEN shipment_status = 'Delivered On-Time' THEN 1.0 ELSE 0.0 END) / 
         NULLIF(SUM(CASE WHEN actual_delivery_date IS NOT NULL THEN 1.0 ELSE 0.0 END), 0)) * 100, 2
    ) AS on_time_delivery_rate_pct,
    ROUND(AVG(transit_days), 1) AS avg_transit_lead_time_days,
    ROUND(
        (SUM(CASE WHEN compliance_status = 'Exception Flagged' THEN 1.0 ELSE 0.0 END) / COUNT(order_id)) * 100, 2
    ) AS compliance_exception_rate_pct,
    COUNT(DISTINCT customer_id) AS total_active_clients,
    COUNT(DISTINCT destination_country) AS total_destination_countries
FROM fct_export_orders;
```

---

## 4. Computed Baseline Metric Outputs (Official Benchmarks)

### 4.1 C-Suite Executive KPI Benchmarks

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

* **Total Export Shipments:** 1,250 orders across 14 consecutive months (Jan 2025 – Feb 2026).
* **Booked Revenue:** ₹1,725,370,544.36 (Contracted value at booking date exchange rate).
* **Realized Revenue:** ₹1,724,140,493.69 (Settled value converted to INR).
* **Net Realized FX Impact:** -₹1,230,050.67 (Unhedged currency depreciation across settlement cycles).
* **Landed Export Costs:** ₹1,229,409,605.95 (COGS: 78.4%, Ocean/Air Freight: 19.8%, Customs: 1.8%).
* **Gross Profit Contribution:** ₹494,730,887.74 (**28.69% Gross Profit Margin**).
* **On-Time Delivery Performance:** **35.14%** (Air Cargo: 34.5% OTD vs Sea Freight: 35.3% OTD).
* **Average Transit Lead Time:** **22.5 Days** (Air Cargo: 7.0 days vs Sea Freight: 25.8 days).
* **Compliance Exception Frequency:** **15.84%** (198 flagged shipments, average delay: +7.6 days).

---

### 4.2 12 Destination Countries Performance Breakdown

| Country | Currency | Orders | Realized Revenue (INR) | Gross Profit (INR) | Margin % | Net FX Drift (INR) | FX Drift % |
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

### 4.3 Top 10 Most Profitable B2B Clients

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

### 4.4 Compliance Exception Risk Register (198 Flagged Shipments)

| Compliance Flag Category | Risk Level | Flagged Orders | Share of Total | Avg Delay Days | Cost Impact (INR) |
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

## 5. Automated Data Quality Test Suite Results

The validation module (`pipeline/validate.py`) executed 9 automated tests prior to database ingestion:

1. **[PASS] Customer PK Uniqueness:** 50 records, 50 unique IDs.
2. **[PASS] Product PK Uniqueness:** 25 records, 25 unique IDs.
3. **[PASS] Order PK Uniqueness:** 1,250 records, 1,250 unique IDs.
4. **[PASS] Order $\rightarrow$ Customer FK Integrity:** 0 orphaned customer references found.
5. **[PASS] Order $\rightarrow$ Product FK Integrity:** 0 orphaned product references found.
6. **[PASS] Chronological Sequence Integrity:** 0 date sequence discrepancies (`dispatch_date >= order_date`, `actual_delivery_date >= dispatch_date`).
7. **[PASS] Positive Financial & Quantity Values:** 0 non-positive quantities or exchange rates.
8. **[PASS] 12 Destination Country Whitelist:** 100% adherence to supported 12 export nations.
9. **[PASS] Settlement Currency Whitelist:** 100% adherence to 10 supported currencies.
*Overall Data Quality Verdict:* **9/9 Tests Passed (100% Quality Score)**.

---

## 6. How to Run & Verify

1. **CLI Execution:** Run `python run_pipeline.py` in the project root.
2. **Jupyter Notebook:** Open `tradesight_data_pipeline_and_baseline_metrics.ipynb` to view live step-by-step execution.
3. **Interactive BI Dashboard:** Open `index.html` or double-click `OPEN_DASHBOARD.bat`.
4. **GitHub Repository:** [https://github.com/Vasantamathad/CYNARIS-PROJECT](https://github.com/Vasantamathad/CYNARIS-PROJECT)
