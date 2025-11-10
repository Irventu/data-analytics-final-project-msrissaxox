"""
Data Visualization Module for Cat Breed Analysis
Creates comprehensive charts and graphs to visualize statistical findings.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set styling
plt.style.use('default')
sns.set_palette("husl")

class CatBreedVisualizer:
    def __init__(self, db_path='cat_breed_analysis.db', results_dir='results'):
        self.db_path = db_path
        self.results_dir = results_dir
        self.connection = sqlite3.connect(db_path)
        self.data = None
        self.breed_stats = None
        
    def load_data(self):
        """Load data from database."""
        self.data = pd.read_sql_query("SELECT * FROM cats", self.connection)
        self.breed_stats = pd.read_sql_query("SELECT * FROM breed_statistics", self.connection)
        print(f"Loaded {len(self.data)} cat records for visualization.")
        
    def create_breed_comparison_plots(self):
        """Create comprehensive breed comparison visualizations."""
        print("Creating breed comparison plots...")
        
        # 1. Life Expectancy and Weight Comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Life expectancy boxplot
        sns.boxplot(data=self.data, x='breed', y='life_expectancy', ax=ax1)
        ax1.set_title('Life Expectancy by Breed', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Breed')
        ax1.set_ylabel('Life Expectancy (years)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Weight comparison with gender
        sns.boxplot(data=self.data, x='breed', y='weight_lbs', hue='gender', ax=ax2)
        ax2.set_title('Weight Distribution by Breed and Gender', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Breed')
        ax2.set_ylabel('Weight (lbs)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend(title='Gender')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/breed_physiology_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Health Conditions Heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Calculate prevalence by breed
        health_data = self.data.groupby('breed')[['has_hcm', 'has_pkd', 'has_hip_dysplasia']].mean() * 100
        health_data.columns = ['HCM (%)', 'PKD (%)', 'Hip Dysplasia (%)']
        
        sns.heatmap(health_data, annot=True, fmt='.1f', cmap='Reds', ax=ax)
        ax.set_title('Health Condition Prevalence by Breed (%)', fontsize=16, fontweight='bold')
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/health_conditions_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Personality Traits Radar Chart
        personality_data = self.data.groupby('breed')[['vocalization_frequency', 'social_interaction_need', 'affection_level']].mean()
        
        fig, axes = plt.subplots(2, 5, figsize=(20, 8), subplot_kw=dict(projection='polar'))
        axes = axes.flatten()
        
        traits = ['Vocalization', 'Social Need', 'Affection']
        angles = np.linspace(0, 2*np.pi, len(traits), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(personality_data)))
        
        for i, (breed, values) in enumerate(personality_data.iterrows()):
            values_plot = values.tolist()
            values_plot += values_plot[:1]  # Complete the circle
            
            axes[i].plot(angles, values_plot, 'o-', color=colors[i], linewidth=2)
            axes[i].fill(angles, values_plot, alpha=0.25, color=colors[i])
            axes[i].set_xticks(angles[:-1])
            axes[i].set_xticklabels(traits)
            axes[i].set_ylim(0, 4)
            axes[i].set_title(breed, fontsize=12, fontweight='bold')
            
        plt.suptitle('Personality Traits by Breed (Radar Charts)', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/personality_radar_charts.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_correlation_heatmap(self):
        """Create correlation matrix visualization."""
        print("Creating correlation heatmap...")
        
        # Select numeric variables
        numeric_vars = ['life_expectancy', 'weight_lbs', 'age', 'health_score',
                       'vocalization_frequency', 'social_interaction_need', 'affection_level']
        
        corr_matrix = self.data[numeric_vars].corr()
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        
        mask = np.triu(np.ones_like(corr_matrix))  # Mask upper triangle
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.3f', 
                   cmap='RdBu_r', center=0, ax=ax,
                   square=True, linewidths=0.5)
        
        ax.set_title('Correlation Matrix of Cat Characteristics', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_statistical_results_summary(self):
        """Create visualization of statistical test results."""
        print("Creating statistical results summary...")
        
        # Get analysis results
        analysis_results = pd.read_sql_query("SELECT * FROM analysis_results", self.connection)
        
        # ANOVA results visualization
        anova_results = analysis_results[analysis_results['analysis_type'] == 'ANOVA'].copy()
        anova_results['variables_tested'] = anova_results['variables_tested'].str.replace('_', ' ').str.title()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # F-statistics
        bars1 = ax1.bar(anova_results['variables_tested'], anova_results['test_statistic'])
        ax1.set_title('ANOVA F-Statistics by Variable', fontsize=14, fontweight='bold')
        ax1.set_ylabel('F-Statistic')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}', ha='center', va='bottom')
        
        # Effect sizes (eta-squared)
        bars2 = ax2.bar(anova_results['variables_tested'], anova_results['effect_size'])
        ax2.set_title('ANOVA Effect Sizes (η²)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Eta-squared (η²)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/anova_results_summary.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_gender_differences_plot(self):
        """Create visualization of gender differences."""
        print("Creating gender differences visualization...")
        
        continuous_vars = ['life_expectancy', 'weight_lbs', 'health_score',
                          'vocalization_frequency', 'social_interaction_need', 'affection_level']
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, var in enumerate(continuous_vars):
            sns.boxplot(data=self.data, x='gender', y=var, ax=axes[i])
            axes[i].set_title(f'{var.replace("_", " ").title()} by Gender', fontweight='bold')
            axes[i].set_xlabel('Gender')
            axes[i].set_ylabel(var.replace('_', ' ').title())
            
            # Add statistical annotation
            male_vals = self.data[self.data['gender'] == 'Male'][var]
            female_vals = self.data[self.data['gender'] == 'Female'][var]
            
            from scipy.stats import ttest_ind
            t_stat, p_val = ttest_ind(male_vals, female_vals)
            
            if p_val < 0.001:
                sig_text = "***"
            elif p_val < 0.01:
                sig_text = "**"
            elif p_val < 0.05:
                sig_text = "*"
            else:
                sig_text = "ns"
                
            axes[i].text(0.5, 0.95, f'p = {p_val:.3f} {sig_text}', 
                        transform=axes[i].transAxes, ha='center', va='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.suptitle('Gender Differences in Cat Characteristics', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/gender_differences.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_breed_summary_table(self):
        """Create a comprehensive breed summary table."""
        print("Creating breed summary table...")
        
        # Calculate key metrics by breed
        breed_summary = self.data.groupby('breed').agg({
            'life_expectancy': ['mean', 'std'],
            'weight_lbs': 'mean',
            'has_hcm': lambda x: f"{x.mean()*100:.1f}%",
            'has_pkd': lambda x: f"{x.mean()*100:.1f}%", 
            'has_hip_dysplasia': lambda x: f"{x.mean()*100:.1f}%",
            'vocalization_frequency': 'mean',
            'social_interaction_need': 'mean',
            'affection_level': 'mean',
            'cat_id': 'count'
        }).round(1)
        
        # Flatten column names
        breed_summary.columns = ['Avg_Lifespan', 'Std_Lifespan', 'Avg_Weight', 'HCM_Rate',
                               'PKD_Rate', 'Hip_Dysplasia_Rate', 'Vocalization', 'Social_Need',
                               'Affection', 'Sample_Size']
        
        # Create table visualization
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # Create table
        table_data = breed_summary.reset_index()
        table = ax.table(cellText=table_data.values,
                        colLabels=table_data.columns,
                        cellLoc='center',
                        loc='center',
                        colWidths=[0.12]*len(table_data.columns))
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Color header
        for i in range(len(table_data.columns)):
            table[(0, i)].set_facecolor('#40466e')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Color rows alternately
        for i in range(1, len(table_data) + 1):
            for j in range(len(table_data.columns)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f1f1f2')
        
        plt.title('Comprehensive Cat Breed Characteristics Summary', 
                 fontsize=16, fontweight='bold', pad=20)
        
        plt.savefig(f'{self.results_dir}/breed_summary_table.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Save as CSV too
        breed_summary.to_csv(f'{self.results_dir}/breed_summary_table.csv')
        
    def create_health_trends_visualization(self):
        """Create health trends and patterns visualization."""
        print("Creating health trends visualization...")
        
        # Health score distribution by breed
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Health score distribution
        sns.violinplot(data=self.data, x='breed', y='health_score', ax=ax1)
        ax1.set_title('Health Score Distribution by Breed', fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.set_ylabel('Health Score (0-10)')
        
        # 2. Age vs Health Score scatter
        sns.scatterplot(data=self.data, x='age', y='health_score', hue='breed', ax=ax2, alpha=0.6)
        ax2.set_title('Health Score vs Age by Breed', fontweight='bold')
        ax2.set_xlabel('Age (years)')
        ax2.set_ylabel('Health Score')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 3. Weight category distribution
        weight_breed = pd.crosstab(self.data['breed'], self.data['weight_category'], normalize='index') * 100
        weight_breed.plot(kind='bar', stacked=True, ax=ax3)
        ax3.set_title('Weight Category Distribution by Breed (%)', fontweight='bold')
        ax3.tick_params(axis='x', rotation=45)
        ax3.set_ylabel('Percentage')
        ax3.legend(title='Weight Category')
        
        # 4. Life expectancy vs weight scatter
        sns.scatterplot(data=self.data, x='weight_lbs', y='life_expectancy', hue='breed', ax=ax4, alpha=0.6)
        ax4.set_title('Life Expectancy vs Weight by Breed', fontweight='bold')
        ax4.set_xlabel('Weight (lbs)')
        ax4.set_ylabel('Life Expectancy (years)')
        ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/health_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_all_visualizations(self):
        """Generate all visualizations."""
        print(f"Generating comprehensive visualizations...")
        print(f"Results will be saved to: {self.results_dir}/")
        
        self.load_data()
        
        # Create all visualizations
        self.create_breed_comparison_plots()
        self.create_correlation_heatmap()
        self.create_statistical_results_summary()
        self.create_gender_differences_plot()
        self.create_breed_summary_table()
        self.create_health_trends_visualization()
        
        print(f"\nAll visualizations created successfully!")
        print(f"Generated files:")
        import os
        for file in os.listdir(self.results_dir):
            if file.endswith(('.png', '.csv')):
                print(f"  - {file}")
        
    def close(self):
        """Close database connection."""
        self.connection.close()

def main():
    """Main visualization function."""
    visualizer = CatBreedVisualizer()
    
    try:
        visualizer.generate_all_visualizations()
        print("\nVisualization complete!")
        
    finally:
        visualizer.close()

if __name__ == "__main__":
    main()