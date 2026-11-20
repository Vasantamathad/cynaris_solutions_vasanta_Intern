import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("All libraries imported successfully!")


# ============================================================
# WEEK 2 - DAY 3: EXPLORATORY DATA ANALYSIS (EDA) WORKFLOW
# Dataset: Sample Superstore
# ============================================================

# STEP 1: IMPORT LIBRARIES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import warnings

warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")

print("=" * 60)
print("WEEK 2 - DAY 3: EDA WORKFLOW")
print("=" * 60)


# STEP 2: CREATE OUTPUT DIRECTORIES

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_PATH, "dataset")
CHARTS_PATH = os.path.join(BASE_PATH, "charts")
OUTPUTS_PATH = os.path.join(BASE_PATH, "outputs")

os.makedirs(CHARTS_PATH, exist_ok=True)
os.makedirs(OUTPUTS_PATH, exist_ok=True)


# STEP 3: LOAD DATASET

file_path = os.path.join(DATASET_PATH, "superstore.csv")

df = pd.read_csv(file_path)

print("\nDataset loaded successfully!")

print("Total Rows:", df.shape[0])
print("Total Columns:", df.shape[1])


# STEP 4: DATASET PROFILING

print("\n--- DATASET INFORMATION ---")

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

# Save dataset profile

profile_path = os.path.join(
    OUTPUTS_PATH, "dataset_profile.txt"
)

with open(profile_path, "w", encoding="utf-8") as file:

    file.write("WEEK 2 - DAY 3: DATASET PROFILE\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Total Rows: {df.shape[0]}\n")
    file.write(f"Total Columns: {df.shape[1]}\n\n")

    file.write("COLUMN NAMES:\n")
    file.write(str(df.columns.tolist()) + "\n\n")

    file.write("DATA TYPES:\n")
    file.write(df.dtypes.to_string() + "\n\n")

    file.write("MISSING VALUES:\n")
    file.write(df.isnull().sum().to_string() + "\n\n")

    file.write(
        f"Total Duplicate Records: {df.duplicated().sum()}\n"
    )


# STEP 5: SUMMARY STATISTICS

numeric_cols = df.select_dtypes(
    include=np.number
).columns.tolist()

summary = df[numeric_cols].describe().T

summary["median"] = df[numeric_cols].median()
summary["missing_values"] = df[numeric_cols].isnull().sum()

summary.to_csv(
    os.path.join(OUTPUTS_PATH, "summary_statistics.csv")
)

print("\nSummary statistics generated successfully!")


# STEP 6: VISUALISE ALL NUMERIC COLUMNS

print("\nGenerating numeric distribution charts...")

