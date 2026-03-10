# LCA Data Dictionary Comparison: FY2018 ~ FY2026

## Overview

This document compares the LCA (H-1B, H-1B1, E-3) public disclosure data dictionaries across **all available quarterly and annual PDFs** from fiscal years 2018 through 2026 Q1, published by the U.S. Department of Labor, Office of Foreign Labor Certification (OFLC).

**Source**: https://www.dol.gov/agencies/eta/foreign-labor/performance

---

## PDF Inventory

A total of **27 PDF files** were downloaded and analyzed (25 unique by content, 2 duplicates).

| Fiscal Year | Available PDFs | Notes |
|---|---|---|
| FY2018 | Annual, Q3, Q4 | Annual = Q4 (identical MD5). Q3 also exists. No Q1/Q2 available. |
| FY2019 | Annual only | No quarterly variants exist on the server. |
| FY2020 | Annual only | No quarterly variants exist (older `FY20` naming convention). |
| FY2021 | Annual, Q1, Q2, Q3, Q4 | Annual = Q4 (identical MD5). First year with all 4 quarters. |
| FY2022 | Q1, Q2, Q3, Q4 | No separate annual file. |
| FY2023 | Q1, Q2, Q3, Q4 | No separate annual file. |
| FY2024 | Q1, Q2, Q3, Q4 | No separate annual file. |
| FY2025 | Q1, Q2, Q3, Q4 | No separate annual file. |
| FY2026 | Q1 only | FY2026 is in progress (Q2 not yet published). |

---

## 1. Three Structural Eras

The data dictionaries fall into three distinct structural eras:

| Era | Fiscal Years | System | Field Count | Key Characteristics |
|---|---|---|---|---|
| **iCERT Legacy** | FY2018 | iCERT Visa Portal | 52 | Short field names; single worksite; no POC/Preparer fields |
| **iCERT Expanded** | FY2019 | iCERT Visa Portal | ~260 | 10 worksites flattened into one row with `_1` to `_10` suffixes |
| **FLAG System** | FY2020 ~ FY2026 | FLAG System | 96 ~ 98 | First worksite in main file; additional worksites in separate Appendix A |

### Key Takeaway
- FY2019 is a **transitional year** — its structure differs from both FY2018 and FY2020+.
- FY2020 onward is the **stable baseline**. The schema is nearly identical across these years, with only minor additions over time.

---

## 2. Complete Quarter-by-Quarter Field Count Matrix

Every PDF was read and all field names extracted. Here is the complete matrix:

| Fiscal Year | Quarter | Field Count | Schema Change vs Prior Quarter? |
|---|---|---|---|
| **FY2018** | Q3 | 52 | — |
| **FY2018** | Q4 / Annual | 52 | No change (identical to Q3) |
| **FY2019** | Annual | ~260 | **Major restructure** (iCERT → expanded 10-worksite layout) |
| **FY2020** | Annual | 96 | **Major restructure** (→ FLAG system, single worksite + Appendix A) |
| **FY2021** | Q1 | 96 | No change vs FY2020 |
| **FY2021** | Q2 | 96 | No change |
| **FY2021** | Q3 | 96 | No change |
| **FY2021** | Q4 / Annual | 96 | No change |
| **FY2022** | Q1 | 96 | No change |
| **FY2022** | Q2 | 96 | No change |
| **FY2022** | Q3 | 96 | No change |
| **FY2022** | Q4 | 96 | No change |
| **FY2023** | Q1 | 96 | No change |
| **FY2023** | Q2 | 96 | No change |
| **FY2023** | Q3 | 96 | No change |
| **FY2023** | Q4 | 96 | No change |
| **FY2024** | Q1 | 96 | No change |
| **FY2024** | Q2 | 96 | No change |
| **FY2024** | Q3 | 96 | No change |
| **FY2024** | Q4 | **97** | **+1 field: `EMPLOYER_FEIN` added** |
| **FY2025** | Q1 | 97 | No change vs FY2024 Q4 |
| **FY2025** | Q2 | 97 | No change |
| **FY2025** | Q3 | 97 | No change |
| **FY2025** | Q4 | **98** | **+1 field: `LAWFIRM_BUSINESS_FEIN` added** |
| **FY2026** | Q1 | 98 | No change vs FY2025 Q4 |

