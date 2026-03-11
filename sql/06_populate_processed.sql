-- Populate processed tables from raw tables.
-- This SQL is used as a template — {TABLE_NAME} is replaced at runtime.
--
-- Cleaning operations:
--   1. Filter out empty rows (case_number IS NULL or blank)
--   2. TRIM all TEXT fields to remove leading/trailing whitespace
--   3. Cast date fields from "YYYY-MM-DD HH:MM:SS" TEXT -> DATE
--   4. Cast numeric wage fields from TEXT -> NUMERIC
--   5. Cast integer fields from TEXT -> INTEGER
--   6. Add source_table lineage column

TRUNCATE processed.{TABLE_NAME};

INSERT INTO processed.{TABLE_NAME}
SELECT
    -- Identifiers
    TRIM(case_number) AS case_number,
    TRIM(case_status) AS case_status,
    TRIM(visa_class) AS visa_class,

    -- Dates: "YYYY-MM-DD HH:MM:SS" -> DATE
    CASE WHEN TRIM(received_date) = '' THEN NULL
         ELSE CAST(LEFT(TRIM(received_date), 10) AS DATE) END AS received_date,
    CASE WHEN TRIM(decision_date) = '' THEN NULL
         ELSE CAST(LEFT(TRIM(decision_date), 10) AS DATE) END AS decision_date,
    CASE WHEN TRIM(original_cert_date) = '' THEN NULL
         ELSE CAST(LEFT(TRIM(original_cert_date), 10) AS DATE) END AS original_cert_date,
    CASE WHEN TRIM(begin_date) = '' THEN NULL
         ELSE CAST(LEFT(TRIM(begin_date), 10) AS DATE) END AS begin_date,
    CASE WHEN TRIM(end_date) = '' THEN NULL
         ELSE CAST(LEFT(TRIM(end_date), 10) AS DATE) END AS end_date,

    -- Job info
    TRIM(job_title) AS job_title,
    TRIM(soc_code) AS soc_code,
    TRIM(soc_title) AS soc_title,
    TRIM(full_time_position) AS full_time_position,
    CASE WHEN TRIM(total_worker_positions) ~ '^\d+$'
         THEN CAST(TRIM(total_worker_positions) AS INTEGER) ELSE NULL END AS total_worker_positions,

    -- Employment type (kept as text — values are mixed integer counts and Y/N)
    TRIM(new_employment) AS new_employment,
    TRIM(continued_employment) AS continued_employment,
    TRIM(change_previous_employment) AS change_previous_employment,
    TRIM(new_concurrent_employment) AS new_concurrent_employment,
    TRIM(change_employer) AS change_employer,
    TRIM(amended_petition) AS amended_petition,

    -- Employer info
    TRIM(employer_name) AS employer_name,
    TRIM(trade_name_dba) AS trade_name_dba,
    TRIM(employer_address1) AS employer_address1,
    TRIM(employer_address2) AS employer_address2,
    TRIM(employer_city) AS employer_city,
    TRIM(employer_state) AS employer_state,
    TRIM(employer_postal_code) AS employer_postal_code,
    TRIM(employer_country) AS employer_country,
    TRIM(employer_province) AS employer_province,
    TRIM(employer_phone) AS employer_phone,
    TRIM(employer_phone_ext) AS employer_phone_ext,
    TRIM(employer_fein) AS employer_fein,
    TRIM(naics_code) AS naics_code,

    -- Employer POC
    TRIM(employer_poc_last_name) AS employer_poc_last_name,
    TRIM(employer_poc_first_name) AS employer_poc_first_name,
    TRIM(employer_poc_middle_name) AS employer_poc_middle_name,
    TRIM(employer_poc_job_title) AS employer_poc_job_title,
    TRIM(employer_poc_address1) AS employer_poc_address1,
    TRIM(employer_poc_address2) AS employer_poc_address2,
    TRIM(employer_poc_city) AS employer_poc_city,
    TRIM(employer_poc_state) AS employer_poc_state,
    TRIM(employer_poc_postal_code) AS employer_poc_postal_code,
    TRIM(employer_poc_country) AS employer_poc_country,
    TRIM(employer_poc_province) AS employer_poc_province,
    TRIM(employer_poc_phone) AS employer_poc_phone,
    TRIM(employer_poc_phone_ext) AS employer_poc_phone_ext,
    TRIM(employer_poc_email) AS employer_poc_email,

    -- Agent / Attorney
    TRIM(agent_representing_employer) AS agent_representing_employer,
    TRIM(agent_attorney_last_name) AS agent_attorney_last_name,
    TRIM(agent_attorney_first_name) AS agent_attorney_first_name,
    TRIM(agent_attorney_middle_name) AS agent_attorney_middle_name,
    TRIM(agent_attorney_address1) AS agent_attorney_address1,
    TRIM(agent_attorney_address2) AS agent_attorney_address2,
    TRIM(agent_attorney_city) AS agent_attorney_city,
    TRIM(agent_attorney_state) AS agent_attorney_state,
    TRIM(agent_attorney_postal_code) AS agent_attorney_postal_code,
    TRIM(agent_attorney_country) AS agent_attorney_country,
    TRIM(agent_attorney_province) AS agent_attorney_province,
    TRIM(agent_attorney_phone) AS agent_attorney_phone,
    TRIM(agent_attorney_phone_ext) AS agent_attorney_phone_ext,
    TRIM(agent_attorney_email_address) AS agent_attorney_email_address,
    TRIM(lawfirm_name_business_name) AS lawfirm_name_business_name,
    TRIM(lawfirm_business_fein) AS lawfirm_business_fein,
    TRIM(state_of_highest_court) AS state_of_highest_court,
    TRIM(name_of_highest_state_court) AS name_of_highest_state_court,

    -- Worksite
    CASE WHEN TRIM(worksite_workers) ~ '^\d+$'
         THEN CAST(TRIM(worksite_workers) AS INTEGER) ELSE NULL END AS worksite_workers,
    TRIM(secondary_entity) AS secondary_entity,
    TRIM(secondary_entity_business_name) AS secondary_entity_business_name,
    TRIM(worksite_address1) AS worksite_address1,
    TRIM(worksite_address2) AS worksite_address2,
    TRIM(worksite_city) AS worksite_city,
    TRIM(worksite_county) AS worksite_county,
    TRIM(worksite_state) AS worksite_state,
    TRIM(worksite_postal_code) AS worksite_postal_code,

    -- Wage (numeric)
    CASE WHEN TRIM(wage_rate_of_pay_from) ~ '^\d+(\.\d+)?$'
         THEN CAST(TRIM(wage_rate_of_pay_from) AS NUMERIC) ELSE NULL END AS wage_rate_of_pay_from,
    CASE WHEN TRIM(wage_rate_of_pay_to) ~ '^\d+(\.\d+)?$'
         THEN CAST(TRIM(wage_rate_of_pay_to) AS NUMERIC) ELSE NULL END AS wage_rate_of_pay_to,
    TRIM(wage_unit_of_pay) AS wage_unit_of_pay,
    CASE WHEN TRIM(prevailing_wage) ~ '^\d+(\.\d+)?$'
         THEN CAST(TRIM(prevailing_wage) AS NUMERIC) ELSE NULL END AS prevailing_wage,
    TRIM(pw_unit_of_pay) AS pw_unit_of_pay,
    TRIM(pw_tracking_number) AS pw_tracking_number,
    TRIM(pw_wage_level) AS pw_wage_level,
    TRIM(pw_oes_year) AS pw_oes_year,
    TRIM(pw_other_source) AS pw_other_source,
    TRIM(pw_other_year) AS pw_other_year,
    TRIM(pw_survey_publisher) AS pw_survey_publisher,
    TRIM(pw_survey_name) AS pw_survey_name,
    CASE WHEN TRIM(total_worksite_locations) ~ '^\d+$'
         THEN CAST(TRIM(total_worksite_locations) AS INTEGER) ELSE NULL END AS total_worksite_locations,

    -- Compliance
    TRIM(agree_to_lc_statement) AS agree_to_lc_statement,
    TRIM(h1b_dependent) AS h1b_dependent,
    TRIM(willful_violator) AS willful_violator,
    TRIM(support_h1b) AS support_h1b,
    TRIM(statutory_basis) AS statutory_basis,
    TRIM(appendix_a_attached) AS appendix_a_attached,
    TRIM(public_disclosure) AS public_disclosure,

    -- Preparer
    TRIM(preparer_last_name) AS preparer_last_name,
    TRIM(preparer_first_name) AS preparer_first_name,
    TRIM(preparer_middle_initial) AS preparer_middle_initial,
    TRIM(preparer_business_name) AS preparer_business_name,
    TRIM(preparer_email) AS preparer_email,

    -- Lineage
    '{TABLE_NAME}' AS source_table

FROM raw.{TABLE_NAME}
WHERE case_number IS NOT NULL
  AND TRIM(case_number) != '';
