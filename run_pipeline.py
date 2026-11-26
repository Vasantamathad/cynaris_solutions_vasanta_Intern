"""
TradeSight Repeatable Data Pipeline Runner
Orchestrates Extract -> Transform -> Validate -> Load -> Metrics Calculation
"""

import sys
import time
from pipeline.config import ensure_directories
from pipeline.extract import extract_all
from pipeline.transform import transform_and_save_all
from pipeline.validate import validate_datasets
from pipeline.load import load_star_schema
from pipeline.metrics import calculate_and_persist_baseline_metrics

def main():
    start_time = time.time()
    print("=" * 75)
    print("TRADESIGHT EXPORT ANALYTICS - REPEATABLE DATA PIPELINE")
    print("Cynaris Solutions Learning Path | Capstone Project")
    print("=" * 75)
    
    # 0. Setup
    ensure_directories()
    
    # 1. Extract
    extracted = extract_all()
    
    # 2. Transform & Feature Engineering
    transformed = transform_and_save_all(extracted)
    
    # 3. Validate
    validate_datasets(transformed)
    
    # 4. Load into Star Schema
    conn = load_star_schema(transformed)
    
    # 5. Baseline Metrics
    calculate_and_persist_baseline_metrics(conn)
    conn.close()
    
    duration = time.time() - start_time
    print("=" * 75)
    print(f"PIPELINE EXECUTION COMPLETED SUCCESSFULLY IN {duration:.2f}s")
    print("Database: tradesight.db (Star Schema with Analytical Views)")
    print("Reports:  reports/baseline_metrics_summary.md")
    print("=" * 75)

if __name__ == "__main__":
    main()
