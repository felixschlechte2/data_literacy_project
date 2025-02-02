import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Load and filter data
df = pd.read_csv('../../processed/PM10.csv')
df = df[df['Year']<2025]
df = df[df['Year']>1998]

# Remove outliers using IQR method
Q1 = df['Air Pollution Level'].quantile(0.25)
Q3 = df['Air Pollution Level'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Air Pollution Level'] >= lower_bound) & (df['Air Pollution Level'] <= upper_bound)]

df['Air Quality Station Area'] = df['Air Quality Station Area'].str.lower()

# Create a categorical x-axis
df['Year_StationType'] = df['Year'].astype(str) + '_' + df['Air Quality Station Type']
df['Year_StationArea'] = df['Year'].astype(str) + '_' + df['Air Quality Station Area']



# Create a mapping for x-axis positions
unique_years = sorted(df['Year'].unique())
station_types = sorted(df['Air Quality Station Type'].unique())
station_area = sorted(df['Air Quality Station Area'].unique())

x_mapping = {f"{year}_{stype}": year + (i - 1) * 0.25 
             for year in unique_years 
             for i, stype in enumerate(station_types)}

x_mapping2 = {f"{year}_{stype}": year + (i - 1) * 0.25 
             for year in unique_years 
             for i, stype in enumerate(station_area)}

# Map x-values
df['x_position'] = df['Year_StationType'].map(x_mapping)
df['x_position2'] = df['Year_StationArea'].map(x_mapping2)

import matplotlib.colors as mcolors

# For Station Type plot
plt.figure(figsize=(20, 10))
color_palette = sns.color_palette("deep", n_colors=len(station_types))
# Create a color map
color_map = dict(zip(station_types, color_palette))

# Scatter plot
for stype in station_types:
    stype_data = df[df['Air Quality Station Type'] == stype]
    plt.scatter(stype_data['x_position'], stype_data['Air Pollution Level'], 
                c=[color_map[stype]], alpha=0.5, label=stype)

# Calculate and plot yearly averages for each station type
for stype in station_types:
    stype_data = df[df['Air Quality Station Type'] == stype]
    yearly_avg = stype_data.groupby('Year')['Air Pollution Level'].mean().reset_index()
    plt.plot(yearly_avg['Year'], yearly_avg['Air Pollution Level'], '-', 
             color=color_map[stype], linewidth=2, label=f'{stype} average')

# Rest of the plotting code remains the same
plt.title('Air Pollution Levels Across Years by Station Type (Outliers Removed)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Air Pollution Level', fontsize=12)
plt.legend(title='Station Type', title_fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(unique_years, unique_years)
plt.xlim(min(unique_years) - 0.5, max(unique_years) + 0.5)
plt.tight_layout()
plt.savefig('./PM10_plot_yearly_avg_stationtype.png', dpi=300, bbox_inches='tight')
plt.close()

# For Station Area plot
plt.figure(figsize=(20, 10))

color_palette = sns.color_palette("deep", n_colors=len(station_types))

# Create a color map
color_map = dict(zip(station_area, color_palette))

# Scatter plot
for area in station_area:
    area_data = df[df['Air Quality Station Area'] == area]
    plt.scatter(area_data['x_position2'], area_data['Air Pollution Level'], 
                c=[color_map[area]], alpha=0.5, label=area)

# Calculate and plot yearly averages for each station area
for area in station_area:
    area_data = df[df['Air Quality Station Area'] == area]
    yearly_avg = area_data.groupby('Year')['Air Pollution Level'].mean().reset_index()
    plt.plot(yearly_avg['Year'], yearly_avg['Air Pollution Level'], '-', 
             color=color_map[area], linewidth=2, label=f'{area} average')

# Rest of the plotting code remains the same
plt.title('Air Pollution Levels Across Years by Station Area (Outliers Removed)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Air Pollution Level', fontsize=12)
plt.legend(title='Station Area', title_fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(unique_years, unique_years)
plt.xlim(min(unique_years) - 0.5, max(unique_years) + 0.5)
plt.tight_layout()
plt.savefig('./PM10_plot_yearly_avg_stationarea.png', dpi=300, bbox_inches='tight')
plt.close()

# Generate statistics
total_counts = df['Air Quality Station Type'].value_counts()
yearly_counts = df.groupby(['Year', 'Air Quality Station Type']).size().unstack(fill_value=0)
state_counts = df.groupby(['State', 'Air Quality Station Type']).size().unstack(fill_value=0)

# Save statistics
total_counts.to_csv('./station_type_total_counts.csv')
yearly_counts.to_csv('./station_type_yearly_counts.csv')
state_counts.to_csv('./station_type_state_counts.csv')



# Generate statistics for station area
total_counts_area = df['Air Quality Station Area'].value_counts()
yearly_counts_area = df.groupby(['Year', 'Air Quality Station Area']).size().unstack(fill_value=0)
state_counts_area = df.groupby(['State', 'Air Quality Station Area']).size().unstack(fill_value=0)

# Save statistics for station area
total_counts_area.to_csv('./station_area_total_counts.csv')
yearly_counts_area.to_csv('./station_area_yearly_counts.csv')
state_counts_area.to_csv('./station_area_state_counts.csv')

print("Plot and statistics saved successfully.")