for column in numeric_cols:

    plt.figure(figsize=(9, 5))

    sns.histplot(
        data=df,
        x=column,
        kde=True,
        color="steelblue"
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.tight_layout()

    filename = re.sub(
        r"[^a-zA-Z0-9]+", "_", column.lower()
    ).strip("_") + "_distribution.png"

    plt.savefig(
        os.path.join(CHARTS_PATH, filename),
        dpi=300
    )

    plt.close()

print("All numeric distribution charts saved!")


# STEP 7: CORRELATION HEATMAP

# Exclude Postal Code because it is an identifier,
# not a meaningful continuous measurement.

correlation_cols = [
    col for col in numeric_cols
    if col.lower().replace("_", " ") != "postal code"
]

correlation = df[correlation_cols].corr()

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Correlation Heatmap - Superstore Dataset")

plt.tight_layout()

plt.savefig(
    os.path.join(CHARTS_PATH, "correlation_heatmap.png"),
    dpi=300
)

plt.close()

print("Correlation heatmap generated!")


# STEP 8: FIND BUSINESS INSIGHTS

# Find columns without depending on capitalization.

column_map = {
    col.lower().replace("_", " ").strip(): col
    for col in df.columns
}

def find_column(name):
    return column_map.get(name.lower())


sales_col = find_column("Sales")
profit_col = find_column("Profit")
quantity_col = find_column("Quantity")
discount_col = find_column("Discount")
region_col = find_column("Region")
category_col = find_column("Category")
subcategory_col = find_column("Sub-Category")

insights = []

# INSIGHT 1: REGION WITH HIGHEST SALES

if sales_col and region_col:

    region_sales = df.groupby(
        region_col
    )[sales_col].sum().sort_values(ascending=False)

    best_region = region_sales.index[0]
    best_sales = region_sales.iloc[0]

    insights.append(
        f"1. Highest Sales Region: {best_region} "
        f"with total sales of {best_sales:,.2f}."
    )


# INSIGHT 2: MOST PROFITABLE CATEGORY

if profit_col and category_col:

    category_profit = df.groupby(
        category_col
    )[profit_col].sum().sort_values(ascending=False)

    best_category = category_profit.index[0]
    best_profit = category_profit.iloc[0]

    insights.append(
        f"2. Most Profitable Category: {best_category} "
        f"with total profit of {best_profit:,.2f}."
    )


# INSIGHT 3: TOP SELLING PRODUCT CATEGORY

if sales_col and category_col:

    category_sales = df.groupby(
        category_col
    )[sales_col].sum().sort_values(ascending=False)

    top_category = category_sales.index[0]
    top_sales = category_sales.iloc[0]

    insights.append(
        f"3. Highest Revenue Category: {top_category} "
        f"with sales of {top_sales:,.2f}."
    )


# INSIGHT 4: MOST PROFITABLE SUBCATEGORY

if profit_col and subcategory_col:

    subcategory_profit = df.groupby(
        subcategory_col
    )[profit_col].sum().sort_values(ascending=False)

    best_subcategory = subcategory_profit.index[0]
    subcategory_value = subcategory_profit.iloc[0]

    insights.append(
        f"4. Most Profitable Sub-Category: "
        f"{best_subcategory} with profit of "
        f"{subcategory_value:,.2f}."
    )


# INSIGHT 5: DISCOUNT AND PROFIT RELATIONSHIP

if discount_col and profit_col:

    discount_corr = df[
        [discount_col, profit_col]
    ].corr().iloc[0, 1]

    insights.append(
        f"5. Discount-Profit Correlation: {discount_corr:.3f}. "
        "This indicates the direction and strength of their "
        "linear relationship, not causation."
    )


# STEP 9: CREATE BUSINESS INSIGHTS CHART

fig, axes = plt.subplots(2, 3, figsize=(18, 11))

axes = axes.flatten()

chart_index = 0

# Chart 1: Sales by Region

if sales_col and region_col:

    region_sales = df.groupby(
        region_col
    )[sales_col].sum().sort_values(ascending=False)

    region_sales.plot(
        kind="bar",
        ax=axes[chart_index],
        title="Sales by Region"
    )

    axes[chart_index].set_ylabel("Total Sales")
    chart_index += 1


# Chart 2: Profit by Category

if profit_col and category_col:

    category_profit = df.groupby(
        category_col
    )[profit_col].sum().sort_values(ascending=False)

    category_profit.plot(
        kind="bar",
        ax=axes[chart_index],
        title="Profit by Category"
    )

    axes[chart_index].set_ylabel("Total Profit")
    chart_index += 1


# Chart 3: Sales by Category

if sales_col and category_col:

    category_sales = df.groupby(
        category_col
    )[sales_col].sum().sort_values(ascending=False)

    category_sales.plot(
        kind="bar",
        ax=axes[chart_index],
        title="Sales by Category"
    )

    axes[chart_index].set_ylabel("Total Sales")
    chart_index += 1


# Chart 4: Profit by Subcategory

if profit_col and subcategory_col:

    subcategory_profit = df.groupby(
        subcategory_col
    )[profit_col].sum().sort_values(ascending=False)

    subcategory_profit.plot(
        kind="bar",
        ax=axes[chart_index],
        title="Profit by Sub-Category"
    )

    axes[chart_index].tick_params(
        axis="x", rotation=60
    )

    chart_index += 1


# Chart 5: Discount vs Profit

if discount_col and profit_col:

    sns.scatterplot(
        data=df,
        x=discount_col,
        y=profit_col,
        alpha=0.4,
        ax=axes[chart_index]
    )

    axes[chart_index].set_title(
        "Discount vs Profit"
    )

    chart_index += 1


# Hide unused chart spaces

for i in range(chart_index, len(axes)):
    axes[i].set_visible(False)

plt.suptitle(
    "Superstore - Business Insights Dashboard",
    fontsize=18
)

plt.tight_layout()

plt.savefig(
    os.path.join(CHARTS_PATH, "business_insights.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Business insights chart generated!")


# STEP 10: SAVE BUSINESS INSIGHTS TO TEXT FILE

insights_path = os.path.join(
    OUTPUTS_PATH, "business_insights.txt"
)

with open(
    insights_path, "w", encoding="utf-8"
) as file:

    file.write("WEEK 2 - DAY 3: BUSINESS INSIGHTS\n")
    file.write("=" * 50 + "\n\n")

    for insight in insights:
        file.write(insight + "\n\n")

    file.write("\nDATASET SUMMARY\n")
    file.write("-" * 50 + "\n")

    file.write(f"Total Records: {len(df)}\n")
    file.write(f"Total Columns: {len(df.columns)}\n")

    if sales_col:
        file.write(
            f"Total Sales: {df[sales_col].sum():,.2f}\n"
        )

    if profit_col:
        file.write(
            f"Total Profit: {df[profit_col].sum():,.2f}\n"
        )


# STEP 11: FINAL COMPLETION MESSAGE

print("\n" + "=" * 60)
print("EDA WORKFLOW COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nGenerated Files:")

print("\nCHARTS:")
for filename in sorted(os.listdir(CHARTS_PATH)):
    print("-", filename)

print("\nOUTPUTS:")
for filename in sorted(os.listdir(OUTPUTS_PATH)):
    print("-", filename)

print("\nYour EDA deliverables are saved in:")
print(BASE_PATH)

