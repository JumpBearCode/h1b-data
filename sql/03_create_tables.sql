-- Create raw tables for each LCA disclosure CSV file.
-- All tables share the unified 98-column schema (superset across FY2020-FY2026).
-- All columns use TEXT type for raw ingestion; type casting is done downstream.
-- Columns not present in older CSV files will be NULL.

-- ============================================================
-- FY2020 (Q4 defined first as base; Q1-Q3 from XLSX downloads)
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2020_q4 (
    case_number TEXT,
    case_status TEXT,
    received_date TEXT,
    decision_date TEXT,
    original_cert_date TEXT,
    visa_class TEXT,
    job_title TEXT,
    soc_code TEXT,
    soc_title TEXT,
    full_time_position TEXT,
    begin_date TEXT,
    end_date TEXT,
    total_worker_positions TEXT,
    new_employment TEXT,
    continued_employment TEXT,
    change_previous_employment TEXT,
    new_concurrent_employment TEXT,
    change_employer TEXT,
    amended_petition TEXT,
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
    worksite_workers TEXT,
    secondary_entity TEXT,
    secondary_entity_business_name TEXT,
    worksite_address1 TEXT,
    worksite_address2 TEXT,
    worksite_city TEXT,
    worksite_county TEXT,
    worksite_state TEXT,
    worksite_postal_code TEXT,
    wage_rate_of_pay_from TEXT,
    wage_rate_of_pay_to TEXT,
    wage_unit_of_pay TEXT,
    prevailing_wage TEXT,
    pw_unit_of_pay TEXT,
    pw_tracking_number TEXT,
    pw_wage_level TEXT,
    pw_oes_year TEXT,
    pw_other_source TEXT,
    pw_other_year TEXT,
    pw_survey_publisher TEXT,
    pw_survey_name TEXT,
    total_worksite_locations TEXT,
    agree_to_lc_statement TEXT,
    h1b_dependent TEXT,
    willful_violator TEXT,
    support_h1b TEXT,
    statutory_basis TEXT,
    appendix_a_attached TEXT,
    public_disclosure TEXT,
    preparer_last_name TEXT,
    preparer_first_name TEXT,
    preparer_middle_initial TEXT,
    preparer_business_name TEXT,
    preparer_email TEXT
);

CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2020_q1 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2020_q2 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2020_q3 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

-- ============================================================
-- FY2021
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2021_q1 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2021_q2 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2021_q3 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2021_q4 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

-- ============================================================
-- FY2022
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2022_q1 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2022_q2 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2022_q3 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2022_q4 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

-- ============================================================
-- FY2023
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2023_q1 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2023_q2 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2023_q3 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2023_q4 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

-- ============================================================
-- FY2024
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2024_q1 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2024_q2 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2024_q3 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2024_q4 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

-- ============================================================
-- FY2025
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2025_q1 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2025_q2 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2025_q3 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2025_q4 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);

-- ============================================================
-- FY2026
-- ============================================================
CREATE TABLE IF NOT EXISTS raw.lca_disclosure_data_fy2026_q1 (LIKE raw.lca_disclosure_data_fy2020_q4 INCLUDING ALL);
