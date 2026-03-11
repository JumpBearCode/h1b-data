"""
Build the refined schema from processed data.

Steps:
  1. Create refined schema
  2. Create refined tables (38 columns per FY table + fy_all + employers)
  3. For each fiscal year, UNION quarterly tables, deduplicate by case_number
  4. Build fy_all (UNION of all FY tables)
  5. Build employers dimension table
  6. Run data quality checks

Usage:
    uv run python src/build_refined.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db_connector import get_h1b_connection, execute_sql_file

SQL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")

# Fiscal year -> list of quarterly processed table names
FISCAL_YEAR_QUARTERS = {
    2020: [
        "lca_disclosure_data_fy2020_q1",
        "lca_disclosure_data_fy2020_q2",
        "lca_disclosure_data_fy2020_q3",
        "lca_disclosure_data_fy2020_q4",
    ],
    2021: [
        "lca_disclosure_data_fy2021_q1",
        "lca_disclosure_data_fy2021_q2",
        "lca_disclosure_data_fy2021_q3",
        "lca_disclosure_data_fy2021_q4",
    ],
    2022: [
        "lca_disclosure_data_fy2022_q1",
        "lca_disclosure_data_fy2022_q2",
        "lca_disclosure_data_fy2022_q3",
        "lca_disclosure_data_fy2022_q4",
    ],
    2023: [
        "lca_disclosure_data_fy2023_q1",
        "lca_disclosure_data_fy2023_q2",
        "lca_disclosure_data_fy2023_q3",
        "lca_disclosure_data_fy2023_q4",
    ],
    2024: [
        "lca_disclosure_data_fy2024_q1",
        "lca_disclosure_data_fy2024_q2",
        "lca_disclosure_data_fy2024_q3",
        "lca_disclosure_data_fy2024_q4",
    ],
    2025: [
        "lca_disclosure_data_fy2025_q1",
        "lca_disclosure_data_fy2025_q2",
        "lca_disclosure_data_fy2025_q3",
        "lca_disclosure_data_fy2025_q4",
    ],
    2026: [
        "lca_disclosure_data_fy2026_q1",
    ],
}

FISCAL_YEARS = sorted(FISCAL_YEAR_QUARTERS.keys())


def create_refined_schema(conn):
    """Create the refined schema."""
    execute_sql_file(conn, os.path.join(SQL_DIR, "07_create_refined_schema.sql"))
    print("[OK] Schema 'refined' created.")


def drop_refined_tables(conn):
    """Drop all refined tables so we can recreate with new schema."""
    tables = ["employers", "fy_all"]
    tables += ["fy{}".format(fy) for fy in FISCAL_YEARS]
    with conn.cursor() as cur:
        for t in tables:
            cur.execute("DROP TABLE IF EXISTS refined.{}".format(t))
    conn.commit()
    print("[OK] Dropped existing refined tables.")


def create_refined_tables(conn):
    """Create all refined tables (FY tables + fy_all + employers)."""
    execute_sql_file(conn, os.path.join(SQL_DIR, "08_create_refined_tables.sql"))
    print("[OK] All refined tables created.")


def build_quarter_unions(quarters):
    """Build the UNION ALL SQL fragment for a list of quarterly tables."""
    parts = []
    for table in quarters:
        parts.append("        SELECT * FROM processed.{}".format(table))
    return "\n        UNION ALL\n".join(parts)


def populate_refined_table(conn, fiscal_year, quarters):
    """UNION quarters, deduplicate, and populate refined table for a fiscal year."""
    template_path = os.path.join(SQL_DIR, "09_populate_refined.sql")
    with open(template_path, "r") as f:
        sql_template = f.read()

    quarter_unions = build_quarter_unions(quarters)
    sql = sql_template.replace("{FISCAL_YEAR}", str(fiscal_year))
    sql = sql.replace("{QUARTER_UNIONS}", quarter_unions)

    start = time.time()
    with conn.cursor() as cur:
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        for stmt in statements:
            cur.execute(stmt)
    conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM refined.fy{}".format(fiscal_year))
        count = cur.fetchone()[0]

    elapsed = time.time() - start
    print("    -> refined.fy{}: {:,} rows ({:.1f}s)".format(fiscal_year, count, elapsed))
    return count


def populate_fy_all(conn):
    """Populate refined.fy_all by UNION ALL of all FY tables."""
    sql_path = os.path.join(SQL_DIR, "10_populate_fy_all.sql")
    with open(sql_path, "r") as f:
        sql = f.read()

    start = time.time()
    with conn.cursor() as cur:
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        for stmt in statements:
            cur.execute(stmt)
    conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM refined.fy_all")
        count = cur.fetchone()[0]

    elapsed = time.time() - start
    print("    -> refined.fy_all: {:,} rows ({:.1f}s)".format(count, elapsed))
    return count


def populate_employers(conn):
    """Populate refined.employers dimension table."""
    sql_path = os.path.join(SQL_DIR, "11_populate_employers.sql")
    with open(sql_path, "r") as f:
        sql = f.read()

    start = time.time()
    with conn.cursor() as cur:
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        for stmt in statements:
            cur.execute(stmt)
    conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM refined.employers")
        count = cur.fetchone()[0]

    elapsed = time.time() - start
    print("    -> refined.employers: {:,} rows ({:.1f}s)".format(count, elapsed))
    return count


# ========== Data Quality Checks ==========

def verify_row_counts(conn):
    """Compare processed quarterly totals vs refined fiscal year totals."""
    print("\n[VERIFY] Row count comparison: processed quarters vs refined (deduplicated)")
    header = "{:<12} {:>15} {:>15} {:>15}".format(
        "FY", "Processed Sum", "Refined", "Duplicates Removed"
    )
    print(header)
    print("-" * 60)

    total_processed = 0
    total_refined = 0

    with conn.cursor() as cur:
        for fy, quarters in sorted(FISCAL_YEAR_QUARTERS.items()):
            proc_sum = 0
            for q in quarters:
                cur.execute("SELECT COUNT(*) FROM processed.{}".format(q))
                proc_sum += cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM refined.fy{}".format(fy))
            refined = cur.fetchone()[0]

            dupes_removed = proc_sum - refined
            total_processed += proc_sum
            total_refined += refined

            print("{:<12} {:>15,} {:>15,} {:>15,}".format(
                "FY{}".format(fy), proc_sum, refined, dupes_removed
            ))

    print("-" * 60)
    print("{:<12} {:>15,} {:>15,} {:>15,}".format(
        "TOTAL", total_processed, total_refined, total_processed - total_refined
    ))


def check_fy_all_consistency(conn):
    """Verify fy_all row count matches sum of individual FY tables."""
    print("\n[DQ CHECK 0] fy_all consistency with individual FY tables")
    print("-" * 70)

    with conn.cursor() as cur:
        fy_sum = 0
        for fy in FISCAL_YEARS:
            cur.execute("SELECT COUNT(*) FROM refined.fy{}".format(fy))
            fy_sum += cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM refined.fy_all")
        fy_all_count = cur.fetchone()[0]

        if fy_sum == fy_all_count:
            print("    Sum of FY tables: {:,}".format(fy_sum))
            print("    fy_all count:     {:,}".format(fy_all_count))
            print("    [PASS] fy_all matches sum of individual FY tables.")
        else:
            print("    Sum of FY tables: {:,}".format(fy_sum))
            print("    fy_all count:     {:,}".format(fy_all_count))
            print("    [FAIL] MISMATCH: difference = {:,}".format(fy_all_count - fy_sum))


def check_case_number_uniqueness(conn):
    """Check that case_number is unique within each refined fiscal year table."""
    print("\n[DQ CHECK 1] Case number uniqueness within each fiscal year table")
    print("-" * 70)

    all_unique = True
    with conn.cursor() as cur:
        for fy in FISCAL_YEARS:
            cur.execute("""
                SELECT COUNT(*) AS total_rows,
                       COUNT(DISTINCT case_number) AS distinct_cases
                FROM refined.fy{}
            """.format(fy))
            total, distinct = cur.fetchone()

            if total == distinct:
                print("    refined.fy{}: {:,} rows, {:,} distinct -> UNIQUE".format(
                    fy, total, distinct
                ))
            else:
                dupes = total - distinct
                all_unique = False
                print("    refined.fy{}: {:,} rows, {:,} distinct -> {:,} DUPLICATES".format(
                    fy, total, distinct, dupes
                ))
                cur.execute("""
                    SELECT case_number, COUNT(*) AS cnt
                    FROM refined.fy{}
                    GROUP BY case_number
                    HAVING COUNT(*) > 1
                    ORDER BY cnt DESC
                    LIMIT 5
                """.format(fy))
                for row in cur.fetchall():
                    print("        Example: case_number='{}' appears {} times".format(row[0], row[1]))

    if all_unique:
        print("\n    [PASS] All fiscal year tables have unique case_numbers.")
    else:
        print("\n    [WARN] Some tables have duplicate case_numbers.")

    return all_unique


def check_fy_all_uniqueness(conn):
    """Check case_number uniqueness in fy_all (expect duplicates across years)."""
    print("\n[DQ CHECK 2] Case number analysis in fy_all")
    print("-" * 70)

    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) AS total_rows,
                   COUNT(DISTINCT case_number) AS distinct_cases
            FROM refined.fy_all
        """)
        total, distinct = cur.fetchone()
        dupes = total - distinct

        print("    Total rows:            {:,}".format(total))
        print("    Distinct case_numbers: {:,}".format(distinct))
        print("    Cross-year duplicates: {:,}".format(dupes))

        if dupes > 0:
            # Show which years have overlapping cases
            cur.execute("""
                SELECT fiscal_year, COUNT(*) AS cnt
                FROM (
                    SELECT case_number, fiscal_year
                    FROM refined.fy_all
                    WHERE case_number IN (
                        SELECT case_number FROM refined.fy_all
                        GROUP BY case_number HAVING COUNT(*) > 1
                    )
                ) sub
                GROUP BY fiscal_year
                ORDER BY fiscal_year
            """)
            print("\n    Cases appearing in multiple years, by FY:")
            for fy, cnt in cur.fetchall():
                print("        FY{}: {:,} rows involved in cross-year overlaps".format(fy, cnt))

            cur.execute("""
                SELECT cnt_years, COUNT(*) AS num_cases
                FROM (
                    SELECT case_number, COUNT(DISTINCT fiscal_year) AS cnt_years
                    FROM refined.fy_all
                    GROUP BY case_number
                    HAVING COUNT(DISTINCT fiscal_year) > 1
                ) sub
                GROUP BY cnt_years
                ORDER BY cnt_years
            """)
            print("\n    Distribution of cross-year case appearances:")
            for cnt_years, num_cases in cur.fetchall():
                print("        Appears in {} fiscal years: {:,} cases".format(cnt_years, num_cases))

        print("\n    [INFO] Cross-year duplicates are expected — LCA cases can span fiscal years.")


