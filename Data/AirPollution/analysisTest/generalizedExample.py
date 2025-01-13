import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Input file paths
air_quality_file = '../filtered/PM10.csv'  # Replace with your air quality data file path
election_file = '../../election_data.csv'  # Replace with your election data file path

# Read the input files
air_quality_df = pd.read_csv(air_quality_file)
election_df = pd.read_csv(election_file)

# Rename "Year" in air quality data to "Date" for merging
air_quality_df.rename(columns={"Year": "Date"}, inplace=True)

# Ensure "Date" is integer for alignment purposes
air_quality_df["Date"] = air_quality_df["Date"].astype(int)
election_df["Date"] = election_df["Date"].astype(int)

# Create a continuous year range based on air quality data
min_year, max_year = air_quality_df["Date"].min(), air_quality_df["Date"].max()
year_range = pd.DataFrame({"Date": range(min_year, max_year + 1)})

# Merge election data with the continuous year range
election_df = pd.merge(year_range, election_df, on="Date", how="left")

# Forward-fill election data to propagate values to missing years
election_df.fillna(method="ffill", inplace=True)

# Merge air quality data with the filled election data on City, State, and Date
merged_df1 = pd.merge(
    air_quality_df,
    election_df,
    on=["City", "State", "Date"],
    how="inner",
    
)

merged_df = merged_df1[merged_df1["State"] == "BE"]
merged_df = merged_df[merged_df["City"] == "Berlin"]


# Group by year and calculate average air pollution and vote percentages
grouped_data = merged_df.groupby("Date").agg(
    avg_air_pollution=("Air Pollution Level", "mean"),
    **{party: (party, "mean") for party in ["Linke", "Gruene", "SPD", "FDP", "CDU", "AfD", "Others"]}
).reset_index()

# Plot 1: Time-Series of Air Pollution Levels
plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_data, x="Date", y="avg_air_pollution", label="Air Pollution Level")
plt.title("Time-Series of Average Air Pollution Levels")
plt.xlabel("Year")
plt.ylabel("Air Pollution Level")
plt.grid(True)
plt.show()

# Plot 2: Time-Series of Vote Percentages
plt.figure(figsize=(12, 6))
for party in ["Linke", "Gruene", "SPD", "FDP", "CDU", "AfD", "Others"]:
    sns.lineplot(data=grouped_data, x="Date", y=party, label=party)

plt.title("Time-Series of Vote Percentages")
plt.xlabel("Year")
plt.ylabel("Vote Percentage")
plt.legend()
plt.grid(True)
plt.show()

# Plot 3: Correlation Heatmap
correlation_data = grouped_data.set_index("Date").corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_data, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
plt.title("Correlation Matrix: Air Pollution and Vote Percentages")
plt.show()


# Save the merged data to a new CSV file
output_csv_file = "merged_air_quality_election_data.csv"
merged_df.to_csv(output_csv_file, index=False)
print(f"Merged data saved to {output_csv_file}")

# Save the time-series plot of air pollution levels
air_pollution_plot_file = "air_pollution_time_series.png"
plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_data, x="Date", y="avg_air_pollution", label="Air Pollution Level")
plt.title("Time-Series of Average Air Pollution Levels")
plt.xlabel("Year")
plt.ylabel("Air Pollution Level")
plt.grid(True)
plt.savefig(air_pollution_plot_file)
plt.close()
print(f"Air pollution time-series plot saved to {air_pollution_plot_file}")

# Save the time-series plot of vote percentages
vote_percentage_plot_file = "vote_percentages_time_series.png"
plt.figure(figsize=(12, 6))
for party in ["Linke", "Gruene", "SPD", "FDP", "CDU", "AfD", "Others"]:
    sns.lineplot(data=grouped_data, x="Date", y=party, label=party)

plt.title("Time-Series of Vote Percentages")
plt.xlabel("Year")
plt.ylabel("Vote Percentage")
plt.legend()
plt.grid(True)
plt.savefig(vote_percentage_plot_file)
plt.close()
print(f"Vote percentages time-series plot saved to {vote_percentage_plot_file}")

# Save the correlation heatmap
correlation_plot_file = "correlation_heatmap.png"
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_data, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
plt.title("Correlation Matrix: Air Pollution and Vote Percentages")
plt.savefig(correlation_plot_file)
plt.close()
print(f"Correlation heatmap saved to {correlation_plot_file}")

