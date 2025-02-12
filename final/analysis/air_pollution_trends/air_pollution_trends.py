import pandas as pd
import matplotlib.pyplot as plt
import os

folder_path = '../../data_processed/air_pollution/'

# Load and combine data
all_data = pd.concat(
    [pd.read_csv(os.path.join(folder_path, f)) 
     for f in os.listdir(folder_path) if f.endswith('.csv')],
    ignore_index=True
)

# Calculate yearly averages
average_pollution = all_data.groupby(['Air Pollutant', 'Year'])['Air Pollution Level'].mean().reset_index()
average_pollution = average_pollution[(average_pollution['Year'] > 2012) & (average_pollution['Year'] < 2025)]
# Create plot
plt.figure(figsize=(12, 7))
for pollutant, group in average_pollution.groupby('Air Pollutant'):
    plt.plot(group['Year'], group['Air Pollution Level'], 
             marker='o', linestyle='-', label=pollutant)

plt.xlabel('Year', fontsize=12)
plt.ylabel('Average Pollution Level (ug/m3)', fontsize=12)
# plt.title('Average Air Pollution Levels by Pollutant', fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig('average_air_pollution_levels.png', dpi=300, bbox_inches='tight')
