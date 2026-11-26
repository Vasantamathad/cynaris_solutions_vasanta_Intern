"""
=============================================================================
TradeSight Export Analytics - Analysis & Baseline Metrics Script
Cynaris Solutions Learning Path | Capstone Project (Data Analyst Intern)
=============================================================================

This script performs exploratory and baseline statistical analysis on the 
data warehouse (tradesight.db), generating structured tables for C-Suite KPIs.
"""

import sqlite3
import os
import csv

DB_PATH = "tradesight.db"

def run_analysis():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database {DB_PATH} not found. Please run python pipeline.py first.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("=" * 85)
    print("         TRADESIGHT EXPORT ANALYTICS: BASELINE TRADE ANALYSIS SCRIPT         ")
    print("=" * 85)

    # 1. Product Category Analysis
    print("\n--- 1. Product Category Commercial Performance ---")
    cur.execute("""
        SELECT 
            p.category,
            COUNT(o.order_id) AS orders,
            SUM(o.order_quantity) AS units,
            ROUND(SUM(o.order_value_inr_realized), 2) AS rev_inr,
            ROUND(SUM(o.gross_profit_inr), 2) AS profit_inr,
            ROUND(AVG(o.profit_margin_pct), 2) AS margin_pct
        FROM fct_export_orders o
        JOIN dim_products p ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY rev_inr DESC;
    """)
    cat_rows = cur.fetchall()
    print(f"{'Category':<24} | {'Orders':<6} | {'Units':<8} | {'Revenue (INR)':<16} | {'Profit (INR)':<14} | {'Margin%':<7}")
    print("-" * 85)
    for r in cat_rows:
        print(f"{r[0]:<24} | {r[1]:<6} | {r[2]:<8} | INR {r[3]:>12,.2f} | INR {r[4]:>10,.2f} | {r[5]:>6.2f}%")

    # 2. 12 Destination Countries & FX Impact
    print("\n--- 2. Destination Country Performance & Currency (FX) Impact ---")
    cur.execute("""
        SELECT 
            destination_country,
            settlement_currency,
            COUNT(order_id) AS orders,
            ROUND(SUM(order_value_inr_realized), 2) AS rev_inr,
            ROUND(SUM(gross_profit_inr), 2) AS profit_inr,
            ROUND((SUM(gross_profit_inr) / SUM(order_value_inr_realized)) * 100, 2) AS margin_pct,
            ROUND(SUM(fx_gain_loss_inr), 2) AS net_fx_inr,
            ROUND(AVG(fx_drift_pct), 3) AS avg_drift_pct
        FROM fct_export_orders
        GROUP BY destination_country, settlement_currency
        ORDER BY rev_inr DESC;
    """)
    country_rows = cur.fetchall()
    print(f"{'Destination Country':<22} | {'Cur':<4} | {'Orders':<6} | {'Revenue (INR)':<16} | {'Profit (INR)':<14} | {'Margin%':<7} | {'Net FX Drift (INR)':<18}")
    print("-" * 100)
    for r in country_rows:
        print(f"{r[0]:<22} | {r[1]:<4} | {r[2]:<6} | INR {r[3]:>12,.2f} | INR {r[4]:>10,.2f} | {r[5]:>6.2f}% | INR {r[6]:>14,.2f}")

    # 3. Top 10 B2B Clients by Profitability
    print("\n--- 3. Client Profitability Ranking (Top 10 High-Value Partners) ---")
    cur.execute("""
        SELECT 
            c.customer_id,
            c.company_name,
            c.country,
            c.client_tier,
            COUNT(o.order_id) AS orders,
            ROUND(SUM(o.order_value_inr_realized), 2) AS rev_inr,
            ROUND(SUM(o.gross_profit_inr), 2) AS profit_inr,
            ROUND((SUM(o.gross_profit_inr) / SUM(o.order_value_inr_realized)) * 100, 2) AS margin_pct
        FROM fct_export_orders o
        JOIN dim_customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.company_name, c.country, c.client_tier
        ORDER BY profit_inr DESC
        LIMIT 10;
    """)
    client_rows = cur.fetchall()
    print(f"{'Rank':<4} | {'Client Company Name':<28} | {'Country':<15} | {'Tier':<12} | {'Orders':<6} | {'Profit (INR)':<14} | {'Margin%':<7}")
    print("-" * 100)
    for i, r in enumerate(client_rows, 1):
        tier = r[3].split(" - ")[1] if " - " in r[3] else r[3]
        print(f"#{i:<3} | {r[1]:<28} | {r[2]:<15} | {tier:<12} | {r[4]:<6} | INR {r[6]:>10,.2f} | {r[7]:>6.2f}%")

    # 4. Logistics Transit Performance by Mode & Port
    print("\n--- 4. Port Logistics Transit Efficiency (Air vs Sea) ---")
    cur.execute("""
        SELECT 
            origin_port,
            shipping_mode,
            COUNT(order_id) AS shipments,
            ROUND(AVG(target_transit_days), 1) AS avg_target,
            ROUND(AVG(transit_days), 1) AS avg_actual,
            ROUND(
                (SUM(CASE WHEN shipment_status = 'Delivered On-Time' THEN 1.0 ELSE 0.0 END) / 
                 NULLIF(SUM(CASE WHEN actual_delivery_date IS NOT NULL THEN 1.0 ELSE 0.0 END), 0)) * 100, 2
            ) AS otd_pct
        FROM fct_export_orders
        WHERE actual_delivery_date IS NOT NULL
        GROUP BY origin_port, shipping_mode;
    """)
    transit_rows = cur.fetchall()
    print(f"{'Origin Port':<24} | {'Mode':<10} | {'Shipments':<9} | {'Target':<7} | {'Actual':<7} | {'OTD%':<7}")
    print("-" * 75)
    for r in transit_rows:
        print(f"{r[0]:<24} | {r[1]:<10} | {r[2]:<9} | {r[3]:>5.1f}d | {r[4]:>5.1f}d | {r[5]:>5.2f}%")

    # 5. Compliance Exception Register
    print("\n--- 5. Export Compliance Exception Risk Register ---")
    cur.execute("""
        SELECT 
            compliance_flag_type,
            compliance_risk_level,
            COUNT(order_id) AS cnt,
            ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM fct_export_orders), 2) AS pct,
            ROUND(AVG(compliance_delay_days), 1) AS avg_delay,
            ROUND(SUM(customs_handling_inr), 2) AS extra_cost_inr
        FROM fct_export_orders
        GROUP BY compliance_flag_type, compliance_risk_level
        ORDER BY cnt DESC;
    """)
    flag_rows = cur.fetchall()
    print(f"{'Flag Category':<45} | {'Risk':<10} | {'Count':<5} | {'Share%':<6} | {'Avg Delay':<9} | {'Customs Cost (INR)':<18}")
    print("-" * 105)
    for r in flag_rows:
        print(f"{r[0]:<45} | {r[1]:<10} | {r[2]:<5} | {r[3]:>5.2f}% | {r[4]:>5.1f}d | INR {r[5]:>14,.2f}")

    conn.close()
    print("=" * 85)
    print("Analysis script completed successfully.")

if __name__ == "__main__":
    run_analysis()
