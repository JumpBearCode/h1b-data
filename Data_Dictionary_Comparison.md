# LCA Data Dictionary Comparison: FY2018 ~ FY2026

## Overview

This document compares the LCA (H-1B, H-1B1, E-3) public disclosure data dictionaries across fiscal years 2018 through 2026 Q1, published by the U.S. Department of Labor, Office of Foreign Labor Certification (OFLC).

**Source**: https://www.dol.gov/agencies/eta/foreign-labor/performance

**PDF files analyzed**:

| File | Fiscal Year | Size |
|---|---|---|
| H-1B_FY18_Record_Layout.pdf | FY2018 | 53K |
| H-1B_FY19_Record_Layout.pdf | FY2019 | 436K |
| LCA_Record_Layout_FY20.pdf | FY2020 | 405K |
| LCA_Record_Layout_FY2021.pdf | FY2021 | 164K |
| LCA_Record_Layout_FY2022_Q4.pdf | FY2022 | 167K |
| LCA_Record_Layout_FY2023_Q4.pdf | FY2023 | 169K |
| LCA_Record_Layout_FY2024_Q4.pdf | FY2024 | 167K |
| LCA_Record_Layout_FY2025_Q4.pdf | FY2025 | 168K |
| LCA_Record_Layout_FY2026_Q1.pdf | FY2026 | 167K |

---

## 1. Three Structural Eras

The data dictionaries fall into three distinct structural eras:

| Era | Fiscal Years | System | Approx. Field Count | Key Characteristics |
|---|---|---|---|---|
| **iCERT Legacy** | FY2018 | iCERT Visa Portal | ~52 | Short field names; single worksite only; no POC/Preparer fields |
| **iCERT Expanded** | FY2019 | iCERT Visa Portal | ~260 | All 10 worksites flattened into one row with `_1` to `_10` suffixes |
| **FLAG System** | FY2020 ~ FY2026 | FLAG System | ~96-98 | Only first worksite in main file; additional worksites in separate Appendix A file |

### Key Takeaway
- FY2019 is a **transitional year** — its structure differs from both FY2018 and FY2020+.
- FY2020 onward is the **stable baseline**. The schema is nearly identical across these years.

---

## 2. FY2018 Field Name Mapping

FY2018 uses different field names that must be renamed to align with later years:

| FY2018 Field Name | FY2020+ Equivalent | Notes |
|---|---|---|
| `CASE_SUBMITTED` | `RECEIVED_DATE` | Application receipt date |
| `EMPLOYMENT_START_DATE` | `BEGIN_DATE` | Employment start |
| `EMPLOYMENT_END_DATE` | `END_DATE` | Employment end |
| `SOC_NAME` | `SOC_TITLE` | Occupation title |
| `TOTAL_WORKERS` | `TOTAL_WORKER_POSITIONS` | Number of workers requested |
| `EMPLOYER_BUSINESS_DBA` | `TRADE_NAME_DBA` | DBA name |
| `EMPLOYER_ADDRESS` | `EMPLOYER_ADDRESS1` | FY18 has single address field |
| `AGENT_ATTORNEY_NAME` | Split into `AGENT_ATTORNEY_LAST_NAME` / `FIRST_NAME` / `MIDDLE_NAME` | FY18 combined as one field |
| `WORKSITE_ADDRESS` | `WORKSITE_ADDRESS1` | Single address field |
| `PW_SOURCE` | `PW_OTHER_SOURCE` | Prevailing wage source |
| `PW_SOURCE_YEAR` | `PW_OES_YEAR` / `PW_OTHER_YEAR` | FY18 combined as one field |
| `PW_SOURCE_OTHER` | `PW_SURVEY_PUBLISHER` + `PW_SURVEY_NAME` | FY18 combined as one field |
| `LABOR_CON_AGREE` | `AGREE_TO_LC_STATEMENT` | LC agreement flag |
| `PUBLIC_DISCLOSURE_LOCATION` | `PUBLIC_DISCLOSURE` | Disclosure method |

### Fields present in FY2018 but NOT in FY2020+:
- `EMPLOYER_ADDRESS2` (not present in FY2018 — only one address line)
- No `EMPLOYER_POC_*` fields
- No `PREPARER_*` fields

### Fields in FY2020+ but NOT in FY2018:
- `ORIGINAL_CERT_DATE`
- `EMPLOYER_ADDRESS2`
- `EMPLOYER_FEIN` (varies, see Section 4)
- All `EMPLOYER_POC_*` fields (14 fields)
- All `PREPARER_*` fields (5 fields)
- `SECONDARY_ENTITY`, `SECONDARY_ENTITY_BUSINESS_NAME`
- `WORKSITE_COUNTY`
- `PW_TRACKING_NUMBER`
- `TOTAL_WORKSITE_LOCATIONS`
- `LAWFIRM_NAME_BUSINESS_NAME`, `LAWFIRM_BUSINESS_FEIN`
- `STATE_OF_HIGHEST_COURT`, `NAME_OF_HIGHEST_STATE_COURT`

---

## 3. FY2019 Specifics

FY2019 is unique in several ways:

