import pandas as pd
import matplotlib.pyplot as plt
from linearmodels.panel import PanelOLS

# import file
df = pd.read_csv("PM10_sorted_and_election.csv")

# sort file
df = df.sort_values(by=['City', 'Year'])

# Add Left and right:
df['Left'] = df['Linke'] +  df['Gruene'] + df['SPD']
df['Right'] = df['FDP'] +  df['CDU'] + df['AfD']
df['Left_lag'] = df.groupby('City')['Left'].shift(1)
df['Right_lag'] = df.groupby('City')['Right'].shift(1)

# create separate files in which only cities with a majority of the Left/ Right parties
df_left = df[df['Left'] > df['Right']]
df_left.to_csv("left.csv", index=False, encoding="utf-8")
df_right = df[df['Left'] <= df['Right']]
df_right.to_csv("right.csv", index=False, encoding="utf-8")

# Clarify which Datafram to use
# i.e. df, df_left, df_right
df = df

# Add a coloumn with the Difference of the Average!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
df['Average_diff'] = df['Average'] - df['Average'].shift(1)

# Add coloums to the dataframe in which the party results in the council is laggged
# e.g. 2014: Linke =14% and 2019: Linke =10 % --> 2014: Linke =NaN and 2019: Linke =14 %
# makes sense since the effects of a law isn't directly measureable in the year of the election
parties = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU','AfD']
for party in parties:
    df[f'{party}_lag'] = df.groupby('City')[party].shift(1)

# set index of Dataframe
df = df.set_index(['City', 'Year'])


# Get all usefull cities for plotting, otherwise no use
def get_useful_cities(df):
    cities = {}
    for index, row in df.iterrows():
        if row['City'] not in cities:
            cities[row['City']] = []
        if row['Year'] not in cities[row['City']]:
            cities[row['City']].append(row['Year'])

    cities_keys = list(cities.keys())
    for item in cities_keys:
        if len(cities[item])<2:
            del cities[item]
    useful_cities = list(cities.keys())
    return useful_cities

# If you want to plot any graph of the air pollution Level of useable cities
#
# for i in range(len(useful_cities)):
#     city_df = df[df['City'] == useful_cities[i]]
#     city_df = city_df.sort_values(by= 'Year')
#    values = list(city_df['Average'])
#     years = list(city_df['Year'])
#    plt.plot(years,values, label = useful_cities[i])
# plt.legend()
# plt.show()


# Fixed effects model
mod = PanelOLS.from_formula(
    #'Average_diff ~ Linke_lag + Gruene_lag + SPD_lag + FDP_lag + CDU_lag + AfD_lag + EntityEffects + TimeEffects',
    'Average_diff ~ Left_lag + Right_lag + EntityEffects + TimeEffects',
    #'Average_diff ~ Left_lag + EntityEffects + TimeEffects',
    df
)

res = mod.fit()
print(res.summary)

# Visualization
plt.figure(figsize=(8, 6))
coefficients = res.params[:] 
#custom_names = ['Left Party', 'Greens', 'SPD', 'FDP', 'CDU', 'AfD']
custom_names = ['Left', 'Right']
coefficients.index = custom_names
coefficients.plot(kind='bar')
plt.subplots_adjust(bottom=0.2, top=0.9) 
# save figure
#plt.savefig('Left_majority_AQ_change.png', dpi=300)

plt.title("Influence of left vs Right on the change in air quality")
plt.ylabel("Coefficients")

plt.show()


    
    
    