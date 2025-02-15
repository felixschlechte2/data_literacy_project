import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

import pandas as pd

def classify_cities_by_data_length(panel_df, min_obs=9):
    """Classify cities based on observation counts for each variable
    
    Args:
        panel_df: DataFrame with CityStation, Year, and variable columns
        min_obs: Minimum required observations (9-30 based on literature[1][3][22])
    
    Returns:
        CSV-ready DataFrame with classification
    """
    variables = ['Average'] + [col for col in panel_df.columns 
                             if col in ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']]
    
    # Count valid observations per city-variable pair
    obs_counts = (panel_df.groupby('CityStation')[variables]
                  .apply(lambda x: x.count()))
    
    # Melt to long format and classify
    melted = obs_counts.reset_index().melt(id_vars='CityStation', 
                                         var_name='Variable',
                                         value_name='ObsCount')
    
    melted['DataStatus'] = melted['ObsCount'].apply(
        lambda x: 'Sufficient' if x >= min_obs else 'Insufficient'
    )
    
    return melted

def test_stationarity(series, max_diff=1):
    """Perform the Augmented Dickey-Fuller (ADF) test for stationarity."""
    series = series.dropna()
    
    if len(series) < 5:  # Reduce minimum required data points
        print(f"Skipping ADF test: Series too short ({len(series)} observations).")
        return False, series

    if series.nunique() == 1:  # Check for constant series
        print("Series is constant, skipping ADF test.")
        return False, series
    
    # Try differencing if non-stationary
    for _ in range(max_diff + 1):
        result = adfuller(series)
        if result[1] < 0.05:
            print("Stationary")
            return True, series  # Series is now stationary
        else:
            return False, series

    print("Non-stationary after differencing")
    return False, series  # Still non-stationary after max_diff attempts

def dh_granger_test(panel_df, max_lag=2):
    """Dumitrescu-Hurlin panel Granger causality test with Z̃ statistic"""
    non_stationary_count = 0
    results = {}
    parties = [col for col in panel_df.columns 
              if col in ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']]
    
    for party in parties:
        wald_stats = []
        cities = panel_df['CityStation'].unique()
        
        for city in cities:
            city_data = panel_df[panel_df['CityStation'] == city][['Average', party]].dropna()
            if len(city_data) > max_lag + 5:  # Ensure sufficient observations
                is_stationary, transformed_series = test_stationarity(city_data[party])
                is_stationary_pollution, transformed_pollution = test_stationarity(city_data['Average'])
                # city_data[party] = transformed_series
                # city_data['Average'] = transformed_pollution
                if not is_stationary or not is_stationary_pollution:
                    non_stationary_count += 1
                    continue

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
    panel_df = pd.read_csv('./BalancedPanelPM10.csv')
    print(panel_df.head())
    # Usage
    # city_data_classification = classify_cities_by_data_length(panel_df, min_obs=9)

    # Export to CSV
    # city_data_classification.to_csv('city_stationarity_data_status.csv', index=False)

    # 1. Stationarity Analysis
    # stationarity = stationarity_analysis(panel_df)
    # print("Stationarity Results (% of cities with stationary series):")
    # for var in stationarity['Original']:
    #     print(f"\n{var}:")
    #     print(f"  Original Series: {stationarity['Original'][var]:.1%}")
    #     print(f"  First Difference: {stationarity['Differenced'][var]:.1%}")
    
    # 2. Granger Causality Analysis
    print("\n\nGranger Causality Results (5% significance level):")
    granger_results = dh_granger_test(panel_df)
    for test, res in granger_results.items():
        print(f"\n{test}:")
        print(f"  Z̃ statistic = {res['Z̃']:.2f}")
        print(f"  Conclusion: {res['Conclusion']}")
