# LCA Final Merged Schema (FY2020 ~ FY2026)

## Overview

This document defines the **final unified schema** for merging H-1B/H-1B1/E-3 LCA public disclosure data from **FY2020 through FY2026** (FLAG system era). The schema uses the most complete version (FY2026 Q1, 98 fields) as the canonical baseline.

**Scope**: FY2020 ~ FY2026 only. FY2018 and FY2019 use fundamentally different schemas (iCERT system) and require separate column renaming/mapping before merging — see the [Appendix: Legacy Mapping](#appendix-legacy-field-mapping-fy2018--fy2019) at the end of this document.

**Source**: [DOL OFLC Performance Data](https://www.dol.gov/agencies/eta/foreign-labor/performance)

---

## Schema Notes

- **98 columns total** (the full superset across FY2020 ~ FY2026 Q1)
- `EMPLOYER_FEIN`: NULL for FY2020 ~ FY2024 Q3; populated from FY2024 Q4 onward
- `LAWFIRM_BUSINESS_FEIN`: NULL for FY2020 ~ FY2025 Q3; populated from FY2025 Q4 onward
- All other 96 columns are present and identical across all fiscal years
- A synthetic column `FISCAL_YEAR` should be added during ETL to identify the source year

---

## Final Schema Definition

### 1. Case Information

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 1 | `CASE_NUMBER` | VARCHAR | No | Unique identifier assigned to each LCA application submitted for processing to OFLC. Primary key for the dataset. |
| 2 | `CASE_STATUS` | VARCHAR | No | Status of the last significant event or decision. Valid values: `Certified`, `Certified-Withdrawn`, `Denied`, `Withdrawn`. |
| 3 | `RECEIVED_DATE` | DATE | No | Date the application was received at OFLC. Format: MM/DD/YYYY. |
| 4 | `DECISION_DATE` | DATE | No | Date on which the last significant event or determination was issued by OFLC. Format: MM/DD/YYYY. |
| 5 | `ORIGINAL_CERT_DATE` | DATE | Yes | Original certification date for a "Certified-Withdrawn" application. NULL for other statuses. Format: MM/DD/YYYY. |
| 6 | `VISA_CLASS` | VARCHAR | No | Type of temporary visa application. Valid values: `H-1B`, `E-3 Australian`, `H-1B1 Chile`, `H-1B1 Singapore`. Form ETA-9035 Section A, Item 1. |

### 2. Job Information

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 7 | `JOB_TITLE` | VARCHAR | No | Title of the job being offered. Free-text field. Form ETA-9035 Section B, Item 1. |
| 8 | `SOC_CODE` | VARCHAR | No | Standard Occupational Classification (SOC) code associated with the job. Format: `XX-XXXX` or `XX-XXXX.XX`. Form ETA-9035 Section B, Item 2. |
| 9 | `SOC_TITLE` | VARCHAR | No | Occupational title associated with the SOC/O*NET code. Form ETA-9035 Section B, Item 3. |
| 10 | `FULL_TIME_POSITION` | VARCHAR(1) | No | Whether the position is full-time. `Y` = Full Time; `N` = Part Time. Form ETA-9035 Section B, Item 4. |
| 11 | `BEGIN_DATE` | DATE | No | Requested beginning date of the period of employment. Format: MM/DD/YYYY. Form ETA-9035 Section B, Item 5. |
| 12 | `END_DATE` | DATE | No | Requested ending date of the period of employment. Format: MM/DD/YYYY. Form ETA-9035 Section B, Item 6. |

### 3. Worker Counts & Petition Type

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 13 | `TOTAL_WORKER_POSITIONS` | INTEGER | No | Total number of foreign worker positions requested by the employer. Form ETA-9035 Section B, Item 7. |
| 14 | `NEW_EMPLOYMENT` | INTEGER | Yes | Number of workers beginning employment for a new employer, as defined by USCIS. Form ETA-9035 Section B, Item 7a. |
| 15 | `CONTINUED_EMPLOYMENT` | INTEGER | Yes | Number of workers continuing employment with the same employer, as defined by USCIS. Form ETA-9035 Section B, Item 7b. |
| 16 | `CHANGE_PREVIOUS_EMPLOYMENT` | INTEGER | Yes | Number of workers continuing employment with the same employer without material change to job duties. Form ETA-9035 Section B, Item 7c. |
| 17 | `NEW_CONCURRENT_EMPLOYMENT` | INTEGER | Yes | Number of workers beginning employment with an additional employer. Form ETA-9035 Section B, Item 7d. |
| 18 | `CHANGE_EMPLOYER` | INTEGER | Yes | Number of workers beginning employment for a new employer using the same classification currently held, as defined by USCIS I-129. Form ETA-9035 Section B, Item 7e. |
| 19 | `AMENDED_PETITION` | INTEGER | Yes | Number of workers continuing employment with the same employer with material change to job duties, as defined by USCIS I-129. Form ETA-9035 Section B, Item 7f. |

### 4. Employer Information

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 20 | `EMPLOYER_NAME` | VARCHAR | No | Legal business name of the employer submitting the LCA. Form ETA-9035 Section C, Item 1. |
| 21 | `TRADE_NAME_DBA` | VARCHAR | Yes | Trade name or "Doing Business As" (DBA), if applicable. Form ETA-9035 Section C, Item 2. |
| 22 | `EMPLOYER_ADDRESS1` | VARCHAR | No | Employer street address line 1. Form ETA-9035 Section C, Items 3-11. |
| 23 | `EMPLOYER_ADDRESS2` | VARCHAR | Yes | Employer street address line 2. |
| 24 | `EMPLOYER_CITY` | VARCHAR | No | Employer city. |
| 25 | `EMPLOYER_STATE` | VARCHAR | No | Employer state (2-letter abbreviation for US). |
| 26 | `EMPLOYER_POSTAL_CODE` | VARCHAR | No | Employer postal/ZIP code. |
| 27 | `EMPLOYER_COUNTRY` | VARCHAR | No | Employer country (e.g., `UNITED STATES OF AMERICA`). |
| 28 | `EMPLOYER_PROVINCE` | VARCHAR | Yes | Employer province (for non-US employers). |
| 29 | `EMPLOYER_PHONE` | VARCHAR | No | Employer phone number. |
| 30 | `EMPLOYER_PHONE_EXT` | VARCHAR | Yes | Employer phone extension. |
| 31 | `EMPLOYER_FEIN` | VARCHAR | Yes | Federal Employer Identification Number (FEIN from IRS). **NULL for FY2020 ~ FY2024 Q3** (excluded as PII); available from FY2024 Q4 onward. Form ETA-9035 Section C, Item 12. |
| 32 | `NAICS_CODE` | VARCHAR | No | North American Industry Classification System (NAICS) code for the employer. Form ETA-9035 Section C, Item 13. |

### 5. Employer Point of Contact

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 33 | `EMPLOYER_POC_LAST_NAME` | VARCHAR | Yes | Employer point of contact last name. Form ETA-9035 Section D, Items 1-4. |
| 34 | `EMPLOYER_POC_FIRST_NAME` | VARCHAR | Yes | Employer point of contact first name. |
| 35 | `EMPLOYER_POC_MIDDLE_NAME` | VARCHAR | Yes | Employer point of contact middle name. |
| 36 | `EMPLOYER_POC_JOB_TITLE` | VARCHAR | Yes | Employer point of contact job title. |
| 37 | `EMPLOYER_POC_ADDRESS1` | VARCHAR | Yes | Employer POC street address line 1. Form ETA-9035 Section D, Items 5-14. |
| 38 | `EMPLOYER_POC_ADDRESS2` | VARCHAR | Yes | Employer POC street address line 2. |
| 39 | `EMPLOYER_POC_CITY` | VARCHAR | Yes | Employer POC city. |
| 40 | `EMPLOYER_POC_STATE` | VARCHAR | Yes | Employer POC state. |
| 41 | `EMPLOYER_POC_POSTAL_CODE` | VARCHAR | Yes | Employer POC postal/ZIP code. |
| 42 | `EMPLOYER_POC_COUNTRY` | VARCHAR | Yes | Employer POC country. |
| 43 | `EMPLOYER_POC_PROVINCE` | VARCHAR | Yes | Employer POC province (for non-US). |
| 44 | `EMPLOYER_POC_PHONE` | VARCHAR | Yes | Employer POC phone number. |
| 45 | `EMPLOYER_POC_PHONE_EXT` | VARCHAR | Yes | Employer POC phone extension. |
| 46 | `EMPLOYER_POC_EMAIL` | VARCHAR | Yes | Employer POC email address. |

### 6. Agent / Attorney Information

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 47 | `AGENT_REPRESENTING_EMPLOYER` | VARCHAR(1) | No | Whether the employer is represented by an agent or attorney. `Y` = Yes; `N` = No. Form ETA-9035 Section E, Item 1. |
| 48 | `AGENT_ATTORNEY_LAST_NAME` | VARCHAR | Yes | Agent or attorney last name. Form ETA-9035 Section E, Items 2-4. |
| 49 | `AGENT_ATTORNEY_FIRST_NAME` | VARCHAR | Yes | Agent or attorney first name. |
| 50 | `AGENT_ATTORNEY_MIDDLE_NAME` | VARCHAR | Yes | Agent or attorney middle name. |
| 51 | `AGENT_ATTORNEY_ADDRESS1` | VARCHAR | Yes | Agent/attorney street address line 1. Form ETA-9035 Section E, Items 5-14. |
| 52 | `AGENT_ATTORNEY_ADDRESS2` | VARCHAR | Yes | Agent/attorney street address line 2. |
| 53 | `AGENT_ATTORNEY_CITY` | VARCHAR | Yes | Agent/attorney city. |
| 54 | `AGENT_ATTORNEY_STATE` | VARCHAR | Yes | Agent/attorney state. |
| 55 | `AGENT_ATTORNEY_POSTAL_CODE` | VARCHAR | Yes | Agent/attorney postal/ZIP code. |
| 56 | `AGENT_ATTORNEY_COUNTRY` | VARCHAR | Yes | Agent/attorney country. |
| 57 | `AGENT_ATTORNEY_PROVINCE` | VARCHAR | Yes | Agent/attorney province (for non-US). |
| 58 | `AGENT_ATTORNEY_PHONE` | VARCHAR | Yes | Agent/attorney phone number. |
| 59 | `AGENT_ATTORNEY_PHONE_EXT` | VARCHAR | Yes | Agent/attorney phone extension. |
| 60 | `AGENT_ATTORNEY_EMAIL_ADDRESS` | VARCHAR | Yes | Agent/attorney email address. |

### 7. Law Firm & Court Information

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 61 | `LAWFIRM_NAME_BUSINESS_NAME` | VARCHAR | Yes | Name of law firm representing the employer. Form ETA-9035 Section E, Item 15. |
| 62 | `LAWFIRM_BUSINESS_FEIN` | VARCHAR | Yes | Law firm's Federal Employer Identification Number (FEIN from IRS). **NULL for FY2020 ~ FY2025 Q3**; available from FY2025 Q4 onward. Form ETA-9035 Section E, Item 16. |
| 63 | `STATE_OF_HIGHEST_COURT` | VARCHAR | Yes | State of the highest court where the attorney is in good standing. Form ETA-9035 Section E, Item 18. |
| 64 | `NAME_OF_HIGHEST_STATE_COURT` | VARCHAR | Yes | Name of the highest court where the attorney is in good standing. Form ETA-9035 Section E, Item 19. |

### 8. Worksite Information (First Location)

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 65 | `WORKSITE_WORKERS` | INTEGER | Yes | Number of workers placed at the first worksite location. Form ETA-9035 Section F.a., Item 1. |
| 66 | `SECONDARY_ENTITY` | VARCHAR(1) | Yes | Whether workers will be placed with a secondary entity (third-party worksite). `Y` = Yes; `N` = No. Form ETA-9035 Section F.a., Item 2. |
| 67 | `SECONDARY_ENTITY_BUSINESS_NAME` | VARCHAR | Yes | Name of secondary entity where worker(s) will be placed, if applicable. Form ETA-9035 Section F.a., Item 3. |
| 68 | `WORKSITE_ADDRESS1` | VARCHAR | Yes | First worksite street address line 1. Form ETA-9035 Section F.a., Items 4-9. |
| 69 | `WORKSITE_ADDRESS2` | VARCHAR | Yes | First worksite street address line 2. |
| 70 | `WORKSITE_CITY` | VARCHAR | Yes | First worksite city. |
| 71 | `WORKSITE_COUNTY` | VARCHAR | Yes | First worksite county. |
| 72 | `WORKSITE_STATE` | VARCHAR | Yes | First worksite state. |
| 73 | `WORKSITE_POSTAL_CODE` | VARCHAR | Yes | First worksite postal/ZIP code. |

### 9. Wage Information

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 74 | `WAGE_RATE_OF_PAY_FROM` | DECIMAL | No | Wage rate paid to nonimmigrant workers (low end of range). Interpret with `WAGE_UNIT_OF_PAY`. Form ETA-9035 Section F.a., Item 10. |
| 75 | `WAGE_RATE_OF_PAY_TO` | DECIMAL | Yes | Wage rate paid to nonimmigrant workers (high end of range). NULL if single wage (not a range). Form ETA-9035 Section F.a., Item 10. |
| 76 | `WAGE_UNIT_OF_PAY` | VARCHAR | No | Unit of pay for offered wage. Valid values: `Hour`, `Week`, `Bi-Weekly`, `Month`, `Year`. Form ETA-9035 Section F.a., Item 10a. |
| 77 | `PREVAILING_WAGE` | DECIMAL | No | Prevailing wage for the job at the first worksite location. Interpret with `PW_UNIT_OF_PAY`. Form ETA-9035 Section F.a., Item 11. |
| 78 | `PW_UNIT_OF_PAY` | VARCHAR | No | Unit of pay for prevailing wage. Valid values: `Hour`, `Week`, `Bi-Weekly`, `Month`, `Year`. Form ETA-9035 Section F.a., Item 11a. |
| 79 | `PW_TRACKING_NUMBER` | VARCHAR | Yes | DOL prevailing wage determination tracking number, if the employer received a PW from DOL. Form ETA-9035 Section F.a., Item 12a. |
| 80 | `PW_WAGE_LEVEL` | VARCHAR | Yes | OES wage level, if employer independently determined the OES wage. Valid values: `I`, `II`, `III`, `IV`, `N/A`. Form ETA-9035 Section F.a., Item 13a. |
| 81 | `PW_OES_YEAR` | VARCHAR | Yes | Year of the OES prevailing wage survey, if employer independently determined the OES wage. Form ETA-9035 Section F.a., Item 13b. |
| 82 | `PW_OTHER_SOURCE` | VARCHAR | Yes | Alternative prevailing wage source, if not OES. Valid values: `CBA`, `DBA`, `SCA`, `Other/PW Survey`. Form ETA-9035 Section F.a., Item 14a. |
| 83 | `PW_OTHER_YEAR` | VARCHAR | Yes | Year of the alternative prevailing wage source. Form ETA-9035 Section F.a., Item 14b. |
| 84 | `PW_SURVEY_PUBLISHER` | VARCHAR | Yes | Name of the survey producer/publisher, if prevailing wage was from "Other/PW Survey". Form ETA-9035 Section F.a., Item 14c. |
| 85 | `PW_SURVEY_NAME` | VARCHAR | Yes | Name of the prevailing wage survey, if prevailing wage was from "Other/PW Survey". Form ETA-9035 Section F.a., Item 14d. |

### 10. Worksite Totals & Compliance

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 86 | `TOTAL_WORKSITE_LOCATIONS` | INTEGER | Yes | Total number of worksites for this application. Additional worksites beyond the first are in a separate Appendix A file. Form ETA-9035 Section F.a. |
| 87 | `AGREE_TO_LC_STATEMENT` | VARCHAR(1) | No | Employer has read and agrees to Labor Condition Statements. `Y` = Agrees; `N` = Does not agree. Form ETA-9035 Section G, Item 1. |
| 88 | `H-1B_DEPENDENT` | VARCHAR(1) | No | Whether the employer is H-1B dependent. `Y` = Dependent; `N` = Not dependent. Form ETA-9035 Section H.a., Item 1. |
| 89 | `WILLFUL_VIOLATOR` | VARCHAR(1) | No | Whether the employer has been previously found to be a willful violator. `Y` = Yes; `N` = No. Form ETA-9035 Section H.a., Item 2. |
| 90 | `SUPPORT_H1B` | VARCHAR | No | Whether employer will use the LCA only to support exempt H-1B worker petitions. `Y` = Yes; `N` = No; `N/A` = Not applicable. Form ETA-9035 Section H.a., Item 3. |
| 91 | `STATUTORY_BASIS` | VARCHAR | Yes | Basis of the H-1B support exemption. Valid values: `Wage` (based on $60,000+ annual wage), `Degree` (Master's or higher in related specialty), `Both` (wage and degree). Form ETA-9035 Section H.a., Item 4. |
| 92 | `APPENDIX_A_ATTACHED` | VARCHAR | Yes | Whether employer completed Appendix A (additional worksites). `Y` = Yes; `N` = No; `N/A` = Not applicable. Form ETA-9035 Section H.a., Item 5. |
| 93 | `PUBLIC_DISCLOSURE` | VARCHAR | Yes | Location of required public disclosure information. Valid values: `Disclose Business`, `Disclose Employment`, `Disclose Business and Employment`, `N/A`. Form ETA-9035 Section I, Item 1. |

### 11. Preparer Information

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 94 | `PREPARER_LAST_NAME` | VARCHAR | Yes | Last name of person who prepared the LCA on behalf of the employer. Form ETA-9035 Section K, Items 1-5. |
| 95 | `PREPARER_FIRST_NAME` | VARCHAR | Yes | First name of preparer. |
| 96 | `PREPARER_MIDDLE_INITIAL` | VARCHAR | Yes | Middle initial of preparer. |
| 97 | `PREPARER_BUSINESS_NAME` | VARCHAR | Yes | Business name of preparer. |
| 98 | `PREPARER_EMAIL` | VARCHAR | Yes | Email address of preparer. |

### 12. Synthetic / ETL Columns

| # | Column Name | Data Type | Nullable | Description |
|---|-------------|-----------|----------|-------------|
| 99 | `FISCAL_YEAR` | INTEGER | No | **Added during ETL.** Federal fiscal year of the source data file (e.g., 2020, 2021, ..., 2026). Used to identify which annual/quarterly release the record came from. |

---

## Data Availability Matrix

Shows which columns have data vs NULL by fiscal year:

| Column | FY2020 | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | FY2026 |
|--------|--------|--------|--------|--------|--------|--------|--------|
| All 96 base columns | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| `EMPLOYER_FEIN` | NULL | NULL | NULL | NULL | Q4 only | Yes | Yes |
| `LAWFIRM_BUSINESS_FEIN` | NULL | NULL | NULL | NULL | NULL | Q4 only | Yes |

---

## Data Download Strategy

For each fiscal year, use the **latest available quarterly file** (Q4 preferred, as it is cumulative):

| Fiscal Year | Recommended File | Field Count | Notes |
|-------------|-----------------|-------------|-------|
| FY2020 | Annual | 96 | Only file available |
| FY2021 | Q4 / Annual | 96 | Q4 = Annual (identical) |
| FY2022 | Q4 | 96 | |
| FY2023 | Q4 | 96 | |
| FY2024 | Q4 | 97 | Use Q4 to get `EMPLOYER_FEIN` |
| FY2025 | Q4 | 98 | Use Q4 to get `LAWFIRM_BUSINESS_FEIN` |
| FY2026 | Q1 (latest available) | 98 | FY2026 in progress |

---

## Appendix: Legacy Field Mapping (FY2018 & FY2019)

If you need to include FY2018 or FY2019 data in the merged dataset, apply these column renames before union. Fields not listed below have the same name across all eras.

### FY2018 (iCERT Legacy, 52 fields) -> Final Schema

| FY2018 Source Column | Final Schema Column | Mapping Notes |
|----------------------|---------------------|---------------|
| `CASE_SUBMITTED` | `RECEIVED_DATE` | Application receipt date |
| `EMPLOYMENT_START_DATE` | `BEGIN_DATE` | Employment start |
| `EMPLOYMENT_END_DATE` | `END_DATE` | Employment end |
| `SOC_NAME` | `SOC_TITLE` | Occupation title |
| `TOTAL_WORKERS` | `TOTAL_WORKER_POSITIONS` | Total workers requested |
| `EMPLOYER_BUSINESS_DBA` | `TRADE_NAME_DBA` | DBA name |
| `EMPLOYER_ADDRESS` | `EMPLOYER_ADDRESS1` | FY2018 has single address field only |
| `AGENT_ATTORNEY_NAME` | `AGENT_ATTORNEY_LAST_NAME` | FY2018 stores as single combined field; split or keep in last_name |
| `PW_SOURCE` | `PW_OTHER_SOURCE` | PW source (FY2018 includes "OES" as a value; FY2020+ separates OES vs other) |
| `PW_SOURCE_YEAR` | `PW_OES_YEAR` | Combined year field; map to OES year or other year based on PW_SOURCE |
| `PW_SOURCE_OTHER` | `PW_SURVEY_PUBLISHER` | FY2018 combines publisher + survey name |
| `LABOR_CON_AGREE` | `AGREE_TO_LC_STATEMENT` | Labor condition agreement flag |
| `PUBLIC_DISCLOSURE_LOCATION` | `PUBLIC_DISCLOSURE` | Disclosure location |

**FY2018 columns that will be NULL in the final schema** (not present in FY2018 source):
`EMPLOYER_ADDRESS2`, `EMPLOYER_FEIN`, all `EMPLOYER_POC_*` (14 fields), all `PREPARER_*` (5 fields), `SECONDARY_ENTITY`, `SECONDARY_ENTITY_BUSINESS_NAME`, `WORKSITE_ADDRESS1`, `WORKSITE_ADDRESS2`, `WORKSITE_WORKERS`, `PW_TRACKING_NUMBER`, `TOTAL_WORKSITE_LOCATIONS`, `LAWFIRM_NAME_BUSINESS_NAME`, `LAWFIRM_BUSINESS_FEIN`, `STATE_OF_HIGHEST_COURT`, `NAME_OF_HIGHEST_STATE_COURT`, `STATUTORY_BASIS`, `APPENDIX_A_ATTACHED`, `ORIGINAL_CERT_DATE` (exists in FY2018 but listed at end of file rather than in standard position).

### FY2019 (iCERT Expanded, ~260 fields) -> Final Schema

| FY2019 Source Column | Final Schema Column | Mapping Notes |
|----------------------|---------------------|---------------|
| `CASE_SUBMITTED` | `RECEIVED_DATE` | Application receipt date |
| `PERIOD_OF_EMPLOYMENT_START_DATE` | `BEGIN_DATE` | Employment start |
| `PERIOD_OF_EMPLOYMENT_END_DATE` | `END_DATE` | Employment end |
| `EMPLOYER_BUSINESS_DBA` | `TRADE_NAME_DBA` | DBA name |
| `AGENT_ATTORNEY_LAW_FIRM_BUSINESS_NAME` | `LAWFIRM_NAME_BUSINESS_NAME` | Law firm name |

**FY2019 multi-worksite handling**: FY2019 flattens up to 10 worksites into one row with `_1` through `_10` suffixes. For consistency with FY2020+, use only `_1` suffix fields (first worksite) and strip the suffix. Additional worksites (`_2` through `_10`) are dropped.

**FY2019-only field**: `MASTERS_EXEMPTION` — not present in any other fiscal year; drop during merge.

**FY2019 columns that will be NULL in the final schema**: `EMPLOYER_FEIN`, all `EMPLOYER_POC_*` (14 fields), all `PREPARER_*` (5 fields), `TOTAL_WORKSITE_LOCATIONS`, `AGREE_TO_LC_STATEMENT`, `APPENDIX_A_ATTACHED`, `LAWFIRM_BUSINESS_FEIN`.
