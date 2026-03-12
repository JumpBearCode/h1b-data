# Employer Name Normalization & Similarity Pipeline

## Overview

This pipeline resolves the employer name fragmentation problem in H1B LCA disclosure data.
The same employer appears under many raw name variants due to inconsistent casing, punctuation,
legal suffixes, and typos. The pipeline produces a lookup table (`refined.employer_name_lookup`)
that maps every raw employer name to a canonical form and links it to all similar entries.

**Source**: `refined.fy_all` (3.5M application rows, 214K distinct employer names)

**Output**: `refined.employer_name_lookup` (214K rows)

```bash
uv run python src/employer_normalization.py
```

---

## Output Table Schema

```sql
refined.employer_name_lookup
├── id                INTEGER   -- Primary key (1..214,366)
├── raw_name          TEXT      -- Original employer name from fy_all
├── normalized_name   TEXT      -- Canonicalized name
├── similar_to_id     INTEGER[] -- IDs of all similar rows (excluding self)
└── similar_to_raw    TEXT[]    -- Corresponding raw names (same order as similar_to_id)
```

---

## Pipeline Architecture

```
                    214,366 distinct raw names
                              │
                    Step 1: Normalization (Python)
                    - cleanco suffix removal
                    - custom suffix stripping
                    - abbreviation expansion
                    - punctuation removal
                    - token sorting
                              │
                    160,706 distinct normalized names  (25% reduction)
                              │
                    Step 2: Similarity (PostgreSQL pg_trgm)
                    - Trigram comparison on 160K unique normalized names
                    - Threshold >= 0.8
                    - 7,103 fuzzy pairs found
                              │
                    Step 3: Build neighbor lists
                    - Exact matches (same normalized_name) + fuzzy matches
                    - Write similar_to_id[] and similar_to_raw[] per row
                              │
                    98,817 rows have >= 1 neighbor
                    115,549 rows are truly unique
```

---

## Step 1: Normalization (Python)

### What It Does

Takes a raw employer name and produces a lowercase, deterministic canonical form.
All rules are applied in `normalize_employer_name()` in `src/employer_normalization.py`.

### Normalization Rules (applied in order)

| # | Rule | Example |
|---|------|---------|
| 0 | Split glued suffixes | `SERVICESLIMITED` → `SERVICES LIMITED` |
| 1 | `cleanco` library strips legal suffixes | `Amazon.com Services LLC` → `Amazon.com Services` |
| 1b | Fallback: if cleanco returns empty, keep original | `SCA, Inc.` → `SCA` (not empty) |
| 2 | Lowercase | `Amazon.com Services` → `amazon.com services` |
| 3 | Custom suffix regex (up to 2 passes) | Strips: `inc`, `corp`, `llc`, `llp`, `lp`, `ltd`, `co`, `pc`, `pa`, `dba`, `incorporated`, `corporation`, `limited`, `limited liability company/partnership`, `professional corporation` |
| 3b | Prevent stripping to empty | `KG INC.` → `kg` (not empty) |
| 4 | Expand 29 abbreviations | `&` → `and`, `tech` → `technology`, `svc` → `services`, `intl` → `international`, `dev` → `development`, `info` → `information`, `eng` → `engineering`, `mgmt` → `management`, `mfg` → `manufacturing`, etc. |
| 5 | Remove all punctuation | Non-alphanumeric chars → space |
| 6 | Collapse whitespace | Multiple spaces → single space, trim |
| 7 | Sort tokens alphabetically | `amazon web services` → `amazon services web` |

### Normalization Examples

| Raw Name | Normalized |
|----------|-----------|
| `Amazon.com Services LLC` | `amazon com services` |
| `AMAZON.COM SERVICES, INC.` | `amazon com services` |
| `Amazon Web Services, Inc.` | `amazon services web` |
| `Ernst & Young U.S. LLP` | `ernst s u young` |
| `TATA CONSULTANCY SERVICESLIMITED` | `consultancy services tata` |
| `WAL-MART ASSOCIATES, INC.` | `associates mart wal` |
| `Meta Platforms, Inc.` | `meta platforms` |
| `JPMorgan Chase & Co.` | `chase jpmorgan` |

### Why Token Sorting?

Token sorting makes the normalization order-invariant:

```
"Amazon Web Services" → "amazon services web"
"Web Services Amazon" → "amazon services web"   (same!)
```

### Normalization Statistics

| Metric | Count |
|--------|-------|
| Original distinct raw names | 214,366 |
| Distinct after normalization | 160,706 |
| Names collapsed (exact match) | 53,660 (25.0%) |
| Groups with 2+ raw variants | 37,052 |

---

## Step 2: Trigram Similarity (PostgreSQL pg_trgm)

### What is Trigram Similarity?

A trigram is a contiguous 3-character subsequence. For example:

