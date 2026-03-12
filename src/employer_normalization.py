"""
Employer name normalization pipeline.

Extracts all distinct employer names from refined.fy_all,
applies Python-based canonicalization, and writes results to
refined.employer_name_lookup (raw_name, normalized_name).

Normalization steps:
  1. Lowercase + strip whitespace
  2. Remove legal suffixes (via cleanco + custom rules)
  3. Expand common abbreviations (& → and, svc → services, etc.)
  4. Remove all punctuation
  5. Collapse whitespace
  6. Sort tokens alphabetically (for order-invariant matching)

Usage:
    uv run python src/employer_normalization.py
"""

import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cleanco import basename
from src.db_connector import get_h1b_connection


# ---------------------------------------------------------------------------
# Normalization rules
# ---------------------------------------------------------------------------

# Legal suffixes to strip (beyond what cleanco handles).
# Applied AFTER cleanco, which catches most international forms.
# These catch edge cases and abbreviations cleanco may miss.
LEGAL_SUFFIXES = re.compile(
    r'\b('
    r'incorporated|corporation|professional corporation|'
    r'limited liability company|limited liability partnership|'
    r'limited partnership|limited|'
    r'l\.?l\.?c\.?|l\.?l\.?p\.?|l\.?p\.?|'
    r'inc\.?|corp\.?|co\.?|ltd\.?|p\.?c\.?|p\.?a\.?|'
    r'd/?b/?a'
    r')\s*$',
    re.IGNORECASE
)

# Pattern to split concatenated suffixes like "SERVICESLIMITED" -> "SERVICES LIMITED"
GLUED_SUFFIX = re.compile(
    r'(LIMITED|INCORPORATED|CORPORATION|COMPANY)$',
    re.IGNORECASE
)

# Common abbreviations to expand (order matters: longer patterns first)
ABBREVIATIONS = [
    (re.compile(r'\b&\b'), ' and '),
    (re.compile(r'\bsvcs?\b', re.IGNORECASE), 'services'),
    (re.compile(r'\btech\b', re.IGNORECASE), 'technology'),
    (re.compile(r'\btechs\b', re.IGNORECASE), 'technologies'),
    (re.compile(r'\bintl\b', re.IGNORECASE), 'international'),
    (re.compile(r'\bnatl\b', re.IGNORECASE), 'national'),
    (re.compile(r'\bmgmt\b', re.IGNORECASE), 'management'),
    (re.compile(r'\bmfg\b', re.IGNORECASE), 'manufacturing'),
    (re.compile(r'\bengr\b', re.IGNORECASE), 'engineering'),
    (re.compile(r'\beng\b', re.IGNORECASE), 'engineering'),
    (re.compile(r'\bsys\b', re.IGNORECASE), 'systems'),
    (re.compile(r'\bsoln?s?\b', re.IGNORECASE), 'solutions'),
    (re.compile(r'\binfo\b', re.IGNORECASE), 'information'),
    (re.compile(r'\bassoc\b', re.IGNORECASE), 'associates'),
    (re.compile(r'\buniv\b', re.IGNORECASE), 'university'),
    (re.compile(r'\bhosp\b', re.IGNORECASE), 'hospital'),
    (re.compile(r'\bmed\b', re.IGNORECASE), 'medical'),
    (re.compile(r'\bctr\b', re.IGNORECASE), 'center'),
    (re.compile(r'\bctrs\b', re.IGNORECASE), 'centers'),
    (re.compile(r'\bgvt\b', re.IGNORECASE), 'government'),
    (re.compile(r'\bgov\b', re.IGNORECASE), 'government'),
    (re.compile(r'\bdev\b', re.IGNORECASE), 'development'),
    (re.compile(r'\bcomm\b', re.IGNORECASE), 'communications'),
    (re.compile(r'\bfin\b', re.IGNORECASE), 'financial'),
    (re.compile(r'\bpharm\b', re.IGNORECASE), 'pharmaceutical'),
    (re.compile(r'\blab\b', re.IGNORECASE), 'laboratory'),
    (re.compile(r'\blabs\b', re.IGNORECASE), 'laboratories'),
    (re.compile(r'\bamer\b', re.IGNORECASE), 'america'),
    (re.compile(r'\bconsltg\b', re.IGNORECASE), 'consulting'),
]

