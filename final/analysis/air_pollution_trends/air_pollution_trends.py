import pandas as pd
import matplotlib.pyplot as plt
import os

from tueplots import axes, bundles, markers
from tueplots import cycler
from tueplots.constants.color import palettes

plt.rcParams.update({"figure.dpi": 300})
plt.rcParams.update(bundles.neurips2021(usetex=True, family="serif"))
plt.rcParams.update(axes.spines(top=False, right=False))
plt.rcParams.update(markers.with_edge())
plt.rcParams.update(cycler.cycler(color=palettes.paultol_muted))

pollutant_colors = {
    'index': '#8ABD24',
    'NO2': '#ffed00',
    'PM2.5': '#E3000F',
    'PM10': '#bec1c7',
    'O3': '#D675D8',
}

folder_path = '../../data_processed/air_pollution/'

# Load and combine data
all_data = pd.concat(
    [pd.read_csv(os.path.join(folder_path, f)) 
     for f in os.listdir(folder_path) if f.endswith('.csv')],
    ignore_index=True
)

continuous_index = pd.read_csv('../../continuous_index/continuous_index.csv')
continuous_index['Air Pollutant'] = 'index'
continuous_index['Air Pollution Level'] = continuous_index['Index']

all_data = pd.concat([all_data, continuous_index])

# Calculate yearly averages
average_pollution = all_data.groupby(['Air Pollutant', 'Year'])['Air Pollution Level'].mean().reset_index()
average_pollution = average_pollution[(average_pollution['Year'] > 2013) & (average_pollution['Year'] < 2025)]

# Calculate percentage change relative to first year
average_pollution['First Year Level'] = average_pollution.groupby('Air Pollutant')['Air Pollution Level'].transform('first')
average_pollution['Percentage Change'] = (
    (average_pollution['Air Pollution Level'] - average_pollution['First Year Level']) / 
    average_pollution['First Year Level']
) * 100

# Explicitly set first year to 0% for each pollutant
average_pollution.loc[
    average_pollution.groupby('Air Pollutant')['Year'].transform('min') == average_pollution['Year'],
    'Percentage Change'
] = 0

# Filter out any remaining NaN values
average_pollution = average_pollution.dropna(subset=['Percentage Change'])

plt.figure(figsize=(6, 3))
ax = plt.gca()  # Get current axes

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for pollutant, group in average_pollution.groupby('Air Pollutant'):
    plt.plot(group['Year'], group['Percentage Change'], 
             marker='o', linestyle='-', label=pollutant, color=pollutant_colors[pollutant])

# Set x-ticks to show all years
plt.xticks(average_pollution['Year'].unique())

# Position legend in upper right corner inside plot
plt.legend(loc='lower left', frameon=True)

plt.xlabel('Year', )
plt.ylabel('Change from first year (\%)', )
plt.grid(True)
plt.tight_layout()
plt.savefig('pollution_change_plot.png', dpi=300)
