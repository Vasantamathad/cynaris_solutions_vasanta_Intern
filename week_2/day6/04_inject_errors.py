
import pandas as pd
from pathlib import Path

print("=" * 60)
print("       DATA QUALITY ERROR INJECTION")
print("=" * 60)

# 1. Load original dataset
project_path = Path(__file__).resolve().parents[2]

csv_path = (
    project_path
    / "week1"
    / "day1"
    / "sales_results.csv"
)

df = pd.read_csv(csv_path)

print("\nORIGINAL DATA:")
print(df)

# 2. Create a separate copy
bad_df = df.copy()

# 3. Inject Error 1: Missing customer
bad_df.loc[0, "customer"] = None

# 4. Inject Error 2: Negative amount
bad_df.loc[1, "amount"] = -500

# 5. Inject Error 3: Invalid status
bad_df.loc[2, "status"] = "Unknown"

# 6. Display modified data
print("\nDATA AFTER INJECTING ERRORS:")
print(bad_df)

# 7. Check the three errors
print("\nERROR VERIFICATION")

print(
    "Missing customer:",
    bad_df["customer"].isnull().sum()
)

print(
    "Negative amount:",
    (bad_df["amount"] < 0).sum()
)

print(
    "Invalid status:",
    (~bad_df["status"].isin(
        ["Completed", "Pending", "Cancelled"]
    )).sum()
)

# 8. Save corrupted dataset separately
output_dir = Path(__file__).parent / "outputs"
output_dir.mkdir(exist_ok=True)

bad_df.to_csv(
    output_dir / "sales_data_with_errors.csv",
    index=False
)

print("\nCORRUPTED DATASET SAVED!")
print("\nERROR INJECTION COMPLETED!")