### Key Finding: Intra-Year Schema Changes

Schema changes happen **mid-fiscal-year**, not just between fiscal years:

| Change | Exact Timing | Detail |
|---|---|---|
| `EMPLOYER_FEIN` added | Between **FY2024 Q3** and **FY2024 Q4** | Employer FEIN restored to public disclosure (was excluded as PII since FY2020) |
| `LAWFIRM_BUSINESS_FEIN` added | Between **FY2025 Q3** and **FY2025 Q4** | Law firm FEIN added for the first time |

All other quarters within the same fiscal year have **identical schemas** (verified field-by-field).

---

## 3. PII Exclusion Policy Timeline

The "Important Note" at the top of each PDF lists which fields are withheld as PII. This changed over time:

| Period | PII Fields Excluded from Disclosure |
|---|---|
| FY2018 ~ FY2019 | (no explicit PII note in data dictionary) |
| FY2020 ~ FY2024 Q3 | Employer's FEIN, Attorney's FEIN, Attorney's State Bar Number |
| FY2024 Q4 ~ FY2025 Q3 | Attorney's FEIN, Attorney's State Bar Number |
| FY2025 Q4 ~ FY2026 Q1 | Attorney's State Bar Number only |

---

## 4. FY2018 Detail (iCERT Legacy)

### 4a. Complete Field List (52 fields)

```
CASE_NUMBER, CASE_STATUS, CASE_SUBMITTED, DECISION_DATE, VISA_CLASS,
EMPLOYMENT_START_DATE, EMPLOYMENT_END_DATE, EMPLOYER_NAME,
EMPLOYER_BUSINESS_DBA, EMPLOYER_ADDRESS, EMPLOYER_CITY, EMPLOYER_STATE,
EMPLOYER_POSTAL_CODE, EMPLOYER_COUNTRY, EMPLOYER_PROVINCE, EMPLOYER_PHONE,
EMPLOYER_PHONE_EXT, AGENT_REPRESENTING_EMPLOYER, AGENT_ATTORNEY_NAME,
AGENT_ATTORNEY_CITY, AGENT_ATTORNEY_STATE, JOB_TITLE, SOC_CODE, SOC_NAME,
NAICS_CODE, TOTAL_WORKERS, NEW_EMPLOYMENT, CONTINUED_EMPLOYMENT,
CHANGE_PREVIOUS_EMPLOYMENT, NEW_CONCURRENT_EMPLOYMENT, CHANGE_EMPLOYER,
AMENDED_PETITION, FULL_TIME_POSITION, PREVAILING_WAGE, PW_UNIT_OF_PAY,
PW_WAGE_LEVEL, PW_SOURCE, PW_SOURCE_YEAR, PW_SOURCE_OTHER,
WAGE_RATE_OF_PAY_FROM, WAGE_RATE_OF_PAY_TO, WAGE_UNIT_OF_PAY,
H-1B_DEPENDENT, WILLFUL_VIOLATOR, SUPPORT_H1B, LABOR_CON_AGREE,
PUBLIC_DISCLOSURE_LOCATION, WORKSITE_CITY, WORKSITE_COUNTY, WORKSITE_STATE,
WORKSITE_POSTAL_CODE, ORIGINAL_CERT_DATE
```

### 4b. Quarterly Comparison
- **Q3 vs Q4/Annual**: Identical (52 fields, same names, same order). Only the reporting period end date differs.

### 4c. Field Name Mapping to FY2020+

