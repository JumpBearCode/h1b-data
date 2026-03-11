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

## Refined Schema: 38 Columns

从原始 98 列中精选并合并为 38 列，分为 **核心展示字段** 和 **分析/筛选字段**。

### 合并字段说明

为了保持 38 列不变同时加入雇主地址信息，对以下字段做了合并：

| 合并操作 | 原始字段 | 合并后字段 | 合并逻辑 |
|---------|---------|-----------|---------|
| 地址合并 | `EMPLOYER_ADDRESS1` + `EMPLOYER_ADDRESS2` | `EMPLOYER_ADDRESS` | `CONCAT_WS(', ', addr1, addr2)`，忽略空值 |
| 联系人姓名合并 | `EMPLOYER_POC_FIRST_NAME` + `EMPLOYER_POC_LAST_NAME` | `EMPLOYER_POC_NAME` | `CONCAT_WS(' ', first, last)`，忽略空值 |

同时新增了 `EMPLOYER_POSTAL_CODE`（邮编），砍掉了 `EMPLOYER_POC_PHONE`（联系人电话）。

### A. 核心展示字段（用户直接看到的）— 16 列

这些字段对标 h1bdata.info，是搜索结果表格里直接展示的。

| # | Column Name | Type | 说明 |
|---|-------------|------|------|
| 1 | `CASE_NUMBER` | TEXT | 主键，唯一标识 |
| 2 | `EMPLOYER_NAME` | TEXT | 雇主名称（搜索 & 展示核心） |
| 3 | `JOB_TITLE` | TEXT | 职位名称（搜索 & 展示核心） |
| 4 | `EMPLOYER_ADDRESS` | TEXT | 雇主地址（合并 ADDRESS1 + ADDRESS2） |
| 5 | `EMPLOYER_CITY` | TEXT | 雇主所在城市（公司总部/注册地） |
| 6 | `EMPLOYER_STATE` | TEXT | 雇主所在州（公司总部/注册地） |
| 7 | `EMPLOYER_POSTAL_CODE` | TEXT | 雇主邮编 |
| 8 | `WORKSITE_CITY` | TEXT | 实际工作城市（员工上班地点） |
| 9 | `WORKSITE_STATE` | TEXT | 实际工作州（员工上班地点） |
| 10 | `WAGE_RATE_OF_PAY_FROM` | NUMERIC | 工资下限 |
| 11 | `WAGE_RATE_OF_PAY_TO` | NUMERIC | 工资上限（NULL = 固定薪资） |
| 12 | `WAGE_UNIT_OF_PAY` | TEXT | 工资单位（Hour/Week/Month/Year），年化计算需要 |
| 13 | `RECEIVED_DATE` | DATE | 提交日期 |
| 14 | `BEGIN_DATE` | DATE | 工作开始日期 |
| 15 | `CASE_STATUS` | TEXT | 审批状态（Certified / Denied / Withdrawn 等） |
| 16 | `FISCAL_YEAR` | INTEGER | 财年（ETL 生成） |

### B. 差异化分析字段（超越 h1bdata.info 的竞争力）— 22 列

这些字段是 h1bdata.info **没有** 的，是我们产品的核心差异化。

