# Simulated coursework data

Input: `employee_attrition_dataset.csv`, 1,000 rows. Exact upstream source/license remains unconfirmed; do not describe this file as verified IBM personnel data. Supply your authorized local copy to reproduce.

Required columns for the standalone analysis: `Department`, `Overtime` (Yes/No), `Work_Life_Balance` (original ordinal coding), `Attrition` (Yes/No). The original notebook uses additional income, promotion, tenure and rating columns.

Only grouped counts are distributed in `reports/results.json`; Employee_ID, demographics and row-level records are excluded. Filtering is performed on the group counts, preserving the underlying denominators.
