"""
Baseline Metrics Calculation & Reporting Engine
Calculates C-Suite KPIs, persists baseline metrics, and exports summary reports.
"""

import json
import sqlite3
from collections import defaultdict
from pipeline.config import METRICS_JSON_REPORT, METRICS_MD_REPORT

def calculate_and_persist_baseline_metrics(conn):
    print("  [METRICS] Calculating and persisting baseline trade metrics...")
    cursor = conn.cursor()
    
    # 1. Query C-Suite Rollup View
    cursor.execute("""
        SELECT 
            total_orders,
            total_revenue_booked_inr,
            total_revenue_realized_inr,
            net_fx_impact_inr,
            total_gross_profit_inr,
            gross_profit_margin_pct,
            on_time_delivery_rate_pct,
            avg_transit_lead_time_days,
            compliance_exception_rate_pct,
            total_active_clients,
            total_destination_countries
        FROM vw_c_suite_kpis;
    """)
    kpi_row = cursor.fetchone()
    
    kpis = {
        "total_orders": kpi_row[0],
        "total_revenue_booked_inr": kpi_row[1],
        "total_revenue_realized_inr": kpi_row[2],
        "net_fx_impact_inr": kpi_row[3],
        "total_gross_profit_inr": kpi_row[4],
        "gross_profit_margin_pct": kpi_row[5],
        "on_time_delivery_rate_pct": kpi_row[6],
        "avg_transit_lead_time_days": kpi_row[7],
        "compliance_exception_rate_pct": kpi_row[8],
        "total_active_clients": kpi_row[9],
        "total_destination_countries": kpi_row[10]
    }
    
    # 2. Persist to agg_baseline_metrics table
    cursor.execute("DELETE FROM agg_baseline_metrics;")
    
    metric_entries = [
        ("REV_REALIZED", "Total Realized Export Revenue", "Financial", kpis["total_revenue_realized_inr"], f"INR {kpis['total_revenue_realized_inr']/10000000:.2f} Cr", "INR"),
        ("REV_BOOKED", "Total Booked Export Revenue", "Financial", kpis["total_revenue_booked_inr"], f"INR {kpis['total_revenue_booked_inr']/10000000:.2f} Cr", "INR"),
        ("GROSS_PROFIT", "Total Realized Gross Profit", "Financial", kpis["total_gross_profit_inr"], f"INR {kpis['total_gross_profit_inr']/10000000:.2f} Cr", "INR"),
        ("GROSS_MARGIN", "Overall Gross Profit Margin", "Financial", kpis["gross_profit_margin_pct"], f"{kpis['gross_profit_margin_pct']}%", "Percentage"),
        ("NET_FX_IMPACT", "Net Realized FX Variance", "FX Analytics", kpis["net_fx_impact_inr"], f"INR {kpis['net_fx_impact_inr']/1000:.2f}k", "INR"),
        ("OTD_RATE", "On-Time Delivery Rate", "Logistics", kpis["on_time_delivery_rate_pct"], f"{kpis['on_time_delivery_rate_pct']}%", "Percentage"),
        ("AVG_TRANSIT_DAYS", "Average Transit Lead Time", "Logistics", kpis["avg_transit_lead_time_days"], f"{kpis['avg_transit_lead_time_days']} Days", "Days"),
        ("COMPLIANCE_RATE", "Compliance Exception Rate", "Compliance", kpis["compliance_exception_rate_pct"], f"{kpis['compliance_exception_rate_pct']}%", "Percentage"),
        ("CLIENT_COUNT", "Total Active B2B Clients", "Demographics", kpis["total_active_clients"], str(kpis["total_active_clients"]), "Clients"),
        ("COUNTRY_COUNT", "Destination Markets Covered", "Demographics", kpis["total_destination_countries"], str(kpis["total_destination_countries"]), "Countries")
    ]
    
    cursor.executemany("""
        INSERT INTO agg_baseline_metrics (metric_id, metric_name, category, metric_value_num, metric_value_str, unit)
        VALUES (?, ?, ?, ?, ?, ?)
    """, metric_entries)
    conn.commit()
    
    # 3. Country Performance Summary
    cursor.execute("""
        SELECT 
            destination_country, country_code, region, settlement_currency,
            total_orders, realized_revenue_inr, total_profit_inr,
            gross_margin_pct, net_fx_impact_inr, avg_fx_drift_pct
        FROM vw_country_fx_summary;
    """)
    country_rows = cursor.fetchall()
    countries_data = []
    for r in country_rows:
        countries_data.append({
            "country": r[0],
            "code": r[1],
            "region": r[2],
            "currency": r[3],
            "orders": r[4],
            "realized_revenue_inr": r[5],
            "gross_profit_inr": r[6],
            "margin_pct": r[7],
            "fx_impact_inr": r[8],
            "avg_fx_drift_pct": r[9]
        })

    # 4. Top 5 & Bottom 5 Clients
    cursor.execute("""
        SELECT customer_id, company_name, country, client_tier, total_orders, total_revenue_inr, total_profit_inr, realized_margin_pct
        FROM vw_client_profitability_ranked
        LIMIT 5;
    """)
    top_clients = [{"cid": r[0], "name": r[1], "country": r[2], "tier": r[3], "orders": r[4], "revenue": r[5], "profit": r[6], "margin": r[7]} for r in cursor.fetchall()]

    cursor.execute("""
        SELECT customer_id, company_name, country, client_tier, total_orders, total_revenue_inr, total_profit_inr, realized_margin_pct
        FROM vw_client_profitability_ranked
        ORDER BY total_profit_inr ASC
        LIMIT 5;
    """)
    bottom_clients = [{"cid": r[0], "name": r[1], "country": r[2], "tier": r[3], "orders": r[4], "revenue": r[5], "profit": r[6], "margin": r[7]} for r in cursor.fetchall()]

    # 5. Export JSON Report
    report_payload = {
        "executive_kpis": kpis,
        "countries_summary": countries_data,
        "top_5_clients": top_clients,
        "bottom_5_clients": bottom_clients
    }
    
    with open(METRICS_JSON_REPORT, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)
        
    # 6. Export Markdown Summary
    md_content = f"""# TradeSight Export Analytics - Baseline Metrics Report
**Generated by Automated Repeatable Data Pipeline**

## 1. Executive C-Suite KPIs
* **Total Export Orders:** {kpis['total_orders']:,} shipments
* **Total Realized Revenue:** ₹{kpis['total_revenue_realized_inr']:,.2f} (₹{kpis['total_revenue_realized_inr']/10000000:.2f} Cr)
* **Total Realized Gross Profit:** ₹{kpis['total_gross_profit_inr']:,.2f} (₹{kpis['total_gross_profit_inr']/10000000:.2f} Cr)
* **Overall Gross Profit Margin:** {kpis['gross_profit_margin_pct']}%
* **Net Realized FX Impact:** ₹{kpis['net_fx_impact_inr']:,.2f}
* **On-Time Delivery Rate (OTD%):** {kpis['on_time_delivery_rate_pct']}%
* **Average Transit Lead Time:** {kpis['avg_transit_lead_time_days']} Days
* **Compliance Exception Rate:** {kpis['compliance_exception_rate_pct']}%
* **Active B2B Clients:** {kpis['total_active_clients']} across {kpis['total_destination_countries']} Countries

## 2. 12-Country Performance Table
| Country | Currency | Orders | Realized Revenue (INR) | Gross Profit (INR) | Margin % | Net FX Drift (INR) |
|---|:---:|:---:|---:|---:|:---:|---:|
"""
    for c in countries_data:
        md_content += f"| **{c['country']}** | {c['currency']} | {c['orders']} | ₹{c['realized_revenue_inr']/1000000:.2f}M | ₹{c['gross_profit_inr']/1000000:.2f}M | {c['margin_pct']:.2f}% | ₹{c['fx_impact_inr']/1000:+.2f}k |\n"
        
    md_content += """
## 3. Top 5 Most Profitable Clients
| Client Name | Country | Tier | Orders | Realized Revenue | Gross Profit | Margin % |
|---|---|---|:---:|---:|---:|:---:|
"""
    for cl in top_clients:
        md_content += f"| **{cl['name']}** | {cl['country']} | {cl['tier'].split(' - ')[1]} | {cl['orders']} | ₹{cl['revenue']/1000000:.2f}M | ₹{cl['profit']/1000000:.2f}M | {cl['margin']:.2f}% |\n"

    with open(METRICS_MD_REPORT, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"    - Baseline metrics persisted to table: agg_baseline_metrics")
    print(f"    - Reports generated: {METRICS_JSON_REPORT.name}, {METRICS_MD_REPORT.name}")
    
    return report_payload