| # | Column Name | Type | 说明 | 回答的问题 |
|---|-------------|------|------|-----------|
| 17 | `VISA_CLASS` | TEXT | 签证类型 (H-1B / E-3 / H-1B1) | 区分签证类别 |
| 18 | `SOC_CODE` | TEXT | 标准职业分类代码 | 跨公司、跨地区的职业对比 |
| 19 | `SOC_TITLE` | TEXT | 标准职业名称 | 职业标准化（JOB_TITLE 太自由） |
| 20 | `FULL_TIME_POSITION` | TEXT | 全职/兼职 (Y/N) | Full-time vs Part-time 分析 |
| 21 | `TOTAL_WORKER_POSITIONS` | INTEGER | 该申请涵盖的工人数 | 某公司实际招多少人 |
| 22 | `NEW_EMPLOYMENT` | TEXT | 新雇佣人数 | 区分 new hire vs transfer |
| 23 | `CONTINUED_EMPLOYMENT` | TEXT | 续签人数 | 区分 extension |
| 24 | `CHANGE_EMPLOYER` | TEXT | 换雇主人数 | 区分 transfer |
| 25 | `AMENDED_PETITION` | TEXT | 修改申请人数 | 区分 amendment |
| 26 | `PREVAILING_WAGE` | NUMERIC | 该地区该职位的市场标准工资 | 公司工资 vs 市场水平 |
| 27 | `PW_UNIT_OF_PAY` | TEXT | Prevailing wage 单位 | 年化计算需要 |
| 28 | `PW_WAGE_LEVEL` | TEXT | 工资等级 (I/II/III/IV) | Level I=入门, IV=资深，反映职位资历 |
| 29 | `H1B_DEPENDENT` | TEXT | 是否 H-1B Dependent 雇主 (Y/N) | 识别高度依赖 H1B 的公司 |
| 30 | `WILLFUL_VIOLATOR` | TEXT | 是否有过故意违规 (Y/N) | 雇主合规风险 |
| 31 | `SUPPORT_H1B` | TEXT | 是否仅支持免抽签 H1B (Y/N/N/A) | **核心差异化**: 判断 cap-exempt |
| 32 | `STATUTORY_BASIS` | TEXT | 免抽签依据 (Wage/Degree/Both) | 免抽签是因为薪资还是学历 |
| 33 | `NAICS_CODE` | TEXT | 行业分类代码 | 按行业分析 H1B 趋势 |
| 34 | `SECONDARY_ENTITY` | TEXT | 是否第三方派遣 (Y/N) | 识别 staffing/outsourcing |
| 35 | `LAWFIRM_NAME_BUSINESS_NAME` | TEXT | 代理律所名称 | 哪些律所在帮哪些公司办 H1B |
| 36 | `EMPLOYER_POC_NAME` | TEXT | 雇主联系人姓名（合并 FIRST + LAST） | 雇主联系人信息 |
| 37 | `EMPLOYER_POC_JOB_TITLE` | TEXT | 雇主联系人职位 | 联系人角色（HR / Legal 等） |
| 38 | `EMPLOYER_POC_EMAIL` | TEXT | 雇主联系人邮箱 | 联系渠道 |

### C. 附加表

除了每个 fiscal year 一张表（`refined.fy2020` ~ `refined.fy2026`），还有两张附加表：

#### `refined.fy_all` — 全量表

所有 fiscal year 的 UNION ALL，用于跨年分析：
- **3,514,878 行**（= 所有 FY 表的总和）
- 同一个 case_number 可能出现在多个 fiscal year 中（跨年 LCA 正常现象）
- 3,412,794 个 distinct case_number，102,084 个跨年重复

#### `refined.employers` — 雇主维度表

从 `fy_all` 聚合得到的雇主维度表，每个 employer_name 一行：

| Column | Type | 说明 |
|--------|------|------|
| `employer_name` | TEXT | 雇主名称（主键） |
| `employer_address` | TEXT | 最新地址 |
| `employer_city` | TEXT | 最新城市 |
| `employer_state` | TEXT | 最新州 |
| `employer_postal_code` | TEXT | 最新邮编 |
| `naics_code` | TEXT | 最新 NAICS 行业代码 |
| `h1b_dependent` | TEXT | 最新 H-1B Dependent 标记 |
| `willful_violator` | TEXT | 最新 Willful Violator 标记 |
| `total_applications` | INTEGER | 总申请数（跨所有年份） |
| `first_seen_year` | INTEGER | 最早出现的 fiscal year |
| `last_seen_year` | INTEGER | 最近出现的 fiscal year |

**统计**：214,366 个唯一雇主，Top 10 申请量最大的雇主：

| 雇主 | 总部 | 总申请数 |
|------|------|---------|
| COGNIZANT TECHNOLOGY SOLUTIONS US CORP | College Station, TX | 92,357 |
| Amazon.com Services LLC | Seattle, WA | 60,910 |
| Ernst & Young U.S. LLP | Secaucus, NJ | 57,336 |
| Google LLC | Mountain View, CA | 56,672 |
| Microsoft Corporation | Redmond, WA | 54,619 |
| INFOSYS LIMITED | Richardson, TX | 42,545 |
| TATA CONSULTANCY SERVICES LIMITED | Rockville, MD | 38,159 |
| Apple Inc. | Cupertino, CA | 29,147 |
| Accenture LLP | Chicago, IL | 22,672 |
| Deloitte Consulting LLP | Philadelphia, PA | 21,988 |

