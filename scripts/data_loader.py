"""
Standardized data loading and cleaning for NASA POWER climate data.
"""
import pandas as pd
import numpy as np

def load_and_clean_country(country_name, data_dir="data"):
    """Load and clean NASA POWER data for one country."""
    df = pd.read_csv(f"{data_dir}/{country_name}.csv")
    df['Country'] = country_name.capitalize()
    df['Date'] = pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df.replace(-999, np.nan, inplace=True)
    
    missing = df.isna().sum()
    missing_pct = (missing / len(df)) * 100
    print(f"\n{country_name.upper()} - Shape: {df.shape}")
    print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"Missing > 1%: {missing_pct[missing_pct > 1].to_dict()}")
    print(f"Duplicates: {df.duplicated().sum()}")
    
    return df

def check_missing_values(df):
    """Return missing value report."""
    missing = df.isna().sum()
    missing_pct = (missing / len(df)) * 100
    report = pd.DataFrame({'Missing_Count': missing, 'Missing_Pct': missing_pct})
    return report[report['Missing_Count'] > 0].sort_values('Missing_Pct', ascending=False)
