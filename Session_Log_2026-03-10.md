# Session Log: H1B Raw Data Pipeline Build (2026-03-10)

## Objective

Build a complete pipeline to dump all LCA disclosure CSV files (FY2020–FY2026) into PostgreSQL, organized under a dedicated database and schema.

---

## Step 1: Environment Setup

- Created `.env` file with PostgreSQL connection string:
  ```
  DATABASE_URL=postgresql://bearagent:Yuer0113@192.168.31.61:5432/curion_agent
  ```
- Added `.env` to `.gitignore` to prevent credential leakage.
- Initialized Python project with `uv`, installed `psycopg2-binary` and `python-dotenv`.

---

## Step 2: Schema Analysis

Analyzed `Final_Schema.md` and all 22 CSV files in `Raw_CSV/`. Key findings:

- **98-column unified schema** (superset across FY2020–FY2026).
- **Column count varies by era**:
  - 96 columns: FY2020 Q4 ~ FY2023 Q4
  - 97 columns: FY2024 Q1 ~ FY2025 Q1 (`EMPLOYER_FEIN` added)
  - 98 columns: FY2025 Q2 ~ FY2026 Q1 (`LAWFIRM_BUSINESS_FEIN` added)
- **Header naming inconsistencies** across CSV files:
  - `H-1B_DEPENDENT` / `H1B_DEPENDENT` / `H_1B_DEPENDENT` → normalized to `h1b_dependent`
  - `EMPLOYER_POC_ADDRESS_1` / `EMPLOYER_POC_ADDRESS1` → normalized to `employer_poc_address1`

---

## Step 3: Code Written

### Files Created

| File | Purpose |
|------|---------|
| `src/__init__.py` | Python package marker |
| `src/db_connector.py` | PostgreSQL connector — provides `get_admin_connection()`, `get_h1b_connection()`, `execute_sql_file()` |
| `src/setup_database.py` | Creates database `h1b`, schema `raw`, and all tables |
| `src/import_csv.py` | Reads CSV files, normalizes headers, bulk-loads via `COPY` |
| `sql/01_create_database.sql` | `CREATE DATABASE h1b` |
| `sql/02_create_schema.sql` | `CREATE SCHEMA IF NOT EXISTS raw` |
| `sql/03_create_tables.sql` | Creates all 25 raw tables (unified 98-column TEXT schema) |

### Design Decisions

- **All columns stored as TEXT** in raw tables — type casting deferred to downstream processing.
- **Unified 98-column schema** for all tables — columns not present in older CSVs are simply NULL.
- **PostgreSQL `COPY` with CSV format** for fast bulk loading (handles quoted fields properly).
- **Column name normalization** at import time via a mapping dict in `import_csv.py`.

---

## Step 4: Initial Import (22 CSV files)

Ran `setup_database.py` then `import_csv.py`. All 22 CSVs imported successfully.

**First bug encountered**: Initial implementation used `FORMAT text` with tab delimiter for COPY, which broke on fields containing quotes (e.g., `"VLSI ARCHITECT"`). Fixed by switching to `FORMAT csv`.

---

## Step 5: Data Verification

Row-by-row verification confirmed all 22 CSV files matched their DB tables exactly.

---

## Step 6: Data Quality Check

Investigated why some quarterly files had unusually high row counts (e.g., FY2023 Q2 with 1M+ rows). Findings:

- **Large files contained massive amounts of empty rows** — all 96–98 fields empty. This is a DOL source data quality issue (Excel-to-CSV export artifacts).
- After excluding empty rows, per-quarter data volumes are consistent (80K–240K valid rows).
- **Within valid rows, `case_number` is unique per CSV file** — no true duplicates.
- Some cross-quarter overlaps exist (e.g., FY2023 Q2 fully contains FY2023 Q1 data), indicating DOL's quarterly files are **cumulative** for certain fiscal years.

### Empty Row Summary

| Table | Total Rows | Valid Rows | Empty Rows |
|-------|----------:|----------:|----------:|
| FY2023 Q2 | 1,038,113 | 231,544 | 806,569 |
| FY2023 Q3 | 691,391 | 186,389 | 505,002 |
| FY2023 Q4 | 632,941 | 127,939 | 505,002 |
| FY2024 Q3 | 694,404 | 216,470 | 477,934 |
| FY2024 Q4 | 598,831 | 120,897 | 477,934 |
| FY2025 Q1 | 1,042,871 | 107,414 | 935,457 |
| FY2025 Q3 | 683,534 | 238,425 | 445,109 |
| FY2025 Q4 | 563,689 | 118,580 | 445,109 |
| FY2026 Q1 | 1,042,437 | 83,120 | 959,317 |

---

## Step 7: FY2020 Missing Quarters

Discovered FY2020 only had Q4 locally. Investigation:

1. DOL website lists FY2020 Q1/Q2/Q3/Q4 as separate XLSX files (not multi-tab).
2. Downloaded all 4 XLSX files. FY2020 Q4 XLSX has a single sheet (`LCA_FY2020Q4`, 117K rows) — matches existing CSV.
3. FY2020 Q1/Q2/Q3 XLSX files each have a single sheet but **mislabeled** as `LCA_FY2021_Q1/Q2/Q3`. However, case numbers (e.g., `I-200-19268-*`) confirm they are genuine FY2020 data (fiscal year starting Oct 2019).
4. These files contain **no overlap** with existing FY2021 CSV data — they are a completely independent dataset.
5. Converted Q1/Q2/Q3 XLSX → CSV using `openpyxl`, created tables, and imported.

### FY2020 Complete

| Quarter | Rows | Source |
|---------|-----:|--------|
| Q1 | 112,017 | XLSX download → CSV |
| Q2 | 157,173 | XLSX download → CSV |
| Q3 | 190,749 | XLSX download → CSV |
| Q4 | 117,395 | Original CSV |

---

## Final State

**Database**: `h1b` on `192.168.31.61:5432`
**Schema**: `raw`
**Tables**: 25 (FY2020 Q1–Q4, FY2021 Q1–Q4, ..., FY2026 Q1)
**Total rows**: 9,472,472
**All 25 files verified** — CSV row counts match DB row counts exactly.

### Usage

```bash
# Set up database (run once)
uv run python src/setup_database.py

# Import CSV data
uv run python src/import_csv.py
```

---

## Open Items

- **Empty rows**: 9 CSV files contain large numbers of all-NULL rows (DOL source issue). Not yet filtered — raw layer preserves source data as-is.
- **Cumulative vs. incremental quarters**: Some fiscal years (FY2021, FY2023) have cumulative quarterly files where later quarters include earlier data. Deduplication needed in downstream processing.
- **FY2020 XLSX files on disk**: The downloaded `.xlsx` files remain in `Raw_CSV/` alongside the converted CSVs. Can be cleaned up if not needed.