### 3a. Worksite Flattening
- Contains fields for **10 worksites** in a single row, each with `_1` through `_10` suffix
- Each worksite has 21 fields (address, wage, prevailing wage, etc.)
- This accounts for 210 of the 260 total fields

### 3b. FY2019-Specific Field Name Differences (vs FY2020+)
| FY2019 Field Name | FY2020+ Equivalent |
|---|---|
| `PERIOD_OF_EMPLOYMENT_START_DATE` | `BEGIN_DATE` |
| `PERIOD_OF_EMPLOYMENT_END_DATE` | `END_DATE` |
| `EMPLOYER_BUSINESS_DBA` | `TRADE_NAME_DBA` |
| `AGENT_ATTORNEY_LAW_FIRM_BUSINESS_NAME` | `LAWFIRM_NAME_BUSINESS_NAME` |
| `PW_NON-OES_YEAR_N` | `PW_OTHER_YEAR` |

### 3c. FY2019-Only Fields
- `MASTERS_EXEMPTION` — not present in any other fiscal year

### 3d. Fields Missing in FY2019 (present in FY2020+)
- `EMPLOYER_FEIN`
- All `EMPLOYER_POC_*` fields
- All `PREPARER_*` fields
- `ORIGINAL_CERT_DATE`
- `TOTAL_WORKSITE_LOCATIONS`
- `LAWFIRM_BUSINESS_FEIN`

---

## 4. FY2020 ~ FY2026 Micro-Differences

The FLAG-era years (FY2020 ~ FY2026) share an almost identical schema (~96-98 fields). The only differences are:

| Field | FY2020 | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | FY2026 |
|---|---|---|---|---|---|---|---|
| `EMPLOYER_FEIN` | Missing | Missing | Missing | Missing | **Present** | Present | Present |
| `LAWFIRM_BUSINESS_FEIN` | Missing | Missing | Missing | Missing | Missing | **Present** | Present |

### Explanation
- **FY2020 ~ FY2023**: `EMPLOYER_FEIN` was excluded from public disclosure due to PII concerns.
- **FY2024**: `EMPLOYER_FEIN` was restored to the public disclosure file.
- **FY2025**: `LAWFIRM_BUSINESS_FEIN` was added for the first time.

All other fields remain identical in name, order, and description across FY2020 ~ FY2026.

---

## 5. Recommended Union Schema

### 5a. Target Schema: Use FY2026 as Baseline
Use the FY2026 Q1 field list (~98 fields) as the canonical schema, since it is the most complete.

### 5b. Columns Safe to Drop (Low analytical value)

**Employer Point of Contact (14 fields)** — internal contact info, not useful for analysis:
- `EMPLOYER_POC_LAST_NAME`, `EMPLOYER_POC_FIRST_NAME`, `EMPLOYER_POC_MIDDLE_NAME`
- `EMPLOYER_POC_JOB_TITLE`
- `EMPLOYER_POC_ADDRESS1`, `EMPLOYER_POC_ADDRESS2`, `EMPLOYER_POC_CITY`
- `EMPLOYER_POC_STATE`, `EMPLOYER_POC_POSTAL_CODE`, `EMPLOYER_POC_COUNTRY`, `EMPLOYER_POC_PROVINCE`
- `EMPLOYER_POC_PHONE`, `EMPLOYER_POC_PHONE_EXT`, `EMPLOYER_POC_EMAIL`

**Agent/Attorney Contact Details (~10 fields)** — lawyer contact info:
- `AGENT_ATTORNEY_ADDRESS1`, `AGENT_ATTORNEY_ADDRESS2`, `AGENT_ATTORNEY_CITY`
- `AGENT_ATTORNEY_STATE`, `AGENT_ATTORNEY_POSTAL_CODE`, `AGENT_ATTORNEY_COUNTRY`, `AGENT_ATTORNEY_PROVINCE`
- `AGENT_ATTORNEY_PHONE`, `AGENT_ATTORNEY_PHONE_EXT`, `AGENT_ATTORNEY_EMAIL_ADDRESS`

**Attorney Name Fields (3 fields)** — individual attorney names:
- `AGENT_ATTORNEY_LAST_NAME`, `AGENT_ATTORNEY_FIRST_NAME`, `AGENT_ATTORNEY_MIDDLE_NAME`

**Preparer Fields (5 fields)** — form preparer info:
- `PREPARER_LAST_NAME`, `PREPARER_FIRST_NAME`, `PREPARER_MIDDLE_INITIAL`
- `PREPARER_BUSINESS_NAME`, `PREPARER_EMAIL`

**Court/Law Firm Fields (4 fields)**:
- `STATE_OF_HIGHEST_COURT`, `NAME_OF_HIGHEST_STATE_COURT`
- `LAWFIRM_NAME_BUSINESS_NAME`, `LAWFIRM_BUSINESS_FEIN`

**Other Low-Value Fields (2 fields)**:
- `AGREE_TO_LC_STATEMENT` — almost always "Y"
- `PUBLIC_DISCLOSURE` — disclosure method, not analytically useful

**Total droppable: ~38 fields**

