"""
TradeSight Export Analytics - Pipeline Configuration
Cynaris Solutions Learning Path | Capstone Project
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = BASE_DIR / "reports"
SQL_DIR = BASE_DIR / "sql"

# Database
DB_FILE = BASE_DIR / "tradesight.db"

# Raw Source Files
RAW_ORDERS_FILE = BASE_DIR / "da_b2b_orders.csv"
RAW_CUSTOMERS_FILE = BASE_DIR / "da_customer_profiles.csv"
RAW_PRODUCTS_FILE = BASE_DIR / "da_product_catalogue.csv"

# Processed Files
CLEANED_ORDERS_FILE = PROCESSED_DATA_DIR / "cleaned_b2b_orders.csv"
CLEANED_CUSTOMERS_FILE = PROCESSED_DATA_DIR / "cleaned_customer_profiles.csv"
CLEANED_PRODUCTS_FILE = PROCESSED_DATA_DIR / "cleaned_product_catalogue.csv"

# Reports
METRICS_JSON_REPORT = REPORTS_DIR / "baseline_metrics_report.json"
METRICS_MD_REPORT = REPORTS_DIR / "baseline_metrics_summary.md"
VALIDATION_LOG_FILE = REPORTS_DIR / "data_validation_report.json"

# Business & SLA Thresholds
TARGET_TRANSIT_DAYS = {
    "Air Cargo": 5,
    "Sea Freight": {
        "Middle East": 16,
        "Asia-Pacific": 17,
        "Europe": 27,
        "North America": 34,
        "Africa": 23
    }
}

# 12 Destination Countries Metadata
SUPPORTED_COUNTRIES = [
    "United States", "United Kingdom", "Germany", "United Arab Emirates",
    "Singapore", "Japan", "Australia", "Netherlands",
    "Canada", "France", "Saudi Arabia", "South Africa"
]

SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "AED", "SGD", "JPY", "AUD", "CAD", "SAR", "ZAR"]

ORIGIN_PORTS = [
    "Chennai Port (INMAA)",
    "Kattupalli Port (INKAT)",
    "Ennore Port (INENR)"
]

def ensure_directories():
    for d in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, SQL_DIR]:
        d.mkdir(parents=True, exist_ok=True)
