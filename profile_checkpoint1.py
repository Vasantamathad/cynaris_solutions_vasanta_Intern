"""
TradeSight Export Analytics - Checkpoint 1 Data Profiler & SQLite Ingestion
Cynaris Solutions Learning Path | Capstone Project
"""

import csv
import json
import sqlite3
import os
from collections import Counter, defaultdict

DB_FILE = "tradesight.db"
CUSTOMER_CSV = "da_customer_profiles.csv"
PRODUCT_CSV = "da_product_catalogue.csv"
ORDERS_CSV = "da_b2b_orders.csv"
SQL_FILE = "schema_and_queries.sql"

def load_csv_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames

def build_sqlite_db():
    print(f"[1/4] Building SQLite Database: {DB_FILE}...")
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Read schema
    with open(SQL_FILE, "r", encoding="utf-8") as f:
        full_sql = f.read()
        
    # Split DDL from queries (up to first analytical query)
    ddl_part = full_sql.split("-- ANALYTICAL QUERIES")[0]
    cursor.executescript(ddl_part)
    conn.commit()
    
    # Insert Customers
    cust_rows, _ = load_csv_data(CUSTOMER_CSV)
    cursor.executemany("""
        INSERT INTO customer_profiles VALUES (
            :customer_id, :company_name, :country, :country_code, :region,
            :settlement_currency, :preferred_port, :client_tier, :payment_terms,
            :credit_limit_usd, :reliability_score_pct, :onboarding_date
        )
    """, cust_rows)
    
    # Insert Products
    prod_rows, _ = load_csv_data(PRODUCT_CSV)
    cursor.executemany("""
        INSERT INTO product_catalogue VALUES (
            :product_id, :product_name, :category, :hs_code, :unit_cost_inr,
            :base_price_usd, :export_incentive_rate, :requires_special_license,
            :unit_weight_kg
        )
    """, prod_rows)
    
    # Insert Orders
    order_rows, _ = load_csv_data(ORDERS_CSV)
    # Handle empty transit_days and actual_delivery_date
    cleaned_orders = []
    for o in order_rows:
        row = dict(o)
        if not row["transit_days"]:
            row["transit_days"] = None
        if not row["actual_delivery_date"]:
            row["actual_delivery_date"] = None
        cleaned_orders.append(row)
        
    cursor.executemany("""
        INSERT INTO b2b_orders VALUES (
            :order_id, :order_date, :customer_id, :product_id, :order_quantity,
            :settlement_currency, :unit_price_foreign, :order_value_foreign,
            :booking_fx_rate, :settlement_fx_rate, :order_value_inr_booked,
            :order_value_inr_realized, :fx_gain_loss_inr, :shipping_mode,
            :origin_port, :destination_country, :destination_port, :dispatch_date,
            :target_delivery_date, :actual_delivery_date, :transit_days,
            :shipment_status, :compliance_status, :compliance_flag_type,
            :compliance_delay_days, :cogs_inr, :shipping_cost_inr,
            :customs_handling_inr, :total_cost_inr, :gross_profit_inr,
            :profit_margin_pct
        )
    """, cleaned_orders)
    
    conn.commit()
    print(f"      Loaded {len(cust_rows)} customers, {len(prod_rows)} products, {len(order_rows)} orders.")
    return conn

