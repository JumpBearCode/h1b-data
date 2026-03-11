# PERM Schema Mapping: Old Form (FY2020-FY2024) vs New Form (FY2024 New-FY2026)

> Old Form = FY2024 Q4 (most complete old form, includes EMPLOYER_FEIN)
> New Form = FY2026 Q1 (most complete new form, includes PWD_SOC_CODE/TITLE)

---

## 1. Direct / Near-Exact Mappings (公共相似部分)

These fields map 1:1 between old and new schemas. Same semantic meaning, just renamed.

| # | Old Form Field | New Form Field | Notes |
|---|---|---|---|
| 1 | `CASE_NUMBER` | `CASE_NUMBER` | Identical |
| 2 | `CASE_STATUS` | `CASE_STATUS` | Identical |
| 3 | `RECEIVED_DATE` | `RECEIVED_DATE` | Identical |
| 4 | `DECISION_DATE` | `DECISION_DATE` | Identical |
| 5 | `EMPLOYER_NAME` | `EMP_BUSINESS_NAME` | Renamed |
| 6 | `EMPLOYER_ADDRESS_1` | `EMP_ADDR1` | Renamed |
| 7 | `EMPLOYER_ADDRESS_2` | `EMP_ADDR2` | Renamed |
| 8 | `EMPLOYER_CITY` | `EMP_CITY` | Renamed |
| 9 | `EMPLOYER_STATE_PROVINCE` | `EMP_STATE` | Renamed (province dropped from name, but field covers same) |
| 10 | `EMPLOYER_COUNTRY` | `EMP_COUNTRY` | Renamed |
| 11 | `EMPLOYER_POSTAL_CODE` | `EMP_POSTCODE` | Renamed |
| 12 | `EMPLOYER_PHONE` | `EMP_PHONE` | Renamed |
| 13 | `EMPLOYER_PHONE_EXT` | `EMP_PHONEEXT` | Renamed |
| 14 | `EMPLOYER_FEIN` | `EMP_FEIN` | Renamed (old form only has this in FY2024) |
| 15 | `NAICS_CODE` | `EMP_NAICS` | Renamed |
| 16 | `EMPLOYER_NUM_EMPLOYEES` | `EMP_NUM_PAYROLL` | Renamed (semantics: "employees" → "payroll") |
| 17 | `EMPLOYER_YEAR_COMMENCED_BUSINESS` | `EMP_YEAR_COMMENCED` | Renamed |
| 18 | `FW_OWNERSHIP_INTEREST` | `EMP_WORKER_INTEREST` | Renamed (ownership interest portion) |
| 19 | `EMP_CONTACT_NAME` | `EMP_POC_LAST_NAME` + `EMP_POC_FIRST_NAME` + `EMP_POC_MIDDLE_NAME` | Old=single field, New=split into 3 |
| 20 | `EMP_CONTACT_ADDRESS_1` | `EMP_POC_ADDR1` | Renamed |
| 21 | `EMP_CONTACT_ADDRESS_2` | `EMP_POC_ADDR2` | Renamed |
| 22 | `EMP_CONTACT_CITY` | `EMP_POC_CITY` | Renamed |
| 23 | `EMP_CONTACT_STATE_PROVINCE` | `EMP_POC_STATE` | Renamed |
| 24 | `EMP_CONTACT_COUNTRY` | `EMP_POC_COUNTRY` | Renamed |
| 25 | `EMP_CONTACT_POSTAL_CODE` | `EMP_POC_POSTAL_CODE` | Renamed |
| 26 | `EMP_CONTACT_PHONE` | `EMP_POC_PHONE` | Renamed |
| 27 | `EMP_CONTACT_EMAIL` | `EMP_POC_EMAIL` | Renamed |
| 28 | `AGENT_ATTORNEY_NAME` | `ATTY_AG_LAST_NAME` + `ATTY_AG_FIRST_NAME` + `ATTY_AG_MIDDLE_NAME` | Old=single, New=split into 3 |
| 29 | `AGENT_ATTORNEY_FIRM_NAME` | `ATTY_AG_LAW_FIRM_NAME` | Renamed |
| 30 | `AGENT_ATTORNEY_PHONE` | `ATTY_AG_PHONE` | Renamed |
| 31 | `AGENT_ATTORNEY_PHONE_EXT` | `ATTY_AG_PHONE_EXT` | Renamed |
| 32 | `AGENT_ATTORNEY_ADDRESS_1` | `ATTY_AG_ADDRESS1` | Renamed |
| 33 | `AGENT_ATTORNEY_ADDRESS_2` | `ATTY_AG_ADDRESS2` | Renamed |
| 34 | `AGENT_ATTORNEY_CITY` | `ATTY_AG_CITY` | Renamed |
| 35 | `AGENT_ATTORNEY_STATE_PROVINCE` | `ATTY_AG_STATE` | Renamed |
| 36 | `AGENT_ATTORNEY_COUNTRY` | `ATTY_AG_COUNTRY` | Renamed |
| 37 | `AGENT_ATTORNEY_POSTAL_CODE` | `ATTY_AG_POSTAL_CODE` | Renamed |
| 38 | `AGENT_ATTORNEY_EMAIL` | `ATTY_AG_EMAIL` | Renamed |
| 39 | `PW_TRACK_NUMBER` | `JOB_OPP_PWD_NUMBER` | Renamed (PW tracking # → PWD #) |
| 40 | `PW_SOC_CODE` | `PWD_SOC_CODE` | Renamed (new form FY2026 only) |
| 41 | `PW_SOC_TITLE` | `PWD_SOC_TITLE` | Renamed (new form FY2026 only) |
| 42 | `JOB_TITLE` | `JOB_TITLE` | Identical |
| 43 | `WAGE_OFFER_FROM` | `JOB_OPP_WAGE_FROM` | Renamed |
| 44 | `WAGE_OFFER_TO` | `JOB_OPP_WAGE_TO` | Renamed |
| 45 | `WAGE_OFFER_UNIT_OF_PAY` | `JOB_OPP_WAGE_PER` | Renamed |
| 46 | `WORKSITE_ADDRESS_1` | `PRIMARY_WORKSITE_ADDR1` | Renamed |
| 47 | `WORKSITE_ADDRESS_2` | `PRIMARY_WORKSITE_ADDR2` | Renamed |
| 48 | `WORKSITE_CITY` | `PRIMARY_WORKSITE_CITY` | Renamed |
| 49 | `WORKSITE_STATE` | `PRIMARY_WORKSITE_STATE` | Renamed |
| 50 | `WORKSITE_POSTAL_CODE` | `PRIMARY_WORKSITE_POSTAL_CODE` | Renamed |
| 51 | `COMBINATION_OCCUPATION` | `OTHER_REQ_JOB_COMBO_OCCUP` | Renamed |
| 52 | `FOREIGN_LANGUAGE_REQUIRED` | `OTHER_REQ_JOB_FOREIGN_LANGUAGE` | Renamed |
| 53 | `FOREIGN_WORKER_LIVE_ON_PREM` | `OTHER_REQ_JOB_EMP_PREMISES` | Renamed |
| 54 | `FOREIGN_WORKER_LIVE_IN_DOM_SER` | `OTHER_REQ_IS_LIVEIN_HOUSEHOLD` | Renamed (domestic service → live-in household) |
| 55 | `FOREIGN_WORKER_LIVE_IN_DOM_SVC_CNT` | `OTHER_REQ_IS_FW_EXECUTED_CONT` + `OTHER_REQ_IS_EMP_PROVIDED_CONT` | Old=1 field (contract executed+provided), New=split into 2 |
| 56 | `FOREIGN_WORKER_CURR_EMPLOYED` | `OTHER_REQ_IS_FW_CURRENTLY_WRK` | Renamed |
| 57 | `FOREIGN_WORKER_EXP_WITH_EMPL` | `OTHER_REQ_FW_GAIN_EXP` | Renamed (experience with employer → gain exp) |
| 58 | `FOREIGN_WORKER_EMPL_PAY_FOR_ED` | `OTHER_REQ_EMP_PAY_EDUCATION` | Renamed |
| 59 | `EMP_RECEIVED_PAYMENT` | `OTHER_REQ_EMP_REC_PAYMENT` | Renamed |
| 60 | `LAYOFF_IN_PAST_SIX_MONTHS` | `OTHER_REQ_EMP_LAYOFF` | Renamed |
| 61 | `SWA_JOB_ORDER_START_DATE` | `RECR_INFO_JOB_START_DATE` | Renamed |
| 62 | `SWA_JOB_ORDER_END_DATE` | `RECR_INFO_JOB_END_DATE` | Renamed |
| 63 | `SUNDAY_EDITION_NEWSPAPER` | `RECR_INFO_IS_NEWSPAPER_SUNDAY` | Renamed |
| 64 | `FIRST_NEWSPAPER_NAME` | `RECR_INFO_NEWSPAPER_NAME` | Renamed |
| 65 | `FIRST_ADVERTISEMENT_START_DATE` | `RECR_INFO_AD_DATE1` | Renamed |
| 66 | `SECOND_NEWSPAPER_AD_NAME` | `RECR_INFO_NEWSPAPER_NAME2` | Renamed |
| 67 | `SECOND_AD_START_DATE` | `RECR_INFO_AD_DATE2` | Renamed |
| 68 | `JOB_FAIR_FROM_DATE` | `RECR_OCC_JOB_FAIR_FROM` | Renamed |
| 69 | `JOB_FAIR_TO_DATE` | `RECR_OCC_JOB_FAIR_TO` | Renamed |
| 70 | `ON_CAMPUS_RECRUITING_FROM_DATE` | `RECR_OCC_ON_CAMPUS_FROM` | Renamed |
| 71 | `ON_CAMPUS_RECRUITING_TO_DATE` | `RECR_OCC_ON_CAMPUS_TO` | Renamed |
| 72 | `EMPLOYER_WEBSITE_FROM_DATE` | `RECR_OCC_EMP_WEBSITE_FROM` | Renamed |
| 73 | `EMPLOYER_WEBSITE_TO_DATE` | `RECR_OCC_EMP_WEBSITE_TO` | Renamed |
| 74 | `PRO_ORG_AD_FROM_DATE` | `RECR_OCC_TRADE_ORG_FROM` | Renamed |
| 75 | `PRO_ORG_ADVERTISEMENT_TO_DATE` | `RECR_OCC_TRADE_ORG_TO` | Renamed |
| 76 | `JOB_SEARCH_WEBSITE_FROM_DATE` | `RECR_OCC_JOB_SEARCH_FROM` | Renamed |
| 77 | `JOB_SEARCH_WEBSITE_TO_DATE` | `RECR_OCC_JOB_SEARCH_TO` | Renamed |
| 78 | `PVT_EMPLOYMENT_FIRM_FROM_DATE` | `RECR_OCC_PRIVATE_EMP_FROM` | Renamed |
| 79 | `PVT_EMPLOYMENT_FIRM_TO_DATE` | `RECR_OCC_PRIVATE_EMP_TO` | Renamed |
| 80 | `EMPLOYEE_REF_PROG_FROM_DATE` | `RECR_OCC_EMP_REFERRAL_FROM` | Renamed |
| 81 | `EMPLOYEE_REFERRAL_PROG_TO_DATE` | `RECR_OCC_EMP_REFERRAL_TO` | Renamed |
| 82 | `CAMPUS_PLACEMENT_FROM_DATE` | `RECR_OCC_CAMPUS_PLACEMENT_FROM` | Renamed |
| 83 | `CAMPUS_PLACEMENT_TO_DATE` | `RECR_OCC_CAMPUS_PLACEMENT_TO` | Renamed |
| 84 | `LOCAL_ETHNIC_PAPER_FROM_DATE` | `RECR_OCC_LOCAL_NEWSPAPER_FROM` | Renamed |
| 85 | `LOCAL_ETHNIC_PAPER_TO_DATE` | `RECR_OCC_LOCAL_NEWSPAPER_TO` | Renamed |
| 86 | `RADIO_TV_AD_FROM_DATE` | `RECR_OCC_RADIO_AD_FROM` | Renamed |
| 87 | `RADIO_TV_AD_TO_DATE` | `RECR_OCC_RADIO_AD_TO` | Renamed |

**Total: 87 direct/near-exact mappings** (covering ~90 old fields when counting split fields)

---

## 2. Fuzzy / Semantic Overlap Mappings (模糊相似部分)

Fields where the semantic meaning overlaps but the structure, granularity, or scope has changed significantly.

| # | Old Form Field(s) | New Form Field(s) | Relationship | Notes |
|---|---|---|---|---|
| 1 | `PROFESSIONAL_OCCUPATION` + `APP_FOR_COLLEGE_U_TEACHER` + `SCHD_A_SHEEPHERDER` | `OCCUPATION_TYPE` | Many→One | Old form used 3 separate Y/N flags; New form consolidated into single enum: "Professional occupation", "Non-professional", "College/University Teacher", "None/Professional Athlete", "Schedule A" |
| 2 | `BARGAINING_REP_NOTIFIED` + `POSTED_NOTICE_AT_WORKSITE` | `NOTICE_POST_BARGAIN_REP` + `NOTICE_POST_BARGAIN_REP_PHYSICAL` + `NOTICE_POST_BARGAIN_REP_ELECTRONIC` + `NOTICE_POST_BARGAIN_REP_INHOUSE` + `NOTICE_POST_BARGAIN_REP_PRIVATE` + `NOTICE_POST_EMP_NOT_POSTED` | 2→6 | Old form had 2 summary Y/N fields; New form breaks out into 6 granular notice-posting method fields |
| 3 | `SECOND_ADVERTISEMENT_TYPE` | `RECR_INFO_RECRUIT_AD_TYPE` | 1→1 | Old = "Newspaper or Journal"; New = "Newspaper of general circulation", "Professional journal", "N/A" (more specific enum values) |
| 4 | `ACCEPT_FOREIGN_EDUCATION` | `OTHER_REQ_ACCEPT_DIPLOMA_PWD` | 1→1 | Old = "accept foreign educational equivalent"; New = "accept foreign diploma/degree equivalent to PWD" — similar but new form ties it explicitly to the PWD |
| 5 | `FW_OWNERSHIP_INTEREST` (single field covers both ownership + familial) | `EMP_WORKER_INTEREST` + `EMP_RELATIONSHIP_WORKER` | 1→2 | Old form combined ownership interest and familial relationship into one Y/N; New form splits them into two separate fields |
| 6 | `OFFERED_TO_APPL_FOREIGN_WORKER` | (no direct equivalent) | Fuzzy | New form doesn't have this exact field, but `FW_INFO_APPX_A_ATTACHED` (Appendix A identifying foreign worker) partially covers the concept |
| 7 | `JOB_OPP_REQUIREMENTS_NORMAL` | `OTHER_REQ_JOB_REQ_EXCEED` | Fuzzy inverse | Old = "are requirements normal for occupation?"; New = "do requirements exceed SVP level?" — related but inverted logic, and new form uses SVP as the benchmark |
| 8 | `PAYMENT_DETAILS` | (subsumed into `OTHER_REQ_EMP_REC_PAYMENT`) | Partial | Old form had a separate text field for payment details; New form only has the Y/N flag |
| 9 | `EMPLOYER_COMPLETED_APPLICATION` + `PREPARER_NAME` + `PREPARER_TITLE` + `PREPARER_EMAIL` | `DECL_PREP_LAST_NAME` + `DECL_PREP_FIRST_NAME` + `DECL_PREP_MIDDLE_NAME` + `DECL_PREP_EMAIL` + `DECL_PREP_LAWFIRM_FEIN` + `DECL_PREP_FIRM_BUSINESS_NAME` | Restructured | Old form had preparer info + employer completed flag; New form restructured as declaration/preparer section with more detail (law firm FEIN, business name) but dropped preparer title and employer-completed flag |
| 10 | `EMP_INFO_DECL_NAME` + `EMP_DECL_TITLE` | `DECL_PREP_LAST_NAME` + `DECL_PREP_FIRST_NAME` + `DECL_PREP_MIDDLE_NAME` | Merged | Old had separate employer declaration signer fields; New form merged preparer and declaration signer into one section |
| 11 | `US_WORKERS_CONSIDERED` | (removed) | Partial | Related to layoff — old form asked if laid-off US workers were considered; new form only keeps the layoff flag (`OTHER_REQ_EMP_LAYOFF`) |
| 12 | `COMPETITIVE_PROCESS` + `BASIC_RECRUITMENT_PROCESS` + `TEACHER_SELECT_DATE` + `TEACHER_PUB_JOURNAL_NAME` + `ADD_RECRUIT_INFORMATION` | `RECR_INFO_RECRUIT_SUPERVISED_REQ` | Many→1(partial) | Old form had detailed teacher/competitive recruitment fields; New form has a single supervised recruitment flag. The teacher-specific details are gone. |
| 13 | `FOREIGN_WORKER_REQ_EXPERIENCE` | `OTHER_REQ_EMP_RELY_EXP` | Fuzzy | Old = "does FW have required experience?"; New = "is employer relying solely on FW's experience with them?" — related but different angle |

**Total: ~13 fuzzy mapping groups**

---

## 3. Fields Only in Old Form — No Equivalent in New Form (旧表独有)

These fields exist in the old schema but have **no counterpart** in the new form.

| # | Old Form Field | Category | Description |
|---|---|---|---|
| 1 | `REFILE` | Application History | Whether app was previously filed |
| 2 | `ORIG_FILE_DATE` | Application History | Original filing date |
| 3 | `PREVIOUS_SWA_CASE_NUMBER_STATE` | Application History | Original SWA case number/state |
| 4 | `PW_SKILL_LEVEL` | Prevailing Wage | Level I/II/III/IV — wage skill level |
| 5 | `PW_WAGE` | Prevailing Wage | Prevailing wage amount |
| 6 | `PW_UNIT_OF_PAY` | Prevailing Wage | PW unit of pay |
| 7 | `PW_WAGE_SOURCE` | Prevailing Wage | OES/CBA/Survey/etc. |
| 8 | `PW_SOURCE_NAME_OTHER` | Prevailing Wage | Other PW source name |
| 9 | `PW_DETERMINATION_DATE` | Prevailing Wage | PW decision date |
| 10 | `PW_EXPIRATION_DATE` | Prevailing Wage | PW expiration date |
| 11 | `MINIMUM_EDUCATION` | Job Requirements | Minimum education level |
| 12 | `JOB_EDUCATION_MIN_OTHER` | Job Requirements | Other education specification |
| 13 | `MAJOR_FIELD_OF_STUDY` | Job Requirements | Required major |
| 14 | `REQUIRED_TRAINING` | Job Requirements | Is training required? |
| 15 | `REQUIRED_TRAINING_MONTHS` | Job Requirements | Training months |
| 16 | `REQUIRED_FIELD_OF_TRAINING` | Job Requirements | Training field |
| 17 | `REQUIRED_EXPERIENCE` | Job Requirements | Is experience required? |
| 18 | `REQUIRED_EXPERIENCE_MONTHS` | Job Requirements | Experience months |
| 19 | `ACCEPT_ALT_FIELD_OF_STUDY` | Alt Requirements | Accept alt field of study? |
| 20 | `ACCEPT_ALT_MAJOR_FLD_OF_STUDY` | Alt Requirements | Alt major field |
| 21 | `ACCEPT_ALT_COMBO` | Alt Requirements | Accept alt education+experience combo? |
| 22 | `ACCEPT_ALT_COMBO_EDUCATION` | Alt Requirements | Alt combo education level |
| 23 | `ACCEPT_ALT_COMBO_ED_OTHER` | Alt Requirements | Alt combo other education |
| 24 | `ACCEPT_ALT_COMBO_EDUCATION_YRS` | Alt Requirements | Alt combo years |
| 25 | `ACCEPT_ALT_OCCUPATION` | Alt Requirements | Accept alt occupation? |
| 26 | `ACCEPT_ALT_OCCUPATION_MONTHS` | Alt Requirements | Alt occupation months |
| 27 | `ACCEPT_ALT_JOB_TITLE` | Alt Requirements | Alt job title |
| 28 | `SPECIFIC_SKILLS` | Job Requirements | Specific skills text |
| 29 | `COUNTRY_OF_CITIZENSHIP` | Foreign Worker PII | FW citizenship |
| 30 | `FOREIGN_WORKER_BIRTH_COUNTRY` | Foreign Worker PII | FW birth country |
| 31 | `CLASS_OF_ADMISSION` | Foreign Worker PII | FW visa status |
| 32 | `FOREIGN_WORKER_EDUCATION` | Foreign Worker Education | FW highest education |
| 33 | `FOREIGN_WORKER_EDUCATION_OTHER` | Foreign Worker Education | FW other education |
| 34 | `FOREIGN_WORKER_INFO_MAJOR` | Foreign Worker Education | FW major |
| 35 | `FOREIGN_WORKER_YRS_ED_COMP` | Foreign Worker Education | FW education completion year |
| 36 | `FOREIGN_WORKER_INST_OF_ED` | Foreign Worker Education | FW educational institution |
| 37 | `FOREIGN_WORKER_ED_INST_ADD_1` | Foreign Worker Education | FW institution address 1 |
| 38 | `FOREIGN_WORKER_ED_INST_ADD_2` | Foreign Worker Education | FW institution address 2 |
| 39 | `FOREIGN_WORKER_ED_INST_CITY` | Foreign Worker Education | FW institution city |
| 40 | `FOREIGN_WORKER_ED_INST_STATE_P` | Foreign Worker Education | FW institution state |
| 41 | `FOREIGN_WORKER_ED_INST_COUNTRY` | Foreign Worker Education | FW institution country |
| 42 | `FOREIGN_WORKER_ED_INST_POST_CD` | Foreign Worker Education | FW institution postal code |
| 43 | `FOREIGN_WORKER_TRAINING_COMP` | Foreign Worker Qualifications | FW completed training? |
| 44 | `FOREIGN_WORKER_ALT_ED_EXP` | Foreign Worker Qualifications | FW has alt education+experience? |
| 45 | `FOREIGN_WORKER_ALT_OCC_EXP` | Foreign Worker Qualifications | FW has alt occupation experience? |

**Total: 45 old-form-only fields**

Major categories lost:
- **Prevailing Wage details** (6 fields) — PW level, amount, source, dates all gone
- **Job education/experience requirements** (13 fields) — detailed min education, major, training, alt combos
- **Foreign Worker personal info** (3 fields) — citizenship, birth country, visa class
- **Foreign Worker education details** (10 fields) — institution, major, degree, address
- **Foreign Worker qualification flags** (3 fields) — training completion, alt experience
- **Application refile history** (3 fields)
- **Other** (7 fields) — specific skills, alt occupation details, etc.

---

## 4. Fields Only in New Form — No Equivalent in Old Form (新表独有)

| # | New Form Field | Category | Description |
|---|---|---|---|
| 1 | `EMP_TRADE_NAME` | Employer Info | Trade name (DBA) |
| 2 | `EMP_PROVINCE` | Employer Info | Province (added for non-US) |
| 3 | `EMP_RELATIONSHIP_WORKER` | Employer-Worker | Familial relationship (split from old ownership interest) |
| 4 | `EMP_POC_MIDDLE_NAME` | Employer Contact | POC middle name |
| 5 | `EMP_POC_JOB_TITLE` | Employer Contact | POC job title |
| 6 | `EMP_POC_PROVINCE` | Employer Contact | POC province |
| 7 | `EMP_POC_PHONEEXT` | Employer Contact | POC phone extension |
| 8 | `ATTY_AG_REP_TYPE` | Attorney/Agent | Attorney vs Agent vs None |
| 9 | `ATTY_AG_PROVINCE` | Attorney/Agent | Attorney province |
| 10 | `ATTY_AG_FEIN` | Attorney/Agent | Attorney FEIN |
| 11 | `ATTY_AG_STATE_BAR_NUMBER` | Attorney/Agent | State bar number |
| 12 | `ATTY_AG_GOOD_STANDING_STATE` | Attorney/Agent | Good standing state |
| 13 | `ATTY_AG_GOOD_STANDING_COURT` | Attorney/Agent | Good standing court |
| 14 | `FW_INFO_APPX_A_ATTACHED` | Foreign Worker | Appendix A attached? |
| 15 | `FW_INFO_ATTY_OR_AGENT` | Foreign Worker | Employer contracted with atty who also represents FW? |
| 16 | `JOB_OPP_PWD_ATTACHED` | Job Opportunity | PWD attached? |
| 17 | `JOB_OPP_WAGE_CONDITIONS` | Job Opportunity | Wage conditions text (bonuses, benefits, etc.) |
| 18 | `PRIMARY_WORKSITE_TYPE` | Worksite | Worksite type |
| 19 | `PRIMARY_WORKSITE_COUNTY` | Worksite | County |
| 20 | `PRIMARY_WORKSITE_BLS_AREA` | Worksite | MSA/OES area |
| 21 | `IS_MULTIPLE_LOCATIONS` | Worksite | Multiple work locations? |
| 22 | `IS_APPENDIX_B_ATTACHED` | Worksite | Appendix B attached? |
| 23 | `OTHER_REQ_IS_FULLTIME_EMP` | Job Requirements | Full-time position? |
| 24 | `OTHER_REQ_IS_PAID_EXPERIENCE` | Job Requirements | Live-in domestic: 1 year paid experience? |
| 25 | `OTHER_REQ_IS_EMP_PROVIDED_CONT` | Job Requirements | Employer provided contract to FW? |
| 26 | `OTHER_REQ_IS_FW_QUALIFY` | Job Requirements | FW qualifies only by alt requirements? |
| 27 | `OTHER_REQ_EMP_WILL_ACCEPT` | Job Requirements | Employer accepts any suitable combo? |
| 28 | `OTHER_REQ_EMP_RELY_EXP` | Job Requirements | Employer relying solely on FW experience? |
| 29 | `OTHER_REQ_JOB_REQ_EXCEED` | Job Requirements | Requirements exceed SVP? |
| 30 | `OTHER_REQ_EMP_USE_CREDENTIAL` | Job Requirements | Credentialing service used? |
| 31 | `RECR_INFO_RECRUIT_SUPERVISED_REQ` | Recruitment | Supervised recruitment required? |
| 32 | `RECR_INFO_RECRUIT_AD_TYPE` | Recruitment | Ad type (newspaper/journal/N/A) |
| 33 | `NOTICE_POST_BARGAIN_REP` | Notice/Posting | Bargaining rep notified |
| 34 | `NOTICE_POST_BARGAIN_REP_PHYSICAL` | Notice/Posting | Physical posting |
| 35 | `NOTICE_POST_BARGAIN_REP_ELECTRONIC` | Notice/Posting | Electronic dissemination |
| 36 | `NOTICE_POST_BARGAIN_REP_INHOUSE` | Notice/Posting | In-house media |
| 37 | `NOTICE_POST_BARGAIN_REP_PRIVATE` | Notice/Posting | Private household posting |
| 38 | `NOTICE_POST_EMP_NOT_POSTED` | Notice/Posting | Employer did NOT post |
| 39 | `EMP_CERTIFY_COMPLIANCE` | Compliance | Employer certifies compliance |
| 40 | `DECL_PREP_MIDDLE_NAME` | Declaration | Preparer middle name |
| 41 | `DECL_PREP_LAWFIRM_FEIN` | Declaration | Law firm FEIN |
| 42 | `DECL_PREP_FIRM_BUSINESS_NAME` | Declaration | Firm business name |

**Total: 42 new-form-only fields**

Major categories gained:
- **Attorney/Agent detail** (6 fields) — FEIN, bar number, good standing, rep type
- **Worksite enhancements** (4 fields) — county, BLS area, type, multiple locations
- **Notice posting granularity** (6 fields) — physical/electronic/in-house/private/not-posted
- **New compliance/qualification flags** (7 fields) — full-time, SVP exceed, credentialing, etc.
- **Foreign Worker info restructured** (2 fields) — Appendix A attached, atty conflict
- **Wage conditions** (1 field) — detailed description of compensation
- **Province fields** (3 fields) — for non-US addresses

---

## Summary Statistics

| Category | Count |
|---|---|
| **1. Direct/Near-Exact Mappings** | **87 field pairs** (covering ~90 old + ~95 new fields) |
| **2. Fuzzy/Semantic Overlap** | **13 mapping groups** (covering ~25 old + ~15 new fields) |
| **3a. Old Form Only (no new equivalent)** | **45 fields** |
| **3b. New Form Only (no old equivalent)** | **42 fields** |

### Key Takeaways

1. **~57% of old form fields** have a direct 1:1 mapping to the new form (just renamed)
2. **~16% of old form fields** have fuzzy/restructured counterparts in the new form
3. **~27% of old form fields** are completely gone in the new form (mainly FW personal info + detailed job requirements + PW details)
4. The new form adds **42 entirely new fields** mostly around attorney credentials, worksite detail, compliance, and notice posting granularity
5. The **biggest data loss** in the new form is the removal of all Foreign Worker personal/education data and detailed prevailing wage information — these were moved to Appendix A (not publicly disclosed) or the separate ETA-9141 form
