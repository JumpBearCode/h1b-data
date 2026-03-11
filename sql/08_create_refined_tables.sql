-- Refined tables for H1B LCA data product.
-- 38 columns selected from the 99-column processed schema.
-- One table per fiscal year (quarters UNION'd and deduplicated),
-- plus fy_all (all years combined) and employers (dimension table).
--
-- Naming: refined.fy{YEAR}, refined.fy_all, refined.employers
--
-- Column changes from original processed schema:
--   - employer_address1 + employer_address2 -> employer_address (combined)
--   - employer_postal_code added
--   - employer_poc_first_name + employer_poc_last_name -> employer_poc_name (combined)
--   - Net: 38 columns (same count as before, but with address info)

-- Base table definition
CREATE TABLE IF NOT EXISTS refined.fy2020 (
    -- A. Core Display Fields (15)
    case_number TEXT NOT NULL,
    employer_name TEXT,
    job_title TEXT,
    employer_address TEXT,
    employer_city TEXT,
    employer_state TEXT,
    employer_postal_code TEXT,
    worksite_city TEXT,
    worksite_state TEXT,
    wage_rate_of_pay_from NUMERIC,
    wage_rate_of_pay_to NUMERIC,
    wage_unit_of_pay TEXT,
    received_date DATE,
    begin_date DATE,
    case_status TEXT,
    fiscal_year INTEGER,

    -- B. Differentiation Fields (22)
    visa_class TEXT,
    soc_code TEXT,
    soc_title TEXT,
    full_time_position TEXT,
    total_worker_positions INTEGER,
    new_employment TEXT,
    continued_employment TEXT,
    change_employer TEXT,
    amended_petition TEXT,
    prevailing_wage NUMERIC,
    pw_unit_of_pay TEXT,
    pw_wage_level TEXT,
    h1b_dependent TEXT,
    willful_violator TEXT,
    support_h1b TEXT,
    statutory_basis TEXT,
    naics_code TEXT,
    secondary_entity TEXT,
    lawfirm_name_business_name TEXT,
    employer_poc_name TEXT,
    employer_poc_job_title TEXT,
    employer_poc_email TEXT
);

-- Create all other fiscal year tables with the same structure
CREATE TABLE IF NOT EXISTS refined.fy2021 (LIKE refined.fy2020 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS refined.fy2022 (LIKE refined.fy2020 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS refined.fy2023 (LIKE refined.fy2020 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS refined.fy2024 (LIKE refined.fy2020 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS refined.fy2025 (LIKE refined.fy2020 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS refined.fy2026 (LIKE refined.fy2020 INCLUDING ALL);

-- All fiscal years combined
CREATE TABLE IF NOT EXISTS refined.fy_all (LIKE refined.fy2020 INCLUDING ALL);

-- Employer dimension table
CREATE TABLE IF NOT EXISTS refined.employers (
    employer_name TEXT NOT NULL,
    employer_address TEXT,
    employer_city TEXT,
    employer_state TEXT,
    employer_postal_code TEXT,
    naics_code TEXT,
    h1b_dependent TEXT,
    willful_violator TEXT,
    total_applications INTEGER,
    first_seen_year INTEGER,
    last_seen_year INTEGER
);
