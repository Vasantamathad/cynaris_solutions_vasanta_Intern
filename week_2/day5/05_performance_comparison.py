
import numpy as np
import time

print("========== PERFORMANCE COMPARISON ==========")

# Create one million numbers
size = 1_000_000

python_list = list(range(size))
numpy_array = np.arange(size)

# Python loop performance
start_time = time.perf_counter()

python_result = []

for number in python_list:
    python_result.append(number * 2)

python_time = time.perf_counter() - start_time

# NumPy vectorized performance
start_time = time.perf_counter()

numpy_result = numpy_array * 2

numpy_time = time.perf_counter() - start_time

# Display results
print("\nDATASET SIZE:", size)

print("\nPYTHON LOOP TIME:")
print(f"{python_time:.6f} seconds")

print("\nNUMPY VECTORISED TIME:")
print(f"{numpy_time:.6f} seconds")

# Calculate speed improvement
if numpy_time > 0:
    speedup = python_time / numpy_time
    print("\nNUMPY SPEEDUP:")
    print(f"{speedup:.2f} times")

# Verify results
print("\nRESULTS MATCH:")
print(np.array_equal(python_result, numpy_result))

print("\nFIRST 10 RESULTS:")
print(numpy_result[:10])