| FY2018 Field Name | FY2020+ Equivalent | Notes |
|---|---|---|
| `CASE_SUBMITTED` | `RECEIVED_DATE` | Application receipt date |
| `EMPLOYMENT_START_DATE` | `BEGIN_DATE` | Employment start |
| `EMPLOYMENT_END_DATE` | `END_DATE` | Employment end |
| `SOC_NAME` | `SOC_TITLE` | Occupation title |
| `TOTAL_WORKERS` | `TOTAL_WORKER_POSITIONS` | Number of workers requested |
| `EMPLOYER_BUSINESS_DBA` | `TRADE_NAME_DBA` | DBA name |
| `EMPLOYER_ADDRESS` | `EMPLOYER_ADDRESS1` | FY18 has single address field (no ADDRESS2) |
| `AGENT_ATTORNEY_NAME` | Split: `AGENT_ATTORNEY_LAST_NAME` / `FIRST_NAME` / `MIDDLE_NAME` | FY18 combined as one field |
| `PW_SOURCE` | `PW_OTHER_SOURCE` | Prevailing wage source |
| `PW_SOURCE_YEAR` | `PW_OES_YEAR` / `PW_OTHER_YEAR` | FY18 combined as one field |
| `PW_SOURCE_OTHER` | `PW_SURVEY_PUBLISHER` + `PW_SURVEY_NAME` | FY18 combined as one field |
| `LABOR_CON_AGREE` | `AGREE_TO_LC_STATEMENT` | LC agreement flag |
| `PUBLIC_DISCLOSURE_LOCATION` | `PUBLIC_DISCLOSURE` | Disclosure method |

### 4d. Fields in FY2020+ but NOT in FY2018
- `EMPLOYER_ADDRESS2`, `EMPLOYER_FEIN`
- All `EMPLOYER_POC_*` fields (14 fields)
- All `PREPARER_*` fields (5 fields)
- `SECONDARY_ENTITY`, `SECONDARY_ENTITY_BUSINESS_NAME`
- `WORKSITE_ADDRESS1`, `WORKSITE_ADDRESS2` (FY18 has no worksite address, only city/county/state/zip)
- `WORKSITE_WORKERS`
- `PW_TRACKING_NUMBER`
- `TOTAL_WORKSITE_LOCATIONS`
- `LAWFIRM_NAME_BUSINESS_NAME`, `LAWFIRM_BUSINESS_FEIN`
- `STATE_OF_HIGHEST_COURT`, `NAME_OF_HIGHEST_STATE_COURT`
- `STATUTORY_BASIS`, `APPENDIX_A_ATTACHED`

---

## 5. FY2019 Detail (iCERT Expanded)

### 5a. Worksite Flattening
- Contains fields for **10 worksites** in a single row, each with `_1` through `_10` suffix
- Each worksite has 21 fields (address, wage, prevailing wage, etc.)
- This accounts for 210 of the ~260 total fields
- Only annual file exists (no quarterly variants)

### 5b. Core Fields (non-worksite, 50 fields)

```
CASE_NUMBER, CASE_STATUS, CASE_SUBMITTED, DECISION_DATE, ORIGINAL_CERT_DATE,
VISA_CLASS, JOB_TITLE, SOC_CODE, SOC_TITLE, FULL_TIME_POSITION,
PERIOD_OF_EMPLOYMENT_START_DATE, PERIOD_OF_EMPLOYMENT_END_DATE,
TOTAL_WORKER_POSITIONS, NEW_EMPLOYMENT, CONTINUED_EMPLOYMENT,
CHANGE_PREVIOUS_EMPLOYMENT, NEW_CONCURRENT_EMPLOYMENT, CHANGE_EMPLOYER,
AMENDED_PETITION, EMPLOYER_NAME, EMPLOYER_BUSINESS_DBA,
EMPLOYER_ADDRESS1, EMPLOYER_ADDRESS2, EMPLOYER_CITY, EMPLOYER_STATE,
EMPLOYER_POSTAL_CODE, EMPLOYER_COUNTRY, EMPLOYER_PROVINCE, EMPLOYER_PHONE,
EMPLOYER_PHONE_EXT, NAICS_CODE, AGENT_REPRESENTING_EMPLOYER,
AGENT_ATTORNEY_LAW_FIRM_BUSINESS_NAME, AGENT_ATTORNEY_ADDRESS1,
AGENT_ATTORNEY_ADDRESS2, AGENT_ATTORNEY_CITY, AGENT_ATTORNEY_STATE,
AGENT_ATTORNEY_POSTAL_CODE, AGENT_ATTORNEY_COUNTRY, AGENT_ATTORNEY_PROVINCE,
AGENT_ATTORNEY_PHONE, AGENT_ATTORNEY_PHONE_EXT, STATE_OF_HIGHEST_COURT,
NAME_OF_HIGHEST_STATE_COURT,
[... worksite fields _1 through _10 ...],
H-1B_DEPENDENT, WILLFUL_VIOLATOR, SUPPORT_H1B, STATUTORY_BASIS,
MASTERS_EXEMPTION, PUBLIC_DISCLOSURE
```

