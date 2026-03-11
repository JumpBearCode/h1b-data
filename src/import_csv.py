"""
Import all LCA disclosure CSV files into the H1B raw schema.

Handles column name normalization across fiscal years:
  - H-1B_DEPENDENT / H1B_DEPENDENT / H_1B_DEPENDENT -> h1b_dependent
  - EMPLOYER_POC_ADDRESS_1 -> employer_poc_address1
  - EMPLOYER_POC_ADDRESS_2 -> employer_poc_address2

Uses PostgreSQL COPY for fast bulk loading, with a StringIO buffer
to remap CSV columns to the unified 98-column table schema.

Usage:
    uv run python src/import_csv.py
"""

import csv
import io
import os
import sys
import time
from glob import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db_connector import get_h1b_connection

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Raw_CSV")

# The canonical 98 columns in our raw tables (all lowercase)
CANONICAL_COLUMNS = [
    "case_number", "case_status", "received_date", "decision_date",
    "original_cert_date", "visa_class", "job_title", "soc_code",
    "soc_title", "full_time_position", "begin_date", "end_date",
    "total_worker_positions", "new_employment", "continued_employment",
    "change_previous_employment", "new_concurrent_employment",
    "change_employer", "amended_petition", "employer_name",
    "trade_name_dba", "employer_address1", "employer_address2",
    "employer_city", "employer_state", "employer_postal_code",
    "employer_country", "employer_province", "employer_phone",
    "employer_phone_ext", "employer_fein", "naics_code",
    "employer_poc_last_name", "employer_poc_first_name",
    "employer_poc_middle_name", "employer_poc_job_title",
    "employer_poc_address1", "employer_poc_address2",
    "employer_poc_city", "employer_poc_state",
    "employer_poc_postal_code", "employer_poc_country",
    "employer_poc_province", "employer_poc_phone",
    "employer_poc_phone_ext", "employer_poc_email",
    "agent_representing_employer", "agent_attorney_last_name",
    "agent_attorney_first_name", "agent_attorney_middle_name",
    "agent_attorney_address1", "agent_attorney_address2",
    "agent_attorney_city", "agent_attorney_state",
    "agent_attorney_postal_code", "agent_attorney_country",
    "agent_attorney_province", "agent_attorney_phone",
    "agent_attorney_phone_ext", "agent_attorney_email_address",
    "lawfirm_name_business_name", "lawfirm_business_fein",
    "state_of_highest_court", "name_of_highest_state_court",
    "worksite_workers", "secondary_entity",
    "secondary_entity_business_name", "worksite_address1",
    "worksite_address2", "worksite_city", "worksite_county",
    "worksite_state", "worksite_postal_code",
    "wage_rate_of_pay_from", "wage_rate_of_pay_to",
    "wage_unit_of_pay", "prevailing_wage", "pw_unit_of_pay",
    "pw_tracking_number", "pw_wage_level", "pw_oes_year",
    "pw_other_source", "pw_other_year", "pw_survey_publisher",
    "pw_survey_name", "total_worksite_locations",
    "agree_to_lc_statement", "h1b_dependent", "willful_violator",
    "support_h1b", "statutory_basis", "appendix_a_attached",
    "public_disclosure", "preparer_last_name", "preparer_first_name",
    "preparer_middle_initial", "preparer_business_name",
    "preparer_email",
]

# Map known CSV header variants to canonical column names
COLUMN_NAME_MAP = {
    # H-1B_DEPENDENT variations
    "h-1b_dependent": "h1b_dependent",
    "h1b_dependent": "h1b_dependent",
    "h_1b_dependent": "h1b_dependent",
    # EMPLOYER_POC_ADDRESS variations (some CSVs use underscore before number)
    "employer_poc_address_1": "employer_poc_address1",
    "employer_poc_address_2": "employer_poc_address2",
}


def normalize_column_name(col):
    """Normalize a CSV column header to its canonical lowercase form."""
    normalized = col.strip().lower()
    return COLUMN_NAME_MAP.get(normalized, normalized)


def get_table_name(csv_filename):
    """Derive the table name from CSV filename.

    Example: LCA_Disclosure_Data_FY2020_Q4.csv -> lca_disclosure_data_fy2020_q4
    """
    return os.path.splitext(csv_filename)[0].lower()


def import_single_csv(conn, csv_path):
    """Import one CSV file into its corresponding raw table using COPY."""
    filename = os.path.basename(csv_path)
    table_name = get_table_name(filename)

    print(f"\n  Processing: {filename}")
    start = time.time()

    # Read CSV and normalize headers
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        raw_headers = next(reader)
        csv_columns = [normalize_column_name(h) for h in raw_headers]

        # Build mapping: for each canonical column, find its index in the CSV
        # (or None if the CSV doesn't have it)
        col_indices = {}
        for i, col in enumerate(csv_columns):
            col_indices[col] = i

        # Prepare the COPY buffer using CSV format (handles quoting properly)
        buf = io.StringIO()
        writer = csv.writer(buf, delimiter=",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")

        row_count = 0
        for row in reader:
            out_row = []
            for canon_col in CANONICAL_COLUMNS:
                idx = col_indices.get(canon_col)
                if idx is not None and idx < len(row):
                    val = row[idx]
                    out_row.append(val if val != "" else None)
                else:
                    out_row.append(None)
            writer.writerow(out_row)
            row_count += 1

    # COPY into PostgreSQL using CSV format
    buf.seek(0)
    cur = conn.cursor()
    try:
        columns_sql = ", ".join(CANONICAL_COLUMNS)
        copy_sql = f"COPY raw.{table_name} ({columns_sql}) FROM STDIN WITH (FORMAT csv, NULL '', DELIMITER ',')"
        cur.copy_expert(copy_sql, buf)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()

    elapsed = time.time() - start
    print(f"    -> {row_count:,} rows loaded into raw.{table_name} ({elapsed:.1f}s)")
    return row_count


def main():
    print("=" * 60)
    print("H1B CSV Data Import")
    print("=" * 60)

    csv_files = sorted(glob(os.path.join(CSV_DIR, "LCA_Disclosure_Data_*.csv")))
    if not csv_files:
        print(f"[ERROR] No CSV files found in {CSV_DIR}")
        sys.exit(1)

    print(f"\nFound {len(csv_files)} CSV files to import.")

    conn = get_h1b_connection()
    total_rows = 0
    total_start = time.time()

    try:
        for csv_path in csv_files:
            rows = import_single_csv(conn, csv_path)
            total_rows += rows
    finally:
        conn.close()

    total_elapsed = time.time() - total_start
    print(f"\n{'=' * 60}")
    print(f"Import complete!")
    print(f"  Total rows: {total_rows:,}")
    print(f"  Total time: {total_elapsed:.1f}s")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
