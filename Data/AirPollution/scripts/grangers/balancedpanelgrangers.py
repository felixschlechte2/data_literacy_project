import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

def stationarity_analysis(panel_df):
    """Analyze stationarity of variables in balanced panel"""
    results = {'Original': {}, 'Differenced': {}}
    variables = ['Air Pollution Level'] + [col for col in panel_df.columns 
                                          if col in ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']]
    
    for var in variables:
        # Original series stationarity
        results['Original'][var] = panel_df.groupby('City')[var].apply(
            lambda x: adfuller(x.dropna())[1] < 0.05  # True if stationary
        ).mean()
        
        # First-difference stationarity
        results['Differenced'][var] = panel_df.groupby('City')[var].apply(
            lambda x: adfuller(x.diff().dropna())[1] < 0.05
        ).mean()
    
    return results

def dh_granger_test(panel_df, max_lag=2):
    """Dumitrescu-Hurlin panel Granger causality test with Z̃ statistic"""
    results = {}
    parties = [col for col in panel_df.columns 
              if col in ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']]
    
    for party in parties:
        wald_stats = []
        cities = panel_df['City'].unique()
        
        for city in cities:
            city_data = panel_df[panel_df['City'] == city][['Air Pollution Level', party]].dropna()
            if len(city_data) > max_lag + 5:  # Ensure sufficient observations
                try:
                    test_result = grangercausalitytests(city_data, maxlag=max_lag, verbose=False)
                    wald_stat = test_result[max_lag][0]['ssr_ftest'][0]
                    wald_stats.append(wald_stat)
                except:
                    continue
        
        if not wald_stats:
            results[f"{party} -> Pollution"] = {'Z̃': np.nan, 'Conclusion': 'Insufficient data'}
            continue
            
        N = len(wald_stats)  # Number of cities with valid tests
        T = panel_df['Year'].nunique()  # Time periods
        K = max_lag  # Number of lags
        
        # Calculate Z̃ statistic (Dumitrescu-Hurlin 2012)
        W_bar = np.mean(wald_stats)
        z_tilde = (np.sqrt(N/(2*K)) * 
                  ((T - 3*K - 5)/(T - 2*K - 3)) * 
                  np.sqrt((T - 3*K - 3)/(T - 3*K - 1)) * 
                  (W_bar - K))
        
        results[f"{party} -> Pollution"] = {
            'Z̃': z_tilde,
            'Conclusion': 'Significant' if z_tilde > 1.645 else 'Not significant'
        }
    
    return results

if __name__ == "__main__":
    # Assuming you have a DataFrame called panel_df with:
    # Columns: City, Year, Air Pollution Level, Linke, Gruene, SPD, FDP, CDU, AfD
    
    # Sample data structure if panel_df not available
    panel_df = pd.DataFrame({
        'City': ['City1']*10 + ['City2']*10,
        'Year': list(range(2013, 2023))*2,
        'Air Pollution Level': np.random.normal(50, 5, 20),
        'Linke': np.random.uniform(5, 25, 20),
        'Gruene': np.random.uniform(10, 30, 20),
        'SPD': np.random.uniform(20, 40, 20),
        'FDP': np.random.uniform(5, 15, 20),
        'CDU': np.random.uniform(25, 45, 20),
        'AfD': np.random.uniform(5, 20, 20)
    })
    
    # 1. Stationarity Analysis
    stationarity = stationarity_analysis(panel_df)
    print("Stationarity Results (% of cities with stationary series):")
    for var in stationarity['Original']:
        print(f"\n{var}:")
        print(f"  Original Series: {stationarity['Original'][var]:.1%}")
        print(f"  First Difference: {stationarity['Differenced'][var]:.1%}")
    
    # 2. Granger Causality Analysis
    print("\n\nGranger Causality Results (5% significance level):")
    granger_results = dh_granger_test(panel_df)
    for test, res in granger_results.items():
        print(f"\n{test}:")
        print(f"  Z̃ statistic = {res['Z̃']:.2f}")
        print(f"  Conclusion: {res['Conclusion']}")
