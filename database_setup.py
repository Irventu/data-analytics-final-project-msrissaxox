"""
SQLite Database Setup for Cat Breed Analysis
Creates and manages the database for storing cat breed data.
"""

import sqlite3
import pandas as pd
from datetime import datetime

class CatBreedDatabase:
    def __init__(self, db_path='cat_breed_analysis.db'):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """Create connection to SQLite database."""
        self.connection = sqlite3.connect(self.db_path)
        return self.connection
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
    
    def create_tables(self):
        """Create database tables for cat breed analysis."""
        cursor = self.connection.cursor()
        
        # Main cat data table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cats (
            cat_id INTEGER PRIMARY KEY,
            breed TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight_lbs REAL NOT NULL,
            life_expectancy REAL NOT NULL,
            has_hcm BOOLEAN NOT NULL,
            has_pkd BOOLEAN NOT NULL,
            has_hip_dysplasia BOOLEAN NOT NULL,
            vocalization_frequency INTEGER NOT NULL,
            social_interaction_need INTEGER NOT NULL,
            affection_level INTEGER NOT NULL,
            health_score INTEGER NOT NULL,
            total_personality_score INTEGER NOT NULL,
            weight_category TEXT NOT NULL,
            age_category TEXT NOT NULL,
            data_collection_date TEXT NOT NULL
        )
        ''')
        
        # Breed summary statistics table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS breed_statistics (
            breed TEXT PRIMARY KEY,
            avg_life_expectancy REAL,
            std_life_expectancy REAL,
            min_life_expectancy REAL,
            max_life_expectancy REAL,
            avg_weight REAL,
            std_weight REAL,
            hcm_prevalence REAL,
            pkd_prevalence REAL,
            hip_dysplasia_prevalence REAL,
            avg_vocalization REAL,
            avg_social_need REAL,
            avg_affection REAL,
            avg_health_score REAL,
            sample_size INTEGER,
            last_updated TEXT
        )
        ''')
        
        # Analysis results table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_type TEXT NOT NULL,
            test_statistic REAL,
            p_value REAL,
            effect_size REAL,
            degrees_freedom INTEGER,
            variables_tested TEXT,
            result_interpretation TEXT,
            analysis_date TEXT NOT NULL
        )
        ''')
        
        self.connection.commit()
        print("Database tables created successfully.")
    
    def load_data_from_csv(self, csv_path='cat_breed_dataset.csv'):
        """Load cat data from CSV file into database."""
        try:
            df = pd.read_csv(csv_path)
            
            # Clear existing data
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM cats")
            
            # Insert new data
            df.to_sql('cats', self.connection, if_exists='replace', index=False)
            
            print(f"Loaded {len(df)} records into cats table.")
            return df
            
        except FileNotFoundError:
            print(f"Error: {csv_path} not found. Please generate the dataset first.")
            return None
    
    def update_breed_statistics(self, df):
        """Calculate and store breed-level statistics."""
        cursor = self.connection.cursor()
        
        # Clear existing statistics
        cursor.execute("DELETE FROM breed_statistics")
        
        # Calculate statistics by breed
        breed_stats = df.groupby('breed').agg({
            'life_expectancy': ['mean', 'std', 'min', 'max'],
            'weight_lbs': ['mean', 'std'],
            'has_hcm': 'mean',
            'has_pkd': 'mean',
            'has_hip_dysplasia': 'mean',
            'vocalization_frequency': 'mean',
            'social_interaction_need': 'mean',
            'affection_level': 'mean',
            'health_score': 'mean',
            'cat_id': 'count'
        }).round(4)
        
        # Insert breed statistics
        for breed in breed_stats.index:
            stats = breed_stats.loc[breed]
            cursor.execute('''
            INSERT INTO breed_statistics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                breed,
                stats[('life_expectancy', 'mean')],
                stats[('life_expectancy', 'std')],
                stats[('life_expectancy', 'min')],
                stats[('life_expectancy', 'max')],
                stats[('weight_lbs', 'mean')],
                stats[('weight_lbs', 'std')],
                stats[('has_hcm', 'mean')],
                stats[('has_pkd', 'mean')],
                stats[('has_hip_dysplasia', 'mean')],
                stats[('vocalization_frequency', 'mean')],
                stats[('social_interaction_need', 'mean')],
                stats[('affection_level', 'mean')],
                stats[('health_score', 'mean')],
                int(stats[('cat_id', 'count')]),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
        
        self.connection.commit()
        print("Breed statistics updated successfully.")
    
    def save_analysis_result(self, analysis_type, test_stat, p_value, 
                           effect_size=None, df=None, variables="", interpretation=""):
        """Save statistical analysis results to database."""
        cursor = self.connection.cursor()
        
        cursor.execute('''
        INSERT INTO analysis_results 
        (analysis_type, test_statistic, p_value, effect_size, degrees_freedom, 
         variables_tested, result_interpretation, analysis_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_type,
            test_stat,
            p_value,
            effect_size,
            df,
            variables,
            interpretation,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        self.connection.commit()
    
    def get_breed_statistics(self):
        """Retrieve breed statistics from database."""
        return pd.read_sql_query("SELECT * FROM breed_statistics", self.connection)
    
    def get_analysis_results(self):
        """Retrieve all analysis results from database."""
        return pd.read_sql_query("SELECT * FROM analysis_results", self.connection)
    
    def get_cat_data(self, breed=None):
        """Retrieve cat data, optionally filtered by breed."""
        if breed:
            query = "SELECT * FROM cats WHERE breed = ?"
            return pd.read_sql_query(query, self.connection, params=(breed,))
        else:
            return pd.read_sql_query("SELECT * FROM cats", self.connection)

def setup_database():
    """Initialize database with cat breed data."""
    db = CatBreedDatabase()
    db.connect()
    
    print("Setting up cat breed analysis database...")
    db.create_tables()
    
    # Load data from CSV
    df = db.load_data_from_csv()
    
    if df is not None:
        # Update breed statistics
        db.update_breed_statistics(df)
        
        print(f"\nDatabase setup complete!")
        print(f"Database location: {db.db_path}")
        print(f"Total cats: {len(df)}")
        print(f"Breeds: {df['breed'].nunique()}")
        
        # Show sample data
        breed_stats = db.get_breed_statistics()
        print(f"\nBreed statistics table shape: {breed_stats.shape}")
        print(breed_stats.head())
    
    db.close()
    return db.db_path

if __name__ == "__main__":
    setup_database()