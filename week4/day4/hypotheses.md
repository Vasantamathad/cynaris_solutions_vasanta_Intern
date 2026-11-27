# Week 4 — Day 4: Hypothesis Testing

## Business Scenario 1: Average Delivery Time

**Business claim:** The company's average delivery time is 3 days.

- Null Hypothesis (H₀): The population mean delivery time is 3 days.
- Alternative Hypothesis (H₁): The population mean delivery time is different from 3 days.

This is a two-tailed one-sample t-test.

## Business Scenario 2: Delivery Partner Comparison

**Business question:** Do Partner A and Partner B have different average delivery times?

- Null Hypothesis (H₀): Both partners have equal population mean delivery times.
- Alternative Hypothesis (H₁): The partners have different population mean delivery times.

This is a two-tailed independent two-sample t-test.

## Business Scenario 3: Customer Satisfaction

**Business claim:** A new customer-support process improves the average satisfaction score.

- Null Hypothesis (H₀): The new process does not improve the average satisfaction score.
- Alternative Hypothesis (H₁): The new process improves the average satisfaction score.

This can be tested using a one-tailed t-test when the satisfaction scores are collected from appropriate independent samples.
## Type I and Type II Errors

### Type I Error (False Positive)

A Type I error occurs when we reject a true null hypothesis.

**Business example:** The company concludes that Partner B is significantly slower, even though both delivery partners actually have equal average delivery times.

**Business consequence:** The company may unfairly penalize Partner B, change contracts, or spend money unnecessarily.

The probability of a Type I error is controlled by the significance level, commonly 5%.

### Type II Error (False Negative)

A Type II error occurs when we fail to reject a false null hypothesis.

**Business example:** Partner B is actually slower, but the test fails to detect the difference.

**Business consequence:** The company may continue using an inefficient delivery partner, leading to customer complaints and delayed orders.

### Summary

- Type I error: Detecting a difference that does not actually exist.
- Type II error: Missing a difference that actually exists.
