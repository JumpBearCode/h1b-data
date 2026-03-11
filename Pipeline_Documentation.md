# H1B LCA Data Pipeline: End-to-End Documentation

## Overview

This pipeline ingests DOL (Department of Labor) LCA (Labor Condition Application) disclosure data from CSV files into PostgreSQL, organized in a three-layer architecture:

```
CSV Files (Raw_CSV/)  →  raw schema (TEXT)  →  processed schema (typed + cleaned)  →  refined schema (38 cols, deduplicated by FY)
```

**Database**: `h1b` on `192.168.31.61:5432`
**Fiscal Years**: FY2020 Q1 through FY2026 Q1 (25 quarterly tables)
**Total raw rows**: 9,472,472
**Total processed rows**: 3,915,039 (5,557,433 empty rows removed)
**Total refined rows**: 3,514,878 (400,161 cross-quarter duplicates removed)
**Unique employers**: 214,366

---

## Stage 1: CSV → Raw

### What the raw layer stores

- **Exact copy of source CSV data**, all 98 columns stored as `TEXT`.
- One table per quarterly CSV file (25 tables total in `raw` schema).
- Column names normalized to lowercase (e.g., `H-1B_DEPENDENT` → `h1b_dependent`).
- No filtering — empty rows from DOL source files are preserved as-is.
- Unified 98-column superset schema: columns not present in older CSVs are `NULL`.

### Source files

| Fiscal Year | Quarters | Source Format | Column Count |
|-------------|----------|---------------|:------------:|
| FY2020 | Q1–Q3 | XLSX → CSV (converted via `openpyxl`) | 96 |
| FY2020 | Q4 | CSV (direct download) | 96 |
| FY2021–FY2023 | Q1–Q4 each | CSV (direct download) | 96 |
| FY2024 Q1–FY2025 Q1 | 5 quarters | CSV | 97 (`employer_fein` added) |
| FY2025 Q2–FY2026 Q1 | 4 quarters | CSV | 98 (`lawfirm_business_fein` added) |

### Column name normalization

The import script normalizes known CSV header variants:

| CSV Header Variants | Canonical Name |
|---------------------|---------------|
| `H-1B_DEPENDENT`, `H1B_DEPENDENT`, `H_1B_DEPENDENT` | `h1b_dependent` |
| `EMPLOYER_POC_ADDRESS_1` | `employer_poc_address1` |
| `EMPLOYER_POC_ADDRESS_2` | `employer_poc_address2` |

### How to run

```bash
# 1. Create database, schema, and tables
uv run python src/setup_database.py

# 2. Import CSV files into raw tables
uv run python src/import_csv.py
```

### Code files

| File | Purpose |
|------|---------|
| `src/db_connector.py` | PostgreSQL connection management |
| `src/setup_database.py` | Creates database `h1b`, schema `raw`, all tables |
| `src/import_csv.py` | Reads CSVs, normalizes headers, bulk loads via `COPY` |
| `sql/01_create_database.sql` | `CREATE DATABASE h1b` |
| `sql/02_create_schema.sql` | `CREATE SCHEMA IF NOT EXISTS raw` |
| `sql/03_create_tables.sql` | 25 raw tables with unified 98-column TEXT schema |

---

## Stage 2: Raw → Processed

### What the processed layer stores

- **Cleaned, typed data** in `processed` schema.
- Same 25-table structure (one per quarter), but with proper data types and quality filtering.
- Adds a `source_table` column for data lineage (99 columns total).

### Cleaning operations performed

| # | Operation | Detail |
|---|-----------|--------|
| 1 | **Remove empty rows** | Rows where `case_number` is NULL or blank are excluded. These are DOL source artifacts (Excel-to-CSV export padding). **5,557,433 rows removed** across 9 affected tables. |
| 2 | **Trim whitespace** | All TEXT fields are `TRIM()`-ed to remove leading/trailing whitespace. **6,684+ rows** had whitespace issues in fields like `employer_name` and `job_title`. |
| 3 | **Date type casting** | 5 date columns cast from TEXT (`"YYYY-MM-DD HH:MM:SS"`) to `DATE` type. Time portion (`00:00:00`) is stripped. Columns: `received_date`, `decision_date`, `original_cert_date`, `begin_date`, `end_date`. |
| 4 | **Numeric type casting** | 3 wage columns cast from TEXT to `NUMERIC`: `wage_rate_of_pay_from`, `wage_rate_of_pay_to`, `prevailing_wage`. Non-numeric values safely return NULL. |
| 5 | **Integer type casting** | 3 count columns cast from TEXT to `INTEGER`: `total_worker_positions`, `worksite_workers`, `total_worksite_locations`. Non-integer values safely return NULL. |
| 6 | **Lineage tracking** | `source_table` column added to every row, recording which raw table it came from. |

