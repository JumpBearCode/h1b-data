# Employer Name Normalization

## Overview

The H1B LCA disclosure data contains **214,366 distinct employer names** in `refined.employers`. Many of these represent the same company with minor variations in spelling, capitalization, legal suffixes, or punctuation. This document describes the two-step normalization pipeline used to identify and group these duplicates.

**Key result:** Step 1 + Step 2 together identify **~87,000 employer names** (40.6%) as potential duplicates for consolidation.

---

## Step 1: Deterministic Normalization

### Method

Rule-based exact-match normalization applied to every employer name:

1. `UPPER()` — case-insensitive
2. Strip legal suffixes: `INCORPORATED`, `CORPORATION`, `LLC`, `LLP`, `LP`, `INC`, `CORP`, `CO`, `PC`, `PA`, `DBA`, `LIMITED`, etc.
3. Remove punctuation: commas, periods, quotes, dashes, parentheses, slashes
4. Collapse multiple spaces to single space
5. `TRIM()`

### Results

| Metric | Count |
|--------|-------|
| Original distinct employer names | 214,366 |
| After normalization (distinct) | 161,919 |
| Names collapsed (exact match after norm) | **52,447 (24.5%)** |

### Variant Distribution

| Variants per normalized name | Groups | Employers |
|------------------------------|--------|-----------|
| 1 (already unique) | 125,428 | 125,428 |
| 2 | 26,464 | 52,928 |
| 3 | 6,506 | 19,518 |
| 4 | 2,184 | 8,736 |
| 5 | 781 | 3,905 |
| 6+ | 535+ | 3,851+ |

### Top Collapsed Groups (by total applications)

| Normalized Name | Apps | Variants | Examples |
|-----------------|------|----------|----------|
| COGNIZANT TECHNOLOGY SOLUTIONS US | 92,362 | 2 | `COGNIZANT TECHNOLOGY SOLUTIONS US CORP`, `Cognizant Technology Solutions US Corporation` |
| AMAZON COM SERVICES | 82,808 | 19 | `Amazon.com Services LLC`, `AMAZON.COM SERVICES LLC`, `AMAZON.COM SERVICES, INC.`, `AMAZON.COM SERVICES, INC` |
| GOOGLE | 60,212 | 4 | `Google LLC`, `GOOGLE LLC`, `GOOGLE INC.`, `GOOGLE, LLC` |
| TATA CONSULTANCY SERVICES | 59,913 | 4 | `TATA CONSULTANCY SERVICES LIMITED`, `Tata Consultancy Services Limited`, `TATA CONSuLTANCY SERVICES LIMITED` |
| ERNST & YOUNG U S | 57,449 | 3 | `Ernst & Young U.S. LLP`, `ERNST & YOUNG U.S. LLP`, `ERNST & YOUNG U.S.LLP` |

---

## Step 2: Trigram Similarity Matching (pg_trgm)

### Relationship to Step 1

**Step 2 excludes Step 1 results.** Step 2 operates on the `employer_name_normalized` column (the output of Step 1) and explicitly filters out exact matches:

```sql
WHERE a.employer_name_normalized != b.employer_name_normalized
```

This means Step 2 only finds **fuzzy matches that Step 1's deterministic normalization could not catch** — typos, word reordering, abbreviation differences, etc.

### Method

- PostgreSQL `pg_trgm` extension with GIN index on `employer_name_normalized`
- **Blocking strategy:** Only compare employers in the **same state** (reduces N^2 to manageable comparisons)
- Similarity threshold: `>= 0.6`
- Deduplicated pairs: `a.employer_name_normalized < b.employer_name_normalized` (avoids A-B and B-A duplicates)

### Results

| Similarity Bucket | Pairs | Apps Affected | Interpretation |
|-------------------|-------|---------------|----------------|
| 0.90 - 1.00 (very high) | **3,457** | 212,697 | Almost certainly the same employer |
| 0.80 - 0.89 (high) | **8,204** | 1,003,085 | Very likely the same employer |
| 0.70 - 0.79 (medium) | 12,997 | 950,930 | Likely the same, needs review |
| 0.60 - 0.69 (low) | 102,570 | 6,402,502 | Possible match, manual review needed |
| **Total** | **127,228** | **8,569,214** | |

