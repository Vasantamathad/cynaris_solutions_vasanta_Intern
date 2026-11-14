
import pandas as pd
import great_expectations as gx
from pathlib import Path

print("=" * 60)
print(" GREAT EXPECTATIONS - CORRUPTED DATA VALIDATION")
print("=" * 60)

# 1. Define file paths
day6_path = Path(__file__).resolve().parent
csv_path = day6_path / "outputs" / "sales_data_with_errors.csv"

if not csv_path.exists():
    raise FileNotFoundError(
        f"Corrupted dataset not found: {csv_path}\n"
        "Run 04_inject_errors.py first."
    )

# 2. Load corrupted dataset
df = pd.read_csv(csv_path)

print("\nCORRUPTED DATASET:")
print(df)

print("\nDATASET SHAPE:", df.shape)

# 3. Create Great Expectations context
context = gx.get_context()

data_source = context.data_sources.add_pandas(
    name="corrupted_sales_source"
)

data_asset = data_source.add_dataframe_asset(
    name="corrupted_sales_asset"
)

batch_definition = data_asset.add_batch_definition_whole_dataframe(
    "corrupted_sales_batch"
)

batch = batch_definition.get_batch(
    batch_parameters={"dataframe": df}
)

# 4. Create expectation suite
suite = gx.ExpectationSuite(
    name="corrupted_sales_quality_suite"
)

# 5. Define quality expectations
expectations = [
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="customer"
    ),

    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount",
        min_value=0
    ),

    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["Completed", "Pending", "Cancelled"]
    )
]

for expectation in expectations:
    suite.add_expectation(expectation)

# 6. Validate corrupted data
validation_results = batch.validate(suite)

# 7. Display validation results
print("\n" + "=" * 60)
print("VALIDATION RESULTS")
print("=" * 60)

for result in validation_results.results:
    expectation_type = result.expectation_config.type
    status = "PASSED" if result.success else "FAILED"

    print(f"\nExpectation: {expectation_type}")
    print(f"Status: {status}")

    print("Details:", result.result)

print("\n" + "=" * 60)

if validation_results.success:
    print("ALL EXPECTATIONS PASSED")
else:
    print("DATA QUALITY ISSUES DETECTED!")

print("\nOverall Validation Success:", validation_results.success)
print("\nVALIDATION COMPLETED!")
