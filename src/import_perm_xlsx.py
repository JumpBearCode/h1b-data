"""
Import all PERM disclosure XLSX files into the H1B raw schema as-is.

Reads XLSX headers, lowercases them, and dumps all columns directly into
per-file raw tables. Each table has exactly the columns from its source file.
No column normalization or mapping — raw data preserved as-is.

Uses PostgreSQL COPY for fast bulk loading.

Usage:
    uv run python src/import_perm_xlsx.py
"""

import csv
import io
import os
import sys
import time

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db_connector import get_h1b_connection

XLSX_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Raw_CSV")

# Mapping from xlsx filename stem to raw table name
FILE_TABLE_MAP = {
    "PERM_Disclosure_Data_FY2020": "perm_disclosure_data_fy2020",
    "PERM_Disclosure_Data_FY2021": "perm_disclosure_data_fy2021",
    "PERM_Disclosure_Data_FY2022_Q4": "perm_disclosure_data_fy2022_q4",
    "PERM_Disclosure_Data_FY2023_Q4": "perm_disclosure_data_fy2023_q4",
    "PERM_Disclosure_Data_FY2024_Q4": "perm_disclosure_data_fy2024_q4",
    "PERM_Disclosure_Data_New_Form_FY2024_Q4": "perm_disclosure_data_new_form_fy2024_q4",
    "PERM_Disclosure_Data_FY2025_Q4": "perm_disclosure_data_fy2025_q4",
    "PERM_Disclosure_Data_FY2026_Q1": "perm_disclosure_data_fy2026_q1",
}


def get_table_name(xlsx_filename):
    """Derive the raw table name from the XLSX filename."""
    stem = os.path.splitext(xlsx_filename)[0]
    table = FILE_TABLE_MAP.get(stem)
    if table is None:
        raise ValueError(f"Unknown PERM file: {xlsx_filename}")
    return table


def import_single_xlsx(conn, xlsx_path):
    """Import one XLSX file into its corresponding raw table using COPY."""
    filename = os.path.basename(xlsx_path)
    table_name = get_table_name(filename)

    print(f"\n  Processing: {filename}")
    start = time.time()

    # Open XLSX with openpyxl (read_only for memory efficiency)
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb.active

    rows_iter = ws.iter_rows(values_only=True)
    raw_headers = next(rows_iter)
    # Lowercase headers — these must match the table columns exactly
    columns = [str(h).strip().lower() for h in raw_headers if h is not None]
    num_cols = len(columns)

    print(f"    {num_cols} columns")

    # Build CSV buffer for COPY — dump all columns as-is
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter=",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")

    row_count = 0
    for row in rows_iter:
        out_row = []
        for i in range(num_cols):
            if i < len(row):
                val = row[i]
                if val is None:
                    out_row.append(None)
                else:
                    out_row.append(str(val))
            else:
                out_row.append(None)
        writer.writerow(out_row)
        row_count += 1

    wb.close()

    # COPY into PostgreSQL
    buf.seek(0)
    cur = conn.cursor()
    try:
        columns_sql = ", ".join(columns)
        copy_sql = (
            f"COPY raw.{table_name} ({columns_sql}) "
            f"FROM STDIN WITH (FORMAT csv, NULL '', DELIMITER ',')"
        )
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
    print("PERM XLSX Data Import (as-is)")
    print("=" * 60)

    # Find all PERM xlsx files in the expected order
    xlsx_files = []
    for stem in FILE_TABLE_MAP:
        path = os.path.join(XLSX_DIR, f"{stem}.xlsx")
        if os.path.exists(path):
            xlsx_files.append(path)
        else:
            print(f"  [WARN] Missing: {stem}.xlsx")

    if not xlsx_files:
        print(f"[ERROR] No PERM XLSX files found in {XLSX_DIR}")
        sys.exit(1)

    print(f"\nFound {len(xlsx_files)} PERM XLSX files to import.")

    conn = get_h1b_connection()
    total_rows = 0
    total_start = time.time()

    try:
        for xlsx_path in xlsx_files:
            rows = import_single_xlsx(conn, xlsx_path)
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
