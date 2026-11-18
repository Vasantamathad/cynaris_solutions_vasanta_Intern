# Week 3 – Day 2: DAX Basics

## 1. What is DAX?

DAX stands for Data Analysis Expressions. It is a formula language used in Power BI to perform calculations and analyze data.

## 2. Measures

Measures are calculations performed dynamically based on filters and slicers.

Example:

```dax
Total Sales = SUM(sales_data[Sales])

Total Profit = SUM(sales_data[Profit])

Total Orders = DISTINCTCOUNT(sales_data[OrderID])

Total Quantity = SUM(sales_data[Quantity])
```

## 3. Calculated Columns

Calculated columns create new columns in a table using DAX formulas.

Example:

```dax
Profit Margin Column =
DIVIDE(
    sales_data[Profit],
    sales_data[Sales],
    0
)
```

## 4. CALCULATE Function

CALCULATE evaluates an expression with modified filter conditions.

Example:

```dax
Electronics Sales =
CALCULATE(
    SUM(sales_data[Sales]),
    sales_data[Category] = "Electronics"
)
```

## 5. DATESYTD Function

DATESYTD calculates year-to-date values.

Example:

```dax
YTD Sales =
CALCULATE(
    [Total Sales],
    DATESYTD(sales_data[OrderDate])
)
```

## 6. EARLIER Function

EARLIER is used to access an earlier row context, commonly in calculated columns.

Example:

```dax
Running Total =
CALCULATE(
    SUM(sales_data[Sales]),
    FILTER(
        sales_data,
        sales_data[OrderDate]
            <= EARLIER(sales_data[OrderDate])
    )
)
```

## 7. Running Total Measure

```dax
Running Total Measure =
CALCULATE(
    SUM(sales_data[Sales]),
    FILTER(
        ALL(sales_data[OrderDate]),
        sales_data[OrderDate] <= MAX(sales_data[OrderDate])
    )
)
```

## 8. Row Context and Filter Context

Row Context: Calculations performed for each individual row.

Filter Context: Calculations performed based on applied filters and slicers.

## 9. Context Transition

Context transition happens when CALCULATE converts row context into filter context.

## 10. Important Viva Questions

Q1. What is DAX?

DAX stands for Data Analysis Expressions. It is used for calculations in Power BI.

Q2. What is the difference between a measure and a calculated column?

A measure is calculated dynamically, while a calculated column is calculated row by row.

Q3. What does CALCULATE do?

It evaluates an expression under modified filter conditions.

Q4. What is DATESYTD?

It calculates values from the beginning of the year up to the current date in context.

Q5. What is EARLIER?

It accesses an earlier row context in a calculation.

Q6. What is context transition?

It converts row context into filter context using CALCULATE.

---

## Tools Used

- Microsoft Power BI Desktop
- DAX
- Visual Studio Code
- Git and GitHub