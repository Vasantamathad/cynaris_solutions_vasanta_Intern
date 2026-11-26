"""
Database Loading Module
Loads transformed datasets into the SQLite Star Schema.
"""

import sqlite3
from pipeline.config import DB_FILE, SQL_DIR

COUNTRIES_METADATA = [
    ("United States", "USA", "North America", "USD", 83.50, "Port of Los Angeles"),
    ("United Kingdom", "GBR", "Europe", "GBP", 105.80, "Port of Felixstowe"),
    ("Germany", "DEU", "Europe", "EUR", 90.20, "Port of Hamburg"),
    ("United Arab Emirates", "ARE", "Middle East", "AED", 22.75, "Jebel Ali Port"),
    ("Singapore", "SGP", "Asia-Pacific", "SGD", 62.10, "Port of Singapore"),
    ("Japan", "JPN", "Asia-Pacific", "JPY", 0.55, "Port of Yokohama"),
    ("Australia", "AUS", "Asia-Pacific", "AUD", 54.60, "Port of Melbourne"),
    ("Netherlands", "NLD", "Europe", "EUR", 90.20, "Port of Rotterdam"),
    ("Canada", "CAN", "North America", "CAD", 61.30, "Port of Vancouver"),
    ("France", "FRA", "Europe", "EUR", 90.20, "Port of Le Havre"),
    ("Saudi Arabia", "SAU", "Middle East", "SAR", 22.25, "King Abdulaziz Port (Dammam)"),
    ("South Africa", "ZAF", "Africa", "ZAR", 4.50, "Port of Durban")
]

def load_star_schema(transformed_data):
    print(f"  [LOAD] Connecting to database: {DB_FILE}...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Execute DDL Schema
    schema_sql_path = SQL_DIR / "schema.sql"
    with open(schema_sql_path, "r", encoding="utf-8") as f:
        schema_ddl = f.read()
    cursor.executescript(schema_ddl)
    conn.commit()
    print("    - Star Schema DDL and Analytical Views initialized.")
    
    # 2. Insert Countries Dimension
    cursor.executemany("""
        INSERT INTO dim_countries (country_name, country_code, region, default_currency, base_fx_rate, primary_port)
        VALUES (?, ?, ?, ?, ?, ?)
    """, COUNTRIES_METADATA)
    
    # 3. Insert Customers Dimension
    cursor.executemany("""
        INSERT INTO dim_customers VALUES (
            :customer_id, :company_name, :country, :country_code, :region,
            :settlement_currency, :preferred_port, :client_tier, :payment_terms,
            :credit_limit_usd, :reliability_score_pct, :onboarding_date
        )
    """, transformed_data["customers"])
    
    # 4. Insert Products Dimension
    cursor.executemany("""
        INSERT INTO dim_products VALUES (
            :product_id, :product_name, :category, :hs_code, :unit_cost_inr,
            :base_price_usd, :export_incentive_rate, :requires_special_license,
            :unit_weight_kg
        )
    """, transformed_data["products"])
    
    # 5. Insert Orders Fact Table
    cursor.executemany("""
        INSERT INTO fct_export_orders VALUES (
            :order_id, :order_date, :customer_id, :product_id, :order_quantity,
            :settlement_currency, :unit_price_foreign, :order_value_foreign,
            :booking_fx_rate, :settlement_fx_rate, :order_value_inr_booked,
            :order_value_inr_realized, :fx_gain_loss_inr, :fx_drift_pct,
            :fx_exposure_tier, :shipping_mode, :origin_port, :destination_country,
            :destination_port, :dispatch_date, :target_delivery_date,
            :actual_delivery_date, :target_transit_days, :transit_days,
            :transit_delay_days, :is_delayed, :shipment_status, :compliance_status,
            :compliance_flag_type, :compliance_delay_days, :compliance_risk_level,
            :cogs_inr, :shipping_cost_inr, :customs_handling_inr, :total_cost_inr,
            :gross_profit_inr, :profit_margin_pct, :margin_tier
        )
    """, transformed_data["orders"])
    
    conn.commit()
    
    # Verify counts
    cursor.execute("SELECT count(*) FROM dim_customers")
    c_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM dim_products")
    p_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM dim_countries")
    co_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM fct_export_orders")
    o_cnt = cursor.fetchone()[0]
    
    print(f"    - Loaded dim_countries: {co_cnt} records")
    print(f"    - Loaded dim_customers: {c_cnt} records")
    print(f"    - Loaded dim_products:  {p_cnt} records")
    print(f"    - Loaded fct_export_orders: {o_cnt} records")
    
    return conn
