
# =====================================================
# WEEK 2 - DAY 4: DATA CLEANING
# Dataset: Sample Superstore
# =====================================================

# STEP 1: IMPORT LIBRARIES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings("ignore")

print("=" * 60)
print("WEEK 2 - DAY 4: DATA CLEANING")
print("=" * 60)


# STEP 2: DEFINE PROJECT PATHS

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_PATH, "dataset")
CLEANED_PATH = os.path.join(BASE_PATH, "cleaned")
REPORTS_PATH = os.path.join(BASE_PATH, "reports")

os.makedirs(CLEANED_PATH, exist_ok=True)
os.makedirs(REPORTS_PATH, exist_ok=True)


# STEP 3: LOAD ORIGINAL DATASET

file_path = os.path.join(
    DATASET_PATH,
    "superstore.csv"
)

df = pd.read_csv(file_path)

print("\nDataset loaded successfully!")

print("\nOriginal Dataset Shape:")
print(df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Information:")
df.info()


# STEP 4: IDENTIFY MISSING VALUES

print("\n" + "=" * 50)
print("MISSING VALUE ANALYSIS")
print("=" * 50)

missing_values = df.isnull().sum()

missing_percentage = (
    df.isnull().mean() * 100
).round(2)

missing_report = pd.DataFrame({
    "Missing_Count": missing_values,
    "Missing_Percentage": missing_percentage
})

print("\nMissing Value Report:")
print(missing_report)

print(
    "\nTotal Missing Values:",
    df.isnull().sum().sum()
)

missing_report.to_csv(
    os.path.join(REPORTS_PATH, "missing_values_report.csv")
)


# STEP 5: HANDLE MISSING VALUES

print("\nMISSING VALUE IMPUTATION")

# Create a working copy
df_cleaned = df.copy()

# Track cleaning decisions
cleaning_log = []

for column in df_cleaned.columns:

    missing_count = df_cleaned[column].isnull().sum()

    if missing_count > 0:

        # Numerical columns
        if pd.api.types.is_numeric_dtype(
            df_cleaned[column]
        ):

            skewness = df_cleaned[column].skew()

            if abs(skewness) < 0.5:

                fill_value = df_cleaned[column].mean()
                strategy = "Mean Imputation"

            else:

                fill_value = df_cleaned[column].median()
                strategy = "Median Imputation"

            df_cleaned[column] = (
                df_cleaned[column].fillna(fill_value)
            )

        # Categorical columns
        else:

            mode_values = df_cleaned[column].mode()

            if not mode_values.empty:

                fill_value = mode_values.iloc[0]

                df_cleaned[column] = (
                    df_cleaned[column].fillna(fill_value)
                )

                strategy = "Mode Imputation"

            else:
                strategy = "No valid mode available"

        cleaning_log.append(
            f"{column}: {missing_count} missing values "
            f"handled using {strategy}"
        )

# Forward-fill example for ordered data
# Only use this when row order has a meaningful sequence.

print("\nMissing values after imputation:")
print(df_cleaned.isnull().sum())

print("\nImputation completed!")


# STEP 6: DUPLICATE DETECTION AND REMOVAL

print("\nDUPLICATE RECORD ANALYSIS")

duplicates_before = df_cleaned.duplicated().sum()

print("Duplicate Records Found:", duplicates_before)

df_cleaned = df_cleaned.drop_duplicates()

duplicates_after = df_cleaned.duplicated().sum()

print("Duplicate Records Remaining:", duplicates_after)

cleaning_log.append(
    f"Duplicate records found: {duplicates_before}"
)

cleaning_log.append(
    f"Duplicate records removed: {duplicates_before - duplicates_after}"
)


# STEP 7: OUTLIER DETECTION AND CAPPING

print("\nOUTLIER ANALYSIS USING IQR")

# Do not treat identifiers such as postal codes
# as continuous numerical measurements.

exclude_columns = [
    "Postal Code",
    "Row ID"
]

numeric_columns = df_cleaned.select_dtypes(
    include=np.number
).columns.tolist()

outlier_report = []

for column in numeric_columns:

    if column in exclude_columns:
        continue

    Q1 = df_cleaned[column].quantile(0.25)
    Q3 = df_cleaned[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = (
        (df_cleaned[column] < lower_limit) |
        (df_cleaned[column] > upper_limit)
    )

    outlier_count = outliers.sum()

    print(f"\nColumn: {column}")
    print("Outliers Found:", outlier_count)
    print("Lower Limit:", lower_limit)
    print("Upper Limit:", upper_limit)

    # Cap extreme values at IQR boundaries

    df_cleaned[column] = df_cleaned[column].clip(
        lower=lower_limit,
        upper=upper_limit
    )

    outlier_report.append({
        "Column": column,
        "Outliers_Found": outlier_count,
        "Lower_Limit": lower_limit,
        "Upper_Limit": upper_limit
    })

    cleaning_log.append(
        f"{column}: Detected {outlier_count} outliers; "
        "capped using IQR boundaries."
    )

outlier_df = pd.DataFrame(outlier_report)

outlier_df.to_csv(
    os.path.join(REPORTS_PATH, "outlier_report.csv"),
    index=False
)

print("\nOutlier treatment completed!")


# STEP 8: STRING STANDARDISATION

print("\nSTRING STANDARDISATION")

# Standardise whitespace in all text columns

for column in df_cleaned.select_dtypes(
    include="object"
).columns:

    df_cleaned[column] = (
        df_cleaned[column]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

# Standardise selected categorical columns

categorical_columns = [
    "Region",
    "Category",
    "Sub-Category",
    "Segment",
    "Ship Mode"
]

for column in categorical_columns:

    if column in df_cleaned.columns:

        df_cleaned[column] = (
            df_cleaned[column].str.title()
        )

        cleaning_log.append(
            f"{column}: Standardised whitespace and casing."
        )

print("String standardisation completed!")


# STEP 9: GENERATE CLEANING VISUALISATIONS

print("\nGenerating cleaning charts...")

# Chart 1: Missing values before cleaning

missing_before = df.isnull().sum()
missing_before = missing_before[missing_before > 0]

plt.figure(figsize=(10, 5))

if not missing_before.empty:

    sns.barplot(
        x=missing_before.index,
        y=missing_before.values
    )

    plt.xticks(rotation=45)
    plt.title("Missing Values Before Cleaning")
    plt.ylabel("Missing Count")

else:

    plt.text(
        0.5, 0.5,
        "No missing values found",
        ha="center",
        va="center",
        fontsize=16
    )

    plt.title("Missing Values Before Cleaning")

plt.tight_layout()

plt.savefig(
    os.path.join(REPORTS_PATH, "missing_values_before.png"),
    dpi=300
)

plt.close()


# Chart 2: Outlier comparison for numeric columns

for column in numeric_columns:

    if column in exclude_columns:
        continue

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.boxplot(y=df[column], ax=axes[0])
    axes[0].set_title(f"Before Cleaning: {column}")

    sns.boxplot(y=df_cleaned[column], ax=axes[1])
    axes[1].set_title(f"After Cleaning: {column}")

    plt.tight_layout()

    safe_name = column.lower().replace(" ", "_")

    plt.savefig(
        os.path.join(
            REPORTS_PATH,
            f"{safe_name}_outlier_comparison.png"
        ),
        dpi=300
    )

    plt.close()

print("Cleaning visualisations generated!")


# STEP 10: SAVE CLEANED DATASET

cleaned_file = os.path.join(
    CLEANED_PATH,
    "superstore_cleaned.csv"
)

df_cleaned.to_csv(
    cleaned_file,
    index=False
)

print("\nCleaned dataset saved successfully!")
print(cleaned_file)


# STEP 11: GENERATE DATA QUALITY LOG

quality_log_path = os.path.join(
    REPORTS_PATH,
    "data_quality_log.txt"
)

with open(
    quality_log_path,
    "w",
    encoding="utf-8"
) as file:

    file.write("WEEK 2 - DAY 4: DATA QUALITY LOG\n")
    file.write("=" * 60 + "\n\n")

    file.write("DATASET INFORMATION\n")
    file.write("-" * 40 + "\n")

    file.write(f"Original Rows: {len(df)}\n")
    file.write(f"Original Columns: {len(df.columns)}\n")

    file.write(
        f"Missing Values Before: "
        f"{df.isnull().sum().sum()}\n"
    )

    file.write(
        f"Duplicate Rows Before: "
        f"{df.duplicated().sum()}\n\n"
    )

    file.write("CLEANING ACTIONS\n")
    file.write("-" * 40 + "\n")

    if cleaning_log:

        for item in cleaning_log:
            file.write(item + "\n")

    else:
        file.write(
            "No cleaning actions were required.\n"
        )

    file.write("\nFINAL DATASET INFORMATION\n")
    file.write("-" * 40 + "\n")

    file.write(f"Final Rows: {len(df_cleaned)}\n")
    file.write(f"Final Columns: {len(df_cleaned.columns)}\n")

    file.write(
        f"Remaining Missing Values: "
        f"{df_cleaned.isnull().sum().sum()}\n"
    )

    file.write(
        f"Remaining Duplicates: "
        f"{df_cleaned.duplicated().sum()}\n"
    )

    file.write("\nFINAL VALIDATION\n")
    file.write("-" * 40 + "\n")

    file.write(
        "Dataset saved as superstore_cleaned.csv\n"
    )

print("Data quality log generated!")


# STEP 12: FINAL DATA QUALITY VALIDATION

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nOriginal Dataset Shape:", df.shape)

print("Cleaned Dataset Shape:", df_cleaned.shape)

print(
    "\nRemaining Missing Values:",
    df_cleaned.isnull().sum().sum()
)

print(
    "Remaining Duplicate Records:",
    df_cleaned.duplicated().sum()
)

print("\nGenerated Deliverables:")

for folder in [CLEANED_PATH, REPORTS_PATH]:

    print(f"\n{os.path.basename(folder)}/")

    for filename in sorted(os.listdir(folder)):
        print("  ", filename)

print("\nYour Day 4 task is ready for review!")
