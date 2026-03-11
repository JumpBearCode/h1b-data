-- Processed tables for LCA disclosure data.
-- These tables have proper data types, empty rows removed, and text fields trimmed.
--
-- Key differences from raw schema:
--   1. All date columns: TEXT -> DATE (format: YYYY-MM-DD from "YYYY-MM-DD HH:MM:SS")
--   2. Numeric columns: TEXT -> NUMERIC (wage_rate_of_pay_from/to, prevailing_wage)
--   3. Integer columns: TEXT -> INTEGER (total_worker_positions, worksite_workers, etc.)
--   4. Boolean-like columns: TEXT -> TEXT (kept as text since values are Y/N/Yes/No/N\A/0/1)
--   5. All TEXT fields trimmed of leading/trailing whitespace
--   6. Empty rows (case_number IS NULL) are excluded
--   7. source_table column added to track data lineage

-- ============================================================
-- Per-quarter processed tables (one per raw table)
-- ============================================================

CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2020_q4 (
    -- Identifiers
    case_number TEXT NOT NULL,
    case_status TEXT,
    visa_class TEXT,

    -- Dates (cast from "YYYY-MM-DD HH:MM:SS" text to DATE)
    received_date DATE,
    decision_date DATE,
    original_cert_date DATE,
    begin_date DATE,
    end_date DATE,

    -- Job info
    job_title TEXT,
    soc_code TEXT,
    soc_title TEXT,
    full_time_position TEXT,
    total_worker_positions INTEGER,

    -- Employment type (integer counts in newer data)
    new_employment TEXT,
    continued_employment TEXT,
    change_previous_employment TEXT,
    new_concurrent_employment TEXT,
    change_employer TEXT,
    amended_petition TEXT,

    -- Employer info
    employer_name TEXT,
    trade_name_dba TEXT,
    employer_address1 TEXT,
    employer_address2 TEXT,
    employer_city TEXT,
    employer_state TEXT,
    employer_postal_code TEXT,
    employer_country TEXT,
    employer_province TEXT,
    employer_phone TEXT,
    employer_phone_ext TEXT,
    employer_fein TEXT,
    naics_code TEXT,

    -- Employer POC
    employer_poc_last_name TEXT,
    employer_poc_first_name TEXT,
    employer_poc_middle_name TEXT,
    employer_poc_job_title TEXT,
    employer_poc_address1 TEXT,
    employer_poc_address2 TEXT,
    employer_poc_city TEXT,
    employer_poc_state TEXT,
    employer_poc_postal_code TEXT,
    employer_poc_country TEXT,
    employer_poc_province TEXT,
    employer_poc_phone TEXT,
    employer_poc_phone_ext TEXT,
    employer_poc_email TEXT,

    -- Agent / Attorney
    agent_representing_employer TEXT,
    agent_attorney_last_name TEXT,
    agent_attorney_first_name TEXT,
    agent_attorney_middle_name TEXT,
    agent_attorney_address1 TEXT,
    agent_attorney_address2 TEXT,
    agent_attorney_city TEXT,
    agent_attorney_state TEXT,
    agent_attorney_postal_code TEXT,
    agent_attorney_country TEXT,
    agent_attorney_province TEXT,
    agent_attorney_phone TEXT,
    agent_attorney_phone_ext TEXT,
    agent_attorney_email_address TEXT,
    lawfirm_name_business_name TEXT,
    lawfirm_business_fein TEXT,
    state_of_highest_court TEXT,
    name_of_highest_state_court TEXT,

    -- Worksite
    worksite_workers INTEGER,
    secondary_entity TEXT,
    secondary_entity_business_name TEXT,
    worksite_address1 TEXT,
    worksite_address2 TEXT,
    worksite_city TEXT,
    worksite_county TEXT,
    worksite_state TEXT,
    worksite_postal_code TEXT,

    -- Wage
    wage_rate_of_pay_from NUMERIC,
    wage_rate_of_pay_to NUMERIC,
    wage_unit_of_pay TEXT,
    prevailing_wage NUMERIC,
    pw_unit_of_pay TEXT,
    pw_tracking_number TEXT,
    pw_wage_level TEXT,
    pw_oes_year TEXT,
    pw_other_source TEXT,
    pw_other_year TEXT,
    pw_survey_publisher TEXT,
    pw_survey_name TEXT,
    total_worksite_locations INTEGER,

    -- Compliance
    agree_to_lc_statement TEXT,
    h1b_dependent TEXT,
    willful_violator TEXT,
    support_h1b TEXT,
    statutory_basis TEXT,
    appendix_a_attached TEXT,
    public_disclosure TEXT,

    -- Preparer
    preparer_last_name TEXT,
    preparer_first_name TEXT,
    preparer_middle_initial TEXT,
    preparer_business_name TEXT,
    preparer_email TEXT,

    -- Lineage
    source_table TEXT NOT NULL
);

-- Create all other quarterly tables with the same structure
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2020_q1 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2020_q2 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2020_q3 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2021_q1 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2021_q2 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2021_q3 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2021_q4 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2022_q1 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2022_q2 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2022_q3 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2022_q4 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2023_q1 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2023_q2 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2023_q3 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2023_q4 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2024_q1 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2024_q2 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2024_q3 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2024_q4 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2025_q1 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2025_q2 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2025_q3 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2025_q4 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

CREATE TABLE IF NOT EXISTS processed.lca_disclosure_data_fy2026_q1 (LIKE processed.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