# Punctuation pattern: everything that is not alphanumeric or whitespace
PUNCTUATION = re.compile(r'[^a-z0-9\s]')

# Multiple whitespace
MULTI_SPACE = re.compile(r'\s+')


def normalize_employer_name(raw_name: str) -> str:
    """
    Apply full canonicalization pipeline to a single employer name.

    Returns lowercase, suffix-stripped, abbreviation-expanded,
    punctuation-free, token-sorted string.
    """
    if not raw_name:
        return ''

    name = raw_name.strip()

    # Step 0: split concatenated suffixes like "SERVICESLIMITED"
    name = GLUED_SUFFIX.sub(lambda m: ' ' + m.group(1), name)

    # Step 1: cleanco strips legal suffixes (handles international forms too)
    cleaned = basename(name)
    # If cleanco returns empty, fall back to original (happens with short names like SCA, SHA)
    if not cleaned.strip():
        cleaned = name
    name = cleaned

    # Step 2: lowercase
    name = name.lower()

    # Step 3: strip remaining legal suffixes our regex catches
    # Apply up to 2 times to catch stacked suffixes like "... Inc Corp"
    for _ in range(2):
        prev = name
        name = LEGAL_SUFFIXES.sub('', name).strip()
        # Don't allow stripping to empty
        if not name:
            name = prev
            break
        if name == prev:
            break

    # Step 4: expand abbreviations
    for pattern, replacement in ABBREVIATIONS:
        name = pattern.sub(replacement, name)

    # Step 5: remove all punctuation (replace with space to not merge words)
    name = PUNCTUATION.sub(' ', name)

    # Step 6: collapse whitespace and trim
    name = MULTI_SPACE.sub(' ', name).strip()

    # Step 7: sort tokens for order-invariant matching
    tokens = name.split()
    name = ' '.join(sorted(tokens))

    return name


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def extract_distinct_names(conn):
    """Extract all distinct employer_name values from refined.fy_all."""
    print("=" * 70)
    print("STEP 1: Extract distinct employer names from refined.fy_all")
    print("=" * 70)

    start = time.time()
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT employer_name FROM refined.fy_all ORDER BY employer_name")
        names = [row[0] for row in cur.fetchall()]

    elapsed = time.time() - start
    print(f"    Extracted {len(names):,} distinct employer names ({elapsed:.1f}s)")
    return names


def normalize_all(names):
    """Apply normalization to all names. Returns list of (raw, normalized) tuples."""
    print("\n" + "=" * 70)
    print("STEP 2: Normalize employer names (Python-side)")
    print("=" * 70)

    start = time.time()
    results = []
    for i, raw in enumerate(names):
        normalized = normalize_employer_name(raw)
        results.append((raw, normalized))
        if (i + 1) % 50000 == 0:
            print(f"    Processed {i + 1:,} / {len(names):,}...")

    elapsed = time.time() - start
    print(f"    Normalized {len(results):,} names ({elapsed:.1f}s)")

    # Stats
    distinct_normalized = len(set(r[1] for r in results))
    collapsed = len(results) - distinct_normalized
    pct = collapsed / len(results) * 100 if results else 0
    print(f"\n    Original distinct names:          {len(results):,}")
    print(f"    Distinct after normalization:     {distinct_normalized:,}")
    print(f"    Collapsed (exact match):          {collapsed:,} ({pct:.1f}%)")

    return results


