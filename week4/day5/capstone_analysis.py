
import pandas as pd
import os

# Define dataset path
DATA_PATH = "data/superstore_raw.csv"

# Load the dataset
df = pd.read_csv(DATA_PATH, encoding="latin-1")

# Display basic information
print("\n========== RETAIL SALES DATASET ==========")

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nDataset loaded successfully!")

# ==========================================
# STEP 5: DATA CLEANING AND PREPROCESSING
# ==========================================

print("\n========== DATA CLEANING ==========")

# 1. Check original dataset size
print("Original Dataset Shape:", df.shape)

# 2. Remove duplicate records
df = df.drop_duplicates()
print("After Removing Duplicates:", df.shape)

# 3. Check missing values
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# 4. Remove rows with missing critical values
critical_columns = [
    "Order ID",
    "Order Date",
    "Sales",
    "Profit",
    "Product Name"
]

df = df.dropna(subset=critical_columns)

# 5. Convert date columns
df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], errors="coerce"
)

# Remove rows with invalid order dates
df = df.dropna(subset=["Order Date"])

# 6. Convert numerical columns
numeric_columns = [
    "Sales",
    "Quantity",
    "Discount",
    "Profit"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_columns)

# 7. Create new analytical columns
df["Order Year"] = df["Order Date"].dt.year

df["Order Month"] = df["Order Date"].dt.month

df["Order Month Name"] = df["Order Date"].dt.month_name()

df["Profit Margin"] = (
    df["Profit"] / df["Sales"].replace(0, float("nan"))
) * 100

df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# 8. Save cleaned dataset
os.makedirs("results", exist_ok=True)

df.to_csv("results/cleaned_superstore.csv", index=False)

# 9. Display cleaning results
print("\n========== CLEANING RESULTS ==========")

