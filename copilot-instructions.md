# Copilot Instructions for Data Analytics Final Project

## Goal
Generate beginner-friendly Python code that:
1. Loads or imports a dataset (≥500 rows).
2. Stores it in TinyDB, SQLite, or a Pandas DataFrame.
3. Performs at least one statistical method from class:
   - t-test, ANOVA, MANOVA, linear regression, logistic regression, or correlation.
4. Generates one or more visualizations (charts or tables).
5. Saves a summary of results (JSON or database).
6. Reruns cleanly to update results with new data.

---

## Implementation Details
- Create a main script called `main.py`.
- Include helper functions:
  - `load_or_import_dataset()`
  - `save_dataset_to_database()`
  - `perform_statistical_analysis()`
  - `generate_visualizations()`
  - `save_summary_results()`
- Each function should print clear progress messages.
- When rerun, the script should refresh visuals and summary data automatically.

---

## Data Volume & Validation
- Check that the dataset has **≥500 rows** after cleaning.
- Print total row count.
- For group tests, print per-group counts and warn if any group < 60.
- For logistic regression, print class balance and warn if the minority class < (15 × predictors).

---

## Scalability
- Support large datasets using:
  - `pandas.read_csv(..., chunksize=50000)` if memory is limited.
  - SQLite for fast queries and aggregation.
- Cache results to `results/summary.json` and only recompute if source data changes.

---

## Reproducibility
- Add a function `set_random_seed_for_reproducible_results()` and call it at the top.
- Log:
  - Data source(s)
  - Row counts before/after cleaning
  - Group sizes
  - Train/test splits (if used)
  - Statistical test name and parameters

---

## Output Requirements
- Print:
  - Dataset size and test used
  - Test statistic(s)
  - p-value
  - Effect size (R², η², d, or odds ratio)
- Save:
  - Plots in `results/`
  - Summary data in `results/summary.json` or SQLite table

---

## Style and Readability
- Use **long, descriptive function names** that explain exactly what they do.
- **Comment every line** in simple English.
- Use **clear variable names** (avoid abbreviations).
- Keep the code structure simple and suitable for absolute beginners.

---

## Logging Messages
Examples of printed messages:
```
Loading dataset from data/dataset.csv...
Dataset loaded successfully with 512 rows.
Performing linear regression on salary vs. experience...
R² = 0.83, p = 0.002 — statistically significant.
Saving chart to results/linear_regression_chart.png...
Analysis complete — summary saved to results/summary.json.
```
