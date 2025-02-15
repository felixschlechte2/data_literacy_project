import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from matplotlib import cm
import matplotlib.colors as mcolors

# Function to process data with the desired join
def process_data(party, pollutants, offset):
    election_data = pd.read_csv('../../../election_data.csv')
    pollutant_data = pd.read_csv(f'../../../AirPollution/processed/{pollutants}.csv')
    
    # Select relevant columns from the pollution data
    pollution_features = ['Air Pollution Level', 'Air Quality Station Type', 'Air Quality Station Area']
    pollutant_data = pollutant_data[['Air Quality Station EoI Code', 'Year', 'State', 'City'] + pollution_features]
    
    # Handle non-numeric columns (we will take the mode for categorical columns like 'Air Quality Station Type')
    categorical_columns = ['Air Quality Station Type', 'Air Quality Station Area']
    numeric_columns = [col for col in pollution_features if col not in categorical_columns]
    
    # Group by Air Quality Station EoI Code, Year, and City
    # First, for numeric columns, we can take the mean
    pollutant_data_numeric = pollutant_data.groupby(['Air Quality Station EoI Code', 'Year', 'City', 'State'], as_index=False)[numeric_columns].mean()
    
    # For categorical columns, we'll take the mode (most common value)
    for col in categorical_columns:
        mode_vals = pollutant_data.groupby(['Air Quality Station EoI Code', 'Year', 'City'])[col].agg(lambda x: x.mode()[0])
        pollutant_data_numeric[col] = mode_vals.values

    # Merge on Date and Year
    data = pd.merge(election_data, pollutant_data_numeric, left_on=['City', 'State', 'Date'], right_on=['City', 'State', 'Year'])
    data = data[['Air Quality Station EoI Code', party, 'Date', 'State', 'City'] + pollution_features]

    # Clean and prepare the data
    data = data[data[party] != 0]
    data['Date'] = pd.to_numeric(data['Date'])
    
    # Encode categorical columns with Label Encoding
    label_encoder = LabelEncoder()
    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col])

    # Collect election and pollution data
    x = []
    y = []
    for index, row in data.iterrows():
        station = row['Air Quality Station EoI Code']
        year = row['Date']
        x.append(row[party])
        y.append(row['Air Pollution Level'])
            
    return np.array(x), np.array(y), data

# Function for PCA and plotting
def plot_pca(merged_data, pca_result, features, save_path='pca_output.png'):
    plt.figure(figsize=(12, 8))

    # Combined plot for all parties
    scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], c=merged_data['State'].astype('category').cat.codes, cmap='viridis')
    plt.title('PCA with States')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(scatter, label='State')

    # Add legend with original labels
    unique_states = merged_data['State'].unique()
    
    # Create color map for categorical data
    colormap = cm.get_cmap('tab10', len(unique_states))  # You can adjust 'tab10' to other colormap if needed
    handles = []
    
    for idx, label in enumerate(unique_states):
        color = colormap(idx)  # Get color for the label
        handles.append(plt.Line2D([0], [0], marker='o', color='w', 
                                   markerfacecolor=color, markersize=10, label=str(label)))
    
    plt.legend(handles=handles, title='States')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

# Main function to run PCA and visualize the result
def run_pca_and_plot(party, pollutants, offset=5):
    x, y, merged_data = process_data(party, pollutants, offset)

    # Standardize the data (only for numeric columns)
    scaler = StandardScaler()
    merged_data_scaled = scaler.fit_transform(merged_data[['Air Pollution Level', party]])

    # Perform PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(merged_data_scaled)
    
    # Plot the results
    plot_pca(merged_data, pca_result, features=['State'])

# Example run
party = 'Linke'
pollutants = 'CO'
run_pca_and_plot(party, pollutants)
