
import pandas as pd
from pathlib import Path

print("=" * 60)
print("       DAMA DATA QUALITY ASSESSMENT")
print("=" * 60)

# Load dataset
project_path = Path(__file__).resolve().parents[2]
csv_path = project_path / "week1" / "day1" / "sales_results.csv"

df = pd.read_csv(csv_path)

total_rows = len(df)

# Define six quality dimensions
quality_results = []

# 1. Completeness
missing_values = df.isnull().sum().sum()
completeness = (1 - missing_values / df.size) * 100

quality_results.append(
    ("Completeness", completeness,
     f"{missing_values} missing cells")
)

# 2. Accuracy - basic business-rule checks
accuracy_issues = 0

for column in ["Quantity", "UnitPrice"]:
    if column in df.columns:
        accuracy_issues += (df[column] < 0).sum()

accuracy = (1 - accuracy_issues / max(df.size, 1)) * 100

quality_results.append(
    ("Accuracy", accuracy,
     f"{accuracy_issues} negative quantity/price values")
)

# 3. Consistency - check duplicate records
duplicates = df.duplicated().sum()
consistency = (1 - duplicates / max(total_rows, 1)) * 100

quality_results.append(
    ("Consistency", consistency,
     f"{duplicates} duplicate rows")
)

# 4. Timeliness - check date availability
date_columns = [
    col for col in df.columns
    if "date" in col.lower()
]

if date_columns:
    dates = pd.to_datetime(
        df[date_columns[0]], errors="coerce"
    )
    invalid_dates = dates.isna().sum()
    timeliness = (
        1 - invalid_dates / max(total_rows, 1)
    ) * 100
    timeliness_note = f"{invalid_dates} invalid dates"
else:
    timeliness = None
    timeliness_note = "No date column available; SLA not measurable"

quality_results.append(
    ("Timeliness", timeliness, timeliness_note)
)

# 5. Uniqueness
if "InvoiceNo" in df.columns:
    duplicate_invoices = df["InvoiceNo"].duplicated().sum()
    uniqueness = (
        1 - duplicate_invoices / max(total_rows, 1)
    ) * 100
    uniqueness_note = (
        f"{duplicate_invoices} repeated invoice identifiers; "
        "repetition may be valid at line-item level"
    )
else:
    uniqueness = None
    uniqueness_note = "No confirmed unique business key"

quality_results.append(
    ("Uniqueness", uniqueness, uniqueness_note)
)

# 6. Validity - required field checks
validity_issues = 0
checked_columns = 0

for column in ["InvoiceNo", "Quantity", "UnitPrice"]:
    if column in df.columns:
        checked_columns += 1
        validity_issues += df[column].isnull().sum()

if checked_columns:
    validity = (
        1 - validity_issues /
        (total_rows * checked_columns)
    ) * 100
    validity_note = f"{validity_issues} missing required-field values"
else:
    validity = None
    validity_note = "Required fields not available"

quality_results.append(
    ("Validity", validity, validity_note)
)

# Display results
print("\nDATA QUALITY SCORECARD\n")

for dimension, score, note in quality_results:
    if score is None:
        print(f"{dimension}: NOT MEASURABLE")
    else:
        print(f"{dimension}: {score:.2f}%")
    print("Details:", note)
    print("-" * 50)

# Save report
output_dir = Path(__file__).parent / "outputs"
output_dir.mkdir(exist_ok=True)

report = pd.DataFrame(
    quality_results,
    columns=["Dimension", "Score", "Observation"]
)

report.to_csv(
    output_dir / "dama_quality_scorecard.csv",
    index=False
)

print("\nScorecard saved successfully!")
