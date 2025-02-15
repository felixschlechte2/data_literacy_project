import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
    
# Input file paths
air_quality_file = '../../processed/PM10.csv'  # Replace with your air quality data file path
election_file = '../../../analysis_felix/filled_elec.csv'  # Replace with your election data file path

# Read the input files
air_quality_df = pd.read_csv(air_quality_file)
election_df = pd.read_csv(election_file)

# Rename "Year" in air quality data to "Year" for merging
election_df.rename(columns={"Date": "Year"}, inplace=True)

# Ensure "Year" is integer for alignment purposes
air_quality_df["Year"] = air_quality_df["Year"].astype(int)
election_df["Year"] = election_df["Year"].astype(int)


# Merge air quality data with the filled election data on City, State, and Year
merged_df = pd.merge(
    election_df,
    air_quality_df,
    on=["City", "State", "Year"],
    how="inner"
)

def defineMajority(row):
    if row['left_coalition'] > 50:
        return 'L'
    elif row['right_coalition'] > 50:
        return 'R'
    elif row['Others'] > 50:
        return 'O'
    else:
        return 'N'

merged_df['majority'] = merged_df.apply(defineMajority, axis=1)
merged_df.columns = merged_df.columns.str.replace(" ", "_")

# cityExample = (merged_df[merged_df['City'] == 'Aachen'])

# from statsmodels.formula.api import ols
# model = ols("Normalized_Pollution_Level ~ left_coalition + right_coalition + Others + C(majority)", data=merged_df).fit()
# print(model.summary())

# cityExample = (merged_df[merged_df['City'] == 'Aachen'])
# cityExample['majority']  = cityExample.apply(defineMajority, axis=1)
# merged_df.to_csv('mergedTemp.csv', index=False)
# cityExample.to_csv('BerlinE.csv', index=False)



# from statsmodels.tsa.stattools import grangercausalitytests
# print('grangers causlity left coalition')
# grangercausalitytests(merged_df[['Normalized_Difference', 'left_coalition']], maxlag=4)
# print('grangers causlity right coalition')
# grangercausalitytests(merged_df[['Normalized_Difference', 'right_coalition']], maxlag=4)


correlation_matrix = merged_df[['left_coalition', 'right_coalition', 'Others', 'Normalized_Difference']].corr()
import numpy as np

mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix (Lower Triangle)")
# sns.pairplot(merged_df[['left_coalition', 'right_coalition', 'Others', 'Normalized_Pollution_Level']])
plt.savefig("correlation_heatmap.png", dpi=300, bbox_inches='tight')
plt.show()
# print(election_df['State'].unique())
# print(air_quality_df['State'].unique())

# min_year, max_year = air_quality_df["Year"].min(), air_quality_df["Year"].max()
# print(min_year, max_year)
# min_year, max_year = election_df["Year"].min(), election_df["Year"].max()
# print(min_year, max_year)

# Group by year and calculate average air pollution and vote percentages
# grouped_data = cityExample.groupby("Year").agg(
#     avg_air_pollution=("Air Pollution Level", "mean"),
#     **{party: (party, "mean") for party in ["Linke", "Gruene", "SPD", "FDP", "CDU", "AfD", "Others"]}
# ).reset_index()

# grouped_data.to_csv('cityGrouped.csv', index=False)


# Plot 1: Time-Series of Air Pollution Levels
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=grouped_data, x="Year", y="avg_air_pollution", label="Air Pollution Level")
# plt.title("Time-Series of Average Air Pollution Levels")
# plt.xlabel("Year")
# plt.ylabel("Air Pollution Level")
# plt.grid(True)
# air_pollution_plot_file = "air_pollution_time_series.png"
# plt.savefig(air_pollution_plot_file)
# plt.show()

# # Plot 2: Time-Series of Vote Percentages
# plt.figure(figsize=(12, 6))
# for party in ["Linke", "Gruene", "SPD", "FDP", "CDU", "AfD", "Others"]:
#     sns.lineplot(data=grouped_data, x="Year", y=party, label=party)

# plt.title("Time-Series of Vote Percentages")
# plt.xlabel("Year")
# plt.ylabel("Vote Percentage")
# plt.legend()
# plt.grid(True)
# plt.show()

# # Plot 3: Correlation Heatmap
# correlation_data = grouped_data.set_index("Year").corr()

# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_data, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
# plt.title("Correlation Matrix: Air Pollution and Vote Percentages")
# plt.show()


# # Save the merged data to a new CSV file
# output_csv_file = "merged_air_quality_election_data.csv"
# merged_df.to_csv(output_csv_file, index=False)
# print(f"Merged data saved to {output_csv_file}")

# # Save the time-series plot of air pollution levels
# air_pollution_plot_file = "air_pollution_time_series.png"
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=grouped_data, x="Year", y="avg_air_pollution", label="Air Pollution Level")
# plt.title("Time-Series of Average Air Pollution Levels")
# plt.xlabel("Year")
# plt.ylabel("Air Pollution Level")
# plt.grid(True)
# plt.savefig(air_pollution_plot_file)
# plt.close()
# print(f"Air pollution time-series plot saved to {air_pollution_plot_file}")

# # Save the time-series plot of vote percentages
# vote_percentage_plot_file = "vote_percentages_time_series.png"
# plt.figure(figsize=(12, 6))
# for party in ["Linke", "Gruene", "SPD", "FDP", "CDU", "AfD", "Others"]:
#     sns.lineplot(data=grouped_data, x="Year", y=party, label=party)

# plt.title("Time-Series of Vote Percentages")
# plt.xlabel("Year")
# plt.ylabel("Vote Percentage")
# plt.legend()
# plt.grid(True)
# plt.savefig(vote_percentage_plot_file)
# plt.close()
# print(f"Vote percentages time-series plot saved to {vote_percentage_plot_file}")

# # Save the correlation heatmap
# correlation_plot_file = "correlation_heatmap.png"
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_data, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
# plt.title("Correlation Matrix: Air Pollution and Vote Percentages")
# plt.savefig(correlation_plot_file)
# plt.close()
# print(f"Correlation heatmap saved to {correlation_plot_file}")

