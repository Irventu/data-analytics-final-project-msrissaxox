"""
Cat Breed Data Generator
Creates a comprehensive dataset of top 10 cat breeds with health, physiology, and personality metrics.
Based on veterinary literature and breed standards from CFA, TICA, and scientific studies.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Top 10 most popular cat breeds (based on CFA registration data)
TOP_BREEDS = [
    "Persian", "Maine Coon", "British Shorthair", "Ragdoll", "Bengal", 
    "Abyssinian", "Siamese", "Scottish Fold", "Russian Blue", "American Shorthair"
]

# Base breed characteristics (from veterinary and breed registry data)
BREED_CHARACTERISTICS = {
    "Persian": {
        "avg_lifespan": 12.5, "lifespan_std": 1.8,
        "male_weight_avg": 11.0, "male_weight_std": 1.5,
        "female_weight_avg": 8.5, "female_weight_std": 1.2,
        "hcm_prevalence": 0.06, "pkd_prevalence": 0.38, "hip_dysplasia_prevalence": 0.02,
        "vocalization": "Low", "social_need": "Moderate", "affection": "Lap-sitter"
    },
    "Maine Coon": {
        "avg_lifespan": 13.2, "lifespan_std": 1.9,
        "male_weight_avg": 16.0, "male_weight_std": 2.2,
        "female_weight_avg": 11.5, "female_weight_std": 1.8,
        "hcm_prevalence": 0.10, "pkd_prevalence": 0.02, "hip_dysplasia_prevalence": 0.18,
        "vocalization": "Moderate", "social_need": "High", "affection": "Dog-like"
    },
    "British Shorthair": {
        "avg_lifespan": 14.8, "lifespan_std": 2.1,
        "male_weight_avg": 13.0, "male_weight_std": 1.8,
        "female_weight_avg": 9.5, "female_weight_std": 1.4,
        "hcm_prevalence": 0.08, "pkd_prevalence": 0.01, "hip_dysplasia_prevalence": 0.03,
        "vocalization": "Low", "social_need": "Independent", "affection": "Moderate"
    },
    "Ragdoll": {
        "avg_lifespan": 13.8, "lifespan_std": 1.7,
        "male_weight_avg": 15.5, "male_weight_std": 2.0,
        "female_weight_avg": 11.0, "female_weight_std": 1.6,
        "hcm_prevalence": 0.12, "pkd_prevalence": 0.01, "hip_dysplasia_prevalence": 0.04,
        "vocalization": "Low", "social_need": "High", "affection": "Dog-like"
    },
    "Bengal": {
        "avg_lifespan": 14.2, "lifespan_std": 1.6,
        "male_weight_avg": 12.5, "male_weight_std": 1.7,
        "female_weight_avg": 8.0, "female_weight_std": 1.3,
        "hcm_prevalence": 0.05, "pkd_prevalence": 0.06, "hip_dysplasia_prevalence": 0.02,
        "vocalization": "High", "social_need": "High", "affection": "Dog-like"
    },
    "Abyssinian": {
        "avg_lifespan": 13.5, "lifespan_std": 1.8,
        "male_weight_avg": 10.5, "male_weight_std": 1.4,
        "female_weight_avg": 8.0, "female_weight_std": 1.1,
        "hcm_prevalence": 0.04, "pkd_prevalence": 0.03, "hip_dysplasia_prevalence": 0.01,
        "vocalization": "Moderate", "social_need": "High", "affection": "Dog-like"
    },
    "Siamese": {
        "avg_lifespan": 15.1, "lifespan_std": 2.0,
        "male_weight_avg": 10.0, "male_weight_std": 1.3,
        "female_weight_avg": 7.5, "female_weight_std": 1.0,
        "hcm_prevalence": 0.03, "pkd_prevalence": 0.02, "hip_dysplasia_prevalence": 0.01,
        "vocalization": "High", "social_need": "High", "affection": "Dog-like"
    },
    "Scottish Fold": {
        "avg_lifespan": 13.0, "lifespan_std": 1.9,
        "male_weight_avg": 11.5, "male_weight_std": 1.6,
        "female_weight_avg": 8.5, "female_weight_std": 1.3,
        "hcm_prevalence": 0.07, "pkd_prevalence": 0.02, "hip_dysplasia_prevalence": 0.15,
        "vocalization": "Low", "social_need": "Moderate", "affection": "Lap-sitter"
    },
    "Russian Blue": {
        "avg_lifespan": 15.8, "lifespan_std": 1.8,
        "male_weight_avg": 10.5, "male_weight_std": 1.4,
        "female_weight_avg": 7.5, "female_weight_std": 1.1,
        "hcm_prevalence": 0.02, "pkd_prevalence": 0.01, "hip_dysplasia_prevalence": 0.01,
        "vocalization": "Low", "social_need": "Independent", "affection": "Aloof"
    },
    "American Shorthair": {
        "avg_lifespan": 15.2, "lifespan_std": 1.9,
        "male_weight_avg": 12.0, "male_weight_std": 1.6,
        "female_weight_avg": 9.0, "female_weight_std": 1.3,
        "hcm_prevalence": 0.05, "pkd_prevalence": 0.01, "hip_dysplasia_prevalence": 0.02,
        "vocalization": "Moderate", "social_need": "Moderate", "affection": "Moderate"
    }
}

def generate_cat_data(num_samples_per_breed=55):
    """Generate realistic cat data based on breed characteristics."""
    all_data = []
    
    for breed in TOP_BREEDS:
        chars = BREED_CHARACTERISTICS[breed]
        
        for _ in range(num_samples_per_breed):
            # Generate individual cat data with realistic variation
            gender = random.choice(['Male', 'Female'])
            
            # Age affects some characteristics
            age = max(1, int(np.random.normal(6, 2.5)))  # Age in years
            
            # Life expectancy with slight variation based on age
            life_expectancy = max(8, np.random.normal(chars['avg_lifespan'], chars['lifespan_std']))
            
            # Weight based on gender
            if gender == 'Male':
                weight = max(4, np.random.normal(chars['male_weight_avg'], chars['male_weight_std']))
            else:
                weight = max(3, np.random.normal(chars['female_weight_avg'], chars['female_weight_std']))
            
            # Health conditions (binary: has condition or not)
            has_hcm = np.random.random() < chars['hcm_prevalence']
            has_pkd = np.random.random() < chars['pkd_prevalence']
            has_hip_dysplasia = np.random.random() < chars['hip_dysplasia_prevalence']
            
            # Convert categorical variables to numerical for analysis
            vocalization_map = {'Low': 1, 'Moderate': 2, 'High': 3}
            social_need_map = {'Independent': 1, 'Moderate': 2, 'High': 3}
            affection_map = {'Aloof': 1, 'Moderate': 2, 'Lap-sitter': 3, 'Dog-like': 4}
            
            vocalization_score = vocalization_map[chars['vocalization']]
            social_need_score = social_need_map[chars['social_need']]
            affection_score = affection_map[chars['affection']]
            
            # Add some individual variation to personality traits
            vocalization_score += np.random.randint(-1, 2)
            social_need_score += np.random.randint(-1, 2)
            affection_score += np.random.randint(-1, 2)
            
            # Ensure scores stay in valid range
            vocalization_score = max(1, min(3, vocalization_score))
            social_need_score = max(1, min(3, social_need_score))
            affection_score = max(1, min(4, affection_score))
            
            cat_data = {
                'cat_id': len(all_data) + 1,
                'breed': breed,
                'gender': gender,
                'age': age,
                'weight_lbs': round(weight, 1),
                'life_expectancy': round(life_expectancy, 1),
                'has_hcm': has_hcm,
                'has_pkd': has_pkd,
                'has_hip_dysplasia': has_hip_dysplasia,
                'vocalization_frequency': vocalization_score,  # 1=Low, 2=Moderate, 3=High
                'social_interaction_need': social_need_score,  # 1=Independent, 2=Moderate, 3=High
                'affection_level': affection_score,  # 1=Aloof, 2=Moderate, 3=Lap-sitter, 4=Dog-like
                'data_collection_date': datetime.now().strftime('%Y-%m-%d')
            }
            
            all_data.append(cat_data)
    
    return pd.DataFrame(all_data)

def add_calculated_fields(df):
    """Add calculated fields for analysis."""
    # Health score (inverse of health issues)
    df['health_score'] = 10 - (df['has_hcm'].astype(int) * 4 + 
                               df['has_pkd'].astype(int) * 3 + 
                               df['has_hip_dysplasia'].astype(int) * 3)
    
    # Total personality score
    df['total_personality_score'] = (df['vocalization_frequency'] + 
                                   df['social_interaction_need'] + 
                                   df['affection_level'])
    
    # Weight category
    df['weight_category'] = pd.cut(df['weight_lbs'], 
                                 bins=[0, 8, 12, float('inf')], 
                                 labels=['Small', 'Medium', 'Large'])
    
    # Age category
    df['age_category'] = pd.cut(df['age'], 
                              bins=[0, 3, 7, float('inf')], 
                              labels=['Young', 'Adult', 'Senior'])
    
    return df

def generate_breed_summary_stats(df):
    """Generate breed-level summary statistics."""
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
        'cat_id': 'count'  # Sample size
    }).round(3)
    
    # Flatten column names
    breed_stats.columns = [f'{col[0]}_{col[1]}' if col[1] else col[0] 
                          for col in breed_stats.columns]
    
    return breed_stats

if __name__ == "__main__":
    print("Generating cat breed dataset...")
    
    # Generate main dataset
    cat_df = generate_cat_data(55)  # 55 cats per breed = 550 total
    cat_df = add_calculated_fields(cat_df)
    
    print(f"Generated {len(cat_df)} cat records across {cat_df['breed'].nunique()} breeds")
    print(f"Dataset shape: {cat_df.shape}")
    print("\nBreed distribution:")
    print(cat_df['breed'].value_counts())
    
    # Generate summary statistics
    breed_summary = generate_breed_summary_stats(cat_df)
    
    # Save datasets
    cat_df.to_csv('cat_breed_dataset.csv', index=False)
    breed_summary.to_csv('breed_summary_stats.csv', index=True)
    
    print("\nDataset saved as 'cat_breed_dataset.csv'")
    print("Summary statistics saved as 'breed_summary_stats.csv'")
    
    # Display basic info
    print("\nDataset Info:")
    print(cat_df.info())
    print("\nFirst few rows:")
    print(cat_df.head())