### Empty row removal detail

| Table | Raw Total | Processed | Empty Removed |
|-------|----------:|----------:|--------------:|
| FY2023 Q2 | 1,038,113 | 231,544 | 806,569 |
| FY2023 Q3 | 691,391 | 186,389 | 505,002 |
| FY2023 Q4 | 632,941 | 127,939 | 505,002 |
| FY2024 Q3 | 694,404 | 216,470 | 477,934 |
| FY2024 Q4 | 598,831 | 120,897 | 477,934 |
| FY2025 Q1 | 1,042,871 | 107,414 | 935,457 |
| FY2025 Q3 | 683,534 | 238,425 | 445,109 |
| FY2025 Q4 | 563,689 | 118,580 | 445,109 |
| FY2026 Q1 | 1,042,437 | 83,120 | 959,317 |
| **Other 16 tables** | **3,483,261** | **3,483,261** | **0** |
| **Total** | **9,472,472** | **3,915,039** | **5,557,433** |

### Processed column types

| Category | Columns | Raw Type | Processed Type |
|----------|---------|----------|---------------|
| Dates | `received_date`, `decision_date`, `original_cert_date`, `begin_date`, `end_date` | TEXT | DATE |
| Wages | `wage_rate_of_pay_from`, `wage_rate_of_pay_to`, `prevailing_wage` | TEXT | NUMERIC |
| Counts | `total_worker_positions`, `worksite_workers`, `total_worksite_locations` | TEXT | INTEGER |
| Lineage | `source_table` | — | TEXT (new) |
| All others | 89 columns | TEXT | TEXT (trimmed) |

### Design decisions

- **Boolean-like fields kept as TEXT**: Fields like `full_time_position` (Y/N), `h1b_dependent` (Yes/No), `willful_violator` (Yes/No/N/A), and `new_employment` (integer counts in newer years, Y/N in older years) have inconsistent representations across fiscal years. Casting to BOOLEAN would lose information, so they remain TEXT.
- **Employment type fields kept as TEXT**: `new_employment`, `continued_employment`, etc. contain integer counts in newer data but may have other values. Kept as TEXT for flexibility.
- **Safe casting with regex guards**: All type casts use regex validation (`~ '^\d+$'` for integers, `~ '^\d+(\.\d+)?$'` for numerics) to safely handle unexpected values without errors.
- **Per-quarter tables preserved**: The processed layer mirrors the raw 25-table structure rather than consolidating into a single table. This preserves the DOL's quarterly file structure and enables incremental updates.

### How to run

```bash
# Build processed layer from raw (idempotent — truncates and re-populates)
uv run python src/build_processed.py
```

### Code files

| File | Purpose |
|------|---------|
| `src/build_processed.py` | Orchestrates the full processed layer build |
| `sql/04_create_processed_schema.sql` | `CREATE SCHEMA IF NOT EXISTS processed` |
| `sql/05_create_processed_tables.sql` | 25 processed tables with typed columns |
| `sql/06_populate_processed.sql` | Template SQL for INSERT...SELECT with cleaning |

### Transformation SQL

The core cleaning logic is in `sql/06_populate_processed.sql`. For each table, it runs:

```sql
INSERT INTO processed.{TABLE_NAME}
SELECT
    TRIM(case_number) AS case_number,
    ...
    -- Dates: strip time, cast to DATE
    CAST(LEFT(TRIM(received_date), 10) AS DATE) AS received_date,
    ...
    -- Wages: regex-guarded cast to NUMERIC
    CASE WHEN TRIM(wage_rate_of_pay_from) ~ '^\d+(\.\d+)?$'
         THEN CAST(TRIM(wage_rate_of_pay_from) AS NUMERIC) ELSE NULL END,
    ...
    -- Integers: regex-guarded cast to INTEGER
    CASE WHEN TRIM(total_worker_positions) ~ '^\d+$'
         THEN CAST(TRIM(total_worker_positions) AS INTEGER) ELSE NULL END,
    ...
    '{TABLE_NAME}' AS source_table
FROM raw.{TABLE_NAME}
WHERE case_number IS NOT NULL
  AND TRIM(case_number) != '';
```

---

---

## Stage 3: Processed → Refined

### What the refined layer stores

