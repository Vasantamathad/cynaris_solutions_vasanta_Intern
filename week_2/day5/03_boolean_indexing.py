
import numpy as np

print("========== BOOLEAN MASKING AND FANCY INDEXING ==========")

# Create an array
marks = np.array([45, 67, 89, 32, 76, 90, 55, 28])

print("\nORIGINAL MARKS:")
print(marks)

# Boolean masking: marks greater than 60
mask = marks > 60

print("\nBOOLEAN MASK:")
print(mask)

print("\nMARKS GREATER THAN 60:")
print(marks[mask])

# Filter marks between 40 and 80
filtered_marks = marks[(marks >= 40) & (marks <= 80)]

print("\nMARKS BETWEEN 40 AND 80:")
print(filtered_marks)

# Find failed students
failed_marks = marks[marks < 35]

print("\nFAILED MARKS:")
print(failed_marks)

# Fancy indexing
selected_marks = marks[[0, 2, 4, 6]]

print("\nSELECTED MARKS USING FANCY INDEXING:")
print(selected_marks)

# Modify values using Boolean indexing
marks[marks < 35] = 35

print("\nUPDATED MARKS:")
print(marks)

# 2D fancy indexing
data = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

print("\nSELECTED ROWS:")
print(data[[0, 2]])
