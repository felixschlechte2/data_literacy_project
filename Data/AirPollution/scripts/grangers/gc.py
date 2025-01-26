from statsmodels.tsa.stattools import adfuller, grangercausalitytests
import pandas as pd
import numpy as np
import seaborn as sns

def test_stationarity(series):
    """Perform the Augmented Dickey-Fuller (ADF) test for stationarity."""
    result = adfuller(series)
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    print("Stationary" if result[1] < 0.05 else "Non-stationary")
    return result[1] < 0.05

def granger_causality_analysis(data, max_lag=5):
    """Perform Granger causality tests on time series data."""
    print("\nRunning Granger Causality Test...")
    result = grangercausalitytests(data, max_lag, verbose=True)
    return result

def process_data(party, pollutant, offset):
    election_data = pd.read_csv('../../../election_data.csv')
    pollutant_data = pd.read_csv(f'../../../AirPollution/processed/{pollutant}.csv')
    pollutant_data = pollutant_data[['Air Quality Station EoI Code', 'Year', 'Normalized Difference', 'City']]
    pollutant_data = pollutant_data.groupby(['Air Quality Station EoI Code', 'Year', 'City'], as_index=False).mean()

    data = pd.merge(election_data, pollutant_data, left_on=['City', 'Date'], right_on=['City', 'Year'])

    data = data[['Air Quality Station EoI Code', party, 'Date', 'Normalized Difference', 'City']]

    data = data[data[party] != 0]
    data['Date'] = pd.to_numeric(data['Date'])

    x = []
    y = []

    for index, row in data.iterrows():
        station = row['Air Quality Station EoI Code']
        year = row['Date']
        if pollutant_data[(pollutant_data['Air Quality Station EoI Code'] == station) & (pollutant_data['Year'] == year + offset)].any()['Normalized Difference'] and year + offset < 2025:
            election_result = row[party]
            pollution_before = row['Normalized Difference']
            pollution_after = pollutant_data[(pollutant_data['Air Quality Station EoI Code'] == station) & (pollutant_data['Year'] == year + offset)]['Normalized Difference'].values[0]
            pollution_change = pollution_before
            x.append(election_result)
            y.append(pollution_change)
            
    return np.array(x), np.array(y)

offset=5
parties = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']
# parties = ['Linke', 'SPD',]
pollutants = ['CO', 'NO2', 'O3', 'PM10', 'SO2']
# pollutants = ['PM10']

import matplotlib.pyplot as plt
import seaborn as sns

def granger_causality_summary(granger_results, max_lag):
    """Extract the minimum p-value across lags for Granger causality tests."""
    return min(granger_results[lag][0]['ssr_ftest'][1] for lag in range(1, max_lag + 1))

# Initialize variables for heatmap
summary_data = []

# Figure for combined plots
fig, axes = plt.subplots(len(pollutants), len(parties), figsize=(20, 15), constrained_layout=True)

max_lag = 5
for i, pollutant in enumerate(pollutants):
    heatmap_row = []
    for j, party in enumerate(parties):
        x, y = process_data(party, pollutant, offset)
        combined_data = pd.concat([pd.Series(x, name='party'), pd.Series(y, name='pollutant')], axis=1).dropna()

        try:
            # Perform Granger causality test
            granger_results = granger_causality_analysis(combined_data, max_lag=max_lag)

            # Extract p-values for plotting
            p_values = [granger_results[lag][0]['ssr_ftest'][1] for lag in range(1, max_lag + 1)]
            f_stats = [granger_results[lag][0]['ssr_ftest'][0] for lag in range(1, max_lag + 1)]

            # Plot p-values
            ax = axes[i, j]
            ax.bar(range(1, max_lag + 1), p_values, color='skyblue', alpha=0.7)
            ax.axhline(y=0.05, color='r', linestyle='--', label='p=0.05')
            ax.set_title(f'{party} -> {pollutant}', fontsize=10)
            ax.set_xlabel('Lag')
            ax.set_ylabel('p-value')
            ax.set_xticks(range(1, max_lag + 1))
            ax.legend(fontsize=8)

            # Heatmap data: whether Granger causality is significant
            min_p_value = min(p_values)
            heatmap_row.append(min_p_value < 0.05)  # True if significant
        except Exception as e:
            print(f"Error processing {party} and {pollutant}: {e}")
            heatmap_row.append(False)  # No causality if an error occurs

    summary_data.append(heatmap_row)

# Save the combined plots
plt.suptitle('Granger Causality: P-Values for Party -> Pollutant', fontsize=16)
plt.savefig('granger_causality_plots.png', dpi=300)
plt.close()

# Create a heatmap
summary_df = pd.DataFrame(summary_data, columns=parties, index=pollutants)
plt.figure(figsize=(10, 8))
sns.heatmap(summary_df, annot=True, cmap='coolwarm', cbar=False, 
            xticklabels=parties, yticklabels=pollutants, linewidths=0.5)
plt.title('Granger Causality Significance (p < 0.05)', fontsize=16)
plt.xlabel('Political Party')
plt.ylabel('Pollutant')
plt.savefig('granger_causality_heatmap.png', dpi=300)
plt.close()