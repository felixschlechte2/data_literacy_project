import pandas as pd

def merge_data( pollutant):
    # Load election and pollution data
    election_data = pd.read_csv('../../../analysis_felix/filled_elec.csv')
    pollutant_data = pd.read_csv(f'../../../AirPollution/sorted_by_type/{pollutant}_sorted.csv')

    election_data['Date'] = pd.to_numeric(election_data['Date'])
    pollutant_data['Year'] = pd.to_numeric(pollutant_data['Year'])    

    # Merge on city and year (ensure election 'Date' matches pollution 'Year')
    data = pd.merge(election_data, pollutant_data, left_on=['City', 'Date'], right_on=['City', 'Year'])
    data['CityStation'] = data['City']+'_'+data['Air Quality Station Type']

    # Drop rows with NaN pollution levels (because of shifting)
    data = data.dropna()

    # print('shape of the merged file')
    # print(data.shape)
    # print(data.head())

    return data

def create_balanced_panel(df):
    """Create balanced panel with backfilled election data"""
    # Identify party columns
    party_cols = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

    # Determine time window
    start_year = df[df['Year'].between(1998, 2004)]['Year'].value_counts().idxmax()
    end_year = df[df['Year'].between(2020, 2024)]['Year'].value_counts().idxmax()
    
    initial_cities = df['CityStation'].nunique()
    print('start_year should be', start_year, end_year)
    # Create balanced panel
    df = df[df['Year'] >= start_year]
    df = df [df['Year'] <= end_year]
    
    print(df.shape)
    
    final_cities = df['CityStation'].nunique()

    return df, initial_cities - final_cities


mergedDf = merge_data('PM10')
balancedPanel, removedCities = create_balanced_panel(mergedDf)
print('no of cities remvoed', removedCities)
print('balanced panel shape', balancedPanel.shape)
print(balancedPanel.head())

balancedPanel.to_csv('./BalancedPanelPM10.csv')
