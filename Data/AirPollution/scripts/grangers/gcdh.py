import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

def create_balanced_panel(df):
    """Create balanced panel with backfilled election data"""
    # Identify party columns
    party_cols = [col for col in df.columns if col not in ['city', 'year', 'pollution']]
    
    # Determine time window
    start_year = df[df['year'].between(1998, 2004)]['year'].value_counts().idxmax()
    end_year = df[df['year'].between(2020, 2024)]['year'].value_counts().idxmax()
    
    # Create balanced panel
    balanced = df.set_index(['city', 'year']).unstack().reindex(
        columns=pd.MultiIndex.from_product([df.columns, range(start_year, end_year+1)])
    ).stack().swaplevel().sort_index()
    
    # Backfill party data within cities
    for party in party_cols:
        balanced[party] = balanced.groupby('city')[party].bfill()
    
    # Remove cities with missing data
    initial_cities = balanced.index.get_level_values('city').nunique()
    balanced = balanced.groupby('city').filter(lambda x: x[party_cols].notna().all().all())
    final_cities = balanced.index.get_level_values('city').nunique()
    
    return balanced, initial_cities - final_cities

def check_stationarity(df, var_list):
    """Check stationarity of variables and their first differences"""
    results = {}
    for var in var_list:
        # Original series
        stationarity = df.groupby('city')[var].apply(
            lambda x: adfuller(x.dropna())[1] < 0.05
        ).mean()
        
        # First difference
        diff_stationarity = df.groupby('city')[var].apply(
            lambda x: adfuller(x.diff().dropna())[1] < 0.05
        ).mean()
        
        results[var] = (stationarity, diff_stationarity)
    return results

def dh_granger_test(df, cause_vars, effect_var, max_lag=2):
    """Dumitrescu-Hurlin panel Granger causality test with Z-tilde statistic"""
    wald_stats = []
    cities = df.index.get_level_values('city').unique()
    
    for city in cities:
        city_data = df.xs(city, level='city').dropna()
        if len(city_data) > max_lag + 5:  # Ensure sufficient observations
            for party in cause_vars:
                try:
                    test_result = grangercausalitytests(
                        city_data[[effect_var, party]], 
                        maxlag=max_lag, 
                        verbose=False
                    )
                    wald_stat = test_result[max_lag][0]['ssr_ftest'][0]
                    wald_stats.append(wald_stat)
                except:
                    continue
    
    if not wald_stats:
        return None, None
    
    N = len(cities)
    T = len(df.index.get_level_values('year').unique())
    K = max_lag
    
    # Calculate Z-tilde statistic
    W_bar = np.mean(wald_stats)
    z_tilde = (np.sqrt(N/(2*K)) * 
              ((T - 3*K - 5)/(T - 2*K - 3)) * 
              np.sqrt((T - 3*K - 3)/(T - 3*K - 1)) * 
              (W_bar - K))
    
    return z_tilde, W_bar

# Sample data creation (replace with your actual data)
data = {
    'city': ['A']*5 + ['B']*5 + ['C']*5,
    'year': list(range(2000, 2005))*3,
    'pollution': np.random.normal(50, 10, 15),
    'party1': np.random.uniform(20, 60, 15),
    'party2': np.random.uniform(10, 50, 15),
    'party3': np.random.uniform(5, 40, 15)
}
df = pd.DataFrame(data)

# 1. Create balanced panel
balanced_df, cities_discarded = create_balanced_panel(df)
print(f'Cities discarded: {cities_discarded}\n')

# 2. Stationarity checks
variables = ['pollution'] + [col for col in df.columns if col.startswith('party')]
stationarity = check_stationarity(balanced_df, variables)

print('Stationarity Results:')
for var, (orig, diff) in stationarity.items():
    print(f'{var}:')
    print(f'  Original: {orig:.1%} stationary')
    print(f'  Differenced: {diff:.1%} stationary\n')

# 3. DH Granger causality test
party_cols = [col for col in df.columns if col.startswith('party')]
z_tilde, W_bar = dh_granger_test(balanced_df, party_cols, 'pollution')

print('\nGranger Causality Results:')
print(f'Average Wald statistic: {W_bar:.2f}')
print(f'Z-tilde statistic: {z_tilde:.2f}')

if z_tilde > 1.645:
    print('Conclusion: Reject H0 - Granger causality exists')
else:
    print('Conclusion: No Granger causality detected')