- **Product-ready data** in `refined` schema.
- **38 columns** selected and combined from the 99-column processed schema (see `refined_schema.md` for selection rationale).
- **Per-FY tables** (quarters UNION'd and deduplicated): `refined.fy2020` through `refined.fy2026`.
- **`refined.fy_all`** — all fiscal years combined (UNION ALL of all FY tables).
- **`refined.employers`** — employer dimension table (one row per employer, aggregated across all years).
- **Deduplicated by `case_number`**: Some DOL quarterly files are cumulative (e.g., FY2021 Q3 contains Q1+Q2+Q3 data). The refined layer resolves this by keeping only one row per `case_number`, preferring the latest quarter's version.

### Column selection: 98 → 38 (with combined fields)

The 38 retained columns are organized into two groups. Some fields are combined from multiple source columns:

| Combined Field | Source Columns | Logic |
|---------------|---------------|-------|
| `employer_address` | `employer_address1` + `employer_address2` | `CONCAT_WS(', ', addr1, addr2)` |
| `employer_poc_name` | `employer_poc_first_name` + `employer_poc_last_name` | `CONCAT_WS(' ', first, last)` |

**A. Core Display Fields (16 columns)** — directly shown in UI:

| # | Column | Type | Purpose |
|---|--------|------|---------|
| 1 | `case_number` | TEXT | Primary key |
| 2 | `employer_name` | TEXT | Employer name |
| 3 | `job_title` | TEXT | Job title |
| 4 | `employer_address` | TEXT | Employer address (combined) |
| 5 | `employer_city` | TEXT | Employer HQ city |
| 6 | `employer_state` | TEXT | Employer HQ state |
| 7 | `employer_postal_code` | TEXT | Employer zip code |
| 8 | `worksite_city` | TEXT | Actual work city |
| 9 | `worksite_state` | TEXT | Actual work state |
| 10 | `wage_rate_of_pay_from` | NUMERIC | Wage lower bound |
| 11 | `wage_rate_of_pay_to` | NUMERIC | Wage upper bound |
| 12 | `wage_unit_of_pay` | TEXT | Wage unit (Hour/Week/Month/Year) |
| 13 | `received_date` | DATE | Submission date |
| 14 | `begin_date` | DATE | Employment start date |
| 15 | `case_status` | TEXT | Certified / Denied / Withdrawn |
| 16 | `fiscal_year` | INTEGER | Fiscal year (derived) |

**B. Differentiation Fields (22 columns)** — features h1bdata.info lacks:

| # | Column | Type | Purpose |
|---|--------|------|---------|
| 17 | `visa_class` | TEXT | H-1B / E-3 / H-1B1 |
| 18 | `soc_code` | TEXT | Standard Occupation Code |
| 19 | `soc_title` | TEXT | Standard Occupation Title |
| 20 | `full_time_position` | TEXT | Full-time Y/N |
| 21 | `total_worker_positions` | INTEGER | Workers covered by this LCA |
| 22 | `new_employment` | TEXT | New hire count |
| 23 | `continued_employment` | TEXT | Extension count |
| 24 | `change_employer` | TEXT | Transfer count |
| 25 | `amended_petition` | TEXT | Amendment count |
| 26 | `prevailing_wage` | NUMERIC | Market standard wage |
| 27 | `pw_unit_of_pay` | TEXT | Prevailing wage unit |
| 28 | `pw_wage_level` | TEXT | Wage level I/II/III/IV |
| 29 | `h1b_dependent` | TEXT | H-1B Dependent employer Y/N |
| 30 | `willful_violator` | TEXT | Willful violator Y/N |
| 31 | `support_h1b` | TEXT | Cap-exempt support Y/N |
| 32 | `statutory_basis` | TEXT | Exemption basis (Wage/Degree/Both) |
| 33 | `naics_code` | TEXT | Industry classification |
| 34 | `secondary_entity` | TEXT | Third-party staffing Y/N |
| 35 | `lawfirm_name_business_name` | TEXT | Attorney/law firm name |
| 36 | `employer_poc_name` | TEXT | POC full name (combined) |
| 37 | `employer_poc_job_title` | TEXT | POC job title |
| 38 | `employer_poc_email` | TEXT | POC email |

**60 columns removed**: See `refined_schema.md` Appendix B for the complete exclusion list with rationale per column.

### Employers dimension table (`refined.employers`)

Aggregated from `fy_all`, one row per unique employer:

| Column | Type | Purpose |
|--------|------|---------|
| `employer_name` | TEXT | Employer name (key) |
| `employer_address` | TEXT | Most recent address |
| `employer_city` | TEXT | Most recent city |
| `employer_state` | TEXT | Most recent state |
| `employer_postal_code` | TEXT | Most recent zip code |
| `naics_code` | TEXT | Most recent NAICS code |
| `h1b_dependent` | TEXT | Most recent H-1B Dependent flag |
| `willful_violator` | TEXT | Most recent Willful Violator flag |
| `total_applications` | INTEGER | Total applications across all years |
| `first_seen_year` | INTEGER | Earliest fiscal year |
| `last_seen_year` | INTEGER | Latest fiscal year |

**Statistics**: 214,366 unique employers across FY2020–FY2026.

### Deduplication logic

```sql
-- For each fiscal year: UNION ALL quarterly tables, then deduplicate
SELECT <38 columns>, fiscal_year
FROM (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY case_number
        ORDER BY source_table DESC  -- keep latest quarter's version
    ) AS rn
    FROM (
        SELECT * FROM processed.lca_disclosure_data_fy{YEAR}_q1
        UNION ALL
        SELECT * FROM processed.lca_disclosure_data_fy{YEAR}_q2
        UNION ALL
        SELECT * FROM processed.lca_disclosure_data_fy{YEAR}_q3
        UNION ALL
        SELECT * FROM processed.lca_disclosure_data_fy{YEAR}_q4
    ) AS all_quarters
) AS deduped
WHERE rn = 1;
```

**Why `ORDER BY source_table DESC`?** — Later quarters (e.g., Q4) may contain updated case status (e.g., a case filed in Q1 may be `Certified` by Q4). Keeping the latest quarter's version gives us the most current information.

### Deduplication results

| Fiscal Year | Processed Sum | Refined | Duplicates Removed |
|-------------|-------------:|--------:|-------------------:|
| FY2020 | 577,334 | 577,334 | 0 |
| FY2021 | 826,305 | 528,902 | 297,403 |
| FY2022 | 626,084 | 626,084 | 0 |
| FY2023 | 644,607 | 543,580 | 101,027 |
| FY2024 | 561,037 | 561,037 | 0 |
| FY2025 | 596,552 | 594,821 | 1,731 |
| FY2026 | 83,120 | 83,120 | 0 |
| **Total** | **3,915,039** | **3,514,878** | **400,161** |

**Notes**:
- FY2021 had the most duplicates (297,403) because its quarterly files were cumulative (Q3 contained Q1+Q2+Q3 data).
- FY2020, FY2022, FY2024, FY2026 had zero duplicates — their quarterly files were non-overlapping.
- FY2025 had a small overlap (1,731 rows) suggesting minor cross-quarter data in the DOL source.

### Data quality checks performed

The build script (`src/build_refined.py`) automatically runs 7 data quality checks:

#### DQ Check 0: fy_all consistency

**Result: PASS** — fy_all row count (3,514,878) matches the sum of all individual FY tables.

#### DQ Check 1: Case number uniqueness (within each fiscal year)

**Result: PASS** — All 7 refined tables have unique `case_number` values. No duplicates remain after deduplication.

| Table | Rows | Distinct case_numbers | Status |
|-------|-----:|-----:|-----:|
| refined.fy2020 | 577,334 | 577,334 | UNIQUE |
| refined.fy2021 | 528,902 | 528,902 | UNIQUE |
| refined.fy2022 | 626,084 | 626,084 | UNIQUE |
| refined.fy2023 | 543,580 | 543,580 | UNIQUE |
| refined.fy2024 | 561,037 | 561,037 | UNIQUE |
| refined.fy2025 | 594,821 | 594,821 | UNIQUE |
| refined.fy2026 | 83,120 | 83,120 | UNIQUE |

#### DQ Check 2: fy_all case_number analysis

- 3,514,878 total rows, 3,412,794 distinct case_numbers
- 102,084 cases appear in exactly 2 fiscal years (expected — LCA cases can span FYs)

#### DQ Check 3: Employers dimension table

- 214,366 unique employers
- 0 employers with NULL/empty name
- Address completeness: >99.9% for all address fields
- Top employer: COGNIZANT TECHNOLOGY SOLUTIONS US CORP (92,357 applications)

#### DQ Check 4: Combined field quality

- `employer_address` NULL/empty: 0 / 3,514,878 (0.0%)
- `employer_poc_name` NULL/empty: 0 / 3,514,878 (0.0%)

#### DQ Check 5: Case status distribution (fy_all)

| Status | Count | Share |
|--------|------:|------:|
| Certified | 3,253,687 | 92.6% |
| Certified - Withdrawn | 178,089 | 5.1% |
| Withdrawn | 61,936 | 1.8% |
| Denied | 21,166 | 0.6% |

#### DQ Check 6: NULL rates for key columns (fy_all)

**Result: Excellent** — All key columns have near-zero NULL rates. Only `prevailing_wage` had a notable rate (1,962 rows, 0.1%).

### How to run

```bash
# Build refined layer from processed (idempotent — drops and recreates all tables)
uv run python src/build_refined.py
```

### Code files

| File | Purpose |
|------|---------|
| `src/build_refined.py` | Orchestrates refined build + data quality checks |
| `sql/07_create_refined_schema.sql` | `CREATE SCHEMA IF NOT EXISTS refined` |
| `sql/08_create_refined_tables.sql` | FY tables + fy_all + employers with 38-column schema |
| `sql/09_populate_refined.sql` | Template SQL for UNION + dedup + column selection |
| `sql/10_populate_fy_all.sql` | UNION ALL of all FY tables into fy_all |
| `sql/11_populate_employers.sql` | Employer dimension table aggregation |

---

## Known data quality notes

1. **Cumulative quarters**: Some DOL fiscal year files are cumulative (later quarters contain earlier data). For example, FY2021 Q3 contains all of Q1+Q2+Q3. Deduplication across quarters is **not** performed in the processed layer — this is deferred to the refined layer, where `ROW_NUMBER()` by `case_number` resolves duplicates.

2. **Cross-year case_number overlap**: The same case_number can appear in multiple fiscal years. This is normal — LCA cases span fiscal years due to renewals, amendments, or delayed decisions. Each fiscal year table in the refined layer contains all cases that appeared in that year's quarterly data, even if the same case also appears in adjacent years.

3. **`employer_fein` availability**: Only present from FY2024 Q1 onward. Earlier tables have this column as NULL. (Not included in refined schema.)

4. **`lawfirm_business_fein` availability**: Only present from FY2025 Q2 onward. (Not included in refined schema.)

5. **FY2020 Q1–Q3 source**: These were downloaded as XLSX from DOL and converted to CSV. The XLSX files had mislabeled sheet names (`LCA_FY2021_Q1/Q2/Q3`) but case numbers confirm they are genuine FY2020 data.

---

## Quick reference

```bash
# Full pipeline from scratch
uv run python src/setup_database.py      # Step 1: Create DB + raw tables
uv run python src/import_csv.py          # Step 2: Load CSVs into raw
uv run python src/build_processed.py     # Step 3: Build processed from raw
uv run python src/build_refined.py       # Step 4: Build refined from processed
```

### Schema overview

```
h1b database
├── raw schema (25 tables)
│   └── All TEXT columns, exact CSV copies, includes empty rows
│       98 columns per table
│       9,472,472 total rows
│
├── processed schema (25 tables)
│   └── Typed columns (DATE, NUMERIC, INTEGER, TEXT)
│       Empty rows removed, whitespace trimmed
│       99 columns per table (+source_table lineage)
│       3,915,039 total rows
│
└── refined schema (9 tables)
    ├── Per-FY tables (7): refined.fy2020 ~ refined.fy2026
    │   38 columns, deduplicated by case_number
    │   3,514,878 total rows (sum of all FY tables)
    │
    ├── refined.fy_all
    │   All FY tables combined (UNION ALL)
    │   3,514,878 rows, 3,412,794 distinct case_numbers
    │
    └── refined.employers
        Employer dimension table (one row per employer)
        214,366 unique employers
        11 columns (name, address, city, state, zip, NAICS, flags, stats)
```

### Adding new data (e.g., FY2026 Q2)

When a new quarterly CSV is released:

1. **Place the CSV** in `Raw_CSV/` with naming `LCA_Disclosure_Data_FY{YEAR}_Q{QUARTER}.csv`.

2. **Add a raw table** in `sql/03_create_tables.sql`:
   ```sql
   CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2026_q2
       (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
   ```

3. **Add a processed table** in `sql/05_create_processed_tables.sql`:
   ```sql
   CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2026_q2
       (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
   ```

4. **Update Python table lists**:
   - `src/import_csv.py` — the CSV-to-table mapping (if not auto-detected)
   - `src/build_processed.py` — add to `RAW_TABLES` list
   - `src/build_refined.py` — add to `FISCAL_YEAR_QUARTERS[2026]` list

5. **Run the pipeline**:
   ```bash
   uv run python src/setup_database.py      # Creates new raw/processed tables
   uv run python src/import_csv.py          # Imports new CSV
   uv run python src/build_processed.py     # Populates processed table
   uv run python src/build_refined.py       # Rebuilds refined.fy2026 with Q1+Q2
   ```

6. **Review the data quality report** printed by `build_refined.py` — check for uniqueness, NULL rates, and row count changes.
