import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tslearn.clustering import TimeSeriesKMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess
df = pd.read_csv('../../processed/PM10.csv')
df = df.sort_values(['Air Quality Station EoI Code', 'Year'])
df = df[df['Year']<2025 and df['Year']>1998]
# Create time series matrix
ts_matrix = df.pivot_table(index='Air Quality Station EoI Code', 
                          columns='Year', 
                          values='Air Pollution Level')

# Handle missing values (linear interpolation)
ts_matrix = ts_matrix.interpolate(axis=1).ffill().bfill()

# Normalize time series
scaler = StandardScaler()
ts_scaled = scaler.fit_transform(ts_matrix.T).T

# Time-aware clustering
n_clusters = 3
model = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", random_state=42)
clusters = model.fit_predict(ts_scaled)

# Add cluster labels to original dataframe
cluster_map = pd.Series(clusters, index=ts_matrix.index, name='TS_Cluster')
df = df.merge(cluster_map, left_on='Air Quality Station EoI Code', right_index=True)

plt.figure(figsize=(10,6))
years = ts_matrix.columns.astype(int).values

for cluster in range(n_clusters):
    cluster_data = ts_scaled[clusters == cluster]
    mean_traj = np.mean(cluster_data, axis=0)
    std_traj = np.std(cluster_data, axis=0)
    
    plt.plot(years, mean_traj, lw=2, label=f'Cluster {cluster}')
    plt.fill_between(years, 
                     mean_traj - std_traj, 
                     mean_traj + std_traj, 
                     alpha=0.1)

plt.title("Normalized Pollution Trajectories by Cluster")
plt.xlabel("Year")
plt.ylabel("Z-Score Pollution Level")
plt.legend()
plt.grid(True)
plt.show()

# Create facet grid by cluster and station type
g = sns.FacetGrid(df, col='TS_Cluster', row='Air Quality Station Type', 
                 margin_titles=True, height=4, aspect=1.2)
g.map_dataframe(sns.lineplot, x='Year', y='Air Pollution Level', 
               estimator='median', errorbar=('ci', 95))
g.set_axis_labels("Year", "PM10 Level (μg/m³)")
g.set_titles(col_template="Cluster {col_name}", row_template="{row_name}")
plt.tight_layout()

plt.show()
