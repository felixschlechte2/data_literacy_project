import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
import os
import geopandas as gpd

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
        series = series.diff().dropna()  # Apply differencing

    print("Non-stationary after differencing")
    return False, series  # Still non-stationary after max_diff attempts

def process_data(party, pollutant, offset=1):
    """Process election & pollution data for Granger causality analysis."""
    
    # Load election and pollution data
    election_data = pd.read_csv('../../../analysis_felix/filled_elec.csv')
    pollutant_data = pd.read_csv(f'../../../AirPollution/processed/{pollutant}.csv')
    election_data['Date'] = pd.to_numeric(election_data['Date'])
    pollutant_data['Year'] = pd.to_numeric(pollutant_data['Year'])
    pollutant_data = pollutant_data[['City', 'State', 'Year', 'Air Pollution Level']]
    
    # Aggregate pollution data at the city-year level
    pollutant_data = pollutant_data.groupby(['City', 'State', 'Year'], as_index=False).mean()

    # Merge on city and year (ensure election 'Date' matches pollution 'Year')
    data = pd.merge(election_data, pollutant_data, left_on=['City', 'State', 'Date'], right_on=['City', 'State', 'Year'])

    # Select relevant columns
    data = data[['City', 'Year', party, 'Air Pollution Level']]

    # Lag pollution data by offset years
    data['Pollution Next Year'] = data.groupby('City')['Air Pollution Level'].shift(-offset)

    data['Pollution Diff'] = data['Pollution Next Year'] - data['Air Pollution Level']

    # Drop rows with NaN pollution levels (because of shifting)
    data = data.dropna()

    return data

def granger_causality_summary(granger_results, max_lag):
    """Extract the minimum p-value across lags for Granger causality tests."""
    return min(granger_results[lag][0]['ssr_ftest'][1] for lag in range(1, max_lag + 1))

# === Main Analysis Loop ===
offset = 1  # Check causality with a 1-year gap
parties = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']
pollutants = ['NO2', 'O3', 'PM10']

summary_data = []
output_dir = "granger_results"
os.makedirs(output_dir, exist_ok=True)

fig, axes = plt.subplots(len(pollutants), len(parties), figsize=(20, 15), constrained_layout=True)
max_lag = 3  # Maximum lag to consider

# Store information about skipped cities and successful analyses
city_skip_info = []

for i, pollutant in enumerate(pollutants):
    heatmap_row = []
    for j, party in enumerate(parties):
        data = process_data(party, pollutant, offset)
        
        if data.shape[0] < max_lag:
            print(f"Skipping {party} -> {pollutant} due to insufficient data.")
            heatmap_row.append(0)  # 0 indicates skipped due to insufficient data
            city_skip_info.append(f"{party} -> {pollutant}: Skipped (Insufficient data)")
            continue
        
        city_results = []
        non_stationary_count, insufficient_data_count = 0, 0
        significant_cities_count = 0
        non_significant_cities_count = 0

        for city, city_data in data.groupby('City'):
            if city_data.shape[0] < 3:  # Reduce required observations
                insufficient_data_count += 1
                continue  
            
            # Test for stationarity and get transformed series if needed
            is_stationary, transformed_series = test_stationarity(city_data[party])
            is_stationary_pollution, transformed_pollution = test_stationarity(city_data['Air Pollution Level'])
            
            if not is_stationary or not is_stationary_pollution:
                non_stationary_count += 1
                continue
            
            # Run Granger Causality Test
            try:
                granger_results = grangercausalitytests(city_data[[party, 'Air Pollution Level']], max_lag, verbose=False)
                p_values = [granger_results[lag][0]['ssr_ftest'][1] for lag in range(1, max_lag + 1)]
                min_p_value = min(p_values)
                city_results.append((city, min_p_value))
                
                if min_p_value < 0.05:
                    significant_cities_count += 1
                else:
                    non_significant_cities_count += 1
            except Exception as e:
                print(f"Error processing {city}: {party} and {pollutant}: {e}")

        print(f"{party} -> {pollutant}: Skipped {insufficient_data_count} cities (too few data), {non_stationary_count} cities (non-stationary)")

        city_skip_info.append(f"{party} -> {pollutant}: Skipped {insufficient_data_count} cities (Too few data), {non_stationary_count} cities (Non-stationary)")

        # Store number of significant, non-significant, and skipped cities
        heatmap_row.append(significant_cities_count)
        heatmap_row.append(non_significant_cities_count)
        heatmap_row.append(insufficient_data_count + non_stationary_count)  # Total skipped cities

        # Create a detailed summary table for each pollutant-party pair
        summary_df = pd.DataFrame({
            'City': [r[0] for r in city_results],
            'Min P-Value': [r[1] for r in city_results],
            'Significant': ['Yes' if r[1] < 0.05 else 'No' for r in city_results]
        })

        # Save summary table as CSV
        summary_df.to_csv(f"{output_dir}/{party}_{pollutant}_granger_results.csv", index=False)

    # Add the heatmap row for the current pollutant
    summary_data.append(heatmap_row)

