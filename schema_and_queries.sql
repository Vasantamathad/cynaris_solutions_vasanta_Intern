-- ==============================================================================
-- TRADESIGHT EXPORT ANALYTICS PLATFORM
-- Checkpoint 1 | Week 1: Relational Schema DDL & Analytical SQL Queries
-- Cynaris Solutions Learning Path | Capstone Project
-- ==============================================================================

-- Drop tables if already exist
DROP TABLE IF EXISTS b2b_orders;
DROP TABLE IF EXISTS customer_profiles;
DROP TABLE IF EXISTS product_catalogue;

-- ------------------------------------------------------------------------------
-- 1. Table DDL: Customer Profiles Dimension
-- ------------------------------------------------------------------------------
CREATE TABLE customer_profiles (
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

-- ------------------------------------------------------------------------------
-- 2. Table DDL: Product Catalogue Dimension
-- ------------------------------------------------------------------------------
CREATE TABLE product_catalogue (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    hs_code VARCHAR(20) NOT NULL,
    unit_cost_inr NUMERIC(12, 2) NOT NULL,
    base_price_usd NUMERIC(12, 2) NOT NULL,
    export_incentive_rate NUMERIC(5, 4) NOT NULL,
    requires_special_license BOOLEAN NOT NULL,
    unit_weight_kg NUMERIC(8, 2) NOT NULL
);

-- ------------------------------------------------------------------------------
-- 3. Table DDL: B2B Export Orders Fact Table
-- ------------------------------------------------------------------------------
CREATE TABLE b2b_orders (
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
    shipping_mode VARCHAR(30) NOT NULL,
    origin_port VARCHAR(100) NOT NULL,
    destination_country VARCHAR(100) NOT NULL,
    destination_port VARCHAR(150) NOT NULL,
    dispatch_date DATE NOT NULL,
    target_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    transit_days INTEGER,
    shipment_status VARCHAR(50) NOT NULL,
    compliance_status VARCHAR(50) NOT NULL,
    compliance_flag_type VARCHAR(100) NOT NULL,
    compliance_delay_days INTEGER NOT NULL,
    cogs_inr NUMERIC(14, 2) NOT NULL,
    shipping_cost_inr NUMERIC(14, 2) NOT NULL,
    customs_handling_inr NUMERIC(14, 2) NOT NULL,
    total_cost_inr NUMERIC(14, 2) NOT NULL,
    gross_profit_inr NUMERIC(14, 2) NOT NULL,
    profit_margin_pct NUMERIC(6, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer_profiles(customer_id),
    FOREIGN KEY (product_id) REFERENCES product_catalogue(product_id)
);

-- Indices for performance optimization
CREATE INDEX idx_orders_cust ON b2b_orders(customer_id);
CREATE INDEX idx_orders_prod ON b2b_orders(product_id);
CREATE INDEX idx_orders_date ON b2b_orders(order_date);
CREATE INDEX idx_orders_country ON b2b_orders(destination_country);
CREATE INDEX idx_orders_compliance ON b2b_orders(compliance_status);

-- ==============================================================================
-- ANALYTICAL QUERIES ANSWERING THE FIVE CHECKPOINT 1 QUESTIONS
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Question 1: Overall Sales Results & Product Category Performance
-- ------------------------------------------------------------------------------
SELECT 
    p.category,
    COUNT(o.order_id) AS total_orders,
    SUM(o.order_quantity) AS total_units_sold,
    ROUND(SUM(o.order_value_inr_realized), 2) AS total_revenue_realized_inr,
    ROUND(SUM(o.gross_profit_inr), 2) AS total_gross_profit_inr,
    ROUND(AVG(o.profit_margin_pct), 2) AS avg_margin_pct,
    ROUND(AVG(o.order_value_inr_realized), 2) AS avg_order_value_inr
FROM b2b_orders o
JOIN product_catalogue p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue_realized_inr DESC;

-- ------------------------------------------------------------------------------
-- Question 2: Foreign Exchange (FX) Currency Impact Across 12 Countries
-- ------------------------------------------------------------------------------
SELECT 
    destination_country,
    settlement_currency,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_value_inr_booked), 2) AS booked_revenue_inr,
    ROUND(SUM(order_value_inr_realized), 2) AS realized_revenue_inr,
    ROUND(SUM(fx_gain_loss_inr), 2) AS net_fx_gain_loss_inr,
    ROUND((SUM(fx_gain_loss_inr) / SUM(order_value_inr_booked)) * 100, 2) AS fx_drift_pct,
    CASE 
        WHEN SUM(fx_gain_loss_inr) >= 0 THEN 'FX Windfall / Gain'
        ELSE 'FX Margin Erosion'
    END AS fx_impact_category
