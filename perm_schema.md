# PERM Unified Schema — All Years (FY2020–FY2026)

> Unified column definitions for the PERM (Form ETA-9089) public disclosure data.
> Designed to union data across old form (FY2020–FY2024) and new form (FY2024 New–FY2026).
> Fields use standardized names; see `old_form_source` and `new_form_source` for original column names.
> NULL when not available in a given form era.

---

## Section A: Case Information

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 1 | `case_number` | VARCHAR | Unique case identifier assigned by OFLC | `CASE_NUMBER` | `CASE_NUMBER` | All years |
| 2 | `case_status` | VARCHAR | Final determination status. Values: Certified, Certified-Expired, Denied, Withdrawn | `CASE_STATUS` | `CASE_STATUS` | All years |
| 3 | `received_date` | DATE | Date application was received by OFLC | `RECEIVED_DATE` | `RECEIVED_DATE` | All years |
| 4 | `decision_date` | DATE | Date determination was issued by OFLC | `DECISION_DATE` | `DECISION_DATE` | All years |
| 5 | `refile` | VARCHAR | Whether application was previously filed (Y/N) | `REFILE` | — | Old form only |
| 6 | `orig_file_date` | DATE | Original filing date if refiled | `ORIG_FILE_DATE` | — | Old form only |
| 7 | `previous_swa_case_number_state` | VARCHAR | SWA case number or state of original filing | `PREVIOUS_SWA_CASE_NUMBER_STATE` | — | Old form only |

## Section B: Occupation Classification

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 8 | `occupation_type` | VARCHAR | Type of occupation. Values: Professional occupation, Non-professional, College/University Teacher, None/Professional Athlete, Schedule A | Derived from `PROFESSIONAL_OCCUPATION` + `APP_FOR_COLLEGE_U_TEACHER` + `SCHD_A_SHEEPHERDER` | `OCCUPATION_TYPE` | All years (old form: derived) |
| 9 | `schd_a_sheepherder` | VARCHAR | Whether application is for Schedule A or Sheepherder (Y/N) | `SCHD_A_SHEEPHERDER` | Derivable from `OCCUPATION_TYPE` = 'Schedule A' | All years |
| 10 | `professional_occupation` | VARCHAR | Application is for professional occupation other than college teacher (Y/N) | `PROFESSIONAL_OCCUPATION` | Derivable from `OCCUPATION_TYPE` = 'Professional occupation' | All years |
| 11 | `app_for_college_u_teacher` | VARCHAR | Application is for college/university teacher (Y/N) | `APP_FOR_COLLEGE_U_TEACHER` | Derivable from `OCCUPATION_TYPE` = 'College/University Teacher' | All years |