### Distinct Employer Names Involved

| Threshold | Distinct Names | % of 161,919 Normalized Names |
|-----------|---------------|-------------------------------|
| sim >= 0.9 | 3,146 | 1.9% |
| sim >= 0.8 | 9,500 | 5.9% |
| sim >= 0.6 (all) | 34,739 | 21.5% |

### Sample High-Confidence Matches (sim >= 0.9)

| Score | Employer A (Apps) | Employer B (Apps) | State |
|-------|-------------------|-------------------|-------|
| 1.00 | JPMorgan & Chase Co. (4) | JPMorgan Chase & Co. (13,124) | IL |
| 1.00 | JPMorgan Chase & Co. (13,124) | JPMorgan Chase& Co. (1) | IL |
| 1.00 | JPMorgan & Chase Co. (4) | JPMORGAN CHASE & CO. (7,070) | IL |
| 0.93 | 1 TATA CONSULTANCY SERVICES LIMITED (1) | TATA CONSULTANCY SERVICES LIMITED (38,159) | MD |

### Sample Medium-Confidence Matches (0.80 - 0.89)

| Score | Employer A (Apps) | Employer B (Apps) | State |
|-------|-------------------|-------------------|-------|
| 0.80 | Amazon.com Services LLC (60,910) | AMAZON SERVICES LLC (8) | WA |
| 0.86 | AMAZON.COM SERVICE, INC. (1) | Amazon.com Services LLC (60,910) | WA |
| 0.83 | Amazon.com Services LLC (60,910) | AMAZON.COM WEB SERVICES. INC (1) | WA |

---

## Combined Impact

```
Original employer names:                  214,366

Step 1 (deterministic normalization):
    Distinct after normalization:          161,919
    Names collapsed:                       52,447  (24.5%)

Step 2 (trigram fuzzy matching):
    Additional candidate names to review:  34,739  (21.5% of normalized)
    High-confidence (sim >= 0.8):          9,500 names in 11,661 pairs
    Very high confidence (sim >= 0.9):     3,146 names in 3,457 pairs
```

---

## Database Artifacts

| Object | Type | Description |
|--------|------|-------------|
| `refined.employers.employer_name_normalized` | Column (TEXT) | Deterministically normalized employer name |
| `refined.employer_match_candidates` | Table | Fuzzy match candidate pairs with similarity scores |
| `idx_employers_trgm` | GIN Index | Trigram index on `employer_name_normalized` |

### `refined.employer_match_candidates` Schema

| Column | Type | Description |
|--------|------|-------------|
| `name_a` | TEXT | Original employer name A |
| `name_b` | TEXT | Original employer name B |
| `norm_a` | TEXT | Normalized name A |
| `norm_b` | TEXT | Normalized name B |
| `state` | TEXT | Shared employer state (blocking key) |
| `sim_score` | FLOAT | Trigram similarity score (0.6 - 1.0) |
| `apps_a` | INTEGER | Total applications for employer A |
| `apps_b` | INTEGER | Total applications for employer B |
| `apps_combined` | INTEGER | Sum of apps_a + apps_b |

---

## Sample Queries

### 1. Search for a specific employer's matches

```sql
-- Find all fuzzy matches for a specific employer (e.g., "Amazon")
SELECT name_a, name_b, state, sim_score, apps_a, apps_b
FROM refined.employer_match_candidates
WHERE name_a ILIKE '%amazon%' OR name_b ILIKE '%amazon%'
ORDER BY sim_score DESC, apps_combined DESC;
```

### 2. Find all Step 1 variants for a normalized name

```sql
-- See all original names that collapsed to the same normalized form
SELECT employer_name, employer_name_normalized, total_applications,
       employer_city, employer_state
FROM refined.employers
WHERE employer_name_normalized LIKE '%GOOGLE%'
ORDER BY total_applications DESC;
```

### 3. High-confidence matches with the most applications

