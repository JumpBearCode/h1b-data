# Refined Schema for H1B Data Product

## Background

### h1bdata.info 竞品分析

h1bdata.info 展示的数据列非常简洁，只有 **6 个字段**：

| 列名 | 对应原始字段 |
|------|-------------|
| EMPLOYER | `EMPLOYER_NAME` |
| JOB TITLE | `JOB_TITLE` |
| BASE SALARY | `WAGE_RATE_OF_PAY_FROM` (年化后) |
| LOCATION | `WORKSITE_CITY` + `WORKSITE_STATE` |
| SUBMIT DATE | `RECEIVED_DATE` |
| START DATE | `BEGIN_DATE` |

**h1bdata.info 提供的聚合功能**：
- 按公司/职位/城市搜索
- 中位数薪资 (Median Salary)
- 薪资分布 (例: 21% > $200K, 71% $150K-$200K)
- 按公司、职位、城市维度的 "Highest Paid" 排行

**h1bdata.info 的不足 / 我们的差异化机会**：
- 没有 cap-exempt / 免抽签信息
- 没有 H-1B Dependent 雇主标记
- 没有 petition type 区分（new vs. transfer vs. amendment）
- 没有 prevailing wage 对比（无法判断公司给的工资相对市场水平如何）
- 没有 denial rate / case status 统计
- 没有 NAICS 行业分类

---

## 我们的目标 Business Questions

| # | Business Question | 需要的字段 |
|---|------------------|-----------|
| 1 | 某公司在某地区申请了多少 H1B？ | `EMPLOYER_NAME`, `WORKSITE_CITY`, `WORKSITE_STATE`, count |
| 1b | 某公司总部在哪里？ | `EMPLOYER_CITY`, `EMPLOYER_STATE` |
| 1c | 哪些公司总部在 A 州但把员工派到 B 州工作？ | `EMPLOYER_STATE` vs `WORKSITE_STATE` |
| 2 | 他们的工资是怎样的？（中位数、范围、分布） | `WAGE_RATE_OF_PAY_FROM`, `WAGE_RATE_OF_PAY_TO`, `WAGE_UNIT_OF_PAY` |
| 3 | H1B 支不支持免抽签（cap-exempt）？ | `SUPPORT_H1B`, `H-1B_DEPENDENT`, `STATUTORY_BASIS` |
| 4 | 该公司的 H1B 通过率如何？ | `CASE_STATUS`, `EMPLOYER_NAME` |
| 5 | 是 new hire 还是 transfer / amendment？ | `NEW_EMPLOYMENT`, `CONTINUED_EMPLOYMENT`, `CHANGE_EMPLOYER`, `AMENDED_PETITION` |
| 6 | 公司给的工资 vs 市场 prevailing wage 差多少？ | `WAGE_RATE_OF_PAY_FROM`, `PREVAILING_WAGE`, `PW_WAGE_LEVEL` |
| 7 | 哪些行业/公司是 H-1B Dependent？ | `H-1B_DEPENDENT`, `NAICS_CODE`, `EMPLOYER_NAME` |
| 8 | 某个 SOC 职业在不同城市的薪资对比？ | `SOC_CODE`, `SOC_TITLE`, `WORKSITE_CITY`, `WORKSITE_STATE`, `WAGE_RATE_OF_PAY_FROM` |
| 9 | 某公司是否曾经有 willful violation？ | `WILLFUL_VIOLATOR`, `EMPLOYER_NAME` |
| 10 | 某公司的 H1B 申请趋势（按年）？ | `EMPLOYER_NAME`, `FISCAL_YEAR`, count |
| 11 | 是否有第三方派遣（outsourcing / staffing）？ | `SECONDARY_ENTITY`, `SECONDARY_ENTITY_BUSINESS_NAME` |
| 12 | Full-time vs Part-time 分布？ | `FULL_TIME_POSITION` |

---

## Refined Schema: 32 Columns

从原始 98 列中精选 32 列，分为 **核心展示字段** 和 **分析/筛选字段**。

### A. 核心展示字段（用户直接看到的）

这些字段对标 h1bdata.info，是搜索结果表格里直接展示的。