# Convert summary data into a DataFrame for heatmap plotting
columns = [f"{party}_Significant" for party in parties] + \
          [f"{party}_Non-Significant" for party in parties] + \
          [f"{party}_Skipped" for party in parties]  # Adding new columns for non-significant and skipped cities

summary_df = pd.DataFrame(summary_data, columns=columns, index=pollutants)

# Modify the heatmap to have value 1 if significant cities > non-significant and skipped cities
heatmap_data = np.zeros((len(pollutants), len(parties)))

for i, pollutant in enumerate(pollutants):
    for j, party in enumerate(parties):
        significant = summary_df.loc[pollutant, f"{party}_Significant"]
        non_significant = summary_df.loc[pollutant, f"{party}_Non-Significant"]
        skipped = summary_df.loc[pollutant, f"{party}_Skipped"]
        
        if significant > non_significant:
            heatmap_data[i, j] = 1

# Plotting the heatmap with better labeling and annotations
plt.figure(figsize=(12, 10))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='coolwarm', cbar=False, 
            xticklabels=parties, yticklabels=pollutants, linewidths=0.5, 
            annot_kws={"size": 10})
plt.title('City-Level Granger Causality Results', fontsize=16)
plt.xlabel('Political Party')
plt.ylabel('Pollutant')
plt.tight_layout()

# Save the heatmap image
plt.savefig(f"{output_dir}/granger_causality_heatmap.png", dpi=300)
plt.close()

# Create a detailed table with subcolumns for each party
detailed_table = pd.DataFrame(index=pollutants)

for party in parties:
    detailed_table[f"{party}_Significant"] = summary_df[f"{party}_Significant"]
    detailed_table[f"{party}_Non-Significant"] = summary_df[f"{party}_Non-Significant"]
    detailed_table[f"{party}_Skipped"] = summary_df[f"{party}_Skipped"]
    detailed_table[f"{party}_Total"] = summary_df[f"{party}_Significant"] + summary_df[f"{party}_Non-Significant"] + summary_df[f"{party}_Skipped"]

# Bold the majority of the three counts (significant, non-significant, skipped)
def bold_majority(row):
    for party in parties:
        significant = row[f"{party}_Significant"]
        non_significant = row[f"{party}_Non-Significant"]
        skipped = row[f"{party}_Skipped"]
        
        max_val = max(significant, non_significant, skipped)
        
        # if significant == max_val:
        #     row[f"{party}_Significant"] = f"\\textbf{{{significant}}}"
        # if non_significant == max_val:
        #     row[f"{party}_Non-Significant"] = f"\\textbf{{{non_significant}}}"
        # if skipped == max_val:
        #     row[f"{party}_Skipped"] = f"\\textbf{{{skipped}}}"
    
    return row

detailed_table = detailed_table.apply(bold_majority, axis=1)

# Save detailed table as CSV
detailed_table.to_csv(f"{output_dir}/detailed_summary_table.csv", index=True)

# Save detailed table image
detailed_table_fig = plt.figure(figsize=(20, 10))
plt.table(cellText=detailed_table.values, colLabels=detailed_table.columns, rowLabels=detailed_table.index, loc='center')
plt.axis('off')
detailed_table_fig.savefig(f"{output_dir}/detailed_summary_table_image.png", dpi=300)

print("Granger causality analysis complete.")

# Plot cities on map of Germany
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
germany = gdf[gdf.name == "Germany"]

city_data = pd.DataFrame({
    'City': ['Berlin', 'Munich', 'Hamburg', 'Cologne'],  # Replace with your city list
    'Latitude': [52.52, 48.13, 53.55, 50.94],
    'Longitude': [13.405, 11.582, 9.993, 6.96]
})

gdf_cities = gpd.GeoDataFrame(city_data, geometry=gpd.points_from_xy(city_data['Longitude'], city_data['Latitude']))

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))
germany.plot(ax=ax, color='lightgray')
gdf_cities.plot(ax=ax, color='red', marker='o', label='Cities')

# Add labels
for x, y, label in zip(city_data['Longitude'], city_data['Latitude'], city_data['City']):
    ax.text(x + 0.05, y + 0.05, label, fontsize=9, color='black')

plt.title('Cities on Map of Germany')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()

print("Granger causality analysis complete.")