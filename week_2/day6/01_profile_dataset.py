
import pandas as pd
from pathlib import Path

print("=" * 50)
print("       DATASET PROFILE")
print("=" * 50)

# Locate the existing CSV file
project_path = Path(__file__).resolve().parents[2]

csv_path = project_path / "week1" / "day1" / "sales_results.csv"

# Check whether the CSV exists
if not csv_path.exists():
    raise FileNotFoundError(f"Dataset not found: {csv_path}")

# Load the dataset
df = pd.read_csv(csv_path)

# 1. Display first five records
print("\nFIRST FIVE RECORDS:")
print(df.head())

# 2. Display dataset dimensions
print("\nDATASET SHAPE:")
print(df.shape)

# 3. Display column names
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

# 4. Display data types and missing values
print("\nDATASET INFORMATION:")
df.info()

# 5. Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# 6. Check duplicate records
print("\nDUPLICATE ROWS:")
print(df.duplicated().sum())

# 7. Statistical summary
print("\nSTATISTICAL SUMMARY:")
print(df.describe(include="all"))

print("\nDATASET PROFILE COMPLETED!")