| # | Column Name | Type | 说明 |
|---|-------------|------|------|
| 1 | `CASE_NUMBER` | VARCHAR | 主键，唯一标识 |
| 2 | `EMPLOYER_NAME` | VARCHAR | 雇主名称（搜索 & 展示核心） |
| 3 | `JOB_TITLE` | VARCHAR | 职位名称（搜索 & 展示核心） |
| 4 | `EMPLOYER_CITY` | VARCHAR | 雇主所在城市（公司总部/注册地） |
| 5 | `EMPLOYER_STATE` | VARCHAR | 雇主所在州（公司总部/注册地） |
| 6 | `WORKSITE_CITY` | VARCHAR | 实际工作城市（员工上班地点） |
| 7 | `WORKSITE_STATE` | VARCHAR | 实际工作州（员工上班地点） |
| 8 | `WAGE_RATE_OF_PAY_FROM` | DECIMAL | 工资下限 |
| 9 | `WAGE_RATE_OF_PAY_TO` | DECIMAL | 工资上限（NULL = 固定薪资） |
| 10 | `WAGE_UNIT_OF_PAY` | VARCHAR | 工资单位（Hour/Week/Month/Year），年化计算需要 |
| 11 | `RECEIVED_DATE` | DATE | 提交日期 |
| 12 | `BEGIN_DATE` | DATE | 工作开始日期 |
| 13 | `CASE_STATUS` | VARCHAR | 审批状态（Certified / Denied / Withdrawn 等） |
| 14 | `FISCAL_YEAR` | INTEGER | 财年（ETL 生成） |

### B. 差异化分析字段（超越 h1bdata.info 的竞争力）

这些字段是 h1bdata.info **没有** 的，是我们产品的核心差异化。

| # | Column Name | Type | 说明 | 回答的问题 |
|---|-------------|------|------|-----------|
| 15 | `VISA_CLASS` | VARCHAR | 签证类型 (H-1B / E-3 / H-1B1) | 区分签证类别 |
| 16 | `SOC_CODE` | VARCHAR | 标准职业分类代码 | 跨公司、跨地区的职业对比 |
| 17 | `SOC_TITLE` | VARCHAR | 标准职业名称 | 职业标准化（JOB_TITLE 太自由） |
| 18 | `FULL_TIME_POSITION` | VARCHAR(1) | 全职/兼职 (Y/N) | Full-time vs Part-time 分析 |
| 19 | `TOTAL_WORKER_POSITIONS` | INTEGER | 该申请涵盖的工人数 | 某公司实际招多少人 |
| 20 | `NEW_EMPLOYMENT` | INTEGER | 新雇佣人数 | 区分 new hire vs transfer |
| 21 | `CONTINUED_EMPLOYMENT` | INTEGER | 续签人数 | 区分 extension |
| 22 | `CHANGE_EMPLOYER` | INTEGER | 换雇主人数 | 区分 transfer |
| 23 | `AMENDED_PETITION` | INTEGER | 修改申请人数 | 区分 amendment |
| 24 | `PREVAILING_WAGE` | DECIMAL | 该地区该职位的市场标准工资 | 公司工资 vs 市场水平 |
| 25 | `PW_UNIT_OF_PAY` | VARCHAR | Prevailing wage 单位 | 年化计算需要 |
| 26 | `PW_WAGE_LEVEL` | VARCHAR | 工资等级 (I/II/III/IV) | Level I=入门, IV=资深，反映职位资历 |
| 27 | `H-1B_DEPENDENT` | VARCHAR(1) | 是否 H-1B Dependent 雇主 (Y/N) | 识别高度依赖 H1B 的公司 |
| 28 | `WILLFUL_VIOLATOR` | VARCHAR(1) | 是否有过故意违规 (Y/N) | 雇主合规风险 |
| 29 | `SUPPORT_H1B` | VARCHAR | 是否仅支持免抽签 H1B (Y/N/N/A) | **核心差异化**: 判断 cap-exempt |
| 30 | `STATUTORY_BASIS` | VARCHAR | 免抽签依据 (Wage/Degree/Both) | 免抽签是因为薪资还是学历 |
| 31 | `NAICS_CODE` | VARCHAR | 行业分类代码 | 按行业分析 H1B 趋势 |
| 32 | `SECONDARY_ENTITY` | VARCHAR(1) | 是否第三方派遣 (Y/N) | 识别 staffing/outsourcing |