```
"amazon"  →  {ama, maz, azo, zon}
```

The similarity between two strings is the overlap of their trigram sets:

```
similarity = |A ∩ B| / |A ∪ B|
```

PostgreSQL provides this via the `pg_trgm` extension with a GIN inverted index.
The index stores a mapping of `trigram → row_ids`, so when comparing two strings,
the database only examines rows that share enough trigrams — avoiding a full N x N scan.

### How the Comparison Works

1. **Deduplicate**: 214K rows → 160K unique normalized names (temp `_norm_dedup` table)
2. **Build GIN trigram index** on the 160K unique names
3. **Self-join** with `%` operator (threshold = 0.8) to find fuzzy pairs
4. **Expand** fuzzy pairs back to all 214K rows

The comparison is 160K x 160K at the trigram level, but the GIN index makes it
sub-quadratic — only strings sharing enough trigrams are actually compared.

### Threshold Selection

| Threshold | Pairs Found | Notes |
|-----------|-------------|-------|
| 0.9 | 1,108 | Very conservative, misses many true matches |
| **0.8** | **7,103** | **Catches typos and abbreviation differences, few false positives** |
| 0.7 | 41,836 | Too noisy: matches different school districts, different hospitals |
| 0.6 | 520,571 | Unusable: massive false positives for short generic names |

**0.8** is used because:
- Catches real variations: `amazon services` ↔ `amazon com services` (0.80)
- Catches typos: `consultancy servies tata` ↔ `consultancy services tata` (0.83)
- Avoids false positives: `elkton nursing` ↔ `ruston nursing` (0.79, different entities) is excluded

---

## Step 3: Building Neighbor Lists

For each of the 214K rows, `similar_to_id` and `similar_to_raw` contain **all** related rows
from two sources:

1. **Exact matches** (score = 1.0): Other rows with the **same** `normalized_name` but different `raw_name`
2. **Fuzzy matches** (score >= 0.8): Rows with a **different but similar** `normalized_name`

Each row excludes itself from its own neighbor list.

This is implemented as a single SQL CTE that UNIONs exact and fuzzy neighbors, then
aggregates per source row with `array_agg`.

### Neighbor Distribution

| Neighbor Count | Rows |
|----------------|------|
| 0 (unique) | 115,549 |
| 1-5 | 95,191 |
| 6-10 | 3,127 |
| 11-20 | 374 |
| 21-50 | 121 |
| >50 | 4 |

---

## Sample Output

### Amazon.com Services LLC (ID 10762)

Normalized: `amazon com services` — **23 neighbors**

19 exact matches (same normalized name) + 4 fuzzy matches (different normalized name):

| ID | raw_name | Match Type |
|----|----------|------------|
| 10678 | AMAZON COM SERVICES LLC | exact |
| 10758 | AMAZON. COM SERVICES LLC | exact |
| 10760 | Amazon.com Services | exact |
| 10761 | AMAZON.COM SERVICES  LLC | exact |
| 10763 | Amazon.Com Services Llc | exact |
| 10764 | AMAZoN.COM SERVICES LLC | exact |
| 10765 | AMAZON.COM SERVICEs LLC | exact |
| 10766 | AMAZON.COM SERVICES LLC | exact |
| 10769 | Amazon.com Services LLC. | exact |
| 10770 | AMAZON.COM SERVICES LLC. | exact |
| 10771 | Amazon.com Services, Inc | exact |
| 10772 | AMAZON.COM SERVICES, INC | exact |
| 10773 | Amazon.com Services, Inc. | exact |
| 10774 | Amazon.com Services, Inc.† | exact |
| 10775 | AMAZON.COM SERVICES, INC. | exact |
| 10776 | Amazon.com Services, Inc. (trailing whitespace) | exact |
| 10777 | Amazon.com Services, LLC | exact |
| 10778 | AMAZON.COM SERVICES, LLC | exact |
| 10779 | Amazon.com Services, LLC. | exact |
| 10729 | Amazon Services LLC | fuzzy (0.80) |
| 10730 | AMAZON SERVICES LLC | fuzzy (0.80) |
| 10759 | AMAZON.COM SERVICE, INC. | fuzzy (0.86) |
| 10780 | AMAZON.COM WEB SERVICES. INC | fuzzy (0.83) |

### Google LLC (ID 79467)

Normalized: `google` — **3 neighbors**

| ID | raw_name |
|----|----------|
| 79466 | GOOGLE INC. |
| 79468 | GOOGLE LLC |
| 79471 | GOOGLE, LLC |

### TATA CONSULTANCY SERVICES LIMITED (ID 183647)

Normalized: `consultancy services tata` — **5 neighbors**