### 5c. FY2019-Specific Field Name Differences (vs FY2020+)

| FY2019 Field Name | FY2020+ Equivalent |
|---|---|
| `CASE_SUBMITTED` | `RECEIVED_DATE` |
| `PERIOD_OF_EMPLOYMENT_START_DATE` | `BEGIN_DATE` |
| `PERIOD_OF_EMPLOYMENT_END_DATE` | `END_DATE` |
| `EMPLOYER_BUSINESS_DBA` | `TRADE_NAME_DBA` |
| `AGENT_ATTORNEY_LAW_FIRM_BUSINESS_NAME` | `LAWFIRM_NAME_BUSINESS_NAME` |
| `PW_NON-OES_YEAR_N` | `PW_OTHER_YEAR` |
| Worksite fields suffixed `_1` to `_10` | No suffix (single worksite in main file) |

### 5d. FY2019-Only Fields
- `MASTERS_EXEMPTION` — not present in any other fiscal year

### 5e. Fields Missing in FY2019 (present in FY2020+)
- `EMPLOYER_FEIN`
- All `EMPLOYER_POC_*` fields (14 fields)
- All `PREPARER_*` fields (5 fields)
- `TOTAL_WORKSITE_LOCATIONS`
- `AGREE_TO_LC_STATEMENT`
- `APPENDIX_A_ATTACHED`
- `LAWFIRM_BUSINESS_FEIN`

---

## 6. FY2020 ~ FY2026 Detail (FLAG System)

### 6a. Base Schema (96 fields — FY2020 through FY2024 Q3)

This is the stable baseline that persisted for 4.5 fiscal years without change:

```
CASE_NUMBER, CASE_STATUS, RECEIVED_DATE, DECISION_DATE, ORIGINAL_CERT_DATE,
VISA_CLASS, JOB_TITLE, SOC_CODE, SOC_TITLE, FULL_TIME_POSITION,
BEGIN_DATE, END_DATE, TOTAL_WORKER_POSITIONS, NEW_EMPLOYMENT,
CONTINUED_EMPLOYMENT, CHANGE_PREVIOUS_EMPLOYMENT, NEW_CONCURRENT_EMPLOYMENT,
CHANGE_EMPLOYER, AMENDED_PETITION, EMPLOYER_NAME, TRADE_NAME_DBA,
EMPLOYER_ADDRESS1, EMPLOYER_ADDRESS2, EMPLOYER_CITY, EMPLOYER_STATE,
EMPLOYER_POSTAL_CODE, EMPLOYER_COUNTRY, EMPLOYER_PROVINCE, EMPLOYER_PHONE,
EMPLOYER_PHONE_EXT, NAICS_CODE, EMPLOYER_POC_LAST_NAME,
EMPLOYER_POC_FIRST_NAME, EMPLOYER_POC_MIDDLE_NAME, EMPLOYER_POC_JOB_TITLE,
EMPLOYER_POC_ADDRESS1, EMPLOYER_POC_ADDRESS2, EMPLOYER_POC_CITY,
EMPLOYER_POC_STATE, EMPLOYER_POC_POSTAL_CODE, EMPLOYER_POC_COUNTRY,
EMPLOYER_POC_PROVINCE, EMPLOYER_POC_PHONE, EMPLOYER_POC_PHONE_EXT,
EMPLOYER_POC_EMAIL, AGENT_REPRESENTING_EMPLOYER, AGENT_ATTORNEY_LAST_NAME,
AGENT_ATTORNEY_FIRST_NAME, AGENT_ATTORNEY_MIDDLE_NAME,
AGENT_ATTORNEY_ADDRESS1, AGENT_ATTORNEY_ADDRESS2, AGENT_ATTORNEY_CITY,
AGENT_ATTORNEY_STATE, AGENT_ATTORNEY_POSTAL_CODE, AGENT_ATTORNEY_COUNTRY,
AGENT_ATTORNEY_PROVINCE, AGENT_ATTORNEY_PHONE, AGENT_ATTORNEY_PHONE_EXT,
AGENT_ATTORNEY_EMAIL_ADDRESS, LAWFIRM_NAME_BUSINESS_NAME,
STATE_OF_HIGHEST_COURT, NAME_OF_HIGHEST_STATE_COURT, WORKSITE_WORKERS,
SECONDARY_ENTITY, SECONDARY_ENTITY_BUSINESS_NAME, WORKSITE_ADDRESS1,
WORKSITE_ADDRESS2, WORKSITE_CITY, WORKSITE_COUNTY, WORKSITE_STATE,
WORKSITE_POSTAL_CODE, WAGE_RATE_OF_PAY_FROM, WAGE_RATE_OF_PAY_TO,
WAGE_UNIT_OF_PAY, PREVAILING_WAGE, PW_UNIT_OF_PAY, PW_TRACKING_NUMBER,
PW_WAGE_LEVEL, PW_OES_YEAR, PW_OTHER_SOURCE, PW_OTHER_YEAR,
PW_SURVEY_PUBLISHER, PW_SURVEY_NAME, TOTAL_WORKSITE_LOCATIONS,
AGREE_TO_LC_STATEMENT, H-1B_DEPENDENT, WILLFUL_VIOLATOR, SUPPORT_H1B,
STATUTORY_BASIS, APPENDIX_A_ATTACHED, PUBLIC_DISCLOSURE,
PREPARER_LAST_NAME, PREPARER_FIRST_NAME, PREPARER_MIDDLE_INITIAL,
PREPARER_BUSINESS_NAME, PREPARER_EMAIL
```