### C. 砍掉的字段（66 列）及理由

| 砍掉的类别 | 列数 | 理由 |
|-----------|------|------|
| Employer POC 联系人 (33-46) | 14 | 个人联系信息，对终端用户无分析价值 |
| Agent/Attorney 信息 (47-60) | 14 | 律师联系方式，非核心业务问题 |
| Preparer 信息 (94-98) | 5 | 表格填写人信息，无分析价值 |
| Employer 详细地址 (22-23, 26-28, 30) | 5 | 保留了 CITY/STATE，砍掉 ADDRESS1/2, POSTAL_CODE, COUNTRY, PROVINCE |
| Law Firm 信息 (61-64) | 4 | 律所名称/FEIN/法院信息，非核心 |
| Worksite 详细地址 (68-69, 73) | 3 | 只保留 city/state，详细街道无需 |
| PW 详细来源 (79, 82-85) | 5 | Prevailing wage 追踪号和调查来源，太细节 |
| 合规声明 & 披露 (87, 92-93) | 3 | 几乎所有记录都是 Y，无分析价值 |
| 其他低价值 (21, 29, 31, 62, 71, 75, 81, 86 等) | 13 | TRADE_NAME_DBA / EMPLOYER_PHONE / EMPLOYER_FEIN 等 |

> **注意**: `WORKSITE_COUNTY` (col 71) 和 `END_DATE` (col 12) 作为候选保留项，如果未来需要更细粒度的地理分析或签证有效期分析可以加回。

---

## 年化工资计算逻辑

h1bdata.info 只展示一个 "BASE SALARY" 数字，实际上需要根据 `WAGE_UNIT_OF_PAY` 做年化转换：

```
annualized_salary = CASE WAGE_UNIT_OF_PAY
  WHEN 'Year'     THEN WAGE_RATE_OF_PAY_FROM
  WHEN 'Month'    THEN WAGE_RATE_OF_PAY_FROM * 12
  WHEN 'Bi-Weekly' THEN WAGE_RATE_OF_PAY_FROM * 26
  WHEN 'Week'     THEN WAGE_RATE_OF_PAY_FROM * 52
  WHEN 'Hour'     THEN WAGE_RATE_OF_PAY_FROM * 2080
END
```

同理对 `PREVAILING_WAGE` 也需做年化处理，以便与 offered wage 对比。

---

## Cap-Exempt（免抽签）判断逻辑

这是我们相对 h1bdata.info 的**最大差异化**。LCA 数据中没有直接的 "cap-exempt" 字段，但可以通过以下组合推断：

| 字段 | 值 | 含义 |
|------|-----|------|
| `SUPPORT_H1B` = `Y` | 仅支持免抽签工人 | 该 LCA 仅用于 cap-exempt petition |
| `H-1B_DEPENDENT` = `Y` | H-1B Dependent 雇主 | 雇主高度依赖 H1B，有额外合规义务 |
| `STATUTORY_BASIS` = `Wage` | 年薪 ≥ $60K | 免抽签依据是高薪 |
| `STATUTORY_BASIS` = `Degree` | 硕士及以上 | 免抽签依据是学历 |
| `STATUTORY_BASIS` = `Both` | 两者都满足 | 同时满足薪资和学历 |

> **重要**: `SUPPORT_H1B` 和 `STATUTORY_BASIS` 主要针对 H-1B Dependent / Willful Violator 雇主的合规声明。真正的 cap-exempt（如大学、非营利研究机构）需要结合 `NAICS_CODE` 和 `EMPLOYER_NAME` 来识别（例如 NAICS 6113xx = 大学）。

---

## 建议的衍生字段（在 processed 层计算）

在 ETL 的 processed 层，建议额外计算以下衍生字段：

| 衍生字段 | 计算逻辑 | 用途 |
|---------|---------|------|
| `ANNUALIZED_WAGE_FROM` | 根据 `WAGE_UNIT_OF_PAY` 年化 | 统一对比薪资 |
| `ANNUALIZED_WAGE_TO` | 同上 | 薪资范围上限 |
| `ANNUALIZED_PREVAILING_WAGE` | 根据 `PW_UNIT_OF_PAY` 年化 | 统一对比 prevailing wage |
| `WAGE_VS_PREVAILING_PCT` | `(ANNUALIZED_WAGE_FROM / ANNUALIZED_PREVAILING_WAGE - 1) * 100` | 工资高于/低于市场水平的百分比 |
| `PETITION_TYPE` | 根据 NEW_EMPLOYMENT / CHANGE_EMPLOYER / CONTINUED / AMENDED 推断 | 简化为 "New" / "Transfer" / "Extension" / "Amendment" |
| `IS_LIKELY_CAP_EXEMPT` | 根据 NAICS_CODE + EMPLOYER_NAME 推断 | 是否可能是免抽签雇主（大学、非营利等） |

