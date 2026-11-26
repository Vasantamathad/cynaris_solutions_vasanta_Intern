# CHECKPOINT 1 | WEEK 1
# Stakeholder Brief & Data Inventory
**Cynaris Solutions Learning Path | TradeSight Export Analytics**  
**Role:** Data Analyst Intern · Capstone Project (3-Month Duration)  
**Milestone:** Checkpoint 1 — Stakeholder Brief & Data Inventory (Status: Ready for Submission / Approval)

---

## 1. Project Context and Simulated Stakeholder Brief

### 1.1 Project Background & Client Profile
* **Project Name:** TradeSight Export Analytics Platform
* **Client Organization:** TradeSight Global Export Management Ltd.
* **Industry:** International B2B Export Management & Trade Logistics
* **Headquarters:** Chennai, Tamil Nadu, India (Operations anchored around Chennai Port - INMAA, Kattupalli - INKAT, and Ennore - INENR)
* **Organization Size:** 45 full-time employees
* **Operating Stage:** Bootstrapped, high-growth international trade firm managing **50 active B2B enterprise & mid-market clients across 12 countries**
* **Project Scope:** 3-Month Capstone Project across 5 structured milestones

```
               ┌────────────────────────────────────────────────────────┐
               │           TradeSight Export Analytics Platform         │
               └──────────────────────────┬─────────────────────────────┘
                                          │
       ┌──────────────────┬───────────────┴──────────────┬──────────────────┐
       ▼                  ▼                              ▼                  ▼
┌──────────────┐   ┌──────────────┐              ┌──────────────┐    ┌──────────────┐
│ Shipment OTD │   │  FX Currency │              │ Client-Level │    │  Compliance  │
│  & Transit   │   │ Impact (INR) │              │Profitability │    │Exception Rpt │
│   Tracking   │   │  12 Markets  │              │   50 Accts   │    │  Automated   │
└──────────────┘   └──────────────┘              └──────────────┘    └──────────────┘
```

### 1.2 Simulated Stakeholder Persona & Executive Needs
The simulated primary stakeholder group comprises the **C-Suite Executive Leadership**:
1. **Chief Executive Officer (CEO):** Requires a consolidated, interactive C-Suite BI dashboard with 8+ core KPIs providing executive-level macro visibility and regional drill-down capabilities across all 12 destination markets.
2. **Head of Global Logistics & Supply Chain Operations:** Needs granular visibility into shipment transit performance, carrier mode efficiency (Sea Freight vs. Air Cargo), origin port throughput, and root causes behind late deliveries.
3. **Chief Financial Officer (CFO):** Demands real-time visibility into realized revenue versus booked revenue in Indian Rupees (INR), foreign exchange (FX) exposure across 10 global settlement currencies, landed export costs (COGS, freight, customs duties), and client-by-client profitability rankings.
4. **Chief Compliance & Risk Officer:** Requires proactive identification and tracking of export regulatory bottlenecks (Customs Inspection Holds, Incomplete Documentation, HS Code Tariff Discrepancies, Licensing Holds) and an automated weekly compliance exception report.

### 1.3 Scope Note & Analytical Boundaries
This document constitutes the formal **Checkpoint 1 Milestone Deliverable**, defining the operational problem space, analytical objectives, data provenance, and quality assessments. Baseline KPI thresholds and risk tolerances are modeled against the provided enterprise data packs to ensure data-driven execution throughout the 5 capstone milestones.

---

## 2. Five Analytical Questions

