import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
from tueplots import figsizes, fonts
from linearmodels.panel import PanelOLS

processed_file = r".\processed.csv"

def process_data(parties,station_type, offset):
    election_data = pd.read_csv(r'.\election_data.csv')
    if station_type:
        pollutant_data = pd.read_csv(fr'.\continuous_german_index_sorted.csv')
        pollutant_data = pollutant_data[pollutant_data['Air Quality Station Type'] == station_type]
    else: 
        pollutant_data = pd.read_csv(fr'.\continuous_german_index.csv')

    data = pd.merge(election_data, pollutant_data, left_on=['City', 'Date'], right_on=['City', 'Year'])
    data = data[['Date', 'Index', 'City'] + parties]

    data['Date'] = pd.to_numeric(data['Date'])
    data['Change'] = 'None'

    for index, row in data.iterrows():
        city = row['City']
        year = row['Date']
        if data[(data['City'] == city) & (data['Date'] == year + offset)].any()['Index'] and year + offset < 2025:
            election_result = row[parties]
            pollution_before = row['Index']
            pollution_after = data[(data['City'] == city) & (data['Date'] == year + offset)]['Index'].values[0]
            pollution_change =  (pollution_after - pollution_before)  #/ pollution_before
            row['Change'] = pollution_change
            data.iloc[index] = row
    data = data[data['Change'] != 'None']
    data['Change'] = data['Change'].astype('float64')
    return data

parties = ['Linke','Gruene','SPD','FDP','CDU','AfD']

df = process_data(parties, None, 5)

df = df.sort_values(by=['City', 'Date'])
# df = df[df['Date'] <= 2013]
df.to_csv(processed_file, index=False)

df = df.set_index(['City', 'Date'])
mod = PanelOLS.from_formula(
    'Change ~ Linke + Gruene + SPD + FDP + CDU + AfD + EntityEffects + TimeEffects',
    df
)

res = mod.fit()
print(res.summary)

# Visualization
#plt.figure(figsize=(8, 6))
#plt.rcParams.update({"figure.dpi": 150})
#plt.rcParams.update(figsizes.cvpr2024_full())
#plt.rcParams.update(fonts.neurips2021(family = "sans-serif"))
coefficients = res.params[:]
custom_names = ['Left Party', 'Greens', 'SPD', 'FDP', 'CDU', 'AfD']
coefficients.index = custom_names

x_pos = [i + 3 for i in range(len(coefficients))]

colors = ['#BE3075', '#46962B', '#E3000F', '#FFFF00', '#151518', '#009EE0']

# Create bar plot
fig, ax = plt.subplots()
bars = ax.bar(coefficients.index, coefficients.values, color=colors, edgecolor='black')#, width=0.6)#, edgecolor='black')

#ax = coefficients.plot(kind='bar',color = colors)

# Move x-axis to y=0
ax.axhline(0, color='black', linewidth=1.5)  # Draws x-axis at y=0
ax.spines['top'].set_visible(False)  # Remove top border
ax.spines['right'].set_visible(False)  # Remove right border
#ax.spines['left'].set_position(('data', 0))  # Moves y-axis to x=0
ax.spines['bottom'].set_position(('data', 0))  # Moves x-axis to y=0

# Remove grid for a clean look
#ax.grid(False)
for i,bar in enumerate(bars):
    height = bar.get_height()
    if i == 3:
        text_color = 'black'
    else:
        text_color = 'white'
    text_color = 'black' # ------> if pvalue outside
    ax.text(bar.get_x() + bar.get_width()/2, height + (-0.00005 if height < 0 else 0.00005),#(+0.002 if height < 0 else -0.01), 
            f'p={res.pvalues.iloc[i]:.3f}', ha='center', fontsize=10, color= text_color)

# Add legend
#handles = [plt.Rectangle((0, 0), 1, 1, color=label) for label in colors]
#ax.legend(handles, custom_names, loc="upper right", fontsize=8)
#ax.set_xticks(x_pos) ->smaller
ax.set_xticklabels([])
ax.tick_params(axis='x', which='both', length=0) 

#plt.subplots_adjust(bottom=0.2, top=0.9) 
# save figure
plt.savefig('Analysis_index', dpi= 300)

plt.title("fixed effects coefficients on index", fontsize = 15)
plt.ylabel("Coefficients")

#fig.text(0.5, 0.1, 'Influence of parties on PM10 concentration', ha='center', va='center', fontsize=12, style='italic')
# bessere caption
plt.show()

