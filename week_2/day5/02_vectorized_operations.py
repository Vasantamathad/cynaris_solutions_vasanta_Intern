
import numpy as np

print("========== VECTORIZED OPERATIONS ==========")

# Create two arrays
array1 = np.array([10, 20, 30, 40, 50])
array2 = np.array([1, 2, 3, 4, 5])

# Addition
print("\nADDITION:")
print(array1 + array2)

# Subtraction
print("\nSUBTRACTION:")
print(array1 - array2)

# Multiplication
print("\nMULTIPLICATION:")
print(array1 * array2)

# Division
print("\nDIVISION:")
print(array1 / array2)

# Scalar multiplication
print("\nSCALAR MULTIPLICATION:")
print(array1 * 2)

# 2D array for axis operations
data = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

print("\nORIGINAL DATA:")
print(data)

# Sum of all elements
print("\nTOTAL SUM:")
print(np.sum(data))

# Sum across rows (axis=1)
print("\nROW SUMS:")
print(np.sum(data, axis=1))

# Sum across columns (axis=0)
print("\nCOLUMN SUMS:")
print(np.sum(data, axis=0))

# Mean across columns
print("\nCOLUMN MEAN:")
print(np.mean(data, axis=0))

# Maximum and minimum
print("\nMAXIMUM:", np.max(data))
print("MINIMUM:", np.min(data))