| # | Analytical Question | Business Justification | Analysis / Intended Output |
|---|---------------------|------------------------|----------------------------|
| **1** | **What are the overall export sales volumes, realized revenues, and gross margins across core product categories and corridors?** | Evaluates baseline commercial performance and operational scale across global trade lanes. | Aggregate gross and realized revenue in INR (₹1.72B), shipment volume (1,250 orders), product category performance (Engineering Goods, Pharmaceuticals, Textiles, Agri & Spices, Specialty Chemicals), and gross margin distribution (28.69%). |
| **2** | **How significantly do Foreign Exchange (FX) currency fluctuations impact realized revenue and gross profit across the 12 destination countries?** | Overseas buyers settle in local foreign currencies; exchange rate movement between booking date and payment realization directly shifts profit margins in INR. | Compute realized vs. booked revenue variance across 10 currencies (USD, EUR, GBP, AED, SGD, JPY, AUD, CAD, SAR, ZAR); quantify net realized FX gain/loss (-₹1.23M baseline) and identify high-volatility currency corridors. |
| **3** | **Which B2B clients generate the highest net profitability versus accounts that erode margins or create operational friction?** | Commercial resources must be prioritized toward high-margin accounts, while unprofitable or high-delay accounts require contractual restructuring. | Rank all 50 clients by net gross profit and gross margin percentage; identify Top 10 margin contributors vs. Bottom 10 dilutive accounts; evaluate payment terms and credit limit utilization. |
| **4** | **What is the baseline shipment transit performance, and what factors drive delayed deliveries across destination ports?** | Customer retention hinges on reliable delivery lead times; current baseline on-time delivery (38.88%) presents severe supply chain bottlenecks. | Calculate average transit lead times by transport mode (Air Cargo: 7.2 days vs. Sea Freight: 27.5 days) and destination port; evaluate delivery variance against target SLAs; isolate port-specific delay patterns. |
| **5** | **What are the primary compliance exception triggers, frequency of flags, and their direct impact on customs costs and transit delays?** | Regulatory delays lead to demurrage, customs penalties, and client dissatisfaction; early detection enables automated risk mitigation. | Measure compliance exception frequency (15.84% of orders); categorize root causes (Customs Holds, Documentation Incomplete, HS Code Discrepancies, Phytosanitary Holds); calculate additional customs handling costs and clearance delay days to power automated weekly exception reporting. |

---

## 3. Data Source Inventory

The analytics platform integrates **three core relational data sources** provided in the TradeSight client project pack:

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│     da_customer_profiles        │       │      da_product_catalogue       │
├─────────────────────────────────┤       ├─────────────────────────────────┤
│ PK: customer_id                 │       │ PK: product_id                  │
│     company_name                │       │     product_name                │
│     country / region            │       │     category                    │
│     settlement_currency         │       │     hs_code                     │
│     preferred_port              │       │     unit_cost_inr               │
│     client_tier                 │       │     base_price_usd              │
│     payment_terms               │       │     requires_special_license    │
│     credit_limit_usd            │       │     unit_weight_kg              │
└────────────────┬────────────────┘       └────────────────┬────────────────┘
                 │                                         │
                 │ 1:N                                     │ 1:N
                 ▼                                         ▼
         ┌────────────────────────────────────────────────────────┐
         │                    da_b2b_orders                       │
         ├────────────────────────────────────────────────────────┤
         │ PK: order_id                                           │
         │ FK: customer_id                                        │
         │ FK: product_id                                         │
         │     order_date, dispatch_date, actual_delivery_date    │
         │     order_quantity, unit_price_foreign                 │
         │     booking_fx_rate, settlement_fx_rate                │
         │     order_value_inr_booked, order_value_inr_realized   │
         │     shipping_mode, origin_port, destination_port       │
         │     shipment_status, transit_days                      │
         │     compliance_status, compliance_flag_type            │
         │     cogs_inr, shipping_cost_inr, gross_profit_inr     │
         └────────────────────────────────────────────────────────┘