def check_employers_table(conn):
    """Validate the employers dimension table."""
    print("\n[DQ CHECK 3] Employers dimension table")
    print("-" * 70)

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM refined.employers")
        total = cur.fetchone()[0]
        print("    Total unique employers: {:,}".format(total))

        cur.execute("""
            SELECT COUNT(*) FROM refined.employers
            WHERE employer_name IS NULL OR employer_name = ''
        """)
        null_names = cur.fetchone()[0]
        print("    Employers with NULL/empty name: {} {}".format(
            null_names, "[PASS]" if null_names == 0 else "[WARN]"
        ))

        # Check address completeness
        for col in ["employer_address", "employer_city", "employer_state", "employer_postal_code"]:
            cur.execute("""
                SELECT COUNT(*) FROM refined.employers
                WHERE {} IS NULL OR {} = ''
            """.format(col, col))
            nulls = cur.fetchone()[0]
            pct = nulls / total * 100 if total > 0 else 0
            print("    {} NULL/empty: {:,} ({:.1f}%)".format(col, nulls, pct))

        # Top employers by application count
        cur.execute("""
            SELECT employer_name, employer_city, employer_state, total_applications
            FROM refined.employers
            ORDER BY total_applications DESC
            LIMIT 10
        """)
        print("\n    Top 10 employers by total applications:")
        for name, city, state, apps in cur.fetchall():
            loc = "{}, {}".format(city or "?", state or "?")
            print("        {:,} apps | {} ({})".format(apps, name, loc))

        # Year span
        cur.execute("""
            SELECT MIN(first_seen_year), MAX(last_seen_year),
                   AVG(last_seen_year - first_seen_year + 1)
            FROM refined.employers
        """)
        min_year, max_year, avg_span = cur.fetchone()
        print("\n    Year coverage: {} to {}".format(min_year, max_year))
        print("    Average employer lifespan: {:.1f} years".format(float(avg_span)))