---

## 总结

| 维度 | h1bdata.info | 我们的产品 |
|------|-------------|-----------|
| 字段数 | 6 | 32 + 6 衍生字段 |
| 工资分析 | 只有 base salary | 工资 + prevailing wage + 差值百分比 + 工资等级 |
| 免抽签分析 | 无 | SUPPORT_H1B + STATUTORY_BASIS + NAICS 推断 |
| 申请类型 | 无 | New / Transfer / Extension / Amendment |
| 审批状态 | 无 | Certified / Denied / Withdrawn 统计 |
| 行业分析 | 无 | NAICS 行业代码 |
| H-1B Dependent | 无 | 标记高度依赖 H1B 的雇主 |
| 合规风险 | 无 | Willful Violator 标记 |
| 第三方派遣 | 无 | Secondary Entity 标记 |
| 雇主地理 | 无 | EMPLOYER_CITY/STATE（公司总部 vs 工作地点对比） |
| 搜索维度 | 公司 / 职位 / 城市 / 年份 | 公司 / 职位 / 城市 / 年份 / SOC / 行业 / 签证类型 / 雇主所在地 |

---

## Appendix A: 完整保留字段清单 (32 columns)

以下是从原始 99 列（98 原始 + 1 ETL）中保留的 32 列完整清单。

| # | Column Name | 原始序号 | Type | 分类 |
|---|-------------|---------|------|------|
| 1 | `CASE_NUMBER` | 1 | VARCHAR | 核心展示 |
| 2 | `EMPLOYER_NAME` | 20 | VARCHAR | 核心展示 |
| 3 | `JOB_TITLE` | 7 | VARCHAR | 核心展示 |
| 4 | `EMPLOYER_CITY` | 24 | VARCHAR | 核心展示 |
| 5 | `EMPLOYER_STATE` | 25 | VARCHAR | 核心展示 |
| 6 | `WORKSITE_CITY` | 70 | VARCHAR | 核心展示 |
| 7 | `WORKSITE_STATE` | 72 | VARCHAR | 核心展示 |
| 8 | `WAGE_RATE_OF_PAY_FROM` | 74 | DECIMAL | 核心展示 |
| 9 | `WAGE_RATE_OF_PAY_TO` | 75 | DECIMAL | 核心展示 |
| 10 | `WAGE_UNIT_OF_PAY` | 76 | VARCHAR | 核心展示 |
| 11 | `RECEIVED_DATE` | 3 | DATE | 核心展示 |
| 12 | `BEGIN_DATE` | 11 | DATE | 核心展示 |
| 13 | `CASE_STATUS` | 2 | VARCHAR | 核心展示 |
| 14 | `FISCAL_YEAR` | 99 (ETL) | INTEGER | 核心展示 |
| 15 | `VISA_CLASS` | 6 | VARCHAR | 差异化分析 |
| 16 | `SOC_CODE` | 8 | VARCHAR | 差异化分析 |
| 17 | `SOC_TITLE` | 9 | VARCHAR | 差异化分析 |
| 18 | `FULL_TIME_POSITION` | 10 | VARCHAR(1) | 差异化分析 |
| 19 | `TOTAL_WORKER_POSITIONS` | 13 | INTEGER | 差异化分析 |
| 20 | `NEW_EMPLOYMENT` | 14 | INTEGER | 差异化分析 |
| 21 | `CONTINUED_EMPLOYMENT` | 15 | INTEGER | 差异化分析 |
| 22 | `CHANGE_EMPLOYER` | 18 | INTEGER | 差异化分析 |
| 23 | `AMENDED_PETITION` | 19 | INTEGER | 差异化分析 |
| 24 | `PREVAILING_WAGE` | 77 | DECIMAL | 差异化分析 |
| 25 | `PW_UNIT_OF_PAY` | 78 | VARCHAR | 差异化分析 |
| 26 | `PW_WAGE_LEVEL` | 80 | VARCHAR | 差异化分析 |
| 27 | `H-1B_DEPENDENT` | 88 | VARCHAR(1) | 差异化分析 |
| 28 | `WILLFUL_VIOLATOR` | 89 | VARCHAR(1) | 差异化分析 |
| 29 | `SUPPORT_H1B` | 90 | VARCHAR | 差异化分析 |
| 30 | `STATUTORY_BASIS` | 91 | VARCHAR | 差异化分析 |
| 31 | `NAICS_CODE` | 32 | VARCHAR | 差异化分析 |
| 32 | `SECONDARY_ENTITY` | 66 | VARCHAR(1) | 差异化分析 |