def run_analytical_queries(conn):
    print("[2/4] Executing Checkpoint 1 Analytical Queries...")
    cursor = conn.cursor()
    
    # Q1: Category performance
    print("\n--- Question 1: Sales & Margin by Product Category ---")
    cursor.execute("""
        SELECT 
            p.category,
            COUNT(o.order_id) AS orders,
            ROUND(SUM(o.order_value_inr_realized) / 1000000.0, 2) AS rev_m_inr,
            ROUND(SUM(o.gross_profit_inr) / 1000000.0, 2) AS profit_m_inr,
            ROUND(AVG(o.profit_margin_pct), 2) AS margin_pct
        FROM b2b_orders o
        JOIN product_catalogue p ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY rev_m_inr DESC;
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:<24} | Orders: {row[1]:<4} | Rev: ₹{row[2]:>7.2f}M | Profit: ₹{row[3]:>6.2f}M | Margin: {row[4]:>5.2f}%")
        
    # Q2: FX Impact across 12 countries
    print("\n--- Question 2: FX Impact Across 12 Destination Countries ---")
    cursor.execute("""
        SELECT 
            destination_country,
            settlement_currency,
            COUNT(order_id) AS orders,
            ROUND(SUM(order_value_inr_realized) / 1000000.0, 2) AS rev_m,
            ROUND(SUM(fx_gain_loss_inr) / 1000.0, 2) AS net_fx_k_inr
        FROM b2b_orders
        GROUP BY destination_country, settlement_currency
        ORDER BY net_fx_k_inr ASC;
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:<22} ({row[1]}) | Orders: {row[2]:<4} | Rev: ₹{row[3]:>6.2f}M | Net FX: ₹{row[4]:>8.2f}k")
        
    # Q4: Transit performance
    print("\n--- Question 4: Transit Performance by Origin Port & Mode ---")
    cursor.execute("""
        SELECT 
            origin_port,
            shipping_mode,
            COUNT(order_id) AS shipments,
            ROUND(AVG(transit_days), 1) AS avg_transit,
            ROUND(SUM(CASE WHEN shipment_status = 'Delivered On-Time' THEN 1.0 ELSE 0.0 END) * 100.0 / 
                  NULLIF(SUM(CASE WHEN actual_delivery_date IS NOT NULL THEN 1.0 ELSE 0.0 END), 0), 2) AS otd_pct
        FROM b2b_orders
        GROUP BY origin_port, shipping_mode;
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:<25} | {row[1]:<10} | Shipments: {row[2]:<4} | Avg Transit: {row[3]:>4.1f}d | OTD%: {row[4]:>5.2f}%")

    # Q5: Compliance flags
    print("\n--- Question 5: Compliance Exception Flags Breakdown ---")
    cursor.execute("""
        SELECT 
            compliance_flag_type,
            COUNT(order_id) AS cnt,
            ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM b2b_orders), 2) AS pct,
            ROUND(AVG(compliance_delay_days), 1) AS avg_delay
        FROM b2b_orders
        GROUP BY compliance_flag_type
        ORDER BY cnt DESC;
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:<45} | Count: {row[1]:<4} ({row[2]:>5.2f}%) | Avg Delay: {row[3]:>4.1f}d")

    # Executive Roll-Up
    print("\n--- C-Suite Executive KPI Roll-Up ---")
    cursor.execute("""
        SELECT 
            COUNT(order_id),
            ROUND(SUM(order_value_inr_realized) / 1000000.0, 2),
            ROUND(SUM(gross_profit_inr) / 1000000.0, 2),
            ROUND((SUM(gross_profit_inr) / SUM(order_value_inr_realized)) * 100, 2),
            ROUND(SUM(fx_gain_loss_inr) / 1000.0, 2),
            ROUND(
                (SUM(CASE WHEN shipment_status = 'Delivered On-Time' THEN 1.0 ELSE 0.0 END) / 
                 NULLIF(SUM(CASE WHEN actual_delivery_date IS NOT NULL THEN 1.0 ELSE 0.0 END), 0)) * 100, 2
            ),
            ROUND(
                (SUM(CASE WHEN compliance_status = 'Exception Flagged' THEN 1.0 ELSE 0.0 END) / COUNT(order_id)) * 100, 2
            ),
            ROUND(AVG(transit_days), 1)
        FROM b2b_orders;
    """)
    kpi = cursor.fetchone()
    print(f"  Total Orders:              {kpi[0]}")
    print(f"  Total Realized Revenue:    ₹{kpi[1]} Million (₹{kpi[1]/10:.2f} Cr)")
    print(f"  Total Gross Profit:        ₹{kpi[2]} Million (₹{kpi[2]/10:.2f} Cr)")
    print(f"  Gross Profit Margin:       {kpi[3]}%")
    print(f"  Net FX Impact:             ₹{kpi[4]} Thousand")
    print(f"  On-Time Delivery Rate:     {kpi[5]}%")
    print(f"  Compliance Exception Rate: {kpi[6]}%")
    print(f"  Average Transit Days:      {kpi[7]} days")

def main():
    print("="*75)
    print("TRADESIGHT EXPORT ANALYTICS - CHECKPOINT 1 DATA PROFILING")
    print("Cynaris Solutions Learning Path | Capstone Project")
    print("="*75)
    
    conn = build_sqlite_db()
    run_analytical_queries(conn)
    conn.close()
    
    print("\n[3/4] Checkpoint 1 verification completed successfully.")
    print("[4/4] Output database ready at: tradesight.db")

if __name__ == "__main__":
    main()