def check_combined_fields(conn):
    """Verify combined fields (employer_address, employer_poc_name) are populated."""
    print("\n[DQ CHECK 4] Combined field quality")
    print("-" * 70)

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM refined.fy_all")
        total = cur.fetchone()[0]

        # employer_address
        cur.execute("""
            SELECT COUNT(*) FROM refined.fy_all
            WHERE employer_address IS NULL OR employer_address = ''
        """)
        addr_null = cur.fetchone()[0]

        # employer_poc_name
        cur.execute("""
            SELECT COUNT(*) FROM refined.fy_all
            WHERE employer_poc_name IS NULL OR employer_poc_name = ''
        """)
        poc_null = cur.fetchone()[0]

        print("    employer_address NULL/empty: {:,} / {:,} ({:.1f}%)".format(
            addr_null, total, addr_null / total * 100 if total > 0 else 0
        ))
        print("    employer_poc_name NULL/empty: {:,} / {:,} ({:.1f}%)".format(
            poc_null, total, poc_null / total * 100 if total > 0 else 0
        ))

        # Sample combined values
        cur.execute("""
            SELECT employer_address, employer_poc_name
            FROM refined.fy_all
            WHERE employer_address IS NOT NULL AND employer_address != ''
              AND employer_poc_name IS NOT NULL AND employer_poc_name != ''
            LIMIT 5
        """)
        print("\n    Sample combined values:")
        for addr, poc in cur.fetchall():
            print("        address: {}".format(addr[:80]))
            print("        poc:     {}".format(poc))
            print()


