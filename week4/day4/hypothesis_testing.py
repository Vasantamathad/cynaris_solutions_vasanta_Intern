
import pandas as pd
from scipy import stats

# --------------------------------------------------
# Week 4 - Day 4: Hypothesis Testing
# --------------------------------------------------

# Load dataset
data = pd.read_csv("week4/day4/dataset/delivery_data.csv")

delivery = data["delivery_days"]
partner_a = data[data["partner"] == "A"]["delivery_days"]
partner_b = data[data["partner"] == "B"]["delivery_days"]

alpha = 0.05

print("=" * 50)
print("HYPOTHESIS TESTING")
print("=" * 50)

# --------------------------------------------------
# TEST 1: One-Sample T-Test
# --------------------------------------------------

print("\n1. ONE-SAMPLE T-TEST")

claimed_mean = 3.0

# H0: Population mean = 3 days
# H1: Population mean != 3 days

t_stat, p_value = stats.ttest_1samp(
    delivery,
    popmean=claimed_mean
)

confidence_interval = stats.t.interval(
    confidence=0.95,
    df=len(delivery) - 1,
    loc=delivery.mean(),
    scale=stats.sem(delivery)
)

print("Sample Mean:", round(delivery.mean(), 3))
print("Claimed Mean:", claimed_mean)
print("T-Statistic:", round(t_stat, 4))
print("P-Value:", round(p_value, 4))
print("95% Confidence Interval:", confidence_interval)

if p_value < alpha:
    print("Decision: Reject H0")
    print("Conclusion: Average delivery time differs from 3 days.")
else:
    print("Decision: Fail to reject H0")
    print("Conclusion: Insufficient evidence that mean differs from 3 days.")

# --------------------------------------------------
# TEST 2: Independent Two-Sample T-Test
# --------------------------------------------------

print("\n2. TWO-SAMPLE T-TEST")

# H0: Partner A and B have equal population means
# H1: Partner A and B have different population means

t_stat_2, p_value_2 = stats.ttest_ind(
    partner_a,
    partner_b,
    equal_var=False
)

print("Partner A Mean:", round(partner_a.mean(), 3))
print("Partner B Mean:", round(partner_b.mean(), 3))
print("T-Statistic:", round(t_stat_2, 4))
print("P-Value:", round(p_value_2, 4))

if p_value_2 < alpha:
    print("Decision: Reject H0")
    print("Conclusion: Delivery times differ significantly.")
else:
    print("Decision: Fail to reject H0")
    print("Conclusion: No significant difference detected.")

# --------------------------------------------------
# TEST 3: Confidence Interval for Partner A
# --------------------------------------------------

print("\n3. PARTNER A CONFIDENCE INTERVAL")

ci_a = stats.t.interval(
    confidence=0.95,
    df=len(partner_a) - 1,
    loc=partner_a.mean(),
    scale=stats.sem(partner_a)
)

print("Partner A 95% Confidence Interval:", ci_a)

print("\nHypothesis testing completed successfully.")
