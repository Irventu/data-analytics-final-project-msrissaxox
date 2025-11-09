# 🧠 Final Project Specifications
**Data Analytics with AI Certificate — Capstone Project**

### 🎯 Overview
For your final project, you’ll create a **data-driven Python application** about a topic that personally interests you — anything from sports performance to movie ratings, weather trends, health tracking, fashion choices, or your own simulated dataset.

Your project should:
1. Gather or simulate a dataset.
2. Save it in a simple database.
3. Perform at least **one analysis method covered in class** (ANOVA, MANOVA, linear regression, logistic regression, correlation, or Student’s t-test).
4. Generate at least one visual representation of your results.
5. Save an **aggregated summary** of your analysis for quick queries.
6. Be **fully repeatable** — when new data is added, running the Python script again should automatically update all results.

---

## 📋 Requirements

### 1. Choose a Topic and Dataset
- Pick something you care about.
- Use a **dataset with at least 500 cleaned rows** (no duplicates, valid data types).
- Data can come from:
  - A public dataset (Kaggle, data.gov, sports/music/weather APIs)
  - Your own simulation (explain how you generated it)
  - A combination of compatible datasets (document how you merged them)
- You may not duplicate rows or artificially inflate data counts.

### 2. Store the Data
- Use **TinyDB**, **SQLite**, or a **Pandas DataFrame** saved as CSV or JSON.
- The data should persist between runs.
- For 500+ rows, **SQLite is recommended** for faster queries and aggregation.

### 3. Perform at Least One Analysis
Use **one or more** of the methods covered in class:
- **Descriptive statistics** (mean, median, mode, variance)
- **Student’s t-test**
- **ANOVA / MANOVA**
- **Linear regression**
- **Logistic regression**
- **Correlation analysis**

Your code should:
- Print or save the key statistic(s): t, F, p-value, R², or effect size (η², d, odds ratio, etc.)
- Include a **plain-English explanation** of what the numbers mean.

### 4. Visualize Results
- Create one or more charts, graphs, or tables using `matplotlib` or `pandas.plot`.
- Save visuals into a folder named `results/`.

### 5. Aggregate and Save Results
- Store a summary of your findings (averages, model outputs, etc.) in `results/summary.json` or a database table.
- The summary should allow quick lookups without rerunning the analysis.

### 6. Make the Code Repeatable
Running `python main.py` should:
1. Load or import new data.
2. Save it to the database.
3. Run your analysis.
4. Update charts and summaries.
5. Print progress messages (e.g., “Analysis complete — summary saved.”)

---

## 🔢 Dataset Size & Power Guidance

| Method | Recommended Total | Notes |
|--------|------------------:|------|
| **t-test (2 groups)** | ≥ 200 total (≈100 per group) | Unequal n OK, note group sizes |
| **One-way ANOVA (3+ groups)** | ≥ 300 total (≈100 per group) | More groups require more samples |
| **Two-way ANOVA** | ≥ 400–600 total | ≥60–100 per cell |
| **MANOVA** | ≥ 300 total | ≥15–20 cases per DV per group |
| **Linear regression** | ≥15–20× predictors (≥500 total preferred) | e.g., 5 predictors → 75–100+ |
| **Logistic regression** | ≥15–20 events per predictor | “Events” = minority class |
| **Correlation** | ≥200 | ≥500 preferred |

If you can’t reach those sample sizes, you may simulate or merge data sources — but explain your assumptions.

---

## 🧰 Technical Setup

**Language:** Python 3  
**Suggested Libraries:** `pandas`, `numpy`, `matplotlib`, `tinydb` or `sqlite3`, `scipy.stats`  
**Folder Structure:**
```
project/
├── main.py
├── data/
│   └── dataset.csv
├── results/
│   ├── chart.png
│   └── summary.json
└── copilot-instructions.md
```

---

## ✏️ Code Style Rules

1. **Use long, descriptive function names** even if they’re verbose.  
   ✅ `perform_linear_regression_on_health_data()`  
   ❌ `linreg()`

2. **Comment every line in simple English.**  
   ```python
   # Load the CSV file into a pandas DataFrame
   data_table = pandas.read_csv("data/my_data.csv")
   ```

3. **Use clear variable names** (no abbreviations).  
   ✅ `average_heart_rate_per_person`  
   ❌ `ahrp`

4. **Avoid complex syntax.**  
   - No one-liners or lambdas unless Copilot writes them.  
   - Clarity > cleverness.

---

## 🔁 Reproducibility

Your project must:
- Run entirely from `main.py`  
- Be repeatable (rerunning updates all results)  
- Log data counts, analysis type, and outcomes to the console  
- Set a random seed for reproducible results (if random sampling is used)

---

## 📊 Deliverables

- `main.py` (fully commented, descriptive names)
- At least one chart in `results/`
- Aggregated summary in `results/summary.json` or database
- Console output with test results, p-values, and effect sizes
- All code reproducible via Copilot instructions