---

## Appendix B: 完整排除字段清单 (67 columns)

以下是被排除的 67 列，按原始 schema 分组，附排除理由。

### Case Information（排除 3 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 4 | `DECISION_DATE` | 审批决定日期，有 CASE_STATUS 足够；可作为候选保留项 |
| 5 | `ORIGINAL_CERT_DATE` | 仅对 Certified-Withdrawn 有值，绝大部分为 NULL |
| 12 | `END_DATE` | 候选保留项，暂不纳入；如需分析签证有效期可加回 |

### Worker Counts（排除 2 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 16 | `CHANGE_PREVIOUS_EMPLOYMENT` | 细分类型，与 CONTINUED_EMPLOYMENT 重叠，使用频率低 |
| 17 | `NEW_CONCURRENT_EMPLOYMENT` | 并发雇佣，属于边缘场景，使用频率低 |

### Employer Information（排除 7 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 21 | `TRADE_NAME_DBA` | DBA 名称，绝大部分为 NULL，有 EMPLOYER_NAME 足够 |
| 22 | `EMPLOYER_ADDRESS1` | 详细街道地址，粒度太细，保留了 CITY/STATE |
| 23 | `EMPLOYER_ADDRESS2` | 地址第二行，绝大部分为 NULL |
| 26 | `EMPLOYER_POSTAL_CODE` | 邮编，有 CITY/STATE 足够定位 |
| 27 | `EMPLOYER_COUNTRY` | 几乎全部为 "UNITED STATES OF AMERICA"，信息量低 |
| 28 | `EMPLOYER_PROVINCE` | 仅非美国雇主有值，极少数记录 |
| 29 | `EMPLOYER_PHONE` | 电话号码，对终端用户无分析价值 |
| 30 | `EMPLOYER_PHONE_EXT` | 分机号，对终端用户无分析价值 |
| 31 | `EMPLOYER_FEIN` | 联邦雇主识别号（PII），FY2024 Q4 前全部为 NULL |

### Employer POC（排除 14 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 33 | `EMPLOYER_POC_LAST_NAME` | 个人联系信息，无分析价值 |
| 34 | `EMPLOYER_POC_FIRST_NAME` | 同上 |
| 35 | `EMPLOYER_POC_MIDDLE_NAME` | 同上 |
| 36 | `EMPLOYER_POC_JOB_TITLE` | 同上 |
| 37 | `EMPLOYER_POC_ADDRESS1` | 同上 |
| 38 | `EMPLOYER_POC_ADDRESS2` | 同上 |
| 39 | `EMPLOYER_POC_CITY` | 同上 |
| 40 | `EMPLOYER_POC_STATE` | 同上 |
| 41 | `EMPLOYER_POC_POSTAL_CODE` | 同上 |
| 42 | `EMPLOYER_POC_COUNTRY` | 同上 |
| 43 | `EMPLOYER_POC_PROVINCE` | 同上 |
| 44 | `EMPLOYER_POC_PHONE` | 同上 |
| 45 | `EMPLOYER_POC_PHONE_EXT` | 同上 |
| 46 | `EMPLOYER_POC_EMAIL` | 同上 |

