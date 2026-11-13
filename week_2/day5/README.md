
# Week 2 - Day 5: NumPy for Data

## Overview
This project focuses on using NumPy for efficient numerical computation and array operations in data analysis pipelines.

## Learning Objective
To understand NumPy arrays, vectorized operations, indexing techniques, statistical calculations and performance comparison with Python loops.

## Technologies Used
- Python
- NumPy
- VS Code
- Git
- GitHub

## Practical Tasks Completed

### 1. NumPy Array Creation and Manipulation
- Created 1D, 2D and 3D NumPy arrays.
- Checked array dimensions using ndim.
- Checked array shapes using shape.
- Created arrays using zeros(), ones() and arange().
- Performed array reshaping and modification.

### 2. Vectorized Operations
- Performed array addition and subtraction.
- Applied multiplication and division.
- Implemented scalar multiplication.
- Calculated sum and mean.
- Performed row-wise and column-wise aggregation using axes.

### 3. Boolean Masking and Fancy Indexing
- Applied Boolean conditions to NumPy arrays.
- Filtered elements using comparison operators.
- Selected specific elements using fancy indexing.
- Selected specific rows and columns.
- Modified array values using Boolean masking.

### 4. Statistical Analysis
- Calculated mean and median.
- Calculated standard deviation and variance.
- Identified minimum and maximum values.
- Computed 25th, 50th and 75th percentiles.
- Calculated Pearson correlation using corrcoef().

### 5. Performance Comparison
- Created a dataset containing 1 million elements.
- Implemented multiplication using a Python loop.
- Implemented multiplication using NumPy vectorization.
- Measured execution time using time.perf_counter().
- Compared execution times.
- Verified both results using np.array_equal().

## Project Structure

week2/day5/
- 01_array_creation.py
- 02_vectorized_operations.py
- 03_boolean_indexing.py
- 04_statistical_analysis.py
- 05_performance_comparison.py
- README.md
- outputs/

## Installation

Install NumPy:

    python -m pip install numpy

## Execution

Run the Python files individually:

    python 01_array_creation.py
    python 02_vectorized_operations.py
    python 03_boolean_indexing.py
    python 04_statistical_analysis.py
    python 05_performance_comparison.py

## Results
All five practical exercises are designed to demonstrate NumPy array operations, numerical analysis and performance measurement.

Actual execution times are machine-dependent and are recorded in the performance comparison output.

## Conclusion
This practical exercise provided hands-on experience with NumPy arrays, vectorized computations, Boolean indexing, statistical analysis and performance comparison.

These concepts are useful in data analysis, data processing and data engineering workflows.
