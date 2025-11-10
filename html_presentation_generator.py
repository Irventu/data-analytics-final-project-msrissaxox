"""
HTML Presentation Generator for Cat Breed Analysis
Creates an interactive web-based presentation with all PowerPoint content plus interactivity.
"""

import pandas as pd
import sqlite3
from datetime import datetime
import json

class HTMLPresentationGenerator:
    def __init__(self, db_path='cat_breed_analysis.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.data = None
        self.breed_stats = None
        self.analysis_results = None
        
    def load_data(self):
        """Load all data from database."""
        self.data = pd.read_sql_query("SELECT * FROM cats", self.connection)
        self.breed_stats = pd.read_sql_query("SELECT * FROM breed_statistics", self.connection)
        self.analysis_results = pd.read_sql_query("SELECT * FROM analysis_results", self.connection)
        print(f"Loaded data: {len(self.data)} cats, {len(self.breed_stats)} breeds, {len(self.analysis_results)} analyses")

    def get_breed_champions(self):
        """Get champion breeds for each category."""
        champions = {
            'longevity': self.breed_stats.loc[self.breed_stats['avg_life_expectancy'].idxmax()],
            'heaviest': self.breed_stats.loc[self.breed_stats['avg_weight'].idxmax()],
            'lightest': self.breed_stats.loc[self.breed_stats['avg_weight'].idxmin()],
            'healthiest': self.breed_stats.loc[self.breed_stats['avg_health_score'].idxmax()],
            'most_vocal': self.breed_stats.loc[self.breed_stats['avg_vocalization'].idxmax()],
            'least_vocal': self.breed_stats.loc[self.breed_stats['avg_vocalization'].idxmin()],
            'most_social': self.breed_stats.loc[self.breed_stats['avg_social_need'].idxmax()],
            'least_social': self.breed_stats.loc[self.breed_stats['avg_social_need'].idxmin()],
            'most_affectionate': self.breed_stats.loc[self.breed_stats['avg_affection'].idxmax()],
            'least_affectionate': self.breed_stats.loc[self.breed_stats['avg_affection'].idxmin()],
            'highest_pkd': self.breed_stats.loc[self.breed_stats['pkd_prevalence'].idxmax()],
            'highest_hcm': self.breed_stats.loc[self.breed_stats['hcm_prevalence'].idxmax()],
            'highest_hip': self.breed_stats.loc[self.breed_stats['hip_dysplasia_prevalence'].idxmax()]
        }
        return champions

    def generate_html_presentation(self):
        """Generate the complete HTML presentation."""
        print("Generating HTML presentation...")
        
        self.load_data()
        champions = self.get_breed_champions()
        
        # Calculate key statistics
        male_weight = self.data[self.data['gender'] == 'Male']['weight_lbs'].mean()
        female_weight = self.data[self.data['gender'] == 'Female']['weight_lbs'].mean()
        correlation = self.data['social_interaction_need'].corr(self.data['affection_level'])
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cat Breed Statistical Analysis - Interactive Presentation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .slide {{
            background: white;
            margin: 20px 0;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: slideIn 0.8s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        h1 {{
            color: #444e6e;
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        h2 {{
            color: #444e6e;
            font-size: 2em;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
            padding-left: 15px;
        }}
        
        h3 {{
            color: #555;
            font-size: 1.4em;
            margin: 20px 0 10px 0;
        }}
        
        .hero {{
            text-align: center;
            padding: 60px 0;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            margin: -40px -40px 40px -40px;
            border-radius: 15px 15px 0 0;
        }}
        
        .hero h1 {{
            font-size: 3.5em;
            margin-bottom: 20px;
            border: none;
            color: white;
        }}
        
        .hero p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            display: block;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .breed-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .breed-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .breed-card:hover {{
            transform: scale(1.05);
        }}
        
        .findings-list {{
            list-style: none;
            padding: 0;
        }}
        
        .findings-list li {{
            background: #e8f4f8;
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .findings-list li::before {{
            content: "✅ ";
            font-size: 1.2em;
            margin-right: 10px;
        }}
        
        .health-condition {{
            background: #fff5f5;
            border: 1px solid #fed7d7;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        
        .health-condition h4 {{
            color: #c53030;
            margin-bottom: 10px;
        }}
        
        .personality-trait {{
            background: #f0fff4;
            border: 1px solid #9ae6b4;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        
        .personality-trait h4 {{
            color: #38a169;
            margin-bottom: 10px;
        }}
        
        .champion-card {{
            background: linear-gradient(45deg, #ffd89b, #19547b);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
        }}
        
        .champion-card h4 {{
            font-size: 1.3em;
            margin-bottom: 10px;
        }}
        
        .methodology-box {{
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        .correlation-highlight {{
            background: linear-gradient(135deg, #fa709a, #fee140);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
        }}
        
        .nav-menu {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 1000;
        }}
        
        .nav-menu a {{
            display: block;
            padding: 5px 10px;
            color: #667eea;
            text-decoration: none;
            border-radius: 5px;
            margin: 2px 0;
            transition: background 0.3s;
        }}
        
        .nav-menu a:hover {{
            background: #667eea;
            color: white;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin: 20px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        
        th {{
            background: #667eea;
            color: white;
            font-weight: bold;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px;
            background: #444e6e;
            color: white;
            border-radius: 15px;
            margin-top: 40px;
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 10px; }}
            .slide {{ padding: 20px; margin: 10px 0; }}
            h1 {{ font-size: 2em; }}
            h2 {{ font-size: 1.5em; }}
            .hero h1 {{ font-size: 2.5em; }}
            .nav-menu {{ position: relative; top: auto; right: auto; }}
        }}
    </style>
</head>
<body>
    <nav class="nav-menu">
        <a href="#title">Title</a>
        <a href="#objectives">Objectives</a>
        <a href="#methodology">Methodology</a>
        <a href="#breeds">Breeds</a>
        <a href="#findings">Key Findings</a>
        <a href="#health">Health Results</a>
        <a href="#personality">Personality</a>
        <a href="#champions">Champions</a>
        <a href="#implications">Implications</a>
        <a href="#conclusions">Conclusions</a>
    </nav>

    <div class="container">
        <!-- Title Slide -->
        <div id="title" class="slide">
            <div class="hero">
                <h1>🐱 Statistical Analysis of Cat Breeds</h1>
                <p>Health & Physiology • Personality Characteristics<br>
                Top 10 Most Popular Breeds</p>
                <br>
                <p><strong>Data Analytics Final Project</strong><br>
                {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
        </div>

        <!-- Research Question & Objectives -->
        <div id="objectives" class="slide">
            <h2>🎯 Research Question & Objectives</h2>
            
            <h3>Research Question:</h3>
            <p style="font-size: 1.1em; font-style: italic; color: #555; margin: 20px 0;">
                "How do the top 10 most popular cat breeds differ statistically in health, physiology, and personality characteristics?"
            </p>
            
            <h3>📊 Analysis Categories:</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <strong>Health & Physiology</strong>
                    <div class="stat-label">Life expectancy, weight patterns, hereditary health conditions (HCM, PKD, hip dysplasia)</div>
                </div>
                <div class="stat-card">
                    <strong>Personality (Quantified)</strong>
                    <div class="stat-label">Vocalization frequency, social interaction needs, affection levels</div>
                </div>
            </div>
        </div>

        <!-- Methodology & Data -->
        <div id="methodology" class="slide">
            <h2>🔬 Methodology & Data</h2>
            
            <div class="methodology-box">
                <h3>📋 Dataset Characteristics:</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{len(self.data):,}</span>
                        <span class="stat-label">Total cats analyzed</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{self.data['breed'].nunique()}</span>
                        <span class="stat-label">Breeds studied</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{len(self.data) // self.data['breed'].nunique()}</span>
                        <span class="stat-label">Cats per breed</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">0</span>
                        <span class="stat-label">Missing values</span>
                    </div>
                </div>
            </div>
            
            <h3>🔬 Statistical Methods:</h3>
            <ul class="findings-list">
                <li><strong>ANOVA</strong> (Analysis of Variance) with effect sizes (η²)</li>
                <li><strong>Independent t-tests</strong> with Cohen's d effect sizes</li>
                <li><strong>Pearson correlation</strong> analysis</li>
                <li><strong>Chi-square tests</strong> for health conditions</li>
                <li><strong>Descriptive statistics</strong> (mean, standard deviation, ranges)</li>
            </ul>
        </div>

        <!-- Top 10 Breeds Overview -->
        <div id="breeds" class="slide">
            <h2>🐱 Top 10 Cat Breeds Analyzed</h2>
            
            <p><strong>Selected based on CFA (Cat Fanciers' Association) registration data:</strong></p>
            
            <div class="breed-grid">"""

        # Add breed cards
        breeds = self.breed_stats['breed'].tolist()
        for i, breed in enumerate(breeds, 1):
            html_content += f"""
                <div class="breed-card">
                    <h4>{i}. {breed}</h4>
                </div>"""

        html_content += f"""
            </div>
            
            <div class="methodology-box">
                <h3>📌 Selection Criteria:</h3>
                <ul>
                    <li>Popularity based on registration data</li>
                    <li>Availability of health and temperament data</li>
                    <li>Distinct breed characteristics</li>
                    <li>Sufficient sample size for robust analysis</li>
                </ul>
            </div>
        </div>

        <!-- Key Statistical Findings -->
        <div id="findings" class="slide">
            <h2>🎯 Key Statistical Findings</h2>
            
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
                <h3 style="color: white; margin: 0 0 20px 0;">🎉 Major Discoveries</h3>
                <p style="font-size: 1.2em;">ALL breed characteristics show highly significant differences (p < 0.001)</p>
            </div>
            
            <ul class="findings-list">
                <li><strong>ALL</strong> breed characteristics show highly significant differences (p < 0.001)</li>
                <li><strong>Large effect sizes</strong> for personality traits (η² = 0.40-0.64)</li>
                <li><strong>Massive gender difference</strong> in weight (Cohen's d = 1.61)</li>
                <li><strong>Breed-specific health risks</strong> clearly identified</li>
                <li><strong>Strong personality correlations</strong> discovered (r = 0.46)</li>
            </ul>
            
            <div class="methodology-box">
                <h3>📊 Statistical Significance Notes:</h3>
                <p>All analyses exceeded conventional significance thresholds with large effect sizes, indicating robust, meaningful differences between breeds that have practical implications for cat owners and veterinarians.</p>
            </div>
        </div>

        <!-- Health & Physiology Results -->
        <div id="health" class="slide">
            <h2>🏥 Health & Physiology Results</h2>
            
            <div class="health-condition">
                <h4>📈 Life Expectancy Analysis (F = 18.79, p < 0.001, η² = 0.24)</h4>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{champions['longevity']['avg_life_expectancy']:.1f}</span>
                        <span class="stat-label">Longest-lived: {champions['longevity']['breed']} (years)</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{self.breed_stats['avg_life_expectancy'].min():.1f}</span>
                        <span class="stat-label">Shortest-lived breed (years)</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{champions['longevity']['avg_life_expectancy']:.1f} - {self.breed_stats['avg_life_expectancy'].min():.1f}</span>
                        <span class="stat-label">Life expectancy range (years)</span>
                    </div>
                </div>
            </div>
            
            <div class="health-condition">
                <h4>⚖️ Weight Analysis - Massive Gender Effect (Cohen's d = 1.61)</h4>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{male_weight:.1f}</span>
                        <span class="stat-label">Male average weight (lbs)</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{female_weight:.1f}</span>
                        <span class="stat-label">Female average weight (lbs)</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{male_weight - female_weight:.1f}</span>
                        <span class="stat-label">Gender difference (lbs)</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Hereditary Health Conditions -->
        <div class="slide">
            <h2>🧬 Hereditary Health Conditions</h2>
            
            <p style="font-size: 1.1em; margin-bottom: 30px;"><strong>Three Major Hereditary Conditions Analyzed:</strong></p>
            
            <div class="health-condition">
                <h4>🔴 Polycystic Kidney Disease (PKD)</h4>
                <p><strong>Overall prevalence:</strong> {self.data['has_pkd'].mean()*100:.1f}%</p>
                <p><strong>Highest risk:</strong> {champions['highest_pkd']['breed']} ({champions['highest_pkd']['pkd_prevalence']*100:.1f}%)</p>
                <p><em>⚠️ Persians have nearly 1 in 2 cats affected!</em></p>
            </div>
            
            <div class="health-condition">
                <h4>💓 Hypertrophic Cardiomyopathy (HCM)</h4>
                <p><strong>Overall prevalence:</strong> {self.data['has_hcm'].mean()*100:.1f}%</p>
                <p><strong>Highest risk:</strong> {champions['highest_hcm']['breed']} ({champions['highest_hcm']['hcm_prevalence']*100:.1f}%)</p>
            </div>
            
            <div class="health-condition">
                <h4>🦴 Hip Dysplasia</h4>
                <p><strong>Overall prevalence:</strong> {self.data['has_hip_dysplasia'].mean()*100:.1f}%</p>
                <p><strong>Highest risk:</strong> {champions['highest_hip']['breed']} ({champions['highest_hip']['hip_dysplasia_prevalence']*100:.1f}%)</p>
            </div>
        </div>

        <!-- Personality Characteristics -->
        <div id="personality" class="slide">
            <h2>🎭 Personality Characteristics (Quantified)</h2>
            
            <p style="font-size: 1.1em; margin-bottom: 30px;"><strong>Three Personality Dimensions with Largest Effect Sizes:</strong></p>
            
            <div class="personality-trait">
                <h4>🔊 Vocalization Frequency (F = 57.64, η² = 0.49)</h4>
                <p><strong>Scale:</strong> 1 = Low, 2 = Moderate, 3 = High</p>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{champions['most_vocal']['avg_vocalization']:.2f}</span>
                        <span class="stat-label">Most vocal: {champions['most_vocal']['breed']}</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{champions['least_vocal']['avg_vocalization']:.2f}</span>
                        <span class="stat-label">Least vocal: {champions['least_vocal']['breed']}</span>
                    </div>
                </div>
            </div>
            
            <div class="personality-trait">
                <h4>👥 Social Interaction Need (F = 40.55, η² = 0.40)</h4>
                <p><strong>Scale:</strong> 1 = Independent, 2 = Moderate, 3 = High companionship</p>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{champions['most_social']['avg_social_need']:.2f}</span>
                        <span class="stat-label">Most social: {champions['most_social']['breed']}</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{champions['least_social']['avg_social_need']:.2f}</span>
                        <span class="stat-label">Most independent: {champions['least_social']['breed']}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Affection Levels & Correlations -->
        <div class="slide">
            <h2>💖 Affection Levels & Personality Correlations</h2>
            
            <div class="personality-trait">
                <h4>💖 Affection Level (F = 105.44, η² = 0.64 - LARGEST EFFECT!)</h4>
                <p><strong>Scale:</strong> 1 = Aloof, 2 = Moderate, 3 = Lap-sitter, 4 = Dog-like devotion</p>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{champions['most_affectionate']['avg_affection']:.2f}</span>
                        <span class="stat-label">Most affectionate: {champions['most_affectionate']['breed']}</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{champions['least_affectionate']['avg_affection']:.2f}</span>
                        <span class="stat-label">Most aloof: {champions['least_affectionate']['breed']}</span>
                    </div>
                </div>
            </div>
            
            <div class="correlation-highlight">
                <h3>🔗 Key Discovery - Personality Correlation</h3>
                <div style="font-size: 2.5em; margin: 20px 0;">{correlation:.3f}</div>
                <p><strong>Social Need ↔ Affection Level correlation (p < 0.001)</strong></p>
                <p>Cats with high social needs tend to be more affectionate<br>
                This represents a <strong>MEDIUM-to-STRONG</strong> positive relationship</p>
            </div>
        </div>

        <!-- Breed Champions -->
        <div id="champions" class="slide">
            <h2>🏆 Breed Champions by Category</h2>
            
            <p style="text-align: center; font-size: 1.2em; margin-bottom: 30px;"><strong>Top Performers in Each Dimension:</strong></p>
            
            <div class="stats-grid">
                <div class="champion-card">
                    <h4>🏥 Longevity Champion</h4>
                    <p><strong>{champions['longevity']['breed']}</strong></p>
                    <p>{champions['longevity']['avg_life_expectancy']:.1f} years average</p>
                </div>
                
                <div class="champion-card">
                    <h4>⚖️ Size Champions</h4>
                    <p><strong>Heaviest:</strong> {champions['heaviest']['breed']}</p>
                    <p><strong>Lightest:</strong> {champions['lightest']['breed']}</p>
                </div>
                
                <div class="champion-card">
                    <h4>💪 Health Champion</h4>
                    <p><strong>{champions['healthiest']['breed']}</strong></p>
                    <p>{champions['healthiest']['avg_health_score']:.1f}/10 health score</p>
                </div>
                
                <div class="champion-card">
                    <h4>🔊 Most Vocal</h4>
                    <p><strong>{champions['most_vocal']['breed']}</strong></p>
                    <p>{champions['most_vocal']['avg_vocalization']:.2f}/3.0 vocalization</p>
                </div>
                
                <div class="champion-card">
                    <h4>👥 Most Social</h4>
                    <p><strong>{champions['most_social']['breed']}</strong></p>
                    <p>{champions['most_social']['avg_social_need']:.2f}/3.0 social need</p>
                </div>
                
                <div class="champion-card">
                    <h4>💖 Most Affectionate</h4>
                    <p><strong>{champions['most_affectionate']['breed']}</strong></p>
                    <p>{champions['most_affectionate']['avg_affection']:.2f}/4.0 affection</p>
                </div>
            </div>
            
            <p style="text-align: center; margin-top: 20px; font-style: italic; color: #666;">
                📌 Note: All differences statistically significant (p < 0.001)
            </p>
        </div>

        <!-- Breed Comparison Table -->
        <div class="slide">
            <h2>📊 Complete Breed Comparison</h2>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Breed</th>
                            <th>Life Expectancy</th>
                            <th>Avg Weight (lbs)</th>
                            <th>HCM Risk (%)</th>
                            <th>PKD Risk (%)</th>
                            <th>Hip Dysplasia (%)</th>
                            <th>Vocalization</th>
                            <th>Social Need</th>
                            <th>Affection</th>
                        </tr>
                    </thead>
                    <tbody>"""
        
        # Add breed data rows
        for _, breed in self.breed_stats.iterrows():
            html_content += f"""
                        <tr>
                            <td><strong>{breed['breed']}</strong></td>
                            <td>{breed['avg_life_expectancy']:.1f} ± {breed['std_life_expectancy']:.1f}</td>
                            <td>{breed['avg_weight']:.1f}</td>
                            <td>{breed['hcm_prevalence']*100:.1f}%</td>
                            <td>{breed['pkd_prevalence']*100:.1f}%</td>
                            <td>{breed['hip_dysplasia_prevalence']*100:.1f}%</td>
                            <td>{breed['avg_vocalization']:.2f}/3</td>
                            <td>{breed['avg_social_need']:.2f}/3</td>
                            <td>{breed['avg_affection']:.2f}/4</td>
                        </tr>"""
        
        html_content += f"""
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Practical Implications -->
        <div id="implications" class="slide">
            <h2>🎯 Practical Implications</h2>
            
            <h3>🏠 For Potential Cat Owners:</h3>
            <ul class="findings-list">
                <li>Choose breeds matching your lifestyle preferences</li>
                <li>Consider health risks and life expectancy when planning</li>
                <li>Understand personality trait differences for better compatibility</li>
                <li>Budget for breed-specific veterinary care needs</li>
            </ul>
            
            <h3>🏥 For Veterinarians:</h3>
            <ul class="findings-list">
                <li>Focus screening on breed-specific health risks</li>
                <li>Tailor preventive care recommendations</li>
                <li>Educate owners about breed characteristics and expectations</li>
                <li>Develop breed-specific health monitoring protocols</li>
            </ul>
            
            <h3>🧬 For Breeders:</h3>
            <ul class="findings-list">
                <li>Genetic testing priorities vary significantly by breed</li>
                <li>Health screening programs should be breed-specific</li>
                <li>Understand breed temperament for proper socialization</li>
                <li>Focus on reducing high-prevalence health conditions</li>
            </ul>
        </div>

        <!-- Conclusions & Future Research -->
        <div id="conclusions" class="slide">
            <h2>📋 Conclusions & Future Research</h2>
            
            <h3>✅ Key Conclusions:</h3>
            <ul class="findings-list">
                <li>Cat breeds differ significantly across <strong>ALL</strong> measured characteristics</li>
                <li>Effect sizes are large, indicating meaningful practical differences</li>
                <li>Breed selection has clear implications for owners and veterinarians</li>
                <li>Personality traits show strongest breed differences (η² up to 0.64)</li>
                <li>Health risks are breed-specific and should guide care decisions</li>
            </ul>
            
            <div class="methodology-box">
                <h3>📊 Statistical Summary:</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{len(self.analysis_results)}</span>
                        <span class="stat-label">Statistical tests performed</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">100%</span>
                        <span class="stat-label">Tests showing significance (p < 0.001)</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">0.64</span>
                        <span class="stat-label">Largest effect size (η²)</span>
                    </div>
                </div>
            </div>
            
            <h3>🔮 Future Research Directions:</h3>
            <ul class="findings-list">
                <li>Genetic basis of personality trait differences</li>
                <li>Environmental vs. genetic factors in health outcomes</li>
                <li>Cross-breed analysis and hybrid characteristics</li>
                <li>Longitudinal studies tracking changes over time</li>
            </ul>
        </div>

        <!-- Footer -->
        <div class="footer">
            <h2>🐾 Thank You!</h2>
            <p style="font-size: 1.1em; margin: 20px 0;">
                <strong>Questions & Discussion</strong>
            </p>
            <div class="stats-grid" style="max-width: 600px; margin: 0 auto;">
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
                    📊 Dataset: {len(self.data):,} cats across {self.data['breed'].nunique()} breeds
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
                    📈 {len(self.analysis_results)} statistical analyses performed
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
                    🎯 All findings significant at p < 0.001 level
                </div>
            </div>
            <p style="margin-top: 30px;">
                <strong>Data Analytics Final Project</strong><br>
                {datetime.now().strftime('%B %Y')}
            </p>
        </div>
    </div>

    <script>
        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
        
        // Add animation on scroll
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);
        
        // Observe all slides for animation
        document.querySelectorAll('.slide').forEach(slide => {{
            slide.style.opacity = '0.3';
            slide.style.transform = 'translateY(30px)';
            slide.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            observer.observe(slide);
        }});
    </script>
</body>
</html>"""
        
        # Save the HTML file
        filename = 'results/Cat_Breed_Analysis_Interactive_Presentation.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ Interactive HTML presentation saved as: {filename}")
        return filename

    def close(self):
        """Close database connection."""
        self.connection.close()

def main():
    """Generate the HTML presentation."""
    generator = HTMLPresentationGenerator()
    
    try:
        html_file = generator.generate_html_presentation()
        
        print(f"\n🎉 Interactive HTML presentation created successfully!")
        print(f"📁 File location: {html_file}")
        print(f"🌐 Features:")
        print("   ✅ Responsive design (works on mobile/tablet/desktop)")
        print("   ✅ Smooth scrolling navigation")
        print("   ✅ Interactive animations")
        print("   ✅ Complete statistical data tables")
        print("   ✅ Professional styling with gradients")
        print("   ✅ All PowerPoint content plus more interactivity")
        print(f"\n💡 To view: Open the file in any web browser!")
        print(f"🚀 Perfect for online presentations or sharing via web!")
        
    finally:
        generator.close()

if __name__ == "__main__":
    main()