-- Populate refined.employers dimension table from refined.fy_all.
-- Aggregates employer info across all fiscal years.
--
-- For each employer_name, picks the most recent non-null address/city/state/postal_code,
-- the most recent h1b_dependent and willful_violator flags,
-- and counts total applications.

TRUNCATE refined.employers;

INSERT INTO refined.employers
SELECT
    employer_name,
    employer_address,
    employer_city,
    employer_state,
    employer_postal_code,
    naics_code,
    h1b_dependent,
    willful_violator,
    total_applications,
    first_seen_year,
    last_seen_year
FROM (
    SELECT
        employer_name,
        -- Pick most recent non-null values using FIRST_VALUE
        FIRST_VALUE(employer_address) OVER (
            PARTITION BY employer_name
            ORDER BY CASE WHEN employer_address IS NOT NULL AND employer_address != '' THEN 0 ELSE 1 END,
                     fiscal_year DESC, received_date DESC NULLS LAST
        ) AS employer_address,
        FIRST_VALUE(employer_city) OVER (
            PARTITION BY employer_name
            ORDER BY CASE WHEN employer_city IS NOT NULL AND employer_city != '' THEN 0 ELSE 1 END,
                     fiscal_year DESC, received_date DESC NULLS LAST
        ) AS employer_city,
        FIRST_VALUE(employer_state) OVER (
            PARTITION BY employer_name
            ORDER BY CASE WHEN employer_state IS NOT NULL AND employer_state != '' THEN 0 ELSE 1 END,
                     fiscal_year DESC, received_date DESC NULLS LAST
        ) AS employer_state,
        FIRST_VALUE(employer_postal_code) OVER (
            PARTITION BY employer_name
            ORDER BY CASE WHEN employer_postal_code IS NOT NULL AND employer_postal_code != '' THEN 0 ELSE 1 END,
                     fiscal_year DESC, received_date DESC NULLS LAST
        ) AS employer_postal_code,
        FIRST_VALUE(naics_code) OVER (
            PARTITION BY employer_name
            ORDER BY CASE WHEN naics_code IS NOT NULL AND naics_code != '' THEN 0 ELSE 1 END,
                     fiscal_year DESC, received_date DESC NULLS LAST
        ) AS naics_code,
        FIRST_VALUE(h1b_dependent) OVER (
            PARTITION BY employer_name
            ORDER BY CASE WHEN h1b_dependent IS NOT NULL AND h1b_dependent != '' THEN 0 ELSE 1 END,
                     fiscal_year DESC, received_date DESC NULLS LAST
        ) AS h1b_dependent,
        FIRST_VALUE(willful_violator) OVER (
            PARTITION BY employer_name
            ORDER BY CASE WHEN willful_violator IS NOT NULL AND willful_violator != '' THEN 0 ELSE 1 END,
                     fiscal_year DESC, received_date DESC NULLS LAST
        ) AS willful_violator,
        COUNT(*) OVER (PARTITION BY employer_name) AS total_applications,
        MIN(fiscal_year) OVER (PARTITION BY employer_name) AS first_seen_year,
        MAX(fiscal_year) OVER (PARTITION BY employer_name) AS last_seen_year,
        ROW_NUMBER() OVER (PARTITION BY employer_name ORDER BY fiscal_year DESC, received_date DESC NULLS LAST) AS rn
    FROM refined.fy_all
    WHERE employer_name IS NOT NULL AND employer_name != ''
) sub
WHERE rn = 1;
