"""
Transformation & Feature Engineering Module
Standardizes formats, enriches records with trade metrics, and generates derived features.
"""

import csv
import datetime
from pathlib import Path
from pipeline.config import (
    CLEANED_ORDERS_FILE, CLEANED_CUSTOMERS_FILE, CLEANED_PRODUCTS_FILE,
    ensure_directories
)

def parse_date(d_str):
    if not d_str or not d_str.strip():
        return None
    try:
        return datetime.datetime.strptime(d_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None

def transform_customers(raw_customers):
    cleaned = []
    for c in raw_customers:
        rec = dict(c)
        rec["credit_limit_usd"] = float(rec["credit_limit_usd"])
        rec["reliability_score_pct"] = float(rec["reliability_score_pct"])
        cleaned.append(rec)
    return cleaned

def transform_products(raw_products):
    cleaned = []
    for p in raw_products:
        rec = dict(p)
        rec["unit_cost_inr"] = float(rec["unit_cost_inr"])
        rec["base_price_usd"] = float(rec["base_price_usd"])
        rec["export_incentive_rate"] = float(rec["export_incentive_rate"])
        rec["requires_special_license"] = 1 if str(rec["requires_special_license"]).lower() in ["true", "1"] else 0
        rec["unit_weight_kg"] = float(rec["unit_weight_kg"])
        cleaned.append(rec)
    return cleaned

def transform_orders(raw_orders, customers_dict, products_dict):
    cleaned = []
    
    for o in raw_orders:
        rec = dict(o)
        
        # Numeric conversions
        qty = int(rec["order_quantity"])
        rec["order_quantity"] = qty
        unit_price = float(rec["unit_price_foreign"])
        rec["unit_price_foreign"] = unit_price
        order_val_foreign = float(rec["order_value_foreign"])
        rec["order_value_foreign"] = order_val_foreign
        
        booking_fx = float(rec["booking_fx_rate"])
        rec["booking_fx_rate"] = booking_fx
        settlement_fx = float(rec["settlement_fx_rate"])
        rec["settlement_fx_rate"] = settlement_fx
        
        order_val_booked = float(rec["order_value_inr_booked"])
        rec["order_value_inr_booked"] = order_val_booked
        order_val_realized = float(rec["order_value_inr_realized"])
        rec["order_value_inr_realized"] = order_val_realized
        fx_gain_loss = float(rec["fx_gain_loss_inr"])
        rec["fx_gain_loss_inr"] = fx_gain_loss
        
        # FX Drift percentage & exposure tier
        fx_drift = round(((settlement_fx - booking_fx) / booking_fx) * 100, 3)
        rec["fx_drift_pct"] = fx_drift
        abs_drift = abs(fx_drift)
        if abs_drift > 3.0:
            rec["fx_exposure_tier"] = "High Volatility (>3%)"
        elif abs_drift >= 1.0:
            rec["fx_exposure_tier"] = "Moderate Volatility (1-3%)"
        else:
            rec["fx_exposure_tier"] = "Stable (<1%)"
            
        # Costs and margins
        cogs = float(rec["cogs_inr"])
        shipping_cost = float(rec["shipping_cost_inr"])
        customs_cost = float(rec["customs_handling_inr"])
        total_cost = float(rec["total_cost_inr"])
        gross_profit = float(rec["gross_profit_inr"])
        margin_pct = float(rec["profit_margin_pct"])
        
        rec["cogs_inr"] = cogs
        rec["shipping_cost_inr"] = shipping_cost
        rec["customs_handling_inr"] = customs_cost
        rec["total_cost_inr"] = total_cost
        rec["gross_profit_inr"] = gross_profit
        rec["profit_margin_pct"] = margin_pct
        
        if margin_pct >= 30.0:
            rec["margin_tier"] = "High Margin (>=30%)"
        elif margin_pct >= 25.0:
            rec["margin_tier"] = "Standard Margin (25-30%)"
        elif margin_pct >= 20.0:
            rec["margin_tier"] = "Low Margin (20-25%)"
        else:
            rec["margin_tier"] = "Compressed Margin (<20%)"
            
        # Delivery & Transit dates
        dispatch = parse_date(rec["dispatch_date"])
        target_del = parse_date(rec["target_delivery_date"])
        actual_del = parse_date(rec["actual_delivery_date"])
        
        if dispatch and target_del:
            target_transit = (target_del - dispatch).days
        else:
            target_transit = None
        rec["target_transit_days"] = target_transit
        
        transit_days_raw = rec.get("transit_days", "").strip()
        if transit_days_raw:
            actual_transit = int(transit_days_raw)
            rec["transit_days"] = actual_transit
            rec["transit_delay_days"] = actual_transit - (target_transit if target_transit is not None else actual_transit)
            rec["is_delayed"] = 1 if rec["transit_delay_days"] > 0 else 0
        else:
            rec["transit_days"] = None
            rec["transit_delay_days"] = None
            rec["is_delayed"] = None
            
        # Compliance Risk Level
        flag_type = rec["compliance_flag_type"]
        rec["compliance_delay_days"] = int(rec["compliance_delay_days"])
        if flag_type in ["Customs Inspection Hold", "Country Sanctions Screening"]:
            rec["compliance_risk_level"] = "Critical"
        elif flag_type in ["Documentation Incomplete", "HS Code Discrepancy", "Fumigation / Phytosanitary Certificate Delay"]:
            rec["compliance_risk_level"] = "Moderate"
        elif flag_type in ["Tariff Rate Query"]:
            rec["compliance_risk_level"] = "Low"
        else:
            rec["compliance_risk_level"] = "None"
            
        cleaned.append(rec)
        
    return cleaned

def transform_and_save_all(extracted_data):
    ensure_directories()
    print("  [TRANSFORM] Executing data cleaning and feature engineering...")
    
    customers_dict = {c["customer_id"]: c for c in extracted_data["customers"]}
    products_dict = {p["product_id"]: p for p in extracted_data["products"]}
    
    cleaned_customers = transform_customers(extracted_data["customers"])
    cleaned_products = transform_products(extracted_data["products"])
    cleaned_orders = transform_orders(extracted_data["orders"], customers_dict, products_dict)
    
    # Save processed files
    with open(CLEANED_CUSTOMERS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(cleaned_customers[0].keys()))
        writer.writeheader()
        writer.writerows(cleaned_customers)
        
    with open(CLEANED_PRODUCTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(cleaned_products[0].keys()))
        writer.writeheader()
        writer.writerows(cleaned_products)
        
    with open(CLEANED_ORDERS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(cleaned_orders[0].keys()))
        writer.writeheader()
        writer.writerows(cleaned_orders)
        
    print(f"    - Cleaned orders enriched: {len(cleaned_orders)} records ({len(cleaned_orders[0])} features)")
    print(f"    - Cleaned datasets saved to: {CLEANED_ORDERS_FILE.parent}")
    
    return {
        "customers": cleaned_customers,
        "products": cleaned_products,
        "orders": cleaned_orders
    }
