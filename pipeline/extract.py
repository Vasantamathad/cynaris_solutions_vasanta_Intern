"""
Extraction Module
Reads and validates source CSV datasets.
"""

import csv
import os
from pathlib import Path
from pipeline.config import RAW_ORDERS_FILE, RAW_CUSTOMERS_FILE, RAW_PRODUCTS_FILE

def read_csv_dataset(file_path: Path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found at: {file_path}")
    
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        records = list(reader)
        fieldnames = reader.fieldnames
        
    return records, fieldnames

def extract_all():
    print("  [EXTRACT] Reading raw CSV data packs...")
    customers, cust_fields = read_csv_dataset(RAW_CUSTOMERS_FILE)
    products, prod_fields = read_csv_dataset(RAW_PRODUCTS_FILE)
    orders, order_fields = read_csv_dataset(RAW_ORDERS_FILE)
    
    print(f"    - Customers: {len(customers)} records ({len(cust_fields)} columns)")
    print(f"    - Products:  {len(products)} records ({len(prod_fields)} columns)")
    print(f"    - Orders:    {len(orders)} records ({len(order_fields)} columns)")
    
    return {
        "customers": customers,
        "products": products,
        "orders": orders,
        "fields": {
            "customers": cust_fields,
            "products": prod_fields,
            "orders": order_fields
        }
    }
