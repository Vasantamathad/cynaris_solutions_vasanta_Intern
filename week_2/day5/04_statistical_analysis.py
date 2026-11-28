
import numpy as np

print("========== STATISTICAL ANALYSIS ==========")

# Sample student marks
marks = np.array([65, 70, 75, 80, 85, 90, 95])

# Mean
mean_value = np.mean(marks)
print("\nMEAN:", mean_value)

# Median
median_value = np.median(marks)
print("MEDIAN:", median_value)

# Standard deviation
std_value = np.std(marks)
print("STANDARD DEVIATION:", std_value)

# Variance
variance_value = np.var(marks)
print("VARIANCE:", variance_value)

# Minimum and maximum
print("MINIMUM:", np.min(marks))
print("MAXIMUM:", np.max(marks))

# Percentile
percentile_value = np.percentile(marks, 75)
print("75TH PERCENTILE:", percentile_value)

# Correlation
study_hours = np.array([1, 2, 3, 4, 5, 6])
exam_scores = np.array([40, 50, 60, 70, 80, 90])

correlation = np.corrcoef(study_hours, exam_scores)

print("\nCORRELATION MATRIX:")
print(correlation)

print("\nPEARSON CORRELATION:")
print(correlation[0, 1])
