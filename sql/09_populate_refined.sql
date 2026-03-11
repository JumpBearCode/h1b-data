-- Populate a refined fiscal year table from processed quarterly tables.
-- Template — FISCAL_YEAR and QUARTER_UNIONS placeholders are replaced at runtime.
--
-- Logic:
--   1. UNION ALL quarterly processed tables for the fiscal year
--   2. Deduplicate by case_number (some quarters are cumulative)
--      - Uses ROW_NUMBER() with source_table DESC to keep latest quarter's version
--   3. Select 38 refined columns (with combined fields) + add fiscal_year

TRUNCATE refined.fy{FISCAL_YEAR};

INSERT INTO refined.fy{FISCAL_YEAR}
SELECT
    -- A. Core Display Fields (16)
    case_number,
    employer_name,
    job_title,
    CONCAT_WS(', ', NULLIF(employer_address1, ''), NULLIF(employer_address2, '')) AS employer_address,
    employer_city,
    employer_state,
    employer_postal_code,
    worksite_city,
    worksite_state,
    wage_rate_of_pay_from,
    wage_rate_of_pay_to,
    wage_unit_of_pay,
    received_date,
    begin_date,
    case_status,
    {FISCAL_YEAR} AS fiscal_year,

    -- B. Differentiation Fields (22)
    visa_class,
    soc_code,
    soc_title,
    full_time_position,
    total_worker_positions,
    new_employment,
    continued_employment,
    change_employer,
    amended_petition,
    prevailing_wage,
    pw_unit_of_pay,
    pw_wage_level,
    h1b_dependent,
    willful_violator,
    support_h1b,
    statutory_basis,
    naics_code,
    secondary_entity,
    lawfirm_name_business_name,
    CONCAT_WS(' ', NULLIF(employer_poc_first_name, ''), NULLIF(employer_poc_last_name, '')) AS employer_poc_name,
    employer_poc_job_title,
    employer_poc_email

FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY case_number
            ORDER BY source_table DESC
        ) AS rn
    FROM (
{QUARTER_UNIONS}
    ) AS all_quarters
) AS deduped
WHERE rn = 1;
