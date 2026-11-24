
# PII Classification and Data Protection Policy

## 1. Objective

The objective of this policy is to identify personal information in the sales dataset and protect it from unauthorized access or exposure.

## 2. Dataset Columns and Classification

| Column | Classification | Reason |
|---|---|---|
| sale_id | Internal | Transaction identifier |
| customer | Confidential | May identify an individual |
| city | Internal | General location information |
| product | Internal | Product information |
| amount | Internal | Transaction amount |
| status | Internal | Transaction status |

## 3. PII Identification

The customer column is treated as potential PII because it may contain customer names or identifiable information.

Other columns should be reviewed for combinations that could indirectly identify individuals.

## 4. Data Protection Strategies

### Masking
Hide identifiable customer information when displaying data.

Example:
Ananya Sharma -> A****** S*****

### Tokenization
Replace customer identifiers with randomly generated tokens.

Example:
Customer Name -> CUST_001

### Access Control
Only authorized employees should access identifiable customer information.

### Data Minimization
Collect and retain only the personal information required for business purposes.

## 5. Data Classification Levels

- Public: Information available to everyone.
- Internal: Information intended for employees.
- Confidential: Sensitive business or customer information.
- Restricted: Highly sensitive personal or financial information requiring strict access control.

## 6. DPDP Act Considerations

The Digital Personal Data Protection Act, 2023 requires appropriate protection of digital personal data.

The organization should:
- Process personal data for a lawful purpose.
- Provide required notices and obtain consent where applicable.
- Maintain reasonable security safeguards.
- Apply appropriate retention and deletion practices.
- Respect applicable data principal rights.

## 7. Conclusion

Data classification, masking, tokenization and access control help reduce privacy risks and support responsible data governance.
