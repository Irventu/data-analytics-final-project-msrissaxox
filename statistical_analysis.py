"""
Statistical Analysis Module for Cat Breed Research
Performs comprehensive statistical analyses including ANOVA, correlation analysis, t-tests, and descriptive statistics.
"""

import pandas as pd
import numpy as np
import sqlite3
from scipy import stats
from scipy.stats import f_oneway, pearsonr, spearmanr, ttest_ind
import warnings
warnings.filterwarnings('ignore')

class CatBreedStatisticalAnalysis:
    def __init__(self, db_path='cat_breed_analysis.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.data = None
        self.breed_stats = None
        self.results = {}
        
    def load_data(self):
        """Load data from database."""
        self.data = pd.read_sql_query("SELECT * FROM cats", self.connection)
        self.breed_stats = pd.read_sql_query("SELECT * FROM breed_statistics", self.connection)
        print(f"Loaded {len(self.data)} cat records for analysis.")
        
    def descriptive_statistics(self):
        """Generate comprehensive descriptive statistics."""
        print("\n" + "="*60)
        print("DESCRIPTIVE STATISTICS ANALYSIS")
        print("="*60)
        
        # Overall descriptive stats
        numeric_cols = ['life_expectancy', 'weight_lbs', 'vocalization_frequency', 
                       'social_interaction_need', 'affection_level', 'health_score']
        
        overall_stats = self.data[numeric_cols].describe()
        print("\nOverall Descriptive Statistics:")
        print(overall_stats.round(2))
        
        # Health condition prevalence
        health_conditions = ['has_hcm', 'has_pkd', 'has_hip_dysplasia']
        prevalence = self.data[health_conditions].mean() * 100
        print(f"\nOverall Health Condition Prevalence:")
        for condition, prev in prevalence.items():
            print(f"{condition.replace('has_', '').upper()}: {prev:.1f}%")
        
        # Breed-specific statistics
        print(f"\nBreed-Specific Statistics:")
        breed_summary = self.data.groupby('breed')[numeric_cols].agg(['mean', 'std']).round(2)
        print(breed_summary)
        
        self.results['descriptive_stats'] = {
            'overall': overall_stats,
            'health_prevalence': prevalence,
            'breed_summary': breed_summary
        }
        
        return overall_stats, prevalence, breed_summary
    
    def anova_analysis(self):
        """Perform ANOVA tests on continuous variables across breeds."""
        print("\n" + "="*60)
        print("ANALYSIS OF VARIANCE (ANOVA)")
        print("="*60)
        
        continuous_vars = ['life_expectancy', 'weight_lbs', 'health_score', 
                          'vocalization_frequency', 'social_interaction_need', 'affection_level']
        
        anova_results = {}
        
        for var in continuous_vars:
            # Create groups by breed
            groups = [self.data[self.data['breed'] == breed][var].values 
                     for breed in self.data['breed'].unique()]
            
            # Perform ANOVA
            f_stat, p_value = f_oneway(*groups)
            
            # Calculate effect size (eta-squared)
            # SS_between / SS_total
            grand_mean = self.data[var].mean()
            ss_total = ((self.data[var] - grand_mean) ** 2).sum()
            
            breed_means = self.data.groupby('breed')[var].mean()
            breed_counts = self.data.groupby('breed')[var].count()
            ss_between = ((breed_means - grand_mean) ** 2 * breed_counts).sum()
            eta_squared = ss_between / ss_total
            
            # Interpretation
            if p_value < 0.001:
                significance = "Highly significant (p < 0.001)"
            elif p_value < 0.01:
                significance = "Very significant (p < 0.01)"
            elif p_value < 0.05:
                significance = "Significant (p < 0.05)"
            else:
                significance = "Not significant (p >= 0.05)"
                
            if eta_squared < 0.01:
                effect_size = "Small effect"
            elif eta_squared < 0.06:
                effect_size = "Medium effect"
            else:
                effect_size = "Large effect"
            
            anova_results[var] = {
                'f_statistic': f_stat,
                'p_value': p_value,
                'eta_squared': eta_squared,
                'significance': significance,
                'effect_size': effect_size,
                'df_between': len(groups) - 1,
                'df_within': len(self.data) - len(groups)
            }
            
            print(f"\n{var.replace('_', ' ').title()}:")
            print(f"  F-statistic: {f_stat:.3f}")
            print(f"  p-value: {p_value:.6f}")
            print(f"  η² (eta-squared): {eta_squared:.3f}")
            print(f"  {significance}")
            print(f"  {effect_size}")
            
            # Save to database
            interpretation = f"{significance}. {effect_size}. Breeds differ significantly in {var.replace('_', ' ')} (F={f_stat:.3f}, p={p_value:.6f}, η²={eta_squared:.3f})"
            self._save_analysis_result("ANOVA", f_stat, p_value, eta_squared, 
                                     len(groups)-1, var, interpretation)
        
        self.results['anova'] = anova_results
        return anova_results
    
    def correlation_analysis(self):
        """Perform correlation analysis between variables."""
        print("\n" + "="*60)
        print("CORRELATION ANALYSIS")
        print("="*60)
        
        # Select numeric variables for correlation
        numeric_vars = ['life_expectancy', 'weight_lbs', 'age', 'health_score',
                       'vocalization_frequency', 'social_interaction_need', 'affection_level']
        
        # Pearson correlations
        corr_matrix = self.data[numeric_vars].corr()
        print("\nPearson Correlation Matrix:")
        print(corr_matrix.round(3))
        
        # Find strongest correlations
        print(f"\nStrongest Correlations (|r| > 0.3):")
        strong_correlations = []
        
        for i, var1 in enumerate(numeric_vars):
            for j, var2 in enumerate(numeric_vars):
                if i < j:  # Avoid duplicates
                    r = corr_matrix.loc[var1, var2]
                    if abs(r) > 0.3:
                        # Calculate p-value
                        r_pearson, p_value = pearsonr(self.data[var1], self.data[var2])
                        
                        if p_value < 0.001:
                            significance = "***"
                        elif p_value < 0.01:
                            significance = "**"
                        elif p_value < 0.05:
                            significance = "*"
                        else:
                            significance = ""
                        
                        strong_correlations.append({
                            'var1': var1,
                            'var2': var2,
                            'correlation': r,
                            'p_value': p_value,
                            'significance': significance
                        })
                        
                        print(f"  {var1} ↔ {var2}: r = {r:.3f}{significance} (p = {p_value:.6f})")
                        
                        # Save significant correlations
                        if abs(r) > 0.3 and p_value < 0.05:
                            interpretation = f"Moderate to strong correlation between {var1} and {var2} (r={r:.3f}, p={p_value:.6f})"
                            self._save_analysis_result("Pearson Correlation", r, p_value, 
                                                     r**2, len(self.data)-2, f"{var1} vs {var2}", interpretation)
        
        self.results['correlations'] = {
            'correlation_matrix': corr_matrix,
            'strong_correlations': strong_correlations
        }
        
        return corr_matrix, strong_correlations
    
    def gender_differences_analysis(self):
        """Analyze gender differences using t-tests."""
        print("\n" + "="*60)
        print("GENDER DIFFERENCES ANALYSIS (T-TESTS)")
        print("="*60)
        
        continuous_vars = ['life_expectancy', 'weight_lbs', 'health_score',
                          'vocalization_frequency', 'social_interaction_need', 'affection_level']
        
        gender_results = {}
        
        males = self.data[self.data['gender'] == 'Male']
        females = self.data[self.data['gender'] == 'Female']
        
        print(f"Sample sizes: Males = {len(males)}, Females = {len(females)}")
        
        for var in continuous_vars:
            male_values = males[var].values
            female_values = females[var].values
            
            # Independent t-test
            t_stat, p_value = ttest_ind(male_values, female_values)
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt(((len(male_values)-1)*np.var(male_values, ddof=1) + 
                                (len(female_values)-1)*np.var(female_values, ddof=1)) / 
                               (len(male_values)+len(female_values)-2))
            cohens_d = (np.mean(male_values) - np.mean(female_values)) / pooled_std
            
            # Interpretation
            if p_value < 0.001:
                significance = "Highly significant (p < 0.001)"
            elif p_value < 0.01:
                significance = "Very significant (p < 0.01)"  
            elif p_value < 0.05:
                significance = "Significant (p < 0.05)"
            else:
                significance = "Not significant (p >= 0.05)"
                
            if abs(cohens_d) < 0.2:
                effect_size = "Negligible effect"
            elif abs(cohens_d) < 0.5:
                effect_size = "Small effect"
            elif abs(cohens_d) < 0.8:
                effect_size = "Medium effect"
            else:
                effect_size = "Large effect"
            
            gender_results[var] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'cohens_d': cohens_d,
                'male_mean': np.mean(male_values),
                'female_mean': np.mean(female_values),
                'significance': significance,
                'effect_size': effect_size
            }
            
            print(f"\n{var.replace('_', ' ').title()}:")
            print(f"  Male mean: {np.mean(male_values):.2f}")
            print(f"  Female mean: {np.mean(female_values):.2f}")
            print(f"  t-statistic: {t_stat:.3f}")
            print(f"  p-value: {p_value:.6f}")
            print(f"  Cohen's d: {cohens_d:.3f}")
            print(f"  {significance}")
            print(f"  {effect_size}")
            
            # Save significant results
            if p_value < 0.05:
                interpretation = f"Significant gender difference in {var.replace('_', ' ')} (t={t_stat:.3f}, p={p_value:.6f}, d={cohens_d:.3f}). {effect_size}."
                self._save_analysis_result("Independent t-test", t_stat, p_value, cohens_d,
                                         len(male_values)+len(female_values)-2, f"Gender differences in {var}", interpretation)
        
        self.results['gender_differences'] = gender_results
        return gender_results
    
    def health_condition_analysis(self):
        """Analyze health condition patterns across breeds."""
        print("\n" + "="*60)
        print("HEALTH CONDITION ANALYSIS")
        print("="*60)
        
        health_conditions = ['has_hcm', 'has_pkd', 'has_hip_dysplasia']
        
        # Chi-square tests for breed differences in health conditions
        health_results = {}
        
        for condition in health_conditions:
            # Create contingency table
            contingency = pd.crosstab(self.data['breed'], self.data[condition])
            
            # Chi-square test
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            
            # Cramér's V (effect size for chi-square)
            n = contingency.sum().sum()
            cramers_v = np.sqrt(chi2 / (n * (min(contingency.shape) - 1)))
            
            # Breed-specific prevalence
            breed_prevalence = self.data.groupby('breed')[condition].mean() * 100
            
            health_results[condition] = {
                'chi_square': chi2,
                'p_value': p_value,
                'degrees_freedom': dof,
                'cramers_v': cramers_v,
                'breed_prevalence': breed_prevalence,
                'overall_prevalence': self.data[condition].mean() * 100
            }
            
            condition_name = condition.replace('has_', '').upper()
            print(f"\n{condition_name} Analysis:")
            print(f"  Overall prevalence: {self.data[condition].mean()*100:.1f}%")
            print(f"  χ² = {chi2:.3f}, p = {p_value:.6f}")
            print(f"  Cramér's V = {cramers_v:.3f}")
            print(f"  Breed prevalence rates:")
            
            for breed, prevalence in breed_prevalence.sort_values(ascending=False).items():
                print(f"    {breed}: {prevalence:.1f}%")
            
            # Save significant results
            if p_value < 0.05:
                interpretation = f"Significant breed differences in {condition_name} prevalence (χ²={chi2:.3f}, p={p_value:.6f}, V={cramers_v:.3f})"
                self._save_analysis_result("Chi-square test", chi2, p_value, cramers_v,
                                         dof, f"Breed differences in {condition}", interpretation)
        
        self.results['health_analysis'] = health_results
        return health_results
    
    def _save_analysis_result(self, analysis_type, test_stat, p_value, effect_size, df, variables, interpretation):
        """Save analysis results to database."""
        cursor = self.connection.cursor()
        
        cursor.execute('''
        INSERT INTO analysis_results 
        (analysis_type, test_statistic, p_value, effect_size, degrees_freedom, 
         variables_tested, result_interpretation, analysis_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (analysis_type, test_stat, p_value, effect_size, df, variables, interpretation))
        
        self.connection.commit()
    
    def run_complete_analysis(self):
        """Run all statistical analyses."""
        self.load_data()
        
        print("Starting comprehensive statistical analysis of cat breed data...")
        print(f"Dataset: {len(self.data)} cats across {self.data['breed'].nunique()} breeds")
        
        # Run all analyses
        self.descriptive_statistics()
        self.anova_analysis()
        self.correlation_analysis()
        self.gender_differences_analysis()
        self.health_condition_analysis()
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print("All results have been saved to the database.")
        print("Check the 'analysis_results' table for detailed statistical findings.")
        
        return self.results
    
    def generate_summary_report(self):
        """Generate a summary report of all analyses."""
        # Get analysis results from database
        analysis_df = pd.read_sql_query("SELECT * FROM analysis_results", self.connection)
        
        print("\n" + "="*60)
        print("STATISTICAL ANALYSIS SUMMARY REPORT")
        print("="*60)
        
        print(f"Total analyses performed: {len(analysis_df)}")
        print(f"Analysis types: {', '.join(analysis_df['analysis_type'].unique())}")
        
        # Significant findings
        significant = analysis_df[analysis_df['p_value'] < 0.05]
        print(f"\nSignificant findings (p < 0.05): {len(significant)} out of {len(analysis_df)}")
        
        for _, result in significant.iterrows():
            print(f"\n• {result['analysis_type']} - {result['variables_tested']}:")
            print(f"  {result['result_interpretation']}")
        
        return analysis_df
    
    def close(self):
        """Close database connection."""
        self.connection.close()

def main():
    """Main analysis function."""
    analyzer = CatBreedStatisticalAnalysis()
    
    try:
        # Run complete analysis
        results = analyzer.run_complete_analysis()
        
        # Generate summary report
        summary = analyzer.generate_summary_report()
        
        print(f"\nAnalysis complete! Check the database for detailed results.")
        
    finally:
        analyzer.close()

if __name__ == "__main__":
    main()