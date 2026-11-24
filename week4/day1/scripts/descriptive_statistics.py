
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "retail_sales.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# 1. Load the dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("\n========== DATASET ==========")
print(df.head())

print("\n========== DATASET INFORMATION ==========")
print(df.info())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# --------------------------------------------------
# 2. Descriptive Statistics
# --------------------------------------------------

sales = df["Sales"]

mean_sales = sales.mean()
median_sales = sales.median()
mode_sales = sales.mode().tolist()
variance_sales = sales.var()
std_sales = sales.std()

print("\n========== DESCRIPTIVE STATISTICS ==========")
print("Mean:", mean_sales)
print("Median:", median_sales)
print("Mode:", mode_sales)
print("Sample Variance:", variance_sales)
print("Sample Standard Deviation:", std_sales)

# Save descriptive statistics
summary = pd.DataFrame({
    "Statistic": [
        "Mean",
        "Median",
        "Mode",
        "Sample Variance",
        "Sample Standard Deviation"
    ],
    "Value": [
        mean_sales,
        median_sales,
        str(mode_sales),
        variance_sales,
        std_sales
    ]
})

summary.to_csv(
    OUTPUT_DIR / "descriptive_statistics.csv",
    index=False
)

# --------------------------------------------------
# 3. Frequency Distribution
# --------------------------------------------------

frequency = pd.cut(
    sales,
    bins=5
).value_counts().sort_index()

print("\n========== FREQUENCY DISTRIBUTION ==========")
print(frequency)

frequency.to_csv(
    OUTPUT_DIR / "frequency_distribution.csv"
)

# Histogram
plt.figure(figsize=(8, 5))

plt.hist(
    sales,
    bins=5,
    edgecolor="black"
)

plt.title("Retail Sales Frequency Distribution")
plt.xlabel("Sales Amount (₹)")
plt.ylabel("Frequency")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "sales_histogram.png",
    dpi=300
)

plt.show()

# --------------------------------------------------
# 4. Percentiles and Quartiles
# --------------------------------------------------

percentiles = sales.quantile(
    [0.25, 0.50, 0.75, 0.90]
)

print("\n========== PERCENTILES ==========")
print(percentiles)

q1 = sales.quantile(0.25)
q2 = sales.quantile(0.50)
q3 = sales.quantile(0.75)

iqr = q3 - q1

print("\nQ1:", q1)
print("Q2:", q2)
print("Q3:", q3)
print("Interquartile Range:", iqr)

percentiles.to_csv(
    OUTPUT_DIR / "percentiles.csv"
)

# --------------------------------------------------
# 5. Compare Sales Across Regions
# --------------------------------------------------

region_summary = df.groupby("Region")["Sales"].agg(
    ["mean", "median", "min", "max", "std"]
)

print("\n========== REGION COMPARISON ==========")
print(region_summary)

region_summary.to_csv(
    OUTPUT_DIR / "region_comparison.csv"
)

# Side-by-side box plot
plt.figure(figsize=(8, 5))

df.boxplot(
    column="Sales",
    by="Region"
)

plt.title("Sales Distribution by Region")
plt.suptitle("")
plt.xlabel("Region")
plt.ylabel("Sales Amount (₹)")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "regional_boxplot.png",
    dpi=300
)

plt.show()

# --------------------------------------------------
# 6. Business Insights
# --------------------------------------------------

north_mean = df[df["Region"] == "North"]["Sales"].mean()
south_mean = df[df["Region"] == "South"]["Sales"].mean()

print("\n========== BUSINESS INSIGHTS ==========")

print(f"Average sales across all orders: ₹{mean_sales:.2f}")

print(f"North region average sales: ₹{north_mean:.2f}")

print(f"South region average sales: ₹{south_mean:.2f}")

if north_mean > south_mean:
    print("North region has higher average sales.")
elif south_mean > north_mean:
    print("South region has higher average sales.")
else:
    print("Both regions have equal average sales.")

print(f"Sales standard deviation: ₹{std_sales:.2f}")

print("\nAnalysis completed successfully!")
print("All output files are saved in the output folder.")