### Agent / Attorney（排除 14 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 47 | `AGENT_REPRESENTING_EMPLOYER` | 律师/代理相关，非核心业务问题 |
| 48 | `AGENT_ATTORNEY_LAST_NAME` | 同上 |
| 49 | `AGENT_ATTORNEY_FIRST_NAME` | 同上 |
| 50 | `AGENT_ATTORNEY_MIDDLE_NAME` | 同上 |
| 51 | `AGENT_ATTORNEY_ADDRESS1` | 同上 |
| 52 | `AGENT_ATTORNEY_ADDRESS2` | 同上 |
| 53 | `AGENT_ATTORNEY_CITY` | 同上 |
| 54 | `AGENT_ATTORNEY_STATE` | 同上 |
| 55 | `AGENT_ATTORNEY_POSTAL_CODE` | 同上 |
| 56 | `AGENT_ATTORNEY_COUNTRY` | 同上 |
| 57 | `AGENT_ATTORNEY_PROVINCE` | 同上 |
| 58 | `AGENT_ATTORNEY_PHONE` | 同上 |
| 59 | `AGENT_ATTORNEY_PHONE_EXT` | 同上 |
| 60 | `AGENT_ATTORNEY_EMAIL_ADDRESS` | 同上 |

### Law Firm & Court（排除 4 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 61 | `LAWFIRM_NAME_BUSINESS_NAME` | 律所名称，非核心分析维度 |
| 62 | `LAWFIRM_BUSINESS_FEIN` | 律所 FEIN，FY2025 Q4 前全部为 NULL |
| 63 | `STATE_OF_HIGHEST_COURT` | 律师执照信息，无分析价值 |
| 64 | `NAME_OF_HIGHEST_STATE_COURT` | 同上 |

### Worksite Information（排除 4 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 65 | `WORKSITE_WORKERS` | 第一工作地点的工人数，有 TOTAL_WORKER_POSITIONS 足够 |
| 67 | `SECONDARY_ENTITY_BUSINESS_NAME` | 第三方公司名称，有 SECONDARY_ENTITY (Y/N) 足够判断；候选保留项 |
| 68 | `WORKSITE_ADDRESS1` | 详细街道地址，保留了 CITY/STATE |
| 69 | `WORKSITE_ADDRESS2` | 地址第二行 |
| 71 | `WORKSITE_COUNTY` | 候选保留项，如需 county 级别地理分析可加回 |
| 73 | `WORKSITE_POSTAL_CODE` | 邮编，有 CITY/STATE 足够 |

### Wage - PW Details（排除 6 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 79 | `PW_TRACKING_NUMBER` | DOL 内部追踪号，无分析价值 |
| 81 | `PW_OES_YEAR` | OES 调查年份，太细节 |
| 82 | `PW_OTHER_SOURCE` | 替代工资来源类型，太细节 |
| 83 | `PW_OTHER_YEAR` | 替代来源年份，太细节 |
| 84 | `PW_SURVEY_PUBLISHER` | 调查出版商，太细节 |
| 85 | `PW_SURVEY_NAME` | 调查名称，太细节 |

### Compliance & Disclosure（排除 4 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 86 | `TOTAL_WORKSITE_LOCATIONS` | 总工作地点数，边缘信息 |
| 87 | `AGREE_TO_LC_STATEMENT` | 几乎所有记录都是 Y，无信息量 |
| 92 | `APPENDIX_A_ATTACHED` | 是否有附件 A，与分析无关 |
| 93 | `PUBLIC_DISCLOSURE` | 披露方式，几乎所有值相同 |

### Preparer Information（排除 5 列）

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 94 | `PREPARER_LAST_NAME` | 表格填写人信息，无分析价值 |
| 95 | `PREPARER_FIRST_NAME` | 同上 |
| 96 | `PREPARER_MIDDLE_INITIAL` | 同上 |
| 97 | `PREPARER_BUSINESS_NAME` | 同上 |
| 98 | `PREPARER_EMAIL` | 同上 |

---

### 排除字段统计

| 分类 | 排除列数 |
|------|---------|
| Case Information | 3 |
| Worker Counts | 2 |
| Employer Information | 9 |
| Employer POC | 14 |
| Agent / Attorney | 14 |
| Law Firm & Court | 4 |
| Worksite Information | 6 |
| Wage - PW Details | 6 |
| Compliance & Disclosure | 4 |
| Preparer Information | 5 |
| **总计** | **67** |

> **保留 32 列 + 排除 67 列 = 99 列**（原始 98 列 + 1 ETL 列 `FISCAL_YEAR`）