def write_to_db(conn, results):
    """Write results to refined.employer_name_lookup table."""
    print("\n" + "=" * 70)
    print("STEP 3: Write to refined.employer_name_lookup")
    print("=" * 70)

    start = time.time()
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS refined.employer_name_lookup")
        cur.execute("""
            CREATE TABLE refined.employer_name_lookup (
                raw_name TEXT NOT NULL,
                normalized_name TEXT NOT NULL
            )
        """)
        conn.commit()

        # Batch insert using execute_values for speed
        from psycopg2.extras import execute_values
        batch_size = 10000
        for i in range(0, len(results), batch_size):
            batch = results[i:i + batch_size]
            execute_values(
                cur,
                "INSERT INTO refined.employer_name_lookup (raw_name, normalized_name) VALUES %s",
                batch,
                page_size=batch_size
            )
            if (i + batch_size) % 50000 == 0 or i + batch_size >= len(results):
                conn.commit()
                print(f"    Inserted {min(i + batch_size, len(results)):,} / {len(results):,}...")

        conn.commit()

        # Create indexes
        print("    Creating indexes...")
        cur.execute("CREATE INDEX idx_enl_raw ON refined.employer_name_lookup (raw_name)")
        cur.execute("CREATE INDEX idx_enl_norm ON refined.employer_name_lookup (normalized_name)")
        conn.commit()

    elapsed = time.time() - start
    print(f"    Done ({elapsed:.1f}s)")


def evaluate(conn, results):
    """Print evaluation metrics and sample groups."""
    print("\n" + "=" * 70)
    print("EVALUATION")
    print("=" * 70)

    # Build a mapping: normalized -> list of raw names
    from collections import defaultdict
    groups = defaultdict(list)
    for raw, norm in results:
        groups[norm].append(raw)

    # Multi-variant groups (where normalization actually merged something)
    multi = {k: v for k, v in groups.items() if len(v) > 1}
    multi_sorted = sorted(multi.items(), key=lambda x: len(x[1]), reverse=True)

    print(f"\n    Total groups (distinct normalized names): {len(groups):,}")
    print(f"    Groups with 1 member (already unique):    {len(groups) - len(multi):,}")
    print(f"    Groups with 2+ members (collapsed):       {len(multi):,}")

    # Distribution of group sizes
    from collections import Counter
    size_dist = Counter(len(v) for v in groups.values())
    print("\n    Distribution of group sizes:")
    for size in sorted(size_dist.keys()):
        cnt = size_dist[size]
        if size == 1:
            print(f"        {size} member:   {cnt:,} groups")
        else:
            print(f"        {size} members:  {cnt:,} groups")
        if size > 10:
            break

    # Top 30 groups by number of variants
    print("\n    Top 30 groups (most variants collapsed):")
    for norm, variants in multi_sorted[:30]:
        print(f"\n        [{norm}] — {len(variants)} variants:")
        for v in sorted(variants)[:8]:
            print(f"            - {v}")
        if len(variants) > 8:
            print(f"            ... and {len(variants) - 8} more")

    # Spot-check well-known companies
    print("\n    Spot-check: well-known companies:")
    checks = ['amazon', 'google', 'meta', 'microsoft', 'apple', 'tata', 'ibm',
              'deloitte', 'ernst', 'infosys', 'wipro', 'cognizant']
    for check in checks:
        matching = [(norm, variants) for norm, variants in groups.items()
                    if check in norm]
        if matching:
            for norm, variants in sorted(matching, key=lambda x: len(x[1]), reverse=True)[:3]:
                print(f"\n        [{norm}] — {len(variants)} variants:")
                for v in sorted(variants)[:5]:
                    print(f"            - {v}")
                if len(variants) > 5:
                    print(f"            ... and {len(variants) - 5} more")

    # Verify DB contents
    print("\n    Verifying database table:")
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM refined.employer_name_lookup")
        total_rows = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT raw_name) FROM refined.employer_name_lookup")
        distinct_raw = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT normalized_name) FROM refined.employer_name_lookup")
        distinct_norm = cur.fetchone()[0]
    print(f"        Total rows:              {total_rows:,}")
    print(f"        Distinct raw_name:       {distinct_raw:,}")
    print(f"        Distinct normalized_name: {distinct_norm:,}")
    print(f"        Reduction:               {total_rows - distinct_norm:,} ({(total_rows - distinct_norm)/total_rows*100:.1f}%)")