## Section C: Employer Information

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 12 | `employer_name` | VARCHAR | Legal business name of employer | `EMPLOYER_NAME` | `EMP_BUSINESS_NAME` | All years |
| 13 | `employer_trade_name` | VARCHAR | Trade name / DBA of employer | — | `EMP_TRADE_NAME` | New form only |
| 14 | `employer_address_1` | VARCHAR | Employer street address line 1 | `EMPLOYER_ADDRESS_1` | `EMP_ADDR1` | All years |
| 15 | `employer_address_2` | VARCHAR | Employer street address line 2 | `EMPLOYER_ADDRESS_2` | `EMP_ADDR2` | All years |
| 16 | `employer_city` | VARCHAR | Employer city | `EMPLOYER_CITY` | `EMP_CITY` | All years |
| 17 | `employer_state` | VARCHAR | Employer state/province | `EMPLOYER_STATE_PROVINCE` | `EMP_STATE` | All years |
| 18 | `employer_country` | VARCHAR | Employer country | `EMPLOYER_COUNTRY` | `EMP_COUNTRY` | All years |
| 19 | `employer_postal_code` | VARCHAR | Employer postal code | `EMPLOYER_POSTAL_CODE` | `EMP_POSTCODE` | All years |
| 20 | `employer_province` | VARCHAR | Employer province (non-US) | — | `EMP_PROVINCE` | New form only |
| 21 | `employer_phone` | VARCHAR | Employer phone number | `EMPLOYER_PHONE` | `EMP_PHONE` | All years |
| 22 | `employer_phone_ext` | VARCHAR | Employer phone extension | `EMPLOYER_PHONE_EXT` | `EMP_PHONEEXT` | All years |
| 23 | `employer_fein` | VARCHAR | Employer Federal Employer Identification Number | `EMPLOYER_FEIN` (FY2024 only) | `EMP_FEIN` | FY2024+ |
| 24 | `naics_code` | VARCHAR | NAICS industry code | `NAICS_CODE` | `EMP_NAICS` | All years |
| 25 | `employer_num_employees` | INTEGER | Total number of employees / employees on payroll | `EMPLOYER_NUM_EMPLOYEES` | `EMP_NUM_PAYROLL` | All years |
| 26 | `employer_year_commenced_business` | VARCHAR | Year employer commenced business or incorporated | `EMPLOYER_YEAR_COMMENCED_BUSINESS` | `EMP_YEAR_COMMENCED` | All years |
| 27 | `fw_ownership_interest` | VARCHAR | Foreign worker has ownership interest with employer (Y/N) | `FW_OWNERSHIP_INTEREST` | `EMP_WORKER_INTEREST` | All years |
| 28 | `fw_familial_relationship` | VARCHAR | Foreign worker has familial relationship with employer (Y/N) | Included in `FW_OWNERSHIP_INTEREST` | `EMP_RELATIONSHIP_WORKER` | New form only (old form combined with #27) |

## Section D: Employer Point of Contact

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 29 | `emp_contact_name` | VARCHAR | Full name of employer's point of contact | `EMP_CONTACT_NAME` | Concat(`EMP_POC_FIRST_NAME`, `EMP_POC_MIDDLE_NAME`, `EMP_POC_LAST_NAME`) | All years |
| 30 | `emp_contact_first_name` | VARCHAR | First name of employer's POC | Parsed from `EMP_CONTACT_NAME` | `EMP_POC_FIRST_NAME` | New form native; old form parse |
| 31 | `emp_contact_last_name` | VARCHAR | Last name of employer's POC | Parsed from `EMP_CONTACT_NAME` | `EMP_POC_LAST_NAME` | New form native; old form parse |
| 32 | `emp_contact_middle_name` | VARCHAR | Middle name of employer's POC | — | `EMP_POC_MIDDLE_NAME` | New form only |
| 33 | `emp_contact_job_title` | VARCHAR | Job title of employer's POC | — | `EMP_POC_JOB_TITLE` | New form only |
| 34 | `emp_contact_address_1` | VARCHAR | POC address line 1 | `EMP_CONTACT_ADDRESS_1` | `EMP_POC_ADDR1` | All years |
| 35 | `emp_contact_address_2` | VARCHAR | POC address line 2 | `EMP_CONTACT_ADDRESS_2` | `EMP_POC_ADDR2` | All years |
| 36 | `emp_contact_city` | VARCHAR | POC city | `EMP_CONTACT_CITY` | `EMP_POC_CITY` | All years |
| 37 | `emp_contact_state` | VARCHAR | POC state | `EMP_CONTACT_STATE_PROVINCE` | `EMP_POC_STATE` | All years |
| 38 | `emp_contact_country` | VARCHAR | POC country | `EMP_CONTACT_COUNTRY` | `EMP_POC_COUNTRY` | All years |
| 39 | `emp_contact_postal_code` | VARCHAR | POC postal code | `EMP_CONTACT_POSTAL_CODE` | `EMP_POC_POSTAL_CODE` | All years |
| 40 | `emp_contact_province` | VARCHAR | POC province (non-US) | — | `EMP_POC_PROVINCE` | New form only |
| 41 | `emp_contact_phone` | VARCHAR | POC phone | `EMP_CONTACT_PHONE` | `EMP_POC_PHONE` | All years |
| 42 | `emp_contact_phone_ext` | VARCHAR | POC phone extension | — | `EMP_POC_PHONEEXT` | New form only |
| 43 | `emp_contact_email` | VARCHAR | POC email | `EMP_CONTACT_EMAIL` | `EMP_POC_EMAIL` | All years |

## Section E: Agent / Attorney Information

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 44 | `agent_attorney_rep_type` | VARCHAR | Representative type: Attorney, Agent, or None | — | `ATTY_AG_REP_TYPE` | New form only |
| 45 | `agent_attorney_name` | VARCHAR | Full name of agent/attorney | `AGENT_ATTORNEY_NAME` | Concat(`ATTY_AG_FIRST_NAME`, `ATTY_AG_MIDDLE_NAME`, `ATTY_AG_LAST_NAME`) | All years |
| 46 | `agent_attorney_first_name` | VARCHAR | First name of agent/attorney | Parsed from `AGENT_ATTORNEY_NAME` | `ATTY_AG_FIRST_NAME` | New form native; old form parse |
| 47 | `agent_attorney_last_name` | VARCHAR | Last name of agent/attorney | Parsed from `AGENT_ATTORNEY_NAME` | `ATTY_AG_LAST_NAME` | New form native; old form parse |
| 48 | `agent_attorney_middle_name` | VARCHAR | Middle name of agent/attorney | — | `ATTY_AG_MIDDLE_NAME` | New form only |
| 49 | `agent_attorney_firm_name` | VARCHAR | Name of law firm or business | `AGENT_ATTORNEY_FIRM_NAME` | `ATTY_AG_LAW_FIRM_NAME` | All years |
| 50 | `agent_attorney_phone` | VARCHAR | Attorney phone | `AGENT_ATTORNEY_PHONE` | `ATTY_AG_PHONE` | All years |
| 51 | `agent_attorney_phone_ext` | VARCHAR | Attorney phone extension | `AGENT_ATTORNEY_PHONE_EXT` | `ATTY_AG_PHONE_EXT` | All years |
| 52 | `agent_attorney_address_1` | VARCHAR | Attorney address line 1 | `AGENT_ATTORNEY_ADDRESS_1` | `ATTY_AG_ADDRESS1` | All years |
| 53 | `agent_attorney_address_2` | VARCHAR | Attorney address line 2 | `AGENT_ATTORNEY_ADDRESS_2` | `ATTY_AG_ADDRESS2` | All years |
| 54 | `agent_attorney_city` | VARCHAR | Attorney city | `AGENT_ATTORNEY_CITY` | `ATTY_AG_CITY` | All years |
| 55 | `agent_attorney_state` | VARCHAR | Attorney state | `AGENT_ATTORNEY_STATE_PROVINCE` | `ATTY_AG_STATE` | All years |
| 56 | `agent_attorney_country` | VARCHAR | Attorney country | `AGENT_ATTORNEY_COUNTRY` | `ATTY_AG_COUNTRY` | All years |
| 57 | `agent_attorney_postal_code` | VARCHAR | Attorney postal code | `AGENT_ATTORNEY_POSTAL_CODE` | `ATTY_AG_POSTAL_CODE` | All years |
| 58 | `agent_attorney_province` | VARCHAR | Attorney province (non-US) | — | `ATTY_AG_PROVINCE` | New form only |
| 59 | `agent_attorney_email` | VARCHAR | Attorney email | `AGENT_ATTORNEY_EMAIL` | `ATTY_AG_EMAIL` | All years |
| 60 | `agent_attorney_fein` | VARCHAR | Attorney/firm FEIN | — | `ATTY_AG_FEIN` | New form only |
| 61 | `agent_attorney_state_bar_number` | VARCHAR | State bar number | — | `ATTY_AG_STATE_BAR_NUMBER` | New form only |
| 62 | `agent_attorney_good_standing_state` | VARCHAR | State of good standing | — | `ATTY_AG_GOOD_STANDING_STATE` | New form only |
| 63 | `agent_attorney_good_standing_court` | VARCHAR | Court of good standing | — | `ATTY_AG_GOOD_STANDING_COURT` | New form only |

## Section F: Foreign Worker Information

> These fields are available in the old form (FY2020–FY2024) but removed from the new form's public disclosure.
> In the new form, this information is captured in Appendix A which is not publicly disclosed.
> Columns will be NULL for new form records.

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 64 | `fw_info_appendix_a_attached` | VARCHAR | Whether Appendix A (identifying FW) is attached (Y/N) | — | `FW_INFO_APPX_A_ATTACHED` | New form only |
| 65 | `fw_info_atty_or_agent` | VARCHAR | Whether employer contracted with atty/agent that also represents the FW (Y/N) | — | `FW_INFO_ATTY_OR_AGENT` | New form only |
| 66 | `country_of_citizenship` | VARCHAR | Country of citizenship of foreign worker | `COUNTRY_OF_CITIZENSHIP` | — | Old form only |
| 67 | `fw_birth_country` | VARCHAR | Foreign worker's country of birth | `FOREIGN_WORKER_BIRTH_COUNTRY` | — | Old form only |
| 68 | `class_of_admission` | VARCHAR | Current visa status of foreign worker | `CLASS_OF_ADMISSION` | — | Old form only |
| 69 | `fw_education` | VARCHAR | Highest education achieved. Values: None, High School, Associate's, Bachelor's, Master's, Doctorate, Other | `FOREIGN_WORKER_EDUCATION` | — | Old form only |
| 70 | `fw_education_other` | VARCHAR | Other highest education specification | `FOREIGN_WORKER_EDUCATION_OTHER` | — | Old form only |
| 71 | `fw_info_major` | VARCHAR | Major field(s) of study for highest education | `FOREIGN_WORKER_INFO_MAJOR` | — | Old form only |
| 72 | `fw_yrs_ed_comp` | VARCHAR | Year relevant education was completed | `FOREIGN_WORKER_YRS_ED_COMP` | — | Old form only |
| 73 | `fw_inst_of_ed` | VARCHAR | Name of educational institution | `FOREIGN_WORKER_INST_OF_ED` | — | Old form only |
| 74 | `fw_ed_inst_address_1` | VARCHAR | Educational institution address line 1 | `FOREIGN_WORKER_ED_INST_ADD_1` | — | Old form only |
| 75 | `fw_ed_inst_address_2` | VARCHAR | Educational institution address line 2 | `FOREIGN_WORKER_ED_INST_ADD_2` | — | Old form only |
| 76 | `fw_ed_inst_city` | VARCHAR | Educational institution city | `FOREIGN_WORKER_ED_INST_CITY` | — | Old form only |
| 77 | `fw_ed_inst_state` | VARCHAR | Educational institution state/province | `FOREIGN_WORKER_ED_INST_STATE_P` | — | Old form only |
| 78 | `fw_ed_inst_country` | VARCHAR | Educational institution country | `FOREIGN_WORKER_ED_INST_COUNTRY` | — | Old form only |
| 79 | `fw_ed_inst_postal_code` | VARCHAR | Educational institution postal code | `FOREIGN_WORKER_ED_INST_POST_CD` | — | Old form only |
| 80 | `fw_training_comp` | VARCHAR | FW completed required training (Y/N/N/A) | `FOREIGN_WORKER_TRAINING_COMP` | — | Old form only |
| 81 | `fw_req_experience` | VARCHAR | FW has required experience (Y/N/N/A) | `FOREIGN_WORKER_REQ_EXPERIENCE` | — | Old form only |
| 82 | `fw_alt_ed_exp` | VARCHAR | FW has alternate combination of education and experience (Y/N/N/A) | `FOREIGN_WORKER_ALT_ED_EXP` | — | Old form only |
| 83 | `fw_alt_occ_exp` | VARCHAR | FW has alternate occupation experience (Y/N/N/A) | `FOREIGN_WORKER_ALT_OCC_EXP` | — | Old form only |
| 84 | `fw_exp_with_employer` | VARCHAR | FW gained qualifying experience with this employer (Y/N/N/A) | `FOREIGN_WORKER_EXP_WITH_EMPL` | `OTHER_REQ_FW_GAIN_EXP` | All years |
| 85 | `fw_employer_pay_for_ed` | VARCHAR | Employer paid for FW's education/training (Y/N) | `FOREIGN_WORKER_EMPL_PAY_FOR_ED` | `OTHER_REQ_EMP_PAY_EDUCATION` | All years |
| 86 | `fw_currently_employed` | VARCHAR | FW currently employed by petitioning employer (Y/N) | `FOREIGN_WORKER_CURR_EMPLOYED` | `OTHER_REQ_IS_FW_CURRENTLY_WRK` | All years |

## Section G: Prevailing Wage Determination

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 87 | `pw_tracking_number` | VARCHAR | Unique ID for the Prevailing Wage Determination | `PW_TRACK_NUMBER` | `JOB_OPP_PWD_NUMBER` | All years |
| 88 | `pw_soc_code` | VARCHAR | SOC occupational code | `PW_SOC_CODE` | `PWD_SOC_CODE` (FY2026+) | All years (new form: FY2026+) |
| 89 | `pw_soc_title` | VARCHAR | SOC occupational title | `PW_SOC_TITLE` | `PWD_SOC_TITLE` (FY2026+) | All years (new form: FY2026+) |
| 90 | `pw_skill_level` | VARCHAR | Prevailing wage level: Level I/II/III/IV/N/A | `PW_SKILL_LEVEL` | — | Old form only |
| 91 | `pw_wage` | DECIMAL | Prevailing wage amount | `PW_WAGE` | — | Old form only |
| 92 | `pw_unit_of_pay` | VARCHAR | PW unit: Hour, Week, Bi-Weekly, Month, Year | `PW_UNIT_OF_PAY` | — | Old form only |
| 93 | `pw_wage_source` | VARCHAR | PW source: OES, CBA, Employer Conducted Survey, DBA, SCA, Other | `PW_WAGE_SOURCE` | — | Old form only |
| 94 | `pw_source_name_other` | VARCHAR | Name of other PW source | `PW_SOURCE_NAME_OTHER` | — | Old form only |
| 95 | `pw_determination_date` | DATE | Date PW decision was issued | `PW_DETERMINATION_DATE` | — | Old form only |
| 96 | `pw_expiration_date` | DATE | Date PW expires | `PW_EXPIRATION_DATE` | — | Old form only |
| 97 | `pw_attached` | VARCHAR | Whether a valid PWD is attached (Y/N/N/A) | — | `JOB_OPP_PWD_ATTACHED` | New form only |

## Section H: Wage Offer

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 98 | `wage_offer_from` | DECIMAL | Employer's offered wage (lower bound) | `WAGE_OFFER_FROM` | `JOB_OPP_WAGE_FROM` | All years |
| 99 | `wage_offer_to` | DECIMAL | Employer's offered wage (upper bound, if range) | `WAGE_OFFER_TO` | `JOB_OPP_WAGE_TO` | All years |
| 100 | `wage_offer_unit_of_pay` | VARCHAR | Wage unit: Hour, Week, Bi-Weekly, Month, Year | `WAGE_OFFER_UNIT_OF_PAY` | `JOB_OPP_WAGE_PER` | All years |
| 101 | `wage_offer_conditions` | VARCHAR | Conditions about wage (bonuses, benefits, subsidized housing, etc.) | — | `JOB_OPP_WAGE_CONDITIONS` | New form only |

## Section I: Worksite Information

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 102 | `worksite_type` | VARCHAR | Type of worksite location | — | `PRIMARY_WORKSITE_TYPE` | New form only |
| 103 | `worksite_address_1` | VARCHAR | Primary worksite address line 1 | `WORKSITE_ADDRESS_1` | `PRIMARY_WORKSITE_ADDR1` | All years |
| 104 | `worksite_address_2` | VARCHAR | Primary worksite address line 2 | `WORKSITE_ADDRESS_2` | `PRIMARY_WORKSITE_ADDR2` | All years |
| 105 | `worksite_city` | VARCHAR | Worksite city | `WORKSITE_CITY` | `PRIMARY_WORKSITE_CITY` | All years |
| 106 | `worksite_county` | VARCHAR | Worksite county | — | `PRIMARY_WORKSITE_COUNTY` | New form only |
| 107 | `worksite_state` | VARCHAR | Worksite state | `WORKSITE_STATE` | `PRIMARY_WORKSITE_STATE` | All years |
| 108 | `worksite_postal_code` | VARCHAR | Worksite postal code | `WORKSITE_POSTAL_CODE` | `PRIMARY_WORKSITE_POSTAL_CODE` | All years |
| 109 | `worksite_bls_area` | VARCHAR | MSA/OES area title covering worksite | — | `PRIMARY_WORKSITE_BLS_AREA` | New form only |
| 110 | `is_multiple_locations` | VARCHAR | Work performed at multiple locations (Y/N) | — | `IS_MULTIPLE_LOCATIONS` | New form only |
| 111 | `is_appendix_b_attached` | VARCHAR | Appendix B for multiple locations attached (Y/N/N/A) | — | `IS_APPENDIX_B_ATTACHED` | New form only |

## Section J: Job Requirements (Old Form Detail)

> These detailed job requirement fields are only available in old form. New form captures this
> information on the PWD (ETA-9141) which is not part of the PERM disclosure file.

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 112 | `job_title` | VARCHAR | Title of the permanent job | `JOB_TITLE` | `JOB_TITLE` | All years |
| 113 | `minimum_education` | VARCHAR | Minimum U.S. diploma/degree: None, High School, Associate's, Bachelor's, Master's, Doctorate, Other | `MINIMUM_EDUCATION` | — | Old form only |
| 114 | `job_education_min_other` | VARCHAR | If "Other", the specific degree required | `JOB_EDUCATION_MIN_OTHER` | — | Old form only |
| 115 | `major_field_of_study` | VARCHAR | Required major or field of study | `MAJOR_FIELD_OF_STUDY` | — | Old form only |
| 116 | `required_training` | VARCHAR | Training required (Y/N) | `REQUIRED_TRAINING` | — | Old form only |
| 117 | `required_training_months` | INTEGER | Number of months of training required | `REQUIRED_TRAINING_MONTHS` | — | Old form only |
| 118 | `required_field_of_training` | VARCHAR | Field of training | `REQUIRED_FIELD_OF_TRAINING` | — | Old form only |
| 119 | `required_experience` | VARCHAR | Experience in job required (Y/N) | `REQUIRED_EXPERIENCE` | — | Old form only |
| 120 | `required_experience_months` | INTEGER | Months of experience required | `REQUIRED_EXPERIENCE_MONTHS` | — | Old form only |
| 121 | `accept_alt_field_of_study` | VARCHAR | Alternate field of study acceptable (Y/N) | `ACCEPT_ALT_FIELD_OF_STUDY` | — | Old form only |
| 122 | `accept_alt_major_fld_of_study` | VARCHAR | Alternate field of study name | `ACCEPT_ALT_MAJOR_FLD_OF_STUDY` | — | Old form only |
| 123 | `accept_alt_combo` | VARCHAR | Alternate education+experience combo acceptable (Y/N) | `ACCEPT_ALT_COMBO` | — | Old form only |
| 124 | `accept_alt_combo_education` | VARCHAR | Alternate education level | `ACCEPT_ALT_COMBO_EDUCATION` | — | Old form only |
| 125 | `accept_alt_combo_ed_other` | VARCHAR | Alternate "other" education | `ACCEPT_ALT_COMBO_ED_OTHER` | — | Old form only |
| 126 | `accept_alt_combo_education_yrs` | INTEGER | Alternate: years of experience acceptable | `ACCEPT_ALT_COMBO_EDUCATION_YRS` | — | Old form only |
| 127 | `accept_foreign_education` | VARCHAR | Foreign educational equivalent acceptable (Y/N) | `ACCEPT_FOREIGN_EDUCATION` | Semantically similar: `OTHER_REQ_ACCEPT_DIPLOMA_PWD` | All years (fuzzy) |
| 128 | `accept_alt_occupation` | VARCHAR | Alternate occupation experience acceptable (Y/N) | `ACCEPT_ALT_OCCUPATION` | — | Old form only |
| 129 | `accept_alt_occupation_months` | INTEGER | Months of alternate occupation experience | `ACCEPT_ALT_OCCUPATION_MONTHS` | — | Old form only |
| 130 | `accept_alt_job_title` | VARCHAR | Title of acceptable alternate occupation | `ACCEPT_ALT_JOB_TITLE` | — | Old form only |
| 131 | `specific_skills` | VARCHAR | Specific skills or job-related requirements (free text) | `SPECIFIC_SKILLS` | — | Old form only |
| 132 | `job_opp_requirements_normal` | VARCHAR | Job requirements normal for occupation (Y/N) | `JOB_OPP_REQUIREMENTS_NORMAL` | — | Old form only |

## Section K: Other Job Requirements & Compliance (New Form Detail)

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 133 | `is_fulltime_employment` | VARCHAR | Full-time position (Y/N) | — | `OTHER_REQ_IS_FULLTIME_EMP` | New form only |
| 134 | `is_livein_household` | VARCHAR | Live-in household domestic service worker (Y/N) | `FOREIGN_WORKER_LIVE_IN_DOM_SER` | `OTHER_REQ_IS_LIVEIN_HOUSEHOLD` | All years |
| 135 | `is_paid_experience` | VARCHAR | Live-in domestic: FW has 1 year paid experience (Y/N/N/A) | — | `OTHER_REQ_IS_PAID_EXPERIENCE` | New form only |
| 136 | `fw_executed_contract` | VARCHAR | FW and employer executed employment contract (Y/N/N/A) | `FOREIGN_WORKER_LIVE_IN_DOM_SVC_CNT` | `OTHER_REQ_IS_FW_EXECUTED_CONT` | All years |
| 137 | `emp_provided_contract` | VARCHAR | Employer provided contract copy to FW (Y/N/N/A) | Included in `FOREIGN_WORKER_LIVE_IN_DOM_SVC_CNT` | `OTHER_REQ_IS_EMP_PROVIDED_CONT` | New form only (old form combined in #136) |
| 138 | `accept_foreign_diploma_pwd` | VARCHAR | Employer accepts foreign diploma/degree equivalent to PWD (Y/N/N/A) | Semantically similar: `ACCEPT_FOREIGN_EDUCATION` | `OTHER_REQ_ACCEPT_DIPLOMA_PWD` | All years (fuzzy) |
| 139 | `fw_qualifies_by_alt_requirements` | VARCHAR | FW qualifies only by employer's alternative requirements (Y/N/N/A) | — | `OTHER_REQ_IS_FW_QUALIFY` | New form only |
| 140 | `emp_will_accept_any_combo` | VARCHAR | Employer accepts any suitable combo of education/experience/training (Y/N) | — | `OTHER_REQ_EMP_WILL_ACCEPT` | New form only |
| 141 | `emp_rely_solely_on_fw_exp` | VARCHAR | Employer relying solely on experience FW gained with them (Y/N) | — | `OTHER_REQ_EMP_RELY_EXP` | New form only |
| 142 | `job_on_employer_premises` | VARCHAR | Job requires FW to live on employer premises (Y/N) | `FOREIGN_WORKER_LIVE_ON_PREM` | `OTHER_REQ_JOB_EMP_PREMISES` | All years |
| 143 | `combination_occupation` | VARCHAR | Job involves combination of occupations (Y/N) | `COMBINATION_OCCUPATION` | `OTHER_REQ_JOB_COMBO_OCCUP` | All years |
| 144 | `foreign_language_required` | VARCHAR | Foreign language required/preferred (Y/N) | `FOREIGN_LANGUAGE_REQUIRED` | `OTHER_REQ_JOB_FOREIGN_LANGUAGE` | All years |
| 145 | `job_req_exceed_svp` | VARCHAR | Job requirements exceed SVP level for occupation (Y/N/N/A) | — | `OTHER_REQ_JOB_REQ_EXCEED` | New form only |
| 146 | `emp_use_credentialing_service` | VARCHAR | Employer used credentialing service for FW (Y/N/N/A) | — | `OTHER_REQ_EMP_USE_CREDENTIAL` | New form only |
| 147 | `offered_to_foreign_worker` | VARCHAR | Position offered to FW being sponsored (Y/N) | `OFFERED_TO_APPL_FOREIGN_WORKER` | — | Old form only |
| 148 | `emp_received_payment` | VARCHAR | Employer received payment for this application (Y/N) | `EMP_RECEIVED_PAYMENT` | `OTHER_REQ_EMP_REC_PAYMENT` | All years |
| 149 | `payment_details` | VARCHAR | Details of payment received (amount, date, purpose) | `PAYMENT_DETAILS` | — | Old form only |
| 150 | `layoff_in_past_six_months` | VARCHAR | Employer had layoff in occupation within past 6 months (Y/N) | `LAYOFF_IN_PAST_SIX_MONTHS` | `OTHER_REQ_EMP_LAYOFF` | All years |
| 151 | `us_workers_considered` | VARCHAR | Laid-off US workers notified and considered (Y/N/N/A) | `US_WORKERS_CONSIDERED` | — | Old form only |
| 152 | `emp_certify_compliance` | VARCHAR | Employer certifies compliance with Labor Condition Statements (Y/N) | — | `EMP_CERTIFY_COMPLIANCE` | New form only |

## Section L: Recruitment Information — Teacher/Competitive

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 153 | `competitive_process` | VARCHAR | Teacher selected via competitive recruitment (Y/N) | `COMPETITIVE_PROCESS` | — | Old form only |
| 154 | `basic_recruitment_process` | VARCHAR | Teacher selected via basic recruitment process (Y/N) | `BASIC_RECRUITMENT_PROCESS` | — | Old form only |
| 155 | `teacher_select_date` | DATE | Date FW selected via competitive process | `TEACHER_SELECT_DATE` | — | Old form only |
| 156 | `teacher_pub_journal_name` | VARCHAR | National professional journal name and date | `TEACHER_PUB_JOURNAL_NAME` | — | Old form only |
| 157 | `add_recruit_information` | VARCHAR | Additional recruitment information | `ADD_RECRUIT_INFORMATION` | — | Old form only |
| 158 | `supervised_recruitment_required` | VARCHAR | Employer required to undergo supervised recruitment (Y/N) | — | `RECR_INFO_RECRUIT_SUPERVISED_REQ` | New form only |

## Section M: Recruitment Information — SWA & Advertisements

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 159 | `swa_job_order_start_date` | DATE | SWA job order start date | `SWA_JOB_ORDER_START_DATE` | `RECR_INFO_JOB_START_DATE` | All years |
| 160 | `swa_job_order_end_date` | DATE | SWA job order end date | `SWA_JOB_ORDER_END_DATE` | `RECR_INFO_JOB_END_DATE` | All years |
| 161 | `sunday_edition_newspaper` | VARCHAR | Sunday edition exists in area (Y/N/N/A) | `SUNDAY_EDITION_NEWSPAPER` | `RECR_INFO_IS_NEWSPAPER_SUNDAY` | All years |
| 162 | `first_newspaper_name` | VARCHAR | Name of newspaper for first ad | `FIRST_NEWSPAPER_NAME` | `RECR_INFO_NEWSPAPER_NAME` | All years |
| 163 | `first_ad_start_date` | DATE | Date of first advertisement | `FIRST_ADVERTISEMENT_START_DATE` | `RECR_INFO_AD_DATE1` | All years |
| 164 | `second_ad_type` | VARCHAR | Second ad type: Newspaper or Journal | `SECOND_ADVERTISEMENT_TYPE` | `RECR_INFO_RECRUIT_AD_TYPE` | All years (fuzzy enum) |
| 165 | `second_newspaper_name` | VARCHAR | Name of newspaper/journal for second ad | `SECOND_NEWSPAPER_AD_NAME` | `RECR_INFO_NEWSPAPER_NAME2` | All years |
| 166 | `second_ad_start_date` | DATE | Date of second advertisement | `SECOND_AD_START_DATE` | `RECR_INFO_AD_DATE2` | All years |

## Section N: Recruitment — Additional Methods (Date Ranges)

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 167 | `job_fair_from_date` | DATE | Job fair start date | `JOB_FAIR_FROM_DATE` | `RECR_OCC_JOB_FAIR_FROM` | All years |
| 168 | `job_fair_to_date` | DATE | Job fair end date | `JOB_FAIR_TO_DATE` | `RECR_OCC_JOB_FAIR_TO` | All years |
| 169 | `on_campus_recruiting_from_date` | DATE | On-campus recruiting start date | `ON_CAMPUS_RECRUITING_FROM_DATE` | `RECR_OCC_ON_CAMPUS_FROM` | All years |
| 170 | `on_campus_recruiting_to_date` | DATE | On-campus recruiting end date | `ON_CAMPUS_RECRUITING_TO_DATE` | `RECR_OCC_ON_CAMPUS_TO` | All years |
| 171 | `employer_website_from_date` | DATE | Employer website posting start date | `EMPLOYER_WEBSITE_FROM_DATE` | `RECR_OCC_EMP_WEBSITE_FROM` | All years |
| 172 | `employer_website_to_date` | DATE | Employer website posting end date | `EMPLOYER_WEBSITE_TO_DATE` | `RECR_OCC_EMP_WEBSITE_TO` | All years |
| 173 | `pro_org_ad_from_date` | DATE | Trade/professional org ad start date | `PRO_ORG_AD_FROM_DATE` | `RECR_OCC_TRADE_ORG_FROM` | All years |
| 174 | `pro_org_ad_to_date` | DATE | Trade/professional org ad end date | `PRO_ORG_ADVERTISEMENT_TO_DATE` | `RECR_OCC_TRADE_ORG_TO` | All years |
| 175 | `job_search_website_from_date` | DATE | Job search website start date | `JOB_SEARCH_WEBSITE_FROM_DATE` | `RECR_OCC_JOB_SEARCH_FROM` | All years |
| 176 | `job_search_website_to_date` | DATE | Job search website end date | `JOB_SEARCH_WEBSITE_TO_DATE` | `RECR_OCC_JOB_SEARCH_TO` | All years |
| 177 | `pvt_employment_firm_from_date` | DATE | Private employment firm start date | `PVT_EMPLOYMENT_FIRM_FROM_DATE` | `RECR_OCC_PRIVATE_EMP_FROM` | All years |
| 178 | `pvt_employment_firm_to_date` | DATE | Private employment firm end date | `PVT_EMPLOYMENT_FIRM_TO_DATE` | `RECR_OCC_PRIVATE_EMP_TO` | All years |
| 179 | `employee_referral_from_date` | DATE | Employee referral program start date | `EMPLOYEE_REF_PROG_FROM_DATE` | `RECR_OCC_EMP_REFERRAL_FROM` | All years |
| 180 | `employee_referral_to_date` | DATE | Employee referral program end date | `EMPLOYEE_REFERRAL_PROG_TO_DATE` | `RECR_OCC_EMP_REFERRAL_TO` | All years |
| 181 | `campus_placement_from_date` | DATE | Campus placement office start date | `CAMPUS_PLACEMENT_FROM_DATE` | `RECR_OCC_CAMPUS_PLACEMENT_FROM` | All years |
| 182 | `campus_placement_to_date` | DATE | Campus placement office end date | `CAMPUS_PLACEMENT_TO_DATE` | `RECR_OCC_CAMPUS_PLACEMENT_TO` | All years |
| 183 | `local_ethnic_paper_from_date` | DATE | Local/ethnic newspaper start date | `LOCAL_ETHNIC_PAPER_FROM_DATE` | `RECR_OCC_LOCAL_NEWSPAPER_FROM` | All years |
| 184 | `local_ethnic_paper_to_date` | DATE | Local/ethnic newspaper end date | `LOCAL_ETHNIC_PAPER_TO_DATE` | `RECR_OCC_LOCAL_NEWSPAPER_TO` | All years |
| 185 | `radio_tv_ad_from_date` | DATE | Radio/TV ad start date | `RADIO_TV_AD_FROM_DATE` | `RECR_OCC_RADIO_AD_FROM` | All years |
| 186 | `radio_tv_ad_to_date` | DATE | Radio/TV ad end date | `RADIO_TV_AD_TO_DATE` | `RECR_OCC_RADIO_AD_TO` | All years |

## Section O: Notice of Filing / Posting

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 187 | `bargaining_rep_notified` | VARCHAR | Bargaining representative notified (Y/N/N/A) | `BARGAINING_REP_NOTIFIED` | `NOTICE_POST_BARGAIN_REP` | All years |
| 188 | `posted_notice_at_worksite` | VARCHAR | Notice posted at worksite (Y/N/N/A) | `POSTED_NOTICE_AT_WORKSITE` | — | Old form only |
| 189 | `notice_post_physical` | VARCHAR | Notice physically posted for 10 business days (Y/N) | — | `NOTICE_POST_BARGAIN_REP_PHYSICAL` | New form only |
| 190 | `notice_post_electronic` | VARCHAR | Notice disseminated electronically (Y/N) | — | `NOTICE_POST_BARGAIN_REP_ELECTRONIC` | New form only |
| 191 | `notice_post_inhouse` | VARCHAR | Notice disseminated via in-house media (Y/N) | — | `NOTICE_POST_BARGAIN_REP_INHOUSE` | New form only |
| 192 | `notice_post_private` | VARCHAR | Notice posted in private household (Y/N) | — | `NOTICE_POST_BARGAIN_REP_PRIVATE` | New form only |
| 193 | `notice_emp_not_posted` | VARCHAR | Employer did NOT post notice (Y/N) | — | `NOTICE_POST_EMP_NOT_POSTED` | New form only |

## Section P: Preparer / Declaration

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 194 | `employer_completed_application` | VARCHAR | Application completed by employer (Y/N) | `EMPLOYER_COMPLETED_APPLICATION` | — | Old form only |
| 195 | `preparer_name` | VARCHAR | Name of person who prepared application | `PREPARER_NAME` | Concat(`DECL_PREP_FIRST_NAME`, `DECL_PREP_MIDDLE_NAME`, `DECL_PREP_LAST_NAME`) | All years |
| 196 | `preparer_first_name` | VARCHAR | Preparer first name | Parsed from `PREPARER_NAME` | `DECL_PREP_FIRST_NAME` | New form native; old form parse |
| 197 | `preparer_last_name` | VARCHAR | Preparer last name | Parsed from `PREPARER_NAME` | `DECL_PREP_LAST_NAME` | New form native; old form parse |
| 198 | `preparer_middle_name` | VARCHAR | Preparer middle name | — | `DECL_PREP_MIDDLE_NAME` | New form only |
| 199 | `preparer_title` | VARCHAR | Preparer occupational title | `PREPARER_TITLE` | — | Old form only |
| 200 | `preparer_email` | VARCHAR | Preparer email | `PREPARER_EMAIL` | `DECL_PREP_EMAIL` | All years |
| 201 | `preparer_lawfirm_fein` | VARCHAR | Preparer law firm FEIN | — | `DECL_PREP_LAWFIRM_FEIN` | New form only |
| 202 | `preparer_firm_business_name` | VARCHAR | Preparer firm business name | — | `DECL_PREP_FIRM_BUSINESS_NAME` | New form only |
| 203 | `emp_decl_name` | VARCHAR | Name of person signing employer declaration | `EMP_INFO_DECL_NAME` | Concat(`DECL_PREP_FIRST_NAME`, `DECL_PREP_LAST_NAME`) | All years (new form: merged with preparer) |
| 204 | `emp_decl_title` | VARCHAR | Title of person signing employer declaration | `EMP_DECL_TITLE` / `EMP_INFO_DECL_TITLE` (FY2020) | — | Old form only |

## Section Q: Metadata (ETL-Added)

| # | Unified Column | Type | Description | Old Form Source | New Form Source | Availability |
|---|---|---|---|---|---|---|
| 205 | `fiscal_year` | INTEGER | Federal fiscal year (e.g., 2020, 2024, 2026) | Derived from filename | Derived from filename | All years |
| 206 | `form_version` | VARCHAR | Form version: 'old' (pre-June 2023) or 'new' (post-June 2023) | Derived | Derived | All years |
| 207 | `quarter` | VARCHAR | Reporting quarter (Q1-Q4) if applicable | Derived from filename | Derived from filename | All years |

---

## Summary

| Metric | Count |
|---|---|
| **Total unified columns** | **207** |
| Available in all years (direct mapping) | 87 |
| Available in all years (fuzzy/derived mapping) | 8 |
| Old form only (NULL in new form records) | 62 |
| New form only (NULL in old form records) | 47 |
| ETL metadata columns | 3 |

### Notes on Data Loading

1. **FY2024 is a transition year**: Both old and new form data exist. Use `PERM_Record_Layout_FY2024_Q4.pdf` for old form records and `PERM_New_Form_Record_Layout_FY2024_Q4.pdf` for new form records. Distinguish by the `form_version` column.

2. **Name fields**: Old form has single `NAME` fields; new form splits into `FIRST/MIDDLE/LAST`. The unified schema keeps both the combined and split versions. When loading old form data, the combined name goes into `*_name`; split fields are NULL (or attempt parsing). When loading new form data, concat into `*_name` and also populate the split fields.

3. **Foreign Worker fields**: Columns 64–86 preserve all FW information from the old form. These will be NULL for new form records (FY2024 New – FY2026) since this data moved to non-public Appendix A.

4. **Prevailing Wage details**: Columns 90–96 are old form only. The new form references PWD via the tracking number but doesn't include wage details in the PERM disclosure (they're on the separate ETA-9141).
