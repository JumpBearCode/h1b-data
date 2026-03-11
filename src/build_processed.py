"""
Build the processed schema from raw data.

Steps:
  1. Create processed schema
  2. Create processed tables (with proper data types)
  3. For each raw table, run the cleaning SQL to populate the processed table

Cleaning operations:
  - Remove empty rows (case_number is NULL or blank)
  - TRIM all TEXT fields
  - Cast dates from "YYYY-MM-DD HH:MM:SS" TEXT -> DATE
  - Cast wage fields from TEXT -> NUMERIC
  - Cast integer fields from TEXT -> INTEGER
  - Add source_table lineage column

Usage:
    uv run python src/build_processed.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db_connector import get_h1b_connection, execute_sql_file

SQL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")

# All 25 raw tables in order
RAW_TABLES = [
    "lca_disclosure_data_fy2020_q1",
    "lca_disclosure_data_fy2020_q2",
    "lca_disclosure_data_fy2020_q3",
    "lca_disclosure_data_fy2020_q4",
    "lca_disclosure_data_fy2021_q1",
    "lca_disclosure_data_fy2021_q2",
    "lca_disclosure_data_fy2021_q3",
    "lca_disclosure_data_fy2021_q4",
    "lca_disclosure_data_fy2022_q1",
    "lca_disclosure_data_fy2022_q2",
    "lca_disclosure_data_fy2022_q3",
    "lca_disclosure_data_fy2022_q4",
    "lca_disclosure_data_fy2023_q1",
    "lca_disclosure_data_fy2023_q2",
    "lca_disclosure_data_fy2023_q3",
    "lca_disclosure_data_fy2023_q4",
    "lca_disclosure_data_fy2024_q1",
    "lca_disclosure_data_fy2024_q2",
    "lca_disclosure_data_fy2024_q3",
    "lca_disclosure_data_fy2024_q4",
    "lca_disclosure_data_fy2025_q1",
    "lca_disclosure_data_fy2025_q2",
    "lca_disclosure_data_fy2025_q3",
    "lca_disclosure_data_fy2025_q4",
    "lca_disclosure_data_fy2026_q1",
]


def create_processed_schema(conn):
    """Create the processed schema."""
    execute_sql_file(conn, os.path.join(SQL_DIR, "04_create_processed_schema.sql"))
    print("[OK] Schema 'processed' created.")


def create_processed_tables(conn):
    """Create all processed tables with proper data types."""
    execute_sql_file(conn, os.path.join(SQL_DIR, "05_create_processed_tables.sql"))
    print("[OK] All processed tables created.")


def populate_processed_table(conn, table_name):
    """Run the cleaning INSERT for a single table."""
    template_path = os.path.join(SQL_DIR, "06_populate_processed.sql")
    with open(template_path, "r") as f:
        sql_template = f.read()

    sql = sql_template.replace("{TABLE_NAME}", table_name)

    start = time.time()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

    # Get row count
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM processed.{}".format(table_name))
        count = cur.fetchone()[0]

    elapsed = time.time() - start
    print("    -> processed.{}: {:,} rows ({:.1f}s)".format(table_name, count, elapsed))
    return count


def verify(conn):
    """Print comparison of raw vs processed row counts."""
    print("\n[VERIFY] Raw vs Processed row counts:")
    header = "{:<45} {:>12} {:>12} {:>12}".format("Table", "Raw Total", "Raw Valid", "Processed")
    print(header)
    print("-" * 85)

    total_raw = 0
    total_valid = 0
    total_proc = 0

    with conn.cursor() as cur:
        for t in RAW_TABLES:
            cur.execute("SELECT COUNT(*) FROM raw.{}".format(t))
            raw_total = cur.fetchone()[0]

            cur.execute("""SELECT COUNT(*) FROM raw.{}
                WHERE case_number IS NOT NULL AND TRIM(case_number) != ''""".format(t))
            raw_valid = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM processed.{}".format(t))
            proc = cur.fetchone()[0]

            total_raw += raw_total
            total_valid += raw_valid
            total_proc += proc

            match = "OK" if raw_valid == proc else "MISMATCH"
            print("{:<45} {:>12,} {:>12,} {:>12,}  {}".format(t, raw_total, raw_valid, proc, match))

    print("-" * 85)
    print("{:<45} {:>12,} {:>12,} {:>12,}".format("TOTAL", total_raw, total_valid, total_proc))
    print("\nRows removed (empty): {:,}".format(total_raw - total_proc))


def main():
    print("=" * 60)
    print("H1B Processed Layer Build")
    print("=" * 60)

    conn = get_h1b_connection()
    total_start = time.time()

    try:
        print("\n[Step 1/4] Creating processed schema...")
        create_processed_schema(conn)

        print("\n[Step 2/4] Creating processed tables...")
        create_processed_tables(conn)

        print("\n[Step 3/4] Populating processed tables...")
        total_rows = 0
        for table_name in RAW_TABLES:
            rows = populate_processed_table(conn, table_name)
            total_rows += rows

        print("\n[Step 4/4] Verifying...")
        verify(conn)

    finally:
        conn.close()

    total_elapsed = time.time() - total_start
    print("\n" + "=" * 60)
    print("Processed layer build complete!")
    print("  Total processed rows: {:,}".format(total_rows))
    print("  Total time: {:.1f}s".format(total_elapsed))
    print("=" * 60)


if __name__ == "__main__":
    main()
