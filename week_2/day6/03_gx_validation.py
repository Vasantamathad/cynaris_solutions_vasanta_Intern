
import pandas as pd
import great_expectations as gx
from pathlib import Path

print("=" * 60)
print("       GREAT EXPECTATIONS VALIDATION")
print("=" * 60)

# 1. Load dataset
project_path = Path(__file__).resolve().parents[2]
csv_path = project_path / "week1" / "day1" / "sales_results.csv"

df = pd.read_csv(csv_path)

print("\nDATASET LOADED")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

# 2. Create GX context
context = gx.get_context()

# 3. Create Pandas Data Source
data_source = context.data_sources.add_pandas(
    name="sales_data_source"
)

# 4. Create Data Asset
data_asset = data_source.add_dataframe_asset(
    name="sales_data_asset"
)

# 5. Create Batch Definition
batch_definition = data_asset.add_batch_definition_whole_dataframe(
    "sales_batch"
)

# 6. Get Batch
batch = batch_definition.get_batch(
    batch_parameters={"dataframe": df}
)

# 7. Create Expectation Suite
suite = gx.ExpectationSuite(
    name="sales_quality_suite"
)

# 8. Define eight expectations
expectations = [
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="sale_id"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="customer"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="city"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="product"
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount",
        min_value=0
    ),
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["Completed", "Pending", "Cancelled"]
    ),
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="sale_id"
    ),
    gx.expectations.ExpectColumnValuesToBeOfType(
        column="amount",
        type_="int64"
    )
]

# 9. Add expectations to suite
for expectation in expectations:
    suite.add_expectation(expectation)

# 10. Save suite
suite = context.suites.add(suite)

# 11. Validate batch using suite
validation_results = batch.validate(suite)

# 12. Display results
print("\nEIGHT EXPECTATION RESULTS")

for result in validation_results.results:
    print("\nExpectation:",
          result.expectation_config.type)
    print("Success:", result.success)

print("\nOVERALL SUCCESS:",
      validation_results.success)

# 13. Save results
output_dir = Path(__file__).parent / "outputs"
output_dir.mkdir(exist_ok=True)

result_rows = []

for result in validation_results.results:
    result_rows.append({
        "Expectation": result.expectation_config.type,
        "Success": result.success
    })

pd.DataFrame(result_rows).to_csv(
    output_dir / "gx_validation_results.csv",
    index=False
)

print("\nRESULTS SAVED SUCCESSFULLY!")
print("\nGX VALIDATION COMPLETED!")