print("Final Dataset Shape:", df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nDuplicate Records After Cleaning:")
print(df.duplicated().sum())

print("\nNew Columns Created:")
print([
    "Order Year",
    "Order Month",
    "Order Month Name",
    "Profit Margin",
    "Shipping Days"
])

print("\nCleaned dataset saved successfully!")

# ==========================================
# STEP 6: EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================

print("\n========== EXPLORATORY DATA ANALYSIS ==========")

# 1. Overall business performance
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()
total_quantity = df["Quantity"].sum()

profit_margin = (total_profit / total_sales) * 100

print("\n--- Overall Business Performance ---")
print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Total Quantity Sold:", total_quantity)
print("Overall Profit Margin:", round(profit_margin, 2), "%")

# 2. Sales by category
category_sales = df.groupby("Category")["Sales"].sum().sort_values(
    ascending=False
)

print("\n--- Sales by Category ---")
print(category_sales)

# 3. Profit by category
category_profit = df.groupby("Category")["Profit"].sum().sort_values(
    ascending=False
)

print("\n--- Profit by Category ---")
print(category_profit)

# 4. Sales by region
region_sales = df.groupby("Region")["Sales"].sum().sort_values(
    ascending=False
)

print("\n--- Sales by Region ---")
print(region_sales)

# 5. Profit by region
region_profit = df.groupby("Region")["Profit"].sum().sort_values(
    ascending=False
)

print("\n--- Profit by Region ---")
print(region_profit)

# 6. Top 10 profitable sub-categories
subcategory_profit = (
    df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Top 10 Profitable Sub-Categories ---")
print(subcategory_profit.head(10))

# 7. Monthly sales analysis
monthly_sales = (
    df.groupby(["Order Year", "Order Month"])["Sales"]
    .sum()
    .reset_index()
)

print("\n--- Monthly Sales ---")
print(monthly_sales.head(12))

# 8. Save analysis results
os.makedirs("results", exist_ok=True)

category_sales.to_csv("results/category_sales.csv")
category_profit.to_csv("results/category_profit.csv")
region_sales.to_csv("results/region_sales.csv")
region_profit.to_csv("results/region_profit.csv")
subcategory_profit.to_csv("results/subcategory_profit.csv")
monthly_sales.to_csv("results/monthly_sales.csv", index=False)

print("\nEDA results saved successfully!")

# ==========================================
# STEP 7: DATA VISUALIZATION
# ==========================================

import matplotlib.pyplot as plt
import seaborn as sns

print("\n========== CREATING CHARTS ==========")

os.makedirs("charts", exist_ok=True)

sns.set_theme(style="whitegrid")

# 1. Sales by Category
plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="Category",
    y="Sales",
    estimator=sum,
    errorbar=None
)

plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("charts/sales_by_category.png", dpi=300)
plt.close()


# 2. Profit by Region
region_data = df.groupby("Region", as_index=False)["Profit"].sum()

plt.figure(figsize=(9, 5))

sns.barplot(
    data=region_data,
    x="Region",
    y="Profit",
    hue="Region",
    legend=False
)

plt.title("Total Profit by Region")
plt.xlabel("Region")
plt.ylabel("Total Profit")
plt.tight_layout()
plt.savefig("charts/profit_by_region.png", dpi=300)
plt.close()


# 3. Monthly Sales Trend
monthly_data = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_data["Order Date"] = monthly_data["Order Date"].astype(str)

plt.figure(figsize=(12, 5))

sns.lineplot(
    data=monthly_data,
    x="Order Date",
    y="Sales",
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png", dpi=300)
plt.close()


# 4. Profit by Sub-Category
subcategory_data = (
    df.groupby("Sub-Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=subcategory_data,
    x="Sub-Category",
    y="Profit"
)

plt.title("Profit by Sub-Category")
plt.xlabel("Sub-Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/profit_by_subcategory.png", dpi=300)
plt.close()


# 5. Discount vs Profit
plt.figure(figsize=(9, 5))

sns.scatterplot(
    data=df,
    x="Discount",
    y="Profit",
    alpha=0.5
)

plt.title("Relationship Between Discount and Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("charts/discount_vs_profit.png", dpi=300)
plt.close()

print("\nAll 5 charts created successfully!")

# ==========================================
# STEP 8: STATISTICAL ANALYSIS
# ==========================================

from scipy import stats

print("\n========== STATISTICAL ANALYSIS ==========")

os.makedirs("results", exist_ok=True)

# 1. Correlation between Discount and Profit
correlation, p_value = stats.pearsonr(
    df["Discount"],
    df["Profit"]
)

print("\n--- Correlation Analysis ---")
print("Correlation Coefficient:", round(correlation, 4))
print("P-Value:", round(p_value, 6))

if p_value < 0.05:
    print("Result: Statistically significant relationship.")
else:
    print("Result: No statistically significant linear relationship.")

# 2. ANOVA Test: Compare Profit Across Categories

category_groups = [
    group["Profit"].values
    for _, group in df.groupby("Category")
]

f_statistic, anova_p_value = stats.f_oneway(*category_groups)

print("\n--- ANOVA Test ---")
print("F-Statistic:", round(f_statistic, 4))
print("P-Value:", round(anova_p_value, 6))

if anova_p_value < 0.05:
    print("Result: Mean profit differs significantly across categories.")
else:
    print("Result: No statistically significant difference in mean profit.")

# 3. Descriptive Statistics
descriptive_stats = df[
    ["Sales", "Profit", "Quantity", "Discount"]
].describe()

print("\n--- Descriptive Statistics ---")
print(descriptive_stats)

descriptive_stats.to_csv("results/descriptive_statistics.csv")

# 4. Save Statistical Results
statistical_results = pd.DataFrame({
    "Test": [
        "Pearson Correlation: Discount vs Profit",
        "One-Way ANOVA: Profit Across Categories"
    ],
    "Statistic": [
        correlation,
        f_statistic
    ],
    "P_Value": [
        p_value,
        anova_p_value
    ]
})

statistical_results.to_csv(
    "results/statistical_results.csv",
    index=False
)

print("\nStatistical analysis completed successfully!")
