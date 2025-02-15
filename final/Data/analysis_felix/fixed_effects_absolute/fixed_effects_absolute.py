import pandas as pd
import matplotlib.pyplot as plt
from linearmodels.panel import PanelOLS

merged_file = r'C:\Users\Home\Documents\M. Sc. ML\Data Literacy\analysis_felix\fixed_effects_absolute\PM10_and_elec.csv'
left_file = r'C:\Users\Home\Documents\M. Sc. ML\Data Literacy\analysis_felix\fixed_effects_absolute\PM10_left.csv'
right_file = r'C:\Users\Home\Documents\M. Sc. ML\Data Literacy\analysis_felix\fixed_effects_absolute\PM10_right.csv'

# import file
df = pd.read_csv(merged_file)

# sort file
df = df.sort_values(by=['City', 'Air Quality Station Type', 'Year'])

df.drop(columns=['Air Quality Station EoI Code', 'Unit Of Air Pollution Level', 'District'], errors='ignore', inplace=True)

# Add Left and right:
df['Left'] = df['Linke'] +  df['Gruene'] + df['SPD']
df['Right'] = df['FDP'] +  df['CDU'] + df['AfD']
df['Left_lag'] = df.groupby('City')['Left'].shift(1)
df['Right_lag'] = df.groupby('City')['Right'].shift(1)

df.to_csv(merged_file, index=False, encoding="utf-8")

# create separate files in which only cities with a majority of the Left/ Right parties
df_left = df[df['Left'] > df['Right']]
df_left.to_csv(left_file, index=False, encoding="utf-8")
df_right = df[df['Left'] <= df['Right']]
df_right.to_csv(right_file, index=False, encoding="utf-8")

# Add coloums to the dataframe in which the party results in the council is laggged
# e.g. 2014: Linke =14% and 2019: Linke =10 % --> 2014: Linke =NaN and 2019: Linke =14 %
# makes sense since the effects of a law isn't directly measureable in the year of the election
parties = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU','AfD']
for party in parties:
    df[f'{party}_lag'] = df.groupby('City')[party].shift(1)

df_pre_afd = df[df['Year'] <= 2013]
df_post_afd = df[df['Year'] > 2013]

# # Clarify which Datafram to use
# # i.e. df, df_left, df_right
df = df_post_afd

# # Add a coloumn with the Difference of the Average!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# # df['Average_diff'] = df['Average'] - df['Average'].shift(1)

# set index of Dataframe
df = df.set_index(['City', 'Year'])

# df.to_csv(merged_file, index=False, encoding="utf-8")

# # Get all usefull cities for plotting, otherwise no use
# def get_useful_cities(df):
#     cities = {}
#     for index, row in df.iterrows():
#         if row['City'] not in cities:
#             cities[row['City']] = []
#         if row['Year'] not in cities[row['City']]:
#             cities[row['City']].append(row['Year'])

#     cities_keys = list(cities.keys())
#     for item in cities_keys:
#         if len(cities[item])<2:
#             del cities[item]
#     useful_cities = list(cities.keys())
#     return useful_cities

# # If you want to plot any graph of the air pollution Level of useable cities
# #
# # for i in range(len(useful_cities)):
# #     city_df = df[df['City'] == useful_cities[i]]
# #     city_df = city_df.sort_values(by= 'Year')
# #    values = list(city_df['Average'])
# #     years = list(city_df['Year'])
# #    plt.plot(years,values, label = useful_cities[i])
# # plt.legend()
# # plt.show()


# Fixed effects model
mod = PanelOLS.from_formula(
    'Air_Pollution_Level ~ Linke_lag + Gruene_lag + SPD_lag + FDP_lag + CDU_lag + AfD_lag + EntityEffects + TimeEffects',
    # 'Air_Pollution_Level ~ Left_lag + Right_lag + EntityEffects + TimeEffects',
    # 'Air_Pollution_Level ~ Right_lag + EntityEffects + TimeEffects',
    df
)

res = mod.fit()
print(res.summary)

# Visualization
plt.figure(figsize=(10, 6))
coefficients = res.params[:] 
p_values = res.pvalues[:]

custom_names = ['Left Party', 'Greens', 'SPD', 'FDP', 'CDU', 'AfD']
# custom_names = ['Left', 'Right']
# custom_names = ['Right']
coefficients.index = custom_names
p_values.index = custom_names

bars = coefficients.plot(kind='bar', color='skyblue', edgecolor='black')

for bar, p_value in zip(bars.patches, p_values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # x-Position: Mittelpunkt des Balkens
        bar.get_height() + 0.001,           # y-Position: knapp über dem Balken
        f'p={p_value:.3f}',                # Text mit p-Wert, auf 3 Dezimalstellen gerundet
        ha='center',                       # Horizontal zentriert
        fontsize=10,                       # Schriftgröße
        color='black' if p_value < 0.05 else 'red'                      # Farbe des Textes
    )
# plt.subplots_adjust(bottom=0.2, top=0.9) 
# save figure
#plt.savefig('Left_majority_AQ_change.png', dpi=300)

# plt.title("Influence of right camp on the absolute values of PM10 with their p-values over whole timeline")
# Diagramm anpassen
plt.title("Influence of each Party on the absolute value of PM10 with their p-values after 2013/AfD")
plt.ylabel("Coefficients")
plt.xlabel("Political Parties")
# plt.xlabel("Political camps")
plt.xticks(rotation=90)
plt.tight_layout()

# Zeige das Diagramm
plt.show()


    
    
    