### 6b. Incremental Additions

| Field Added | Inserted After | First Appearance | Field Count After |
|---|---|---|---|
| `EMPLOYER_FEIN` | `EMPLOYER_PHONE_EXT` (before `NAICS_CODE`) | **FY2024 Q4** | 97 |
| `LAWFIRM_BUSINESS_FEIN` | `LAWFIRM_NAME_BUSINESS_NAME` (before `STATE_OF_HIGHEST_COURT`) | **FY2025 Q4** | 98 |

### 6c. Full Quarterly Stability Verification

| Fiscal Year | Intra-Year Change? | Detail |
|---|---|---|
| FY2020 | N/A | Single annual file only |
| FY2021 | **No** | Q1 = Q2 = Q3 = Q4 = Annual (all 96 fields, identical) |
| FY2022 | **No** | Q1 = Q2 = Q3 = Q4 (all 96 fields, identical) |
| FY2023 | **No** | Q1 = Q2 = Q3 = Q4 (all 96 fields, identical) |
| FY2024 | **Yes** | Q1 = Q2 = Q3 (96 fields); **Q4 = 97 fields** (+`EMPLOYER_FEIN`) |
| FY2025 | **Yes** | Q1 = Q2 = Q3 (97 fields); **Q4 = 98 fields** (+`LAWFIRM_BUSINESS_FEIN`) |
| FY2026 | N/A | Only Q1 available so far (98 fields) |

### 6d. Minor Anomalies Found in PDFs

| PDF | Anomaly |
|---|---|
| FY2022 Q2 | Reporting period end date typo: says "March 31, **2021**" (should be 2022) |
| FY2023 Q2 | Reporting period end date typo: says "March 31, **2003**" (should be 2023) |

These are typos in the DOL source PDFs; the field structures are correct.

---

## 7. Recommended Union Schema

### 7a. Target Schema: Use FY2025 Q4 / FY2026 Q1 as Baseline
Use the 98-field schema as the canonical target, since it is the most complete.

### 7b. Columns Safe to Drop (Low analytical value)

**Employer Point of Contact (14 fields)** — internal contact info:
- `EMPLOYER_POC_LAST_NAME`, `EMPLOYER_POC_FIRST_NAME`, `EMPLOYER_POC_MIDDLE_NAME`
- `EMPLOYER_POC_JOB_TITLE`
- `EMPLOYER_POC_ADDRESS1`, `EMPLOYER_POC_ADDRESS2`, `EMPLOYER_POC_CITY`
- `EMPLOYER_POC_STATE`, `EMPLOYER_POC_POSTAL_CODE`, `EMPLOYER_POC_COUNTRY`, `EMPLOYER_POC_PROVINCE`
- `EMPLOYER_POC_PHONE`, `EMPLOYER_POC_PHONE_EXT`, `EMPLOYER_POC_EMAIL`

