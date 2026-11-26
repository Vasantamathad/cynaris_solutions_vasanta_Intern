-- ==============================================================================
-- TRADESIGHT EXPORT ANALYTICS STAR SCHEMA (DDL)
-- Repeatable Data Pipeline Database Architecture
-- ==============================================================================

-- 1. Dimension: Customers
DROP TABLE IF EXISTS dim_customers;
CREATE TABLE dim_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code VARCHAR(10) NOT NULL,
    region VARCHAR(50) NOT NULL,
    settlement_currency VARCHAR(10) NOT NULL,
    preferred_port VARCHAR(150) NOT NULL,
    client_tier VARCHAR(50) NOT NULL,
    payment_terms VARCHAR(50) NOT NULL,
    credit_limit_usd NUMERIC(12, 2) NOT NULL,
    reliability_score_pct NUMERIC(5, 2) NOT NULL,
    onboarding_date DATE NOT NULL
);

-- 2. Dimension: Products
DROP TABLE IF EXISTS dim_products;
CREATE TABLE dim_products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    hs_code VARCHAR(20) NOT NULL,
    unit_cost_inr NUMERIC(12, 2) NOT NULL,
    base_price_usd NUMERIC(12, 2) NOT NULL,
    export_incentive_rate NUMERIC(5, 4) NOT NULL,
    requires_special_license INTEGER NOT NULL,
    unit_weight_kg NUMERIC(8, 2) NOT NULL
);

-- 3. Dimension: Countries & Corridors
DROP TABLE IF EXISTS dim_countries;
CREATE TABLE dim_countries (
    country_name VARCHAR(100) PRIMARY KEY,
    country_code VARCHAR(10) NOT NULL,
    region VARCHAR(50) NOT NULL,
    default_currency VARCHAR(10) NOT NULL,
    base_fx_rate NUMERIC(10, 4) NOT NULL,
    primary_port VARCHAR(150) NOT NULL
);

-- 4. Fact: Export Orders
DROP TABLE IF EXISTS fct_export_orders;
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

-- Performance Indices
CREATE INDEX idx_fct_orders_cust ON fct_export_orders(customer_id);
CREATE INDEX idx_fct_orders_prod ON fct_export_orders(product_id);
CREATE INDEX idx_fct_orders_date ON fct_export_orders(order_date);
CREATE INDEX idx_fct_orders_country ON fct_export_orders(destination_country);
CREATE INDEX idx_fct_orders_status ON fct_export_orders(shipment_status);
CREATE INDEX idx_fct_orders_compliance ON fct_export_orders(compliance_status);

-- 5. Baseline Metrics Aggregation Table
DROP TABLE IF EXISTS agg_baseline_metrics;
CREATE TABLE agg_baseline_metrics (
    metric_id VARCHAR(50) PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    metric_value_num NUMERIC(16, 2),
    metric_value_str VARCHAR(100),
    unit VARCHAR(30),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- ANALYTICAL VIEWS
-- ==============================================================================

-- View 1: C-Suite KPI Rollup
DROP VIEW IF EXISTS vw_c_suite_kpis;
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

-- View 2: Country Performance & FX Risk Summary
DROP VIEW IF EXISTS vw_country_fx_summary;
CREATE VIEW vw_country_fx_summary AS
SELECT 
    f.destination_country,
    c.country_code,
    c.region,
    f.settlement_currency,
    COUNT(f.order_id) AS total_orders,
    ROUND(SUM(f.order_value_inr_realized), 2) AS realized_revenue_inr,
    ROUND(SUM(f.gross_profit_inr), 2) AS total_profit_inr,
    ROUND((SUM(f.gross_profit_inr) / SUM(f.order_value_inr_realized)) * 100, 2) AS gross_margin_pct,
    ROUND(SUM(f.fx_gain_loss_inr), 2) AS net_fx_impact_inr,
    ROUND(AVG(f.fx_drift_pct), 3) AS avg_fx_drift_pct,
    SUM(CASE WHEN f.fx_exposure_tier LIKE 'High%' THEN 1 ELSE 0 END) AS high_fx_volatility_orders
FROM fct_export_orders f
JOIN dim_countries c ON f.destination_country = c.country_name
GROUP BY f.destination_country, c.country_code, c.region, f.settlement_currency
ORDER BY realized_revenue_inr DESC;

-- View 3: Client Profitability Ranking (All 50 Clients)
DROP VIEW IF EXISTS vw_client_profitability_ranked;
CREATE VIEW vw_client_profitability_ranked AS
SELECT 
    c.customer_id,
    c.company_name,
    c.country,
    c.region,
    c.client_tier,
    c.payment_terms,
    COUNT(f.order_id) AS total_orders,
    ROUND(SUM(f.order_value_inr_realized), 2) AS total_revenue_inr,
    ROUND(SUM(f.gross_profit_inr), 2) AS total_profit_inr,
    ROUND((SUM(f.gross_profit_inr) / SUM(f.order_value_inr_realized)) * 100, 2) AS realized_margin_pct,
    ROUND(
        (SUM(CASE WHEN f.shipment_status = 'Delivered On-Time' THEN 1.0 ELSE 0.0 END) / 
         NULLIF(SUM(CASE WHEN f.actual_delivery_date IS NOT NULL THEN 1.0 ELSE 0.0 END), 0)) * 100, 1
    ) AS on_time_delivery_pct,
    SUM(CASE WHEN f.compliance_status = 'Exception Flagged' THEN 1 ELSE 0 END) AS total_exceptions_flagged
FROM fct_export_orders f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.company_name, c.country, c.region, c.client_tier, c.payment_terms
ORDER BY total_profit_inr DESC;

-- View 4: Logistics Route Transit Efficiency
DROP VIEW IF EXISTS vw_route_transit_performance;
CREATE VIEW vw_route_transit_performance AS
SELECT 
    origin_port,
    shipping_mode,
    destination_country,
    COUNT(order_id) AS total_shipments,
    ROUND(AVG(target_transit_days), 1) AS avg_target_transit,
    ROUND(AVG(transit_days), 1) AS avg_actual_transit,
    ROUND(AVG(transit_delay_days), 1) AS avg_delay_days,
    ROUND(
        (SUM(CASE WHEN shipment_status = 'Delivered On-Time' THEN 1.0 ELSE 0.0 END) / 
         NULLIF(SUM(CASE WHEN actual_delivery_date IS NOT NULL THEN 1.0 ELSE 0.0 END), 0)) * 100, 1
    ) AS on_time_rate_pct
FROM fct_export_orders
WHERE actual_delivery_date IS NOT NULL
GROUP BY origin_port, shipping_mode, destination_country
ORDER BY total_shipments DESC;

-- View 5: Compliance Risk & Exception Register
DROP VIEW IF EXISTS vw_compliance_risk_register;
CREATE VIEW vw_compliance_risk_register AS
SELECT 
    compliance_flag_type,
    compliance_risk_level,
    COUNT(order_id) AS flagged_orders,
    ROUND((COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM fct_export_orders)), 2) AS flag_share_pct,
    ROUND(AVG(compliance_delay_days), 1) AS avg_delay_days,
    ROUND(SUM(customs_handling_inr), 2) AS total_customs_costs_inr,
    ROUND(AVG(customs_handling_inr), 2) AS avg_cost_per_shipment_inr
FROM fct_export_orders
GROUP BY compliance_flag_type, compliance_risk_level
ORDER BY flagged_orders DESC;