### 5c. Core Columns to Keep (~40 fields)

#### Case Information
- `CASE_NUMBER` — unique identifier
- `CASE_STATUS` — Certified / Certified-Withdrawn / Denied / Withdrawn
- `RECEIVED_DATE` — application receipt date
- `DECISION_DATE` — determination date
- `ORIGINAL_CERT_DATE` — original cert date (for Certified-Withdrawn)
- `VISA_CLASS` — H-1B / E-3 Australian / H-1B1 Chile / H-1B1 Singapore

#### Job Information
- `JOB_TITLE` — job title
- `SOC_CODE` — Standard Occupational Classification code
- `SOC_TITLE` — occupation title
- `FULL_TIME_POSITION` — Y/N
- `BEGIN_DATE` — employment start date
- `END_DATE` — employment end date

#### Worker Counts & Petition Type
- `TOTAL_WORKER_POSITIONS` — total foreign workers requested
- `NEW_EMPLOYMENT`
- `CONTINUED_EMPLOYMENT`
- `CHANGE_PREVIOUS_EMPLOYMENT`
- `NEW_CONCURRENT_EMPLOYMENT`
- `CHANGE_EMPLOYER`
- `AMENDED_PETITION`

#### Employer Information
- `EMPLOYER_NAME`
- `TRADE_NAME_DBA`
- `EMPLOYER_ADDRESS1`, `EMPLOYER_ADDRESS2`
- `EMPLOYER_CITY`, `EMPLOYER_STATE`, `EMPLOYER_POSTAL_CODE`, `EMPLOYER_COUNTRY`
- `EMPLOYER_PHONE`
- `EMPLOYER_FEIN` — may be NULL for FY2018-FY2023
- `NAICS_CODE`

#### Worksite (First Location Only)
- `WORKSITE_WORKERS`
- `SECONDARY_ENTITY` — Y/N, placed with third party
- `SECONDARY_ENTITY_BUSINESS_NAME`
- `WORKSITE_ADDRESS1`, `WORKSITE_ADDRESS2`
- `WORKSITE_CITY`, `WORKSITE_COUNTY`, `WORKSITE_STATE`, `WORKSITE_POSTAL_CODE`

#### Wage & Prevailing Wage
- `WAGE_RATE_OF_PAY_FROM` — actual wage (low end)
- `WAGE_RATE_OF_PAY_TO` — actual wage (high end)
- `WAGE_UNIT_OF_PAY` — Hour / Week / Bi-Weekly / Month / Year
- `PREVAILING_WAGE` — prevailing wage for the area
- `PW_UNIT_OF_PAY` — prevailing wage unit
- `PW_TRACKING_NUMBER` — DOL prevailing wage tracking number
- `PW_WAGE_LEVEL` — I / II / III / IV / N/A
- `PW_OES_YEAR` — OES wage survey year
- `PW_OTHER_SOURCE` — CBA / DBA / SCA / Other
- `PW_OTHER_YEAR`
- `PW_SURVEY_PUBLISHER`
- `PW_SURVEY_NAME`
- `TOTAL_WORKSITE_LOCATIONS`

#### H-1B Compliance
- `H-1B_DEPENDENT` — employer is H-1B dependent (Y/N)
- `WILLFUL_VIOLATOR` — previous willful violator (Y/N)
- `SUPPORT_H1B` — supports exempt H-1B workers (Y/N/N/A)
- `STATUTORY_BASIS` — Wage / Degree / Both
- `APPENDIX_A_ATTACHED` — Y/N/N/A

#### Agent Representation (keep flag only)
- `AGENT_REPRESENTING_EMPLOYER` — Y/N

### 5d. Handling FY2019 Multi-Worksite Data
For the union, two options:
1. **Option A (Simple)**: Only keep `_1` suffix fields from FY2019 (first worksite), drop `_2` through `_10`. This matches how FY2020+ stores data (first worksite in main file, rest in Appendix A).
2. **Option B (Complete)**: Unpivot FY2019's `_1` to `_10` worksite fields into separate rows, similar to how FY2020+ Appendix A works. This preserves all worksite data.

**Recommendation**: Option A for simplicity. The vast majority of LCA applications have only 1 worksite.

---

## 6. Additional Notes

### 6a. Appendix A & Worksite Files (FY2020+)
Starting FY2020, DOL publishes three separate files per quarter:
- **LCA_Disclosure_Data** — main file (one row per case, first worksite only)
- **LCA_Appendix_A** — additional worksites beyond the first (one row per worksite)
- **LCA_Worksites** — all worksites including the first (one row per worksite)

For a union of the main disclosure data, only the main file is needed.

### 6b. Form Version
- FY2018-FY2019: Forms ETA-9035 & 9035E
- FY2020+: Form ETA-9035 only (electronic filing standardized via FLAG)

### 6c. PII Exclusions (Across All Years)
All years exclude certain PII fields:
- Attorney's FEIN (excluded FY2020-FY2024; included FY2025+)
- Attorney's State Bar Number (always excluded)
- `EMPLOYER_FEIN` was excluded FY2020-FY2023, restored FY2024+