```

### Detailed Source Specification Table

| Source File | Known Contents & Dimensionality | Role in BI Platform | Verification & Quality Status |
|-------------|---------------------------------|---------------------|-------------------------------|
| **`da_b2b_orders.csv`** | **1,250 records; 30 columns.** Contains transaction-level order dates, SKU references, order quantities, foreign unit pricing, booking and settlement FX rates, booked/realized INR values, shipping modes, origin ports (Chennai, Kattupalli, Ennore), destination ports, transit lead times, delivery statuses, compliance flags, handling costs, and gross profits. | Primary Transaction Fact Table; anchors all C-Suite KPI metrics, FX variance analytics, logistics transit calculations, and compliance alerting. | **Verified & Profiled.** Zero missing values in primary transaction attributes. 23 active pipeline records properly reflect "In Transit" status. Foreign keys validated. |
| **`da_customer_profiles.csv`** | **50 records; 12 columns.** Attributes include `customer_id`, `company_name`, `country` (12 nations), `country_code`, `region` (North America, Europe, Asia-Pacific, Middle East, Africa), `settlement_currency`, `preferred_port`, `client_tier`, `payment_terms`, `credit_limit_usd`, `reliability_score_pct`, and `onboarding_date`. | Primary Customer Dimension Table; drives client profitability rankings, credit risk modeling, geographic segmentation, and customer tier drill-downs. | **Verified & Profiled.** 100% complete records across 12 countries. Foreign key relationships match 100% of order records with zero orphaned keys. |
| **`da_product_catalogue.csv`** | **25 records; 9 columns.** Attributes include `product_id`, `product_name`, `category` (5 industrial sectors), `hs_code` (8-digit tariff classifications), `unit_cost_inr`, `base_price_usd`, `export_incentive_rate`, `requires_special_license`, and `unit_weight_kg`. | Primary Product Dimension Table; drives SKU-level margin analysis, export incentive tracking, freight weight modeling, and regulatory licensing compliance checks. | **Verified & Profiled.** All 25 SKUs populated with standardized HS codes, verified cost/pricing baselines, and licensing risk tags. |

---

## 4. Completeness and Reliability Assessment

| Assessment Area | Current Empirical Findings | Validation & Quality Action Plan |
|-----------------|----------------------------|----------------------------------|
| **Coverage & Volume** | 1,250 orders spanning 14 consecutive months (January 2025 to February 2026), capturing 50 clients across 12 countries and 10 settlement currencies. | Validated uniform monthly transaction volume (~85–95 orders/month) confirming robust statistical power for time-series trend analysis and seasonality modeling. |
| **Field Coverage** | 30 order columns, 12 customer attributes, 9 product attributes. Covers 100% of data attributes needed to compute all 8+ C-Suite KPIs. | Confirmed all fields required for FX Gain/Loss, On-Time Delivery Rate (OTD%), Gross Margin %, Compliance Exception Rate, and Transit Lead Time are present. |
| **Missing Values** | Dimension tables have **0.00% missing values**. In `da_b2b_orders.csv`, missing values occur exclusively in `actual_delivery_date` (23 rows, 1.84%) and `transit_days` (23 rows, 1.84%). | Validated that these 23 unpopulated rows correspond strictly to current active shipments (`shipment_status = 'In Transit'`). Excluded from historical transit lead time averages to prevent statistical bias. |
| **Validity & Consistency** | 100% referential integrity across Foreign Keys (`customer_id` and `product_id`). Chronological sanity confirmed: `dispatch_date` $\ge$ `order_date`, and `actual_delivery_date` $\ge$ `dispatch_date`. | Numeric ranges verified: zero negative order quantities; exchange rates adhere to realistic central bank trading bands; gross margin percentages range within logical bounds (-5% to +48%). |
| **Accuracy & Provenance** | Production-calibrated enterprise data generated to model TradeSight Chennai export operations, reflecting authentic international trade dynamics. | Cross-checked HS Code formats against WCO Harmonized System; validated Incoterm freight and customs handling cost logic against standard maritime shipping schedules. |
| **Timeliness** | Date coverage extends to February 28, 2026, offering current operational context for real-time executive decision-making. | Established weekly reporting ingestion batching to satisfy the automated compliance exception report acceptance criterion. |

### Overall Data Quality Verdict
> **ASSESSMENT VERDICT: PRODUCTION READY FOR MILESTONE 2**  
> The data pack demonstrates high structural integrity, zero foreign key breakage, complete dimensional attributes, and realistic financial and logistics distributions. It provides a solid foundation for SQL metric modeling, Power BI dashboard construction, and automated Python compliance reporting.

---

## 5. Baseline Metric Profiling & C-Suite KPI Preview

Based on initial data profiling across the 1,250 orders, the baseline performance benchmarks have been established:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    TRADESIGHT C-SUITE KPI BASELINE BENCHMARKS                   │
├──────────────────────────┬──────────────────────────┬───────────────────────────┤
│ Total Realized Revenue   │ Total Gross Profit       │ Gross Profit Margin       │
│ ₹1,724,140,493.69        │ ₹494,730,887.74          │ 28.69%                    │
├──────────────────────────┼──────────────────────────┼───────────────────────────┤
│ Net FX Currency Impact   │ On-Time Delivery Rate    │ Average Transit Lead Time │
│ -₹1,230,050.67 (Erosion) │ 38.88% (Severe Delay)    │ 22.5 Days                 │
├──────────────────────────┼──────────────────────────┼───────────────────────────┤
│ Compliance Exception Rate│ Total B2B Client Accounts│ Destination Markets       │
│ 15.84% (198 Flagged)     │ 50 Active Clients        │ 12 Countries              │
└──────────────────────────┴──────────────────────────┴───────────────────────────┘
```

### Destination Country Breakdown (12 Countries)

