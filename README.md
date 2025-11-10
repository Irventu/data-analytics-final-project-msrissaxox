# 🐱 Cat Breed Statistical Analysis - Data Analytics Final Project

A comprehensive statistical analysis of the top 10 most popular cat breeds, examining health & physiology characteristics and quantified personality traits.

## 📊 Project Overview

This project provides detailed statistical analysis of cat breed characteristics across three main categories:

### Health & Physiology

- **Life Expectancy**: Average lifespan with statistical ranges
- **Weight Distribution**: Male vs female weight patterns by breed
- **Health Conditions**: Statistical prevalence of HCM, PKD, and hip dysplasia

### Personality (Quantified)

- **Vocalization Frequency**: Low (1) to High (3) scale
- **Social Interaction Need**: Independent (1) to High need (3)
- **Affection Level**: Aloof (1) to Dog-like devotion (4)

## 🗂 Dataset Specifications

- **Sample Size**: 550 cats (55 per breed)
- **Breeds Analyzed**: Persian, Maine Coon, British Shorthair, Ragdoll, Bengal, Abyssinian, Siamese, Scottish Fold, Russian Blue, American Shorthair
- **Data Quality**: No missing values, validated data types, realistic ranges
- **Storage**: SQLite database for persistence and querying

## 📈 Statistical Methods

### Analyses Performed

- **Descriptive Statistics**: Mean, median, standard deviation, ranges
- **ANOVA**: Testing breed differences with eta-squared effect sizes
- **Independent t-tests**: Gender comparisons with Cohen's d
- **Pearson Correlation**: Relationships between traits
- **Chi-square Tests**: Health condition breed differences

### Key Findings

- ✅ **All breed characteristics show highly significant differences (p < 0.001)**
- ✅ **Large effect sizes for personality traits (η² = 0.40-0.64)**
- ✅ **Significant gender dimorphism in weight (d = 1.61)**
- ✅ **Breed-specific health risks identified**
- ✅ **Strong correlation between social needs and affection (r = 0.46)**

## 🚀 Quick Start

### Run Complete Analysis

```bash
python main_analysis.py
```

### Run Individual Components

```bash
# Generate dataset
python cat_breed_data_generator.py

# Setup database
python database_setup.py

# Perform statistical analysis
python statistical_analysis.py

# Create visualizations
python data_visualization.py

# Generate reports
python report_generator.py
```

## 📁 Project Structure

```
cat-breed-analysis/
├── main_analysis.py                 # Main script (run this!)
├── cat_breed_data_generator.py      # Dataset generation
├── database_setup.py                # SQLite database setup
├── statistical_analysis.py          # Statistical tests
├── data_visualization.py            # Chart generation
├── report_generator.py              # Report creation
├── cat_breed_dataset.csv           # Main dataset (generated)
├── cat_breed_analysis.db           # SQLite database (generated)
└── results/                        # Output folder
    ├── *.png                       # Visualizations
    ├── *.txt                       # Reports
    └── *.csv                       # Summary tables
```

## 📊 Generated Outputs

### Visualizations (results/)

- `breed_physiology_comparison.png` - Life expectancy and weight by breed
- `health_conditions_heatmap.png` - Health condition prevalence
- `personality_radar_charts.png` - Personality traits by breed
- `correlation_heatmap.png` - Variable relationships
- `gender_differences.png` - Male vs female comparisons
- `anova_results_summary.png` - Statistical test results
- `health_trends.png` - Health patterns and trends
- `breed_summary_table.png` - Comprehensive breed comparison

### Reports (results/)

- `Cat_Breed_Analysis_Complete_Report.txt` - Full analysis (1,400+ words)
- `Cat_Breed_Analysis_Executive_Summary.txt` - Key findings summary
- `breed_summary_table.csv` - Statistical summary by breed

### Database Tables

- `cats` - Individual cat records (550 rows)
- `breed_statistics` - Aggregated breed statistics
- `analysis_results` - Statistical test results

## 🔍 Key Research Findings

### Life Expectancy Champions

1. **Russian Blue**: 15.3 ± 2.2 years
2. **Siamese**: 15.8 ± 1.6 years
3. **American Shorthair**: 15.1 ± 1.9 years

### Weight Patterns

- **Heaviest**: Maine Coon (♂16.0 lbs, ♀11.5 lbs)
- **Lightest**: Russian Blue/Siamese (~8.7 lbs average)
- **Gender Effect**: Males average 3.4 lbs heavier than females

### Health Risk Profiles

- **PKD Risk**: Persians (43.6% prevalence)
- **HCM Risk**: Maine Coons (10.9% prevalence)
- **Hip Dysplasia**: Maine Coons (16.4% prevalence)

### Personality Insights

- **Most Vocal**: Bengal and Siamese breeds
- **Most Affectionate**: Abyssinian, Bengal, Maine Coon, Ragdoll
- **Most Independent**: Russian Blue and British Shorthair
- **Social-Affection Link**: Strong positive correlation (r = 0.461)

## 🔬 Statistical Rigor

### Effect Size Interpretations

- **Eta-squared (η²)**: Small (0.01), Medium (0.06), Large (0.14)
- **Cohen's d**: Small (0.2), Medium (0.5), Large (0.8)
- **Cramér's V**: Small (0.1), Medium (0.3), Large (0.5)

### Significance Testing

- **Alpha Level**: p < 0.05
- **Power**: High (n = 550)
- **Multiple Comparisons**: Bonferroni correction applied where appropriate

## 🛠 Requirements

### Python Packages

```bash
pip install pandas numpy matplotlib seaborn scipy
```

### System Requirements

- Python 3.7+
- 50MB disk space for outputs
- SQLite support (built-in)

## 🎓 Academic Use

This project fulfills data analytics capstone requirements:

- ✅ 500+ row dataset with no missing values
- ✅ SQLite database for data persistence
- ✅ Multiple statistical methods (ANOVA, t-tests, correlation)
- ✅ Professional visualizations saved to results/
- ✅ Aggregated summary statistics
- ✅ Fully repeatable analysis pipeline

## 📄 Citation

When citing this analysis:

```
Cat Breed Statistical Analysis. (2025). Comprehensive analysis of health
and personality characteristics in top 10 cat breeds. Data Analytics
Final Project. [Dataset: n=550 cats across 10 breeds]
```

---

**🐾 Happy analyzing! May your statistical power be strong and your p-values be significant!** 🐱📊
