# Week 4 – Day 3: Correlation and Regression Analysis

## 1. Project Overview

This project focuses on analyzing relationships between business variables and predicting sales using correlation analysis and simple linear regression.

The analysis uses a sales dataset containing advertising spend, website visitors, discounts, product prices, and sales.

## 2. Objectives

- Calculate Pearson and Spearman correlation coefficients.
- Visualize relationships using a correlation heatmap and scatter matrix.
- Build a simple linear regression model using Scikit-learn.
- Evaluate model performance using R², MAE, MSE, and RMSE.
- Analyze residuals and examine regression assumptions.

## 3. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Scikit-learn
- VS Code

## 4. Dataset Description

The dataset contains 100 records with the following variables:

| Variable | Description |
|---|---|
| advertising_spend | Amount spent on advertising |
| website_visitors | Number of website visitors |
| discount | Discount percentage |
| product_price | Product price |
| sales | Total sales value |

The dataset was generated using Python and saved as `data/sales_data.csv`.

## 5. Methodology

### Data Preparation
- Created and loaded the sales dataset.
- Inspected records and statistical summaries.
- Checked missing values and duplicate records.

### Correlation Analysis
- Calculated Pearson correlation.
- Calculated Spearman correlation.
- Generated a correlation heatmap.
- Created a scatter matrix.

### Regression Analysis
- Selected advertising spend as the independent variable.
- Selected sales as the dependent variable.
- Divided the dataset into 80% training and 20% testing data.
- Trained a Linear Regression model.
- Generated sales predictions.

### Model Evaluation
Evaluated the model using:
- R² Score
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

### Residual Analysis
- Created a residual scatter plot.
- Generated a residual distribution histogram.
- Created a Q-Q plot.
- Performed a Shapiro-Wilk normality test.
- Examined residual patterns.

## 6. Generated Outputs

All generated files are available in the `outputs/` folder:

- correlation_heatmap.png
- scatter_matrix.png
- regression_line.png
- residual_plot.png
- residual_distribution.png
- qq_plot.png
- regression_results.csv

## 7. Key Findings

The analysis helps identify relationships between business variables and sales. The regression model estimates sales based on advertising expenditure.

The actual correlation values and model performance metrics should be interpreted using the results printed when the Python script runs.

## 8. Conclusion

This project demonstrates the application of statistical correlation techniques and simple linear regression for business data analysis. It also demonstrates model evaluation and residual diagnostics using Python libraries.

## 9. How to Run

Install the required libraries:

```bash
python -m pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

Run the analysis:

```bash
python week4/day3/regression_analysis.py
```

---

**Internship:** Cynaris Solutions  
**Module:** Statistics  
**Task:** Week 4 – Day 3: Correlation and Regression Analysis