| ID | raw_name | Notes |
|----|----------|-------|
| 116 | 1 TATA CONSULTANCY SERVICES LIMITED | Prefix "1" (data entry artifact) |
| 183645 | Tata Consultancy Services Limited | Case difference |
| 183646 | TATA CONSuLTANCY SERVICES LIMITED | Typo in casing |
| 183648 | TATA CONSULTANCY SERVICESLIMITED | Glued suffix |
| 183649 | TATA CONSULTANCY SERVIES LIMITED | Typo: SERVIES |

### Microsoft Corporation (ID 122233)

Normalized: `microsoft` — **1 neighbor**

| ID | raw_name |
|----|----------|
| 122234 | MICROSOFT CORPORATION |

### Unique Employer (no neighbors)

| ID | raw_name | normalized_name |
|----|----------|-----------------|
| 10 | Better Nutritionals, LLC | better nutritionals |
| 23 | Future Textiles, Inc | future textiles |
| 34 | LEELA SERVICES INC. | leela services |

---

## Code Architecture

### File: `src/employer_normalization.py`

```
main()
 ├── extract_distinct_names(conn)     # SQL: SELECT DISTINCT from fy_all → 214K names
 ├── normalize_all(names)             # Python: normalize_employer_name() on each name
 ├── write_to_db(conn, results)       # SQL: CREATE TABLE + batch INSERT (psycopg2 execute_values)
 ├── evaluate(conn, results)          # Print normalization stats and spot-checks
 ├── build_similarity_graph(conn)     # SQL: pg_trgm trigram matching → neighbor arrays
 └── evaluate_similarity(conn)        # Print similarity stats and spot-checks
```

### Key Functions

**`normalize_employer_name(raw_name) → str`**

Pure Python function. Takes one raw name string, returns the normalized form.
Uses `cleanco.basename()` for international suffix removal, then applies custom regex
rules, abbreviation expansion, punctuation removal, and token sorting.
Called 214K times (once per distinct raw name). Takes ~5 seconds total.

**`build_similarity_graph(conn, threshold=0.8)`**

Runs entirely in PostgreSQL. Steps:

1. Add `id SERIAL PRIMARY KEY` to the lookup table
2. Create temp `_norm_dedup` table with 160K unique normalized names
3. Build GIN trigram index on `_norm_dedup`
4. Self-join with `%` operator to find 7,103 fuzzy pairs
5. Build neighbor arrays via a single CTE:
   - **Part (a)**: exact matches — `JOIN ON normalized_name = normalized_name AND id != id`
   - **Part (b)**: fuzzy matches — `JOIN via _sim_pairs → JOIN back to all IDs under linked normalized_name`
   - `UNION` both parts, `array_agg(ORDER BY id)` to produce `similar_to_id[]` and `similar_to_raw[]`
6. Clean up temp tables

Takes ~2 minutes total (dominated by the trigram self-join).

### Dependencies

| Package | Purpose |
|---------|---------|
| `cleanco` | Legal suffix removal (handles international forms: GmbH, S.A., Pty Ltd, etc.) |
| `rapidfuzz` | Installed for potential future use (Python-side fuzzy matching) |
| `psycopg2-binary` | PostgreSQL driver |
| `pg_trgm` | PostgreSQL extension for trigram similarity (server-side) |

---

## How To Query

```sql
-- Find all variants of a company by normalized name
SELECT id, raw_name, normalized_name
FROM refined.employer_name_lookup
WHERE normalized_name = 'amazon com services';

-- Find an employer and see all its neighbors
SELECT id, raw_name, similar_to_id, similar_to_raw
FROM refined.employer_name_lookup
WHERE raw_name = 'Amazon.com Services LLC';

-- Join back to fy_all to get application counts per normalized group
SELECT l.normalized_name, COUNT(*) AS total_apps
FROM refined.fy_all f
JOIN refined.employer_name_lookup l ON f.employer_name = l.raw_name
GROUP BY l.normalized_name
ORDER BY total_apps DESC
LIMIT 20;

-- Find employers with the most name variants
SELECT normalized_name, COUNT(*) AS n_variants
FROM refined.employer_name_lookup
GROUP BY normalized_name
HAVING COUNT(*) > 5
ORDER BY n_variants DESC
LIMIT 20;
```

---

## Reproducibility

```bash
uv run python src/employer_normalization.py
```

This will:
1. Extract 214K distinct employer names from `refined.fy_all`
2. Normalize all names in Python (cleanco + custom rules)
3. Write results to `refined.employer_name_lookup` (drops and recreates)
4. Build trigram similarity graph and populate `similar_to_id[]` / `similar_to_raw[]`
5. Print detailed statistics and spot-checks to stdout

**Prerequisites:** PostgreSQL `pg_trgm` extension (auto-created by the script via `CREATE EXTENSION IF NOT EXISTS pg_trgm`).
