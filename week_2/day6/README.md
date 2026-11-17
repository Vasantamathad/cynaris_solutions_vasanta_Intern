# Week 2 – Day 6: Data Governance and Data Quality

## Objective
Apply data quality dimensions, validate data using Great Expectations, create a data contract, and identify personally identifiable information (PII).

## Tasks Completed

1. **Dataset Profiling**
   - Loaded the sales dataset using Pandas.
   - Checked rows, columns, data types, missing values, duplicates, and statistical summary.

2. **DAMA-DMBOK Data Quality Assessment**
   - Assessed completeness.
   - Assessed accuracy.
   - Assessed consistency.
   - Assessed timeliness.
   - Assessed uniqueness.
   - Assessed validity.

3. **Great Expectations**
   - Created data quality expectations.
   - Prepared validation checks for the sales dataset.

4. **Data Quality Error Injection**
   - Introduced a missing customer value.
   - Introduced a negative sales amount.
   - Introduced an invalid status value.
   - Saved the modified dataset in the outputs folder.

5. **Data Contract**
   - Defined producer and consumer responsibilities.
   - Documented required fields and quality rules.
   - Defined data classification and freshness expectations.

6. **PII Classification**
   - Identified potentially sensitive customer information.
   - Documented masking and tokenization approaches.
   - Suggested access control and data protection measures.

## Tools and Technologies
- Python
- Pandas
- Great Expectations
- YAML
- VS Code

## Project Structure

```text
day6/
├── outputs/
├── 01_profile_dataset.py
├── 02_dama_quality_assessment.py
├── 03_gx_validation.py
├── 04_inject_errors.py
├── 05_data_contract.yaml
├── 06_pii_classification.md
├── 07_validate_corrupted_data.py
└── README.md
```

## Expected Outcome
Understand data quality dimensions, define data quality expectations, detect intentional data errors, document data contracts, and identify potential PII risks.

**Status:** Great Expectations validation of the corrupted dataset is pending confirmation.