def build_similarity_graph(conn, threshold=0.8):
    """
    Build similarity pairings on normalized names.

    similar_to includes ALL related rows:
      - Exact matches: other rows with the same normalized_name (score=1.0)
      - Fuzzy matches: rows with different but similar normalized_name (score >= threshold)

    Columns added:
      - id: SERIAL primary key (1..N)
      - similar_to_id: INTEGER[] — IDs of all similar rows (excluding self)
      - similar_to_raw: TEXT[] — corresponding raw_name values (same order)
    """
    print("\n" + "=" * 70)
    print("STEP 4: Build similarity graph (pg_trgm)")
    print("=" * 70)

    start = time.time()

    with conn.cursor() as cur:
        # ----- 4a: Add primary key ID -----
        print("\n    Adding primary key id column...")
        cur.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_schema = 'refined' AND table_name = 'employer_name_lookup'
              AND column_name = 'id'
        """)
        if not cur.fetchone():
            cur.execute("""
                ALTER TABLE refined.employer_name_lookup
                ADD COLUMN id SERIAL PRIMARY KEY
            """)
        else:
            cur.execute("""
                ALTER TABLE refined.employer_name_lookup
                DROP CONSTRAINT IF EXISTS employer_name_lookup_pkey
            """)
            cur.execute("ALTER TABLE refined.employer_name_lookup DROP COLUMN id")
            cur.execute("""
                ALTER TABLE refined.employer_name_lookup
                ADD COLUMN id SERIAL PRIMARY KEY
            """)
        conn.commit()
        print("    [OK] id column added (1 to N)")

        # ----- 4b: Dedup table for trigram comparison -----
        print("    Creating deduplicated working table...")
        cur.execute("DROP TABLE IF EXISTS refined._norm_dedup")
        cur.execute("""
            CREATE TABLE refined._norm_dedup AS
            SELECT MIN(id) AS rep_id, normalized_name
            FROM refined.employer_name_lookup
            GROUP BY normalized_name
        """)
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM refined._norm_dedup")
        n_dedup = cur.fetchone()[0]
        print(f"    [OK] {n_dedup:,} unique normalized names")

        # ----- 4c: pg_trgm index -----
        print("    Creating trigram index...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_norm_dedup_trgm
            ON refined._norm_dedup USING gin (normalized_name gin_trgm_ops)
        """)
        conn.commit()

        cur.execute(f"SET pg_trgm.similarity_threshold = {threshold}")
        conn.commit()
        print(f"    [OK] trigram index ready (threshold={threshold})")

        # ----- 4d: Find fuzzy pairs (different normalized names, score >= threshold) -----
        print(f"    Finding fuzzy pairs (similarity >= {threshold})...")
        cur.execute("DROP TABLE IF EXISTS refined._sim_pairs")
        cur.execute("""
            CREATE TABLE refined._sim_pairs AS
            SELECT
                a.normalized_name AS norm_a,
                b.normalized_name AS norm_b,
                similarity(a.normalized_name, b.normalized_name) AS sim_score
            FROM refined._norm_dedup a
            JOIN refined._norm_dedup b
                ON a.normalized_name % b.normalized_name
                AND a.rep_id < b.rep_id
        """)
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM refined._sim_pairs")
        n_fuzzy_pairs = cur.fetchone()[0]
        elapsed_pairs = time.time() - start
        print(f"    [OK] {n_fuzzy_pairs:,} fuzzy pairs ({elapsed_pairs:.1f}s)")

        # How many normalized_names have exact-match groups (2+ raw names)?
        cur.execute("""
            SELECT COUNT(*) FROM (
                SELECT normalized_name FROM refined.employer_name_lookup
                GROUP BY normalized_name HAVING COUNT(*) > 1
            ) sub
        """)
        n_exact_groups = cur.fetchone()[0]
        cur.execute("""
            SELECT SUM(cnt) FROM (
                SELECT COUNT(*) AS cnt FROM refined.employer_name_lookup
                GROUP BY normalized_name HAVING COUNT(*) > 1
            ) sub
        """)
        n_exact_rows = cur.fetchone()[0]
        print(f"    [OK] {n_exact_groups:,} exact-match groups ({n_exact_rows:,} rows)")

        # ----- 4e: Build similar_to_id and similar_to_raw columns -----
        # For each row, collect:
        #   1. All OTHER rows with the same normalized_name (exact matches)
        #   2. All rows whose normalized_name is fuzzy-similar (from _sim_pairs)
        print("\n    Building similar_to columns (exact + fuzzy)...")

        # Drop old columns if they exist, add new ones
        for col in ['similar_to', 'similar_to_id', 'similar_to_raw']:
            cur.execute(f"""
                ALTER TABLE refined.employer_name_lookup
                DROP COLUMN IF EXISTS {col}
            """)
        cur.execute("""
            ALTER TABLE refined.employer_name_lookup
            ADD COLUMN similar_to_id INTEGER[] DEFAULT '{}',
            ADD COLUMN similar_to_raw TEXT[] DEFAULT '{}'
        """)
        conn.commit()

        # Build the full neighbor set in one query:
        # - exact: same normalized_name, different id
        # - fuzzy: different normalized_name linked via _sim_pairs
        cur.execute("""
            WITH
            -- For each normalized_name, all IDs and raw_names
            norm_members AS (
                SELECT normalized_name, id, raw_name
                FROM refined.employer_name_lookup
            ),
            -- Fuzzy-linked normalized_names (both directions)
            fuzzy_links AS (
                SELECT norm_a AS norm, norm_b AS linked_norm FROM refined._sim_pairs
                UNION ALL
                SELECT norm_b, norm_a FROM refined._sim_pairs
            ),
            -- For each row, collect all neighbor IDs:
            --   (a) exact: same normalized_name, different row
            --   (b) fuzzy: rows under fuzzy-linked normalized_names
            all_neighbors AS (
                -- (a) exact matches
                SELECT t.id AS src_id, m.id AS nbr_id, m.raw_name AS nbr_raw
                FROM refined.employer_name_lookup t
                JOIN norm_members m
                    ON t.normalized_name = m.normalized_name
                    AND t.id != m.id
                UNION
                -- (b) fuzzy matches
                SELECT t.id AS src_id, m.id AS nbr_id, m.raw_name AS nbr_raw
                FROM refined.employer_name_lookup t
                JOIN fuzzy_links fl ON t.normalized_name = fl.norm
                JOIN norm_members m ON fl.linked_norm = m.normalized_name
            ),
            -- Aggregate per source row
            agg AS (
                SELECT
                    src_id,
                    array_agg(nbr_id ORDER BY nbr_id) AS ids,
                    array_agg(nbr_raw ORDER BY nbr_id) AS raws
                FROM all_neighbors
                GROUP BY src_id
            )
            UPDATE refined.employer_name_lookup t
            SET similar_to_id = a.ids,
                similar_to_raw = a.raws
            FROM agg a
            WHERE t.id = a.src_id
        """)
        conn.commit()
        print("    [OK] similar_to_id + similar_to_raw populated")

        # ----- 4f: Stats -----
        cur.execute("""
            SELECT COUNT(*) FROM refined.employer_name_lookup
            WHERE similar_to_id != '{}'
        """)
        rows_with_similar = cur.fetchone()[0]

        cur.execute("""
            SELECT AVG(array_length(similar_to_id, 1))
            FROM refined.employer_name_lookup
            WHERE similar_to_id != '{}'
        """)
        avg_similar = cur.fetchone()[0]

        # Clean up temp tables
        cur.execute("DROP TABLE IF EXISTS refined._norm_dedup")
        cur.execute("DROP TABLE IF EXISTS refined._sim_pairs")
        conn.commit()

    elapsed = time.time() - start
    print(f"\n    Rows with neighbors (exact+fuzzy): {rows_with_similar:,} / 214,366")
    print(f"    Avg neighbor list length:          {avg_similar:.1f}")
    print(f"    Total time: {elapsed:.1f}s")

    return rows_with_similar