def check_case_status_distribution(conn):
    """Show case_status distribution in fy_all."""
    print("\n[DQ CHECK 5] Case status distribution (fy_all)")
    print("-" * 70)

    with conn.cursor() as cur:
        cur.execute("""
            SELECT case_status, COUNT(*) AS cnt,
                   ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
            FROM refined.fy_all
            GROUP BY case_status
            ORDER BY cnt DESC
        """)
        for status, cnt, pct in cur.fetchall():
            print("    {:<30} {:>10,} ({:>5.1f}%)".format(status or "(NULL)", cnt, float(pct)))


def check_null_rates(conn):
    """Check NULL rates for key columns in fy_all."""
    print("\n[DQ CHECK 6] NULL rates for key columns (fy_all)")
    print("-" * 70)

    key_columns = [
        "case_number", "employer_name", "job_title",
        "employer_address", "employer_city", "employer_state", "employer_postal_code",
        "worksite_city", "worksite_state",
        "wage_rate_of_pay_from", "wage_unit_of_pay",
        "case_status", "soc_code", "prevailing_wage",
        "employer_poc_name", "employer_poc_email"
    ]

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM refined.fy_all")
        total = cur.fetchone()[0]

        for col in key_columns:
            cur.execute("""
                SELECT COUNT(*) FROM refined.fy_all
                WHERE {} IS NULL OR TRIM(CAST({} AS TEXT)) = ''
            """.format(col, col))
            nulls = cur.fetchone()[0]
            pct = nulls / total * 100 if total > 0 else 0
            flag = "" if pct < 1 else " <-- HIGH" if pct > 10 else " <-- NOTABLE"
            print("    {:<30} {:>10,} NULL ({:>5.1f}%){}".format(col, nulls, pct, flag))


def main():
    print("=" * 60)
    print("H1B Refined Layer Build")
    print("=" * 60)

    conn = get_h1b_connection()
    total_start = time.time()

    try:
        print("\n[Step 1/8] Creating refined schema...")
        create_refined_schema(conn)

        print("\n[Step 2/8] Dropping existing refined tables (schema change)...")
        drop_refined_tables(conn)

        print("\n[Step 3/8] Creating refined tables...")
        create_refined_tables(conn)

        print("\n[Step 4/8] Populating per-FY refined tables...")
        total_rows = 0
        for fy, quarters in sorted(FISCAL_YEAR_QUARTERS.items()):
            rows = populate_refined_table(conn, fy, quarters)
            total_rows += rows

        print("\n[Step 5/8] Building fy_all (all years combined)...")
        fy_all_rows = populate_fy_all(conn)

        print("\n[Step 6/8] Building employers dimension table...")
        emp_rows = populate_employers(conn)

        print("\n[Step 7/8] Verifying row counts...")
        verify_row_counts(conn)

        print("\n[Step 8/8] Running data quality checks...")
        check_fy_all_consistency(conn)
        check_case_number_uniqueness(conn)
        check_fy_all_uniqueness(conn)
        check_employers_table(conn)
        check_combined_fields(conn)
        check_case_status_distribution(conn)
        check_null_rates(conn)

    finally:
        conn.close()

    total_elapsed = time.time() - total_start
    print("\n" + "=" * 60)
    print("Refined layer build complete!")
    print("  Per-FY rows:    {:,}".format(total_rows))
    print("  fy_all rows:    {:,}".format(fy_all_rows))
    print("  Employers:      {:,}".format(emp_rows))
    print("  Total time:     {:.1f}s".format(total_elapsed))
    print("=" * 60)


if __name__ == "__main__":
    main()