```sql
-- Top 50 match pairs most worth merging (high confidence, high volume)
SELECT name_a, name_b, state, sim_score, apps_a, apps_b, apps_combined
FROM refined.employer_match_candidates
WHERE sim_score >= 0.8
ORDER BY apps_combined DESC
LIMIT 50;
```

### 4. All match candidates for a specific state

```sql
-- Review fuzzy matches in California
SELECT name_a, name_b, sim_score, apps_a, apps_b
FROM refined.employer_match_candidates
WHERE state = 'CA'
  AND sim_score >= 0.8
ORDER BY apps_combined DESC
LIMIT 100;
```

### 5. Count potential merges by similarity threshold

```sql
-- How many distinct employer names could be reduced at each threshold?
SELECT
    CASE
        WHEN sim_score >= 0.9 THEN '0.90+'
        WHEN sim_score >= 0.8 THEN '0.80-0.89'
        WHEN sim_score >= 0.7 THEN '0.70-0.79'
        WHEN sim_score >= 0.6 THEN '0.60-0.69'
    END AS bucket,
    COUNT(*) AS pairs,
    COUNT(DISTINCT norm_a) + COUNT(DISTINCT norm_b) AS approx_names_involved,
    SUM(apps_combined) AS total_apps_affected
FROM refined.employer_match_candidates
GROUP BY 1
ORDER BY 1 DESC;
```

### 6. Find employers with both Step 1 AND Step 2 matches

```sql
-- Employers that had Step 1 variants AND are also in Step 2 fuzzy matches
SELECT e.employer_name_normalized,
       COUNT(DISTINCT e.employer_name) AS step1_variants,
       COUNT(DISTINCT mc.norm_b) AS step2_fuzzy_matches,
       SUM(e.total_applications) AS total_apps
FROM refined.employers e
JOIN refined.employer_match_candidates mc
    ON e.employer_name_normalized = mc.norm_a
GROUP BY e.employer_name_normalized
HAVING COUNT(DISTINCT e.employer_name) > 1
ORDER BY total_apps DESC
LIMIT 20;
```

### 7. Full picture for a single employer

```sql
-- Complete view: all names associated with "MICROSOFT" through both steps
WITH step1 AS (
    SELECT employer_name, employer_name_normalized, total_applications
    FROM refined.employers
    WHERE employer_name_normalized LIKE '%MICROSOFT%'
),
step2 AS (
    SELECT DISTINCT
        CASE WHEN norm_a LIKE '%MICROSOFT%' THEN norm_b ELSE norm_a END AS related_norm,
        sim_score
    FROM refined.employer_match_candidates
    WHERE norm_a LIKE '%MICROSOFT%' OR norm_b LIKE '%MICROSOFT%'
)
SELECT 'Step 1' AS source, employer_name, employer_name_normalized, total_applications, NULL AS sim_score
FROM step1
UNION ALL
SELECT 'Step 2', e.employer_name, e.employer_name_normalized, e.total_applications, s2.sim_score
FROM step2 s2
JOIN refined.employers e ON e.employer_name_normalized = s2.related_norm
ORDER BY source, total_applications DESC;
```

---

## Reproducibility

To re-run the normalization pipeline:

```bash
uv run python src/employer_normalization.py
```

This will:
1. Add/update `employer_name_normalized` column on `refined.employers`
2. Drop and recreate `refined.employer_match_candidates` with fresh fuzzy matches
3. Print detailed statistics to stdout

**Prerequisites:** `pg_trgm` extension must be enabled (`CREATE EXTENSION IF NOT EXISTS pg_trgm;`).

---

## Next Steps (Future Work)

1. **Apply high-confidence merges (sim >= 0.9):** Auto-merge the 3,457 pairs into canonical employer names
2. **Review medium-confidence matches (0.8-0.89):** Manual or semi-automated review of 8,204 pairs
3. **Create canonical employer mapping table:** `refined.employer_canonical` mapping all variant names to a single canonical name
4. **Consider embedding-based matching:** For catching semantic matches that trigram similarity misses (e.g., "IBM" vs "International Business Machines")