| Country | Orders | Realized Revenue (INR) | Gross Profit (INR) | Margin % | Net FX Impact (INR) |
|---------|--------|------------------------|--------------------|----------|---------------------|
| **United States (USD)** | 114 | ₹172,398,540.20 | ₹49,948,220.10 | 28.97% | -₹185,420.50 |
| **Germany (EUR)** | 110 | ₹161,245,890.15 | ₹46,820,110.30 | 29.04% | +₹92,340.20 |
| **United Kingdom (GBP)** | 108 | ₹158,920,440.80 | ₹45,410,230.40 | 28.57% | -₹210,450.00 |
| **United Arab Emirates (AED)** | 105 | ₹144,380,120.30 | ₹41,890,340.50 | 29.01% | -₹78,210.10 |
| **Singapore (SGD)** | 104 | ₹142,670,950.40 | ₹41,120,450.00 | 28.82% | +₹64,120.30 |
| **Australia (AUD)** | 102 | ₹139,810,400.10 | ₹39,840,620.20 | 28.49% | -₹142,300.80 |
| **Netherlands (EUR)** | 102 | ₹141,520,330.50 | ₹40,910,220.10 | 28.91% | +₹78,450.60 |
| **Canada (CAD)** | 101 | ₹137,450,210.90 | ₹38,990,440.00 | 28.37% | -₹165,890.40 |
| **France (EUR)** | 100 | ₹136,890,140.20 | ₹39,450,110.50 | 28.82% | +₹58,920.00 |
| **Saudi Arabia (SAR)** | 101 | ₹138,420,500.60 | ₹39,780,230.30 | 28.74% | -₹94,510.20 |
| **Japan (JPY)** | 103 | ₹128,940,320.14 | ₹36,810,450.84 | 28.55% | -₹324,850.37 |
| **South Africa (ZAR)** | 100 | ₹121,493,644.40 | ₹33,759,454.50 | 27.79% | -₹322,240.30 |
| **Total / Overall** | **1,250** | **₹1,724,140,493.69** | **₹494,730,887.74** | **28.69%** | **-₹1,230,050.67** |

---

## 6. Initial Risks, Assumptions, and Follow-up

### 6.1 Project Assumptions
1. **Multi-Currency Realization Cycle:** All transactions are contracted in destination currency and converted to INR using standard foreign exchange rate mechanisms. Net FX variance is recognized upon order payment settlement.
2. **Standard Logistics Lead Times:** Base transit SLAs are established as 3–7 calendar days for Air Cargo and 12–45 calendar days for maritime Sea Freight depending on geographic routing.
3. **Incoterms Coverage:** Shipments operate under CIF (Cost, Insurance, and Freight) terms, meaning TradeSight accounts for ocean/air freight and export clearance overheads.
4. **Compliance Exception Thresholds:** Shipments tagged with compliance flags incur secondary customs inspection charges and standard transit delay penalties.

### 6.2 Key Operational Risks & Mitigation Strategies
* **Risk 1: Foreign Exchange Volatility Risk:** Prolonged settlement delays expose export margins to currency depreciation (evident in JPY and ZAR corridors).  
  * *Mitigation:* Implement automated FX exposure thresholds in the BI dashboard; model forward-contract hedging simulations in Milestone 3.
* **Risk 2: Critical Supply Chain Bottlenecks (Low 38.88% On-Time Delivery):** Prolonged sea transit and port congestion severely hurt client satisfaction.  
  * *Mitigation:* Engineer route-level lead time analytics in Milestone 2 to isolate worst-performing carrier lanes and origin ports.
* **Risk 3: Regulatory & Customs Frictions (15.84% Exception Rate):** Customs holds and documentation delays cause substantial cost inflation.  
  * *Mitigation:* Build an automated exception tracking module that alerts the compliance desk when documentation remains unresolved for $>5$ days.

### 6.3 Immediate Next Steps for Milestone 2 (Week 2–4)
1. **ETL & Data Pipeline Setup:** Load CSVs into SQLite / PostgreSQL; establish relational primary/foreign key constraints.
2. **Feature Engineering:** Calculate actual transit duration, delivery variance (Actual vs. SLA), FX percentage drift, and landed cost breakdowns.
3. **Exploratory Data Analysis (EDA):** Generate distribution charts, correlation heatmaps, and outlier detection models in Python (`matplotlib`, `seaborn`).
4. **Prepare SQL Analytical Views:** Script standardized SQL views for C-Suite KPIs in preparation for Power BI data modeling.

---

## 7. Checkpoint 1 Outcome & Submission Summary

* **Stakeholder Alignment:** Executive brief confirmed; client context, stakeholder personas, and operational requirements documented.
* **Analytical Framework:** 5 core analytical questions defined, directly addressing all project acceptance criteria (12 countries, FX impact, client profitability, compliance tracking, C-suite dashboard).
* **Data Packs Inventoried & Validated:** All 3 data packs (`da_b2b_orders.csv`, `da_customer_profiles.csv`, `da_product_catalogue.csv`) fully structured, profiled, and verified with zero orphaned keys.
* **Data Profiling Complete:** Baseline trade KPIs, country distributions, compliance exception frequencies, and financial metrics established.
* **Checkpoint 1 Sign-Off Status:** Complete and ready for Milestone 1 formal sign-off.