def evaluate_similarity(conn):
    """Show sample similarity pairings for validation."""
    print("\n" + "=" * 70)
    print("SIMILARITY EVALUATION")
    print("=" * 70)

    with conn.cursor() as cur:
        # Distribution of neighbor list sizes
        print("\n    Distribution of similar_to_id sizes:")
        cur.execute("""
            SELECT
                CASE
                    WHEN similar_to_id = '{}' THEN '0 (unique)'
                    WHEN array_length(similar_to_id, 1) <= 5 THEN '1-5'
                    WHEN array_length(similar_to_id, 1) <= 10 THEN '6-10'
                    WHEN array_length(similar_to_id, 1) <= 20 THEN '11-20'
                    WHEN array_length(similar_to_id, 1) <= 50 THEN '21-50'
                    ELSE '>50'
                END AS bucket,
                COUNT(*) AS rows
            FROM refined.employer_name_lookup
            GROUP BY 1
            ORDER BY 1
        """)
        for bucket, cnt in cur.fetchall():
            print(f"        {bucket:>12}: {cnt:>8,} rows")

        # Top 20 by neighbor count
        print("\n    Top 20 rows by number of neighbors:")
        cur.execute("""
            SELECT id, raw_name, normalized_name,
                   array_length(similar_to_id, 1) AS n
            FROM refined.employer_name_lookup
            WHERE similar_to_id != '{}'
            ORDER BY array_length(similar_to_id, 1) DESC
            LIMIT 20
        """)
        for rid, raw, norm, n in cur.fetchall():
            print(f"        ID {rid:>6}: [{norm}] — {n} neighbors — {raw}")

        # Spot-check Amazon
        print("\n    Spot-check: Amazon")
        cur.execute("""
            SELECT id, raw_name, normalized_name,
                   array_length(similar_to_id, 1) AS n,
                   similar_to_id, similar_to_raw
            FROM refined.employer_name_lookup
            WHERE raw_name = 'Amazon.com Services LLC'
        """)
        row = cur.fetchone()
        if row:
            rid, raw, norm, n, ids, raws = row
            print(f"        ID {rid}: {raw}")
            print(f"        normalized: [{norm}], {n} neighbors:")
            for i in range(min(n or 0, 25)):
                print(f"            → ID {ids[i]}: {raws[i]}")
            if (n or 0) > 25:
                print(f"            ... and {n - 25} more")

        # Spot-check Google
        print("\n    Spot-check: Google")
        cur.execute("""
            SELECT id, raw_name, normalized_name,
                   array_length(similar_to_id, 1) AS n,
                   similar_to_id, similar_to_raw
            FROM refined.employer_name_lookup
            WHERE raw_name = 'Google LLC'
        """)
        row = cur.fetchone()
        if row:
            rid, raw, norm, n, ids, raws = row
            print(f"        ID {rid}: {raw}")
            print(f"        normalized: [{norm}], {n} neighbors:")
            for i in range(min(n or 0, 15)):
                print(f"            → ID {ids[i]}: {raws[i]}")

        # Spot-check Tata
        print("\n    Spot-check: Tata Consultancy")
        cur.execute("""
            SELECT id, raw_name, normalized_name,
                   array_length(similar_to_id, 1) AS n,
                   similar_to_id, similar_to_raw
            FROM refined.employer_name_lookup
            WHERE raw_name = 'TATA CONSULTANCY SERVICES LIMITED'
        """)
        row = cur.fetchone()
        if row:
            rid, raw, norm, n, ids, raws = row
            print(f"        ID {rid}: {raw}")
            print(f"        normalized: [{norm}], {n} neighbors:")
            for i in range(min(n or 0, 15)):
                print(f"            → ID {ids[i]}: {raws[i]}")


def main():
    conn = get_h1b_connection()

    try:
        names = extract_distinct_names(conn)
        results = normalize_all(names)
        write_to_db(conn, results)
        evaluate(conn, results)
        build_similarity_graph(conn, threshold=0.8)
        evaluate_similarity(conn)
    finally:
        conn.close()

    print("\n" + "=" * 70)
    print("DONE — refined.employer_name_lookup is ready")
    print("    Columns: id | raw_name | normalized_name | similar_to_id | similar_to_raw")
    print("=" * 70)


if __name__ == "__main__":
    main()