### D. 砍掉的字段（63 列）及理由

| 砍掉的类别 | 列数 | 理由 |
|-----------|------|------|
| Employer POC 其余字段 (35, 37-43, 45) | 9 | 保留了姓名（合并）、职位、邮箱；砍掉 middle name、地址、省份、电话等 |
| Agent/Attorney 信息 (47-60) | 14 | 律师联系方式，非核心业务问题 |
| Preparer 信息 (94-98) | 5 | 表格填写人信息，无分析价值 |
| Employer 其余地址字段 (27-28, 30) | 3 | 保留了 ADDRESS(合并)、CITY、STATE、POSTAL_CODE；砍掉 COUNTRY、PROVINCE、PHONE |
| Law Firm 其余字段 (62-64) | 3 | 保留了律所名称；砍掉 FEIN、法院信息 |
| Worksite 详细地址 (68-69, 73) | 3 | 只保留 city/state，详细街道无需 |
| PW 详细来源 (79, 82-85) | 5 | Prevailing wage 追踪号和调查来源（见下方说明） |
| 合规声明 & 披露 (87, 92-93) | 3 | 几乎所有记录都是 Y，无分析价值 |
| 其他低价值 (21, 29-31, 65, 71, 81, 86 等) | 14 | TRADE_NAME_DBA / EMPLOYER_PHONE / EMPLOYER_FEIN 等 |
| POC 电话 (44) | 1 | 电话号码对终端用户分析价值低，邮箱已足够 |
| 合并消除 (33+34→POC_NAME, 22+23→ADDRESS) | 3 | 原始 5 列合并为 2 列，净减 3 列 |

**PW 详细来源说明**：Prevailing Wage（市场标准工资）可以来自不同的数据源。`PW_TRACKING_NUMBER` 是 DOL 发放的工资认定追踪号；`PW_OTHER_SOURCE` 标记是来自 CBA（集体谈判协议）、DBA（Davis-Bacon Act）、SCA（Service Contract Act）还是第三方调查；`PW_SURVEY_PUBLISHER/NAME` 是第三方调查的出版商和调查名称；`PW_OES_YEAR/PW_OTHER_YEAR` 是调查的年份。这些字段过于细节，我们只保留了 `PREVAILING_WAGE`（金额）、`PW_UNIT_OF_PAY`（单位）和 `PW_WAGE_LEVEL`（等级 I-IV）这三个最有分析价值的字段。

> **注意**: `WORKSITE_COUNTY` (col 71) 和 `END_DATE` (col 12) 作为候选保留项，如果未来需要更细粒度的地理分析或签证有效期分析可以加回。

---

## JOB_TITLE 跨年度一致性验证

`JOB_TITLE` 是分析的核心字段。经验证，该字段在所有年份中保持一致：

| 年份 | 字段名 | 备注 |
|------|--------|------|
| FY2018 (iCERT Legacy) | `JOB_TITLE` | 字段名一致，无需 mapping |
| FY2019 (iCERT Expanded) | `JOB_TITLE` | 字段名一致，无需 mapping |
| FY2020 ~ FY2026 (FLAG) | `JOB_TITLE` | 字段名一致 |

> **注意**: `JOB_TITLE` 是自由文本字段（free-text），同一职位可能有不同写法（如 "Software Engineer" vs "SOFTWARE ENGINEER" vs "Sr. Software Engineer"）。建议在 ETL 层做 `UPPER(TRIM(JOB_TITLE))` 标准化。对于标准化的职业分析，应优先使用 `SOC_CODE` + `SOC_TITLE`（标准职业分类），`JOB_TITLE` 作为更细粒度的补充。

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
| 字段数 | 6 | 38 + 6 衍生字段 |
| 数据量 | 未知 | 3,514,878 行，214,366 个雇主 |
| 工资分析 | 只有 base salary | 工资 + prevailing wage + 差值百分比 + 工资等级 |
| 免抽签分析 | 无 | SUPPORT_H1B + STATUTORY_BASIS + NAICS 推断 |
| 申请类型 | 无 | New / Transfer / Extension / Amendment |
| 审批状态 | 无 | Certified / Denied / Withdrawn 统计 |
| 行业分析 | 无 | NAICS 行业代码 |
| H-1B Dependent | 无 | 标记高度依赖 H1B 的雇主 |
| 合规风险 | 无 | Willful Violator 标记 |
| 第三方派遣 | 无 | Secondary Entity 标记 |
| 雇主地理 | 无 | EMPLOYER_ADDRESS/CITY/STATE/POSTAL_CODE（完整地址 + 工作地点对比） |
| 代理律所 | 无 | LAWFIRM_NAME_BUSINESS_NAME |
| 雇主联系人 | 无 | POC 姓名（合并）、职位、邮箱 |
| 雇主维度表 | 无 | `refined.employers`：214,366 个雇主聚合信息 |
| 搜索维度 | 公司 / 职位 / 城市 / 年份 | 公司 / 职位 / 城市 / 邮编 / 年份 / SOC / 行业 / 签证类型 / 雇主所在地 |

---

## Appendix A: 完整保留字段清单 (38 columns)

以下是 refined 层的 38 列完整清单。带 `*` 的为合并字段。

| # | Column Name | 来源 | Type | 分类 |
|---|-------------|------|------|------|
| 1 | `CASE_NUMBER` | col 1 | TEXT | 核心展示 |
| 2 | `EMPLOYER_NAME` | col 20 | TEXT | 核心展示 |
| 3 | `JOB_TITLE` | col 7 | TEXT | 核心展示 |
| 4 | `EMPLOYER_ADDRESS` * | col 22 + 23 合并 | TEXT | 核心展示 |
| 5 | `EMPLOYER_CITY` | col 24 | TEXT | 核心展示 |
| 6 | `EMPLOYER_STATE` | col 25 | TEXT | 核心展示 |
| 7 | `EMPLOYER_POSTAL_CODE` | col 26 | TEXT | 核心展示 |
| 8 | `WORKSITE_CITY` | col 70 | TEXT | 核心展示 |
| 9 | `WORKSITE_STATE` | col 72 | TEXT | 核心展示 |
| 10 | `WAGE_RATE_OF_PAY_FROM` | col 74 | NUMERIC | 核心展示 |
| 11 | `WAGE_RATE_OF_PAY_TO` | col 75 | NUMERIC | 核心展示 |
| 12 | `WAGE_UNIT_OF_PAY` | col 76 | TEXT | 核心展示 |
| 13 | `RECEIVED_DATE` | col 3 | DATE | 核心展示 |
| 14 | `BEGIN_DATE` | col 11 | DATE | 核心展示 |
| 15 | `CASE_STATUS` | col 2 | TEXT | 核心展示 |
| 16 | `FISCAL_YEAR` | ETL 生成 | INTEGER | 核心展示 |
| 17 | `VISA_CLASS` | col 6 | TEXT | 差异化分析 |
| 18 | `SOC_CODE` | col 8 | TEXT | 差异化分析 |
| 19 | `SOC_TITLE` | col 9 | TEXT | 差异化分析 |
| 20 | `FULL_TIME_POSITION` | col 10 | TEXT | 差异化分析 |
| 21 | `TOTAL_WORKER_POSITIONS` | col 13 | INTEGER | 差异化分析 |
| 22 | `NEW_EMPLOYMENT` | col 14 | TEXT | 差异化分析 |
| 23 | `CONTINUED_EMPLOYMENT` | col 15 | TEXT | 差异化分析 |
| 24 | `CHANGE_EMPLOYER` | col 18 | TEXT | 差异化分析 |
| 25 | `AMENDED_PETITION` | col 19 | TEXT | 差异化分析 |
| 26 | `PREVAILING_WAGE` | col 77 | NUMERIC | 差异化分析 |
| 27 | `PW_UNIT_OF_PAY` | col 78 | TEXT | 差异化分析 |
| 28 | `PW_WAGE_LEVEL` | col 80 | TEXT | 差异化分析 |
| 29 | `H1B_DEPENDENT` | col 88 | TEXT | 差异化分析 |
| 30 | `WILLFUL_VIOLATOR` | col 89 | TEXT | 差异化分析 |
| 31 | `SUPPORT_H1B` | col 90 | TEXT | 差异化分析 |
| 32 | `STATUTORY_BASIS` | col 91 | TEXT | 差异化分析 |
| 33 | `NAICS_CODE` | col 32 | TEXT | 差异化分析 |
| 34 | `SECONDARY_ENTITY` | col 66 | TEXT | 差异化分析 |
| 35 | `LAWFIRM_NAME_BUSINESS_NAME` | col 61 | TEXT | 差异化分析 |
| 36 | `EMPLOYER_POC_NAME` * | col 34 + 33 合并 | TEXT | 雇主联系人 |
| 37 | `EMPLOYER_POC_JOB_TITLE` | col 36 | TEXT | 雇主联系人 |
| 38 | `EMPLOYER_POC_EMAIL` | col 46 | TEXT | 雇主联系人 |

---

## Appendix B: 完整排除字段清单 (61 columns)

以下是被排除的 61 列，按原始 schema 分组，附排除理由。

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

### Employer Information（排除 6 列，保留了 4 列 → 合并为 3 列）

已保留: `EMPLOYER_ADDRESS` (合并 #22+#23), `EMPLOYER_CITY` (#24), `EMPLOYER_STATE` (#25), `EMPLOYER_POSTAL_CODE` (#26)

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 21 | `TRADE_NAME_DBA` | DBA 名称，绝大部分为 NULL，有 EMPLOYER_NAME 足够 |
| 27 | `EMPLOYER_COUNTRY` | 几乎全部为 "UNITED STATES OF AMERICA"，信息量低 |
| 28 | `EMPLOYER_PROVINCE` | 仅非美国雇主有值，极少数记录 |
| 29 | `EMPLOYER_PHONE` | 电话号码，对终端用户无分析价值 |
| 30 | `EMPLOYER_PHONE_EXT` | 分机号，对终端用户无分析价值 |
| 31 | `EMPLOYER_FEIN` | 联邦雇主识别号（PII），FY2024 Q4 前全部为 NULL |

### Employer POC（排除 11 列，保留了 3 列）

已保留: `EMPLOYER_POC_NAME` (合并 #33+#34), `EMPLOYER_POC_JOB_TITLE` (#36), `EMPLOYER_POC_EMAIL` (#46)

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 35 | `EMPLOYER_POC_MIDDLE_NAME` | Middle name 对联系人识别价值低 |
| 37 | `EMPLOYER_POC_ADDRESS1` | POC 地址，有雇主地址足够 |
| 38 | `EMPLOYER_POC_ADDRESS2` | 同上 |
| 39 | `EMPLOYER_POC_CITY` | 同上 |
| 40 | `EMPLOYER_POC_STATE` | 同上 |
| 41 | `EMPLOYER_POC_POSTAL_CODE` | 同上 |
| 42 | `EMPLOYER_POC_COUNTRY` | 同上 |
| 43 | `EMPLOYER_POC_PROVINCE` | 同上 |
| 44 | `EMPLOYER_POC_PHONE` | 电话号码，有邮箱已足够联系 |
| 45 | `EMPLOYER_POC_PHONE_EXT` | 分机号 |

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

### Law Firm & Court（排除 3 列，保留了 1 列）

已保留: `LAWFIRM_NAME_BUSINESS_NAME` (#61)

| 原始序号 | Column Name | 排除理由 |
|---------|-------------|---------|
| 62 | `LAWFIRM_BUSINESS_FEIN` | 律所 FEIN，FY2025 Q4 前全部为 NULL |
| 63 | `STATE_OF_HIGHEST_COURT` | 律师执照信息，无分析价值 |
| 64 | `NAME_OF_HIGHEST_STATE_COURT` | 同上 |

### Worksite Information（排除 6 列）

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
| Employer Information | 6 |
| Employer POC | 11 |
| Agent / Attorney | 14 |
| Law Firm & Court | 3 |
| Worksite Information | 6 |
| Wage - PW Details | 6 |
| Compliance & Disclosure | 4 |
| Preparer Information | 5 |
| **总计** | **60** |

> **来源**: 98 原始列 + 1 ETL 列 (`source_table`) = 99 列
> **保留**: 40 列（其中 3 对合并为 2 → 净 38 列）+ 1 新增 (`FISCAL_YEAR`)
> **排除**: 60 列（不含 `source_table`，refined 层不需要 lineage）
