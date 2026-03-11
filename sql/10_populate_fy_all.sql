-- Populate refined.fy_all by combining all fiscal year tables.
-- Simple UNION ALL since each FY table is already deduplicated.

TRUNCATE refined.fy_all;

INSERT INTO refined.fy_all
SELECT * FROM refined.fy2020
UNION ALL
SELECT * FROM refined.fy2021
UNION ALL
SELECT * FROM refined.fy2022
UNION ALL
SELECT * FROM refined.fy2023
UNION ALL
SELECT * FROM refined.fy2024
UNION ALL
SELECT * FROM refined.fy2025
UNION ALL
SELECT * FROM refined.fy2026;
