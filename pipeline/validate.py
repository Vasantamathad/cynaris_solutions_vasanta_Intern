"""
Validation & Data Quality Framework
Runs automated validation tests on transformed datasets before loading.
"""

import json
from pipeline.config import VALIDATION_LOG_FILE, SUPPORTED_COUNTRIES, SUPPORTED_CURRENCIES

def validate_datasets(transformed_data):
    print("  [VALIDATE] Running automated data quality test suite...")
    customers = transformed_data["customers"]
    products = transformed_data["products"]
    orders = transformed_data["orders"]
    
    results = {
        "passed": True,
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "details": []
    }
    
    def log_test(name, passed, message):
        results["tests_run"] += 1
        if passed:
            results["tests_passed"] += 1
        else:
            results["tests_failed"] += 1
            results["passed"] = False
        results["details"].append({
            "test_name": name,
            "status": "PASS" if passed else "FAIL",
            "message": message
        })

    # Test 1: Primary Key Uniqueness
    cust_ids = [c["customer_id"] for c in customers]
    cust_pk_pass = len(cust_ids) == len(set(cust_ids))
    log_test("Customer PK Uniqueness", cust_pk_pass, f"{len(cust_ids)} records, {len(set(cust_ids))} unique IDs")

    prod_ids = [p["product_id"] for p in products]
    prod_pk_pass = len(prod_ids) == len(set(prod_ids))
    log_test("Product PK Uniqueness", prod_pk_pass, f"{len(prod_ids)} records, {len(set(prod_ids))} unique IDs")

    order_ids = [o["order_id"] for o in orders]
    order_pk_pass = len(order_ids) == len(set(order_ids))
    log_test("Order PK Uniqueness", order_pk_pass, f"{len(order_ids)} records, {len(set(order_ids))} unique IDs")

    # Test 2: Foreign Key Referential Integrity
    cust_set = set(cust_ids)
    prod_set = set(prod_ids)
    orphaned_cust = [o["order_id"] for o in orders if o["customer_id"] not in cust_set]
    log_test("Order -> Customer FK Integrity", len(orphaned_cust) == 0, f"{len(orphaned_cust)} orphaned customer keys found")

    orphaned_prod = [o["order_id"] for o in orders if o["product_id"] not in prod_set]
    log_test("Order -> Product FK Integrity", len(orphaned_prod) == 0, f"{len(orphaned_prod)} orphaned product keys found")

    # Test 3: Chronological Order Sequence
    chrono_errors = 0
    for o in orders:
        if o["dispatch_date"] < o["order_date"]:
            chrono_errors += 1
        if o["actual_delivery_date"] and o["actual_delivery_date"] < o["dispatch_date"]:
            chrono_errors += 1
    log_test("Chronological Sequence Integrity", chrono_errors == 0, f"{chrono_errors} chronological date discrepancies")

    # Test 4: Positive Financial & Quantity Values
    value_errors = 0
    for o in orders:
        if o["order_quantity"] <= 0 or o["unit_price_foreign"] <= 0 or o["booking_fx_rate"] <= 0:
            value_errors += 1
    log_test("Positive Values & Exchange Rates", value_errors == 0, f"{value_errors} non-positive values encountered")

    # Test 5: Country & Currency Domain Whitelist
    invalid_countries = set(o["destination_country"] for o in orders) - set(SUPPORTED_COUNTRIES)
    log_test("12 Destination Country Whitelist", len(invalid_countries) == 0, f"Unsupported countries: {list(invalid_countries)}")

    invalid_currencies = set(o["settlement_currency"] for o in orders) - set(SUPPORTED_CURRENCIES)
    log_test("Settlement Currency Whitelist", len(invalid_currencies) == 0, f"Unsupported currencies: {list(invalid_currencies)}")

    # Write report
    with open(VALIDATION_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    status_str = "SUCCESS (All Passed)" if results["passed"] else "FAILED (Errors Detected)"
    print(f"    - Test Results: {results['tests_passed']}/{results['tests_run']} passed. Status: {status_str}")
    
    if not results["passed"]:
        raise ValueError(f"Data quality validation failed! See {VALIDATION_LOG_FILE} for details.")
        
    return results
