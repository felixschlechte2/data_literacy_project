import pandas as pd
from scipy import stats
import statsmodels.api as sm
import numpy as np
from matplotlib import pyplot as plt
from tueplots import axes, bundles, markers
from tueplots import cycler
from tueplots import figsizes
from tueplots.constants.color import palettes

def process_data(parties, pollutant, offset):
    election_data = pd.read_csv('../Data/election_data.csv')
    pollutant_data = pd.read_csv(f'../Data/AirPollution/processed/{pollutant}.csv')
    pollutant_data = pollutant_data[['Air Quality Station EoI Code', 'Year', 'Air Pollution Level', 'City']]
    pollutant_data = pollutant_data.groupby(['Air Quality Station EoI Code', 'Year', 'City'], as_index=False).mean()

    data = pd.merge(election_data, pollutant_data, left_on=['City', 'Date'], right_on=['City', 'Year'])

    data = data[['Air Quality Station EoI Code', 'Date', 'Air Pollution Level', 'City'] + parties]

    # data = data[data[party] != 0]
    data['Date'] = pd.to_numeric(data['Date'])

    x = []
    y = []

    for index, row in data.iterrows():
        station = row['Air Quality Station EoI Code']
        year = row['Date']
        if pollutant_data[(pollutant_data['Air Quality Station EoI Code'] == station) & (pollutant_data['Year'] == year + offset)].any()['Air Pollution Level'] and year + offset < 2025:
            election_result = row[parties]
            pollution_before = row['Air Pollution Level']
            pollution_after = pollutant_data[(pollutant_data['Air Quality Station EoI Code'] == station) & (pollutant_data['Year'] == year + offset)]['Air Pollution Level'].values[0]
            pollution_change =  (pollution_after - pollution_before) / pollution_before
            x.append(election_result)
            y.append(pollution_change)
    x = [r for r in x if 0.0 not in r]
    return np.array(x), np.array(y)
    
def analysis_and_plot(x, y, axs):
    N = len(x)

    statistic = lambda x, y: stats.linregress(x, y).rvalue
    res = stats.permutation_test(data=(x, y), statistic=statistic, permutation_type='pairings')

    res = stats.linregress(x, y)
    axs.set_ylim([-0.5, 0.5])
    axs.plot(x, y, 'o', markersize=3, label='original data')
    axs.plot(x, res.intercept + res.slope*x, label='fitted line')
    return res

def run_analysis():
    plt.rcParams.update({"figure.dpi": 300})
    plt.rcParams.update(bundles.neurips2021(usetex=True, family="serif"))
    plt.rcParams.update(figsizes.neurips2021(nrows=2, ncols=2))
    plt.rcParams.update(axes.spines(top=False, right=False))
    plt.rcParams.update(markers.with_edge())
    plt.rcParams.update(cycler.cycler(color=palettes.paultol_muted))

    offset = 5
    parties = ['Linke', 'Gruene' , 'SPD', 'FDP', 'CDU', 'AfD']
    pollutants = ['CO', 'NO2' , 'O3', 'PM10', 'SO2']

    fig, axs = plt.subplots(len(pollutants), len(parties))

    for i, pollutant in enumerate(pollutants):
        for j, party in enumerate(parties):
            x, y = process_data(party, pollutant, offset)
            res = analysis_and_plot(x, y, axs[i, j])
            print(f'Pollutant {pollutant} for {party} done: p = {res.pvalue}, slope={res.slope}')

    for i, party in enumerate(parties):
        axs[len(pollutants)-1][i].set_xlabel(f'{party}')

    for i, pollutant in enumerate(pollutants):
        axs[i][0].set_ylabel(f'{pollutant}')

    plt.show()

x, y = process_data(['Linke', 'Gruene' , 'SPD', 'FDP', 'CDU', 'AfD'], 'SO2', 5)
print(np.array([r for r in x if 0 not in r]).shape)