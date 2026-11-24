
import numpy as np

print("========== NUMPY ARRAY CREATION ==========")

# 1. Create a 1D array
array_1d = np.array([10, 20, 30, 40, 50])

print("\n1D ARRAY:")
print(array_1d)

# 2. Create a 2D array
array_2d = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

print("\n2D ARRAY:")
print(array_2d)

# 3. Create a 3D array
array_3d = np.array([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
])

print("\n3D ARRAY:")
print(array_3d)

# 4. Check array dimensions
print("\nARRAY DIMENSIONS:")
print("1D:", array_1d.ndim)
print("2D:", array_2d.ndim)
print("3D:", array_3d.ndim)

# 5. Check array shapes
print("\nARRAY SHAPES:")
print("1D:", array_1d.shape)
print("2D:", array_2d.shape)
print("3D:", array_3d.shape)

# 6. Create arrays using NumPy functions
zeros_array = np.zeros((2, 3))
ones_array = np.ones((2, 3))
range_array = np.arange(1, 11, 2)

print("\nZEROS ARRAY:")
print(zeros_array)

print("\nONES ARRAY:")
print(ones_array)

print("\nRANGE ARRAY:")
print(range_array)

# 7. Reshape an array
reshaped_array = np.arange(1, 10).reshape(3, 3)

print("\nRESHAPED ARRAY:")
print(reshaped_array)

# 8. Modify array values
array_1d[0] = 100

print("\nMODIFIED 1D ARRAY:")
print(array_1d)