FROM b2b_orders
GROUP BY destination_country, settlement_currency
ORDER BY net_fx_gain_loss_inr ASC;

-- ------------------------------------------------------------------------------
-- Question 3: B2B Client Profitability Ranking (Top 10 vs Bottom 10)
-- ------------------------------------------------------------------------------
-- Top 10 Most Profitable Clients:
SELECT 
    c.customer_id,
    c.company_name,
    c.country,
    c.client_tier,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.order_value_inr_realized), 2) AS total_revenue_inr,
    ROUND(SUM(o.gross_profit_inr), 2) AS total_profit_inr,
    ROUND((SUM(o.gross_profit_inr) / SUM(o.order_value_inr_realized)) * 100, 2) AS realized_margin_pct
FROM b2b_orders o
JOIN customer_profiles c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.company_name, c.country, c.client_tier
ORDER BY total_profit_inr DESC
LIMIT 10;

-- ------------------------------------------------------------------------------
-- Question 4: Shipment Transit Performance & Delays by Port & Mode
-- ------------------------------------------------------------------------------
SELECT 
    origin_port,
    shipping_mode,
    COUNT(order_id) AS total_shipments,
    ROUND(AVG(CASE WHEN transit_days IS NOT NULL THEN transit_days END), 1) AS avg_transit_days,
    SUM(CASE WHEN shipment_status = 'Delivered On-Time' THEN 1 ELSE 0 END) AS on_time_deliveries,
    SUM(CASE WHEN shipment_status = 'Delivered Late' THEN 1 ELSE 0 END) AS late_deliveries,
    SUM(CASE WHEN shipment_status LIKE '%Customs Hold%' THEN 1 ELSE 0 END) AS customs_delayed,
    ROUND(
        (SUM(CASE WHEN shipment_status = 'Delivered On-Time' THEN 1.0 ELSE 0.0 END) / 
         NULLIF(SUM(CASE WHEN actual_delivery_date IS NOT NULL THEN 1.0 ELSE 0.0 END), 0)) * 100, 
        2
    ) AS on_time_delivery_rate_pct
FROM b2b_orders
GROUP BY origin_port, shipping_mode
ORDER BY total_shipments DESC;

-- ------------------------------------------------------------------------------
-- Question 5: Compliance Exception Flags & Operational Cost Impact
-- ------------------------------------------------------------------------------
SELECT 
    compliance_flag_type,
    COUNT(order_id) AS flag_count,
    ROUND((COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM b2b_orders)), 2) AS flag_share_pct,
    ROUND(AVG(compliance_delay_days), 1) AS avg_delay_days,
    ROUND(SUM(customs_handling_inr), 2) AS total_customs_handling_cost_inr,
    ROUND(AVG(customs_handling_inr), 2) AS avg_customs_handling_cost_inr
FROM b2b_orders
GROUP BY compliance_flag_type
ORDER BY flag_count DESC;

-- ==============================================================================
-- C-SUITE EXECUTIVE KPI ROLL-UP VIEW
-- ==============================================================================
CREATE VIEW IF NOT EXISTS c_suite_kpi_summary AS
SELECT 
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_value_inr_booked), 2) AS total_revenue_booked_inr,
    ROUND(SUM(order_value_inr_realized), 2) AS total_revenue_realized_inr,
    ROUND(SUM(fx_gain_loss_inr), 2) AS net_fx_impact_inr,
    ROUND(SUM(gross_profit_inr), 2) AS total_gross_profit_inr,
    ROUND((SUM(gross_profit_inr) / SUM(order_value_inr_realized)) * 100, 2) AS overall_gross_margin_pct,
    ROUND(
        (SUM(CASE WHEN shipment_status = 'Delivered On-Time' THEN 1.0 ELSE 0.0 END) / 
         NULLIF(SUM(CASE WHEN actual_delivery_date IS NOT NULL THEN 1.0 ELSE 0.0 END), 0)) * 100, 
        2
    ) AS on_time_delivery_rate_pct,
    ROUND(
        (SUM(CASE WHEN compliance_status = 'Exception Flagged' THEN 1.0 ELSE 0.0 END) / COUNT(order_id)) * 100, 
        2
    ) AS compliance_exception_rate_pct,
    ROUND(AVG(CASE WHEN transit_days IS NOT NULL THEN transit_days END), 1) AS avg_transit_days
FROM b2b_orders;
