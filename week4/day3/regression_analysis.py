
# ==========================================================
# CYNARIS SOLUTIONS - WEEK 4 DAY 3
# CORRELATION AND REGRESSION ANALYSIS
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from scipy.stats import shapiro, probplot

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

import warnings
warnings.filterwarnings("ignore")

print("=" * 55)
print("CORRELATION AND REGRESSION ANALYSIS")
print("=" * 55)

# STEP 1: CREATE PROJECT FOLDERS

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# STEP 2: CREATE SALES DATASET

np.random.seed(42)

data = pd.DataFrame({
    "advertising_spend": np.random.randint(1000, 10000, 100),
    "website_visitors": np.random.randint(500, 5000, 100),
    "discount": np.random.randint(5, 30, 100),
    "product_price": np.random.randint(200, 2000, 100)
})

data["sales"] = (
    3000
    + 4 * data["advertising_spend"]
    + 2 * data["website_visitors"]
    - 100 * data["discount"]
    + 1.5 * data["product_price"]
    + np.random.normal(0, 4000, 100)
)

data["sales"] = data["sales"].round(2)

data.to_csv(DATA_DIR / "sales_data.csv", index=False)

print("\nDataset created successfully!")
print("Total records:", len(data))

# STEP 3: LOAD AND INSPECT DATASET

df = pd.read_csv(DATA_DIR / "sales_data.csv")

print("\nFIRST FIVE RECORDS")
print(df.head())

print("\nDATASET INFORMATION")
df.info()

print("\nSTATISTICAL SUMMARY")
print(df.describe())

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

# STEP 4: PEARSON AND SPEARMAN CORRELATION

pearson_corr = df.corr(method="pearson")
spearman_corr = df.corr(method="spearman")

print("\nPEARSON CORRELATION WITH SALES")
print(pearson_corr["sales"].sort_values(ascending=False))

print("\nSPEARMAN CORRELATION WITH SALES")
print(spearman_corr["sales"].sort_values(ascending=False))

# STEP 5: CORRELATION HEATMAP

plt.figure(figsize=(10, 7))

sns.heatmap(
    pearson_corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Pearson Correlation Heatmap")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "correlation_heatmap.png")
plt.close()

print("\nCorrelation heatmap saved!")

# STEP 6: SCATTER MATRIX

from pandas.plotting import scatter_matrix

scatter_matrix(
    df,
    figsize=(12, 10),
    diagonal="hist",
    alpha=0.7
)

plt.suptitle("Scatter Matrix of Sales Dataset", y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "scatter_matrix.png")
plt.close()

print("Scatter matrix saved!")

# STEP 7: SIMPLE LINEAR REGRESSION

# Input variable: Advertising Spend
# Target variable: Sales

X = df[["advertising_spend"]]
y = df["sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nLINEAR REGRESSION MODEL")
print("Model trained successfully!")
print("Coefficient:", model.coef_[0])
print("Intercept:", model.intercept_)

# STEP 8: MODEL EVALUATION

r2 = r2_score(y_test, y_pred)

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)

print("\nMODEL PERFORMANCE")
print("R2 Score:", round(r2, 4))
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))

# STEP 9: REGRESSION LINE PLOT

plot_data = pd.DataFrame({
    "advertising_spend": X_test["advertising_spend"].values,
    "actual_sales": y_test.values,
    "predicted_sales": y_pred
}).sort_values("advertising_spend")

plt.figure(figsize=(9, 6))

plt.scatter(
    plot_data["advertising_spend"],
    plot_data["actual_sales"],
    label="Actual Sales",
    alpha=0.7
)

plt.plot(
    plot_data["advertising_spend"],
    plot_data["predicted_sales"],
    color="red",
    label="Regression Line"
)

plt.xlabel("Advertising Spend")
plt.ylabel("Sales")
plt.title("Advertising Spend vs Sales Prediction")
plt.legend()
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "regression_line.png")
plt.close()

print("\nRegression line plot saved!")

# STEP 10: RESIDUAL ANALYSIS

residuals = y_test - y_pred

plt.figure(figsize=(9, 6))

plt.scatter(y_pred, residuals, alpha=0.7)

plt.axhline(
    y=0,
    color="red",
    linestyle="--"
)

plt.xlabel("Predicted Sales")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "residual_plot.png")
plt.close()

print("Residual plot saved!")

# STEP 11: RESIDUAL DISTRIBUTION

plt.figure(figsize=(9, 6))

sns.histplot(
    residuals,
    kde=True,
    bins=20
)

plt.xlabel("Residual Values")
plt.ylabel("Frequency")
plt.title("Distribution of Regression Residuals")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "residual_distribution.png")
plt.close()

print("Residual distribution plot saved!")

# STEP 12: NORMALITY CHECK USING Q-Q PLOT

plt.figure(figsize=(8, 6))

probplot(residuals, dist="norm", plot=plt)

plt.title("Q-Q Plot of Regression Residuals")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "qq_plot.png")
plt.close()

print("Q-Q plot saved!")

# STEP 13: REGRESSION ASSUMPTION CHECKS

print("\nREGRESSION ASSUMPTION CHECKS")

# Normality test
shapiro_stat, shapiro_p = shapiro(residuals)

print("\nShapiro-Wilk Normality Test")
print("Test Statistic:", round(shapiro_stat, 4))
print("P-value:", round(shapiro_p, 4))

if shapiro_p > 0.05:
    print("Result: No strong evidence against normality.")
else:
    print("Result: Residuals may not be normally distributed.")

# Check relationship between predicted values and residuals
residual_corr = np.corrcoef(y_pred, residuals)[0, 1]

print("\nResidual vs Predicted Correlation:")
print(round(residual_corr, 4))

print(
    "Check the residual plot for random scatter "
    "and approximately constant spread."
)

print(
    "Check the Q-Q plot to assess whether residuals "
    "approximately follow a normal distribution."
)

# STEP 14: SAVE MODEL RESULTS

results = pd.DataFrame({
    "Actual_Sales": y_test.values,
    "Predicted_Sales": y_pred,
    "Residuals": residuals.values
})

results.to_csv(
    OUTPUT_DIR / "regression_results.csv",
    index=False
)

# STEP 15: FINAL SUMMARY

print("\n" + "=" * 55)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 55)

print("\nGenerated files:")
for file in sorted(OUTPUT_DIR.iterdir()):
    print("-", file.name)

print("\nDataset saved in:", DATA_DIR)
print("Analysis outputs saved in:", OUTPUT_DIR)
