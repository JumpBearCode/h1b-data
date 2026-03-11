"""
Employer name normalization and fuzzy matching.

Two-step approach:
  Step 1: Deterministic normalization (UPPER + strip suffixes/punctuation)
  Step 2: Trigram similarity matching with blocking (pg_trgm)

Adds `employer_name_normalized` column to refined.employers and
creates refined.employer_match_candidates for fuzzy match review.

Usage:
    uv run python src/employer_normalization.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db_connector import get_h1b_connection


def step1_deterministic_normalization(conn):
    """
    Step 1: Add employer_name_normalized column with deterministic cleaning.

    Rules:
      1. UPPER()
      2. Remove common legal suffixes (LLC, INC, CORP, etc.)
      3. Remove punctuation (commas, periods, quotes, dashes)
      4. Collapse multiple spaces
      5. TRIM
    """
    print("=" * 70)
    print("STEP 1: Deterministic Normalization")
    print("=" * 70)

    start = time.time()

    with conn.cursor() as cur:
        # Add column if not exists
        cur.execute("""
            ALTER TABLE refined.employers
            ADD COLUMN IF NOT EXISTS employer_name_normalized TEXT
        """)
        conn.commit()

        # Normalize: UPPER -> strip suffixes -> strip punctuation -> collapse spaces
        cur.execute("""
            UPDATE refined.employers
            SET employer_name_normalized = (
                SELECT
                    -- Final trim and collapse spaces
                    TRIM(REGEXP_REPLACE(
                        -- Strip punctuation: commas, periods, quotes, dashes, parens, slashes
                        REGEXP_REPLACE(
                            -- Strip common legal suffixes (order matters: longer first)
                            REGEXP_REPLACE(
                                UPPER(TRIM(employer_name)),
                                -- Anchored at end, optional preceding comma/space
                                '[\s,]*(INCORPORATED|CORPORATION|PROFESSIONAL CORPORATION|' ||
                                'LIMITED LIABILITY COMPANY|LIMITED LIABILITY PARTNERSHIP|' ||
                                'LIMITED PARTNERSHIP|LIMITED|' ||
                                'L\.?L\.?C\.?|L\.?L\.?P\.?|L\.?P\.?|' ||
                                'INC\.?|CORP\.?|CO\.?|P\.?C\.?|P\.?A\.?|' ||
                                'D/?B/?A)\s*$',
                                '',
                                'g'
                            ),
                            -- Remove: , . " '' ` - () /
                            '[,\."''`\-\(\)/]',
                            ' ',
                            'g'
                        ),
                        -- Collapse multiple spaces into one
                        '\s{2,}',
                        ' ',
                        'g'
                    ))
            )
        """)
        conn.commit()

        # Stats: how many distinct normalized names vs original
        cur.execute("SELECT COUNT(*) FROM refined.employers")
        total_original = cur.fetchone()[0]

        cur.execute("SELECT COUNT(DISTINCT employer_name_normalized) FROM refined.employers")
        total_normalized = cur.fetchone()[0]

        reduced = total_original - total_normalized
        pct = reduced / total_original * 100 if total_original > 0 else 0

    elapsed = time.time() - start
    print("\n    Original distinct employer_name:    {:,}".format(total_original))
    print("    After normalization (distinct):     {:,}".format(total_normalized))
    print("    Collapsed (exact match after norm): {:,} ({:.1f}%)".format(reduced, pct))
    print("    Time: {:.1f}s".format(elapsed))

    # Show examples of collapsed groups
    print("\n    Top 20 normalized groups (most variants collapsed):")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT employer_name_normalized,
                   COUNT(*) AS cnt,
                   SUM(total_applications) AS total_apps,
                   array_agg(employer_name ORDER BY total_applications DESC) AS variants
            FROM refined.employers
            GROUP BY employer_name_normalized
            HAVING COUNT(*) > 1
            ORDER BY SUM(total_applications) DESC
            LIMIT 20
        """)
        for row in cur.fetchall():
            norm_name, cnt, total_apps, variants = row
            print("\n        [{}] {:,} apps, {} variants:".format(norm_name, total_apps, cnt))
            for v in variants[:5]:
                print("            - {}".format(v))
            if cnt > 5:
                print("            ... and {} more".format(cnt - 5))

    # Show how many groups have N variants
    print("\n    Distribution of variant counts per normalized name:")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT cnt, COUNT(*) AS groups, SUM(cnt) AS total_employers
            FROM (
                SELECT employer_name_normalized, COUNT(*) AS cnt
                FROM refined.employers
                GROUP BY employer_name_normalized
            ) sub
            GROUP BY cnt
            ORDER BY cnt
        """)
        for cnt, groups, total_emp in cur.fetchall():
            if cnt == 1:
                print("        {} variant:  {:,} groups ({:,} employers) -- already unique".format(
                    cnt, groups, total_emp))
            else:
                print("        {} variants: {:,} groups ({:,} employers)".format(
                    cnt, groups, total_emp))

    return total_original, total_normalized


def step2_trigram_similarity(conn):
    """
    Step 2: Use pg_trgm to find fuzzy matches among normalized names.

    Blocking strategy:
      - Only compare employers in the same state (reduces from N^2 to manageable)
      - Use similarity() threshold >= 0.6 for candidates
      - Exclude exact matches (already handled in Step 1)
    """
    print("\n" + "=" * 70)
    print("STEP 2: Trigram Similarity Matching (pg_trgm)")
    print("=" * 70)

    start = time.time()

    with conn.cursor() as cur:
        # Create index for trigram similarity
        print("\n    Creating trigram index on employer_name_normalized...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_employers_trgm
            ON refined.employers
            USING gin (employer_name_normalized gin_trgm_ops)
        """)
        conn.commit()
        print("    [OK] Index created.")

        # Create match candidates table
        print("    Finding fuzzy match candidates (same state, similarity >= 0.6)...")
        cur.execute("DROP TABLE IF EXISTS refined.employer_match_candidates")
        conn.commit()

        cur.execute("""
            CREATE TABLE refined.employer_match_candidates AS
            SELECT
                a.employer_name AS name_a,
                b.employer_name AS name_b,
                a.employer_name_normalized AS norm_a,
                b.employer_name_normalized AS norm_b,
                a.employer_state AS state,
                similarity(a.employer_name_normalized, b.employer_name_normalized) AS sim_score,
                a.total_applications AS apps_a,
                b.total_applications AS apps_b,
                a.total_applications + b.total_applications AS apps_combined
            FROM refined.employers a
            JOIN refined.employers b
                ON a.employer_state = b.employer_state
                AND a.employer_name_normalized < b.employer_name_normalized
                AND a.employer_name_normalized % b.employer_name_normalized
            WHERE similarity(a.employer_name_normalized, b.employer_name_normalized) >= 0.6
              AND a.employer_name_normalized != b.employer_name_normalized
        """)
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM refined.employer_match_candidates")
        total_pairs = cur.fetchone()[0]

    elapsed = time.time() - start
    print("    [OK] Found {:,} candidate pairs ({:.1f}s)".format(total_pairs, elapsed))

    # Show distribution by similarity score
    print("\n    Candidate pairs by similarity score bucket:")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                CASE
                    WHEN sim_score >= 0.9 THEN '0.90-1.00 (very high)'
                    WHEN sim_score >= 0.8 THEN '0.80-0.89 (high)'
                    WHEN sim_score >= 0.7 THEN '0.70-0.79 (medium)'
                    WHEN sim_score >= 0.6 THEN '0.60-0.69 (low)'
                END AS bucket,
                COUNT(*) AS pairs,
                SUM(apps_combined) AS total_apps_affected
            FROM refined.employer_match_candidates
            GROUP BY 1
            ORDER BY 1 DESC
        """)
        for bucket, pairs, apps in cur.fetchall():
            print("        {}: {:,} pairs ({:,} apps affected)".format(bucket, pairs, apps))

    # Show top high-confidence matches
    print("\n    Top 30 highest-confidence matches (sim >= 0.8, by combined apps):")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT name_a, name_b, state, sim_score, apps_a, apps_b
            FROM refined.employer_match_candidates
            WHERE sim_score >= 0.8
            ORDER BY apps_combined DESC
            LIMIT 30
        """)
        for name_a, name_b, state, sim, apps_a, apps_b in cur.fetchall():
            print("        [{:.2f}] {} ({:,}) <-> {} ({:,}) [{}]".format(
                sim, name_a, apps_a, name_b, apps_b, state))

    # Show some medium-confidence matches for review
    print("\n    Sample medium-confidence matches (0.6-0.79, by combined apps):")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT name_a, name_b, state, sim_score, apps_a, apps_b
            FROM refined.employer_match_candidates
            WHERE sim_score >= 0.6 AND sim_score < 0.8
            ORDER BY apps_combined DESC
            LIMIT 20
        """)
        for name_a, name_b, state, sim, apps_a, apps_b in cur.fetchall():
            print("        [{:.2f}] {} ({:,}) <-> {} ({:,}) [{}]".format(
                sim, name_a, apps_a, name_b, apps_b, state))

    return total_pairs


def summary(conn, total_original, total_normalized, total_pairs):
    """Print overall summary."""
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    with conn.cursor() as cur:
        # Count how many normalized groups have 2+ members (Step 1 merges)
        cur.execute("""
            SELECT COUNT(*), SUM(cnt - 1)
            FROM (
                SELECT employer_name_normalized, COUNT(*) AS cnt
                FROM refined.employers
                GROUP BY employer_name_normalized
                HAVING COUNT(*) > 1
            ) sub
        """)
        step1_groups, step1_merges = cur.fetchone()

        # Count unique normalized names involved in Step 2 pairs
        cur.execute("""
            SELECT COUNT(DISTINCT norm_name)
            FROM (
                SELECT norm_a AS norm_name FROM refined.employer_match_candidates
                UNION
                SELECT norm_b FROM refined.employer_match_candidates
            ) sub
        """)
        step2_names = cur.fetchone()[0]

    print("""
    Original employer names:           {:,}

    Step 1 (deterministic normalization):
        Distinct after normalization:  {:,}
        Groups with 2+ variants:      {:,}
        Names collapsed:              {:,}

    Step 2 (trigram fuzzy matching):
        Candidate pairs found:        {:,}
        Distinct names in candidates: {:,}

    Potential total reduction:
        Step 1 alone:                 {:,} → {:,} (-{:.1f}%)
        Step 2 additional candidates: {:,} more names to review
    """.format(
        total_original,
        total_normalized,
        step1_groups,
        total_original - total_normalized,
        total_pairs,
        step2_names,
        total_original, total_normalized,
        (total_original - total_normalized) / total_original * 100,
        step2_names,
    ))


def main():
    conn = get_h1b_connection()

    try:
        total_original, total_normalized = step1_deterministic_normalization(conn)
        total_pairs = step2_trigram_similarity(conn)
        summary(conn, total_original, total_normalized, total_pairs)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