**Agent/Attorney Contact Details (~10 fields)** — lawyer contact info:
- `AGENT_ATTORNEY_ADDRESS1`, `AGENT_ATTORNEY_ADDRESS2`, `AGENT_ATTORNEY_CITY`
- `AGENT_ATTORNEY_STATE`, `AGENT_ATTORNEY_POSTAL_CODE`, `AGENT_ATTORNEY_COUNTRY`, `AGENT_ATTORNEY_PROVINCE`
- `AGENT_ATTORNEY_PHONE`, `AGENT_ATTORNEY_PHONE_EXT`, `AGENT_ATTORNEY_EMAIL_ADDRESS`

**Attorney Name Fields (3 fields)**:
- `AGENT_ATTORNEY_LAST_NAME`, `AGENT_ATTORNEY_FIRST_NAME`, `AGENT_ATTORNEY_MIDDLE_NAME`

**Preparer Fields (5 fields)**:
- `PREPARER_LAST_NAME`, `PREPARER_FIRST_NAME`, `PREPARER_MIDDLE_INITIAL`
- `PREPARER_BUSINESS_NAME`, `PREPARER_EMAIL`

**Court/Law Firm Fields (4 fields)**:
- `STATE_OF_HIGHEST_COURT`, `NAME_OF_HIGHEST_STATE_COURT`
- `LAWFIRM_NAME_BUSINESS_NAME`, `LAWFIRM_BUSINESS_FEIN`

**Other Low-Value Fields (2 fields)**:
- `AGREE_TO_LC_STATEMENT` — almost always "Y"
- `PUBLIC_DISCLOSURE` — disclosure method, not analytically useful

**Total droppable: ~38 fields**

### 7c. Core Columns to Keep (~40 fields)

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
- `EMPLOYER_FEIN` — NULL for FY2018~FY2024 Q3; available from FY2024 Q4+
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

### 7d. Handling FY2019 Multi-Worksite Data
For the union, two options:
1. **Option A (Simple)**: Only keep `_1` suffix fields from FY2019 (first worksite), drop `_2` through `_10`. This matches how FY2020+ stores data (first worksite in main file, rest in Appendix A).
2. **Option B (Complete)**: Unpivot FY2019's `_1` to `_10` worksite fields into separate rows, similar to how FY2020+ Appendix A works. This preserves all worksite data.

**Recommendation**: Option A for simplicity. The vast majority of LCA applications have only 1 worksite.

---

## 8. Additional Notes

### 8a. Appendix A & Worksite Files (FY2020+)
Starting FY2020, DOL publishes three separate files per quarter:
- **LCA_Disclosure_Data** — main file (one row per case, first worksite only)
- **LCA_Appendix_A** — additional worksites beyond the first
- **LCA_Worksites** — all worksites including the first

For a union of the main disclosure data, only the main file is needed.

### 8b. Form Version
- FY2018~FY2019: Forms ETA-9035 & 9035E (iCERT system)
- FY2020+: Form ETA-9035 only (electronic filing standardized via FLAG)

### 8c. Cumulative Reporting Periods
Each quarterly PDF's reporting period is **cumulative** from October 1 through end of that quarter:
- Q1: Oct 1 – Dec 31
- Q2: Oct 1 – Mar 31
- Q3: Oct 1 – Jun 30
- Q4: Oct 1 – Sep 30

This means Q4 data is a superset that includes all cases from Q1–Q3. When downloading actual data, you only need the **Q4 (or latest available) file** for each fiscal year to get the complete year's data.

### 8d. Data Download Strategy
When downloading data files for the union:
- **FY2024**: Use Q4 file (it has `EMPLOYER_FEIN`; Q1-Q3 files do not)
- **FY2025**: Use Q4 file (it has `LAWFIRM_BUSINESS_FEIN`; Q1-Q3 files do not)
- **FY2026**: Use Q1 file (only one available; Q4 data is cumulative so future Q4 will supersede)
- For all other years: Any available file works (schema is identical across quarters)
