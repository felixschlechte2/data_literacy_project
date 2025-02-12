import pandas as pd
from scipy import stats
import statsmodels.api as sm
from sklearn import linear_model
import numpy as np
from matplotlib import pyplot as plt
from tueplots import axes, bundles, markers
from tueplots import cycler
from tueplots import figsizes
from tueplots.constants.color import palettes
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor
from linearmodels.panel import PanelOLS
from statsmodels.stats.diagnostic import het_breuschpagan, acorr_ljungbox

party_colors = {
    'Gruene': '#8ABD24',
    'FDP': '#ffed00',
    'SPD': '#E3000F',
    'CDU': '#bec1c7',
    'Linke': '#D675D8',
    'AfD': '#0BA1DD'
}

def process_data_index(parties, offset):
    election_data = pd.read_csv('../Data/election_data.csv')
    pollutant_data = pd.read_csv(f'continuous_german_index.csv')
    pollutant_data = pollutant_data[['Year', 'Index', 'City']]
    pollutant_data = pollutant_data.groupby(['Year', 'City'], as_index=False).mean()
    
    data = pd.merge(election_data, pollutant_data, left_on=['City', 'Date'], right_on=['City', 'Year'])

    data = data[['Date', 'Index', 'City', 'Others'] + parties]
    #Wooldridge for endogeneity
    for party in parties:
        data[f'{party}_lag'] = data.groupby('City')[party].shift(1)
    #data.to_csv("data.csv", index=False, encoding="utf-8") just to see if correct
    print(data.shape)
    data['Date'] = pd.to_numeric(data['Date'])
    data['Change'] = 'None'
    data = data.reset_index(drop = True)
    for index, row in data.iterrows():
        city = row['City']
        year = row['Date']
        if pollutant_data[(pollutant_data['City'] == city) & (pollutant_data['Year'] == year + offset)].any()['Index'] and year + offset < 2025:
            election_result = row[parties]
            pollution_before = row['Index']
            pollution_after = pollutant_data[(pollutant_data['City'] == city) & (pollutant_data['Year'] == year + offset)]['Index'].values[0]
            pollution_change =  (pollution_after - pollution_before) / pollution_before
            row['Change'] = pollution_change
            data.iloc[index] = row
    data = data[data['Change'] != 'None']
    data['Change'] = data['Change'].astype('float64')
    data = data[data['Others'] < 33]
    data = data[data['Date'] > 2013]
    data = data.reset_index(drop=True)
    z = np.abs(stats.zscore(data['Change']))
    threshold_z = 2
    outlier_indices = np.where(z > threshold_z)[0]
    data = data.drop(outlier_indices)
    data.reset_index(drop = True)
    return data

def process_data(parties, pollutant, offset):
    if pollutant == 'index':
        return process_data_index(parties, offset)
    election_data = pd.read_csv('../Data/election_data.csv')
    pollutant_data = pd.read_csv(f'../Data/AirPollution/processed/{pollutant}.csv')
    pollutant_data = pollutant_data[['Air Quality Station EoI Code', 'Year', 'Air Pollution Level', 'City', 'Air Quality Station Type']]
    pollutant_data = pollutant_data.groupby(['Air Quality Station EoI Code', 'Year', 'City', 'Air Quality Station Type'], as_index=False).mean()
    
    data = pd.merge(election_data, pollutant_data, left_on=['City', 'Date'], right_on=['City', 'Year'])

    data = data[['Air Quality Station EoI Code', 'Date', 'Air Pollution Level', 'City', 'Air Quality Station Type', 'Others'] + parties]
    #Wooldridge for endogeneity
    for party in parties:
        data[f'{party}_lag'] = data.groupby('Air Quality Station EoI Code')[party].shift(1)
    #data.to_csv("data.csv", index=False, encoding="utf-8") just to see if correct
    print(data.shape)
    data['Date'] = pd.to_numeric(data['Date'])
    data['Change'] = 'None'
    data = data.reset_index(drop = True)
    for index, row in data.iterrows():
        station = row['Air Quality Station EoI Code']
        year = row['Date']
        if pollutant_data[(pollutant_data['Air Quality Station EoI Code'] == station) & (pollutant_data['Year'] == year + offset)].any()['Air Pollution Level'] and year + offset < 2025:
            election_result = row[parties]
            pollution_before = row['Air Pollution Level']
            pollution_after = pollutant_data[(pollutant_data['Air Quality Station EoI Code'] == station) & (pollutant_data['Year'] == year + offset)]['Air Pollution Level'].values[0]
            pollution_change =  (pollution_after - pollution_before) / pollution_before
            row['Change'] = pollution_change
            data.iloc[index] = row
    data = data[data['Change'] != 'None']
    data['Change'] = data['Change'].astype('float64')
    data = data[data['Others'] < 33]
    data = data[data['Date'] > 2013]
    data = data.reset_index(drop=True)
    z = np.abs(stats.zscore(data['Change']))
    threshold_z = 3
    outlier_indices = np.where(z > threshold_z)[0]
    data = data.drop(outlier_indices)
    data.reset_index(drop = True)
    return data
    
def analysis_and_plot(x, y, axs):
    # N = len(x)

    # statistic = lambda x, y: stats.linregress(x, y).rvalue
    # res = stats.permutation_test(data=(x, y), statistic=statistic, permutation_type='pairings')

    res = stats.linregress(x, y)
    
    axs.set_ylim([-0.5, 0.5])
    axs.plot(x, y, 'o', markersize=3, label='original data')
    axs.plot(x, res.intercept + res.slope*x, label='fitted line')
    return res

def single_party_regression():
    offset = 5
    parties = ['Linke', 'Gruene' , 'SPD', 'FDP', 'CDU', 'AfD']
    pollutants = ['CO', 'NO2' , 'O3', 'PM10', 'SO2']

    fig, axs = plt.subplots(len(pollutants), len(parties))

    for i, pollutant in enumerate(pollutants):
        data = process_data(parties, pollutant, offset)
        for j, party in enumerate(parties):
            x, y = data[party], data['Change']
            res = analysis_and_plot(x, y, axs[i, j])
            print(f'Pollutant {pollutant} for {party} done: p = {res.pvalue}, slope={res.slope}')

    for i, party in enumerate(parties):
        axs[len(pollutants)-1][i].set_xlabel(f'{party}')

    for i, pollutant in enumerate(pollutants):
        axs[i][0].set_ylabel(f'{pollutant}')

    plt.show()

def mulitvariate_regression():
    offset = 2
    parties = ['Linke', 'Gruene' , 'SPD', 'FDP', 'CDU', 'AfD']
    plot_parties = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']
    pollutants = ['CO', 'NO2' , 'O3', 'PM10', 'SO2']

    fig, axs = plt.subplots(len(pollutants), len(plot_parties))

    for i, pollutant in enumerate(pollutants):
        data = process_data(parties, pollutant, offset)

        # data = data.loc[(data[parties] != 0).all(axis=1)]

        #find design matrix for linear regression model using 'rating' as response variable 
        y, X = dmatrices(f'Change ~ {"+".join(parties)}', data=data, return_type='dataframe')

        #calculate VIF for each explanatory variable
        vif = pd.DataFrame()
        vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        vif['variable'] = X.columns

        #view VIF for each explanatory variable 
        print(vif)

        X = data[parties]
        y = data['Change']

        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()

        print(pollutant)
        print(model.summary())

        for j, party in enumerate(plot_parties):
            if len(pollutants) == 1:
                axs[j].plot(data[party], y, 'o', markersize=3, label='original data', color=party_colors[party], alpha=0.5)
                axs[j].plot(data[party], model.params['const'] + model.params[party]*data[party], label='fitted line', color='#ffa500')
            else:
                axs[i, j].plot(data[party], y, 'o', markersize=3, label='original data', color=party_colors[party], alpha=0.5)
                axs[i, j].plot(data[party], model.params['const'] + model.params[party]*data[party], label='fitted line', color='#ffa500')
        
        for i, party in enumerate(plot_parties):
            if len(pollutants) == 1:
                axs[i].set_xlabel(f'{party}')
            else:
                axs[len(pollutants)-1][i].set_xlabel(f'{party}')

        for i, pollutant in enumerate(pollutants):
            if len(pollutants) == 1:
                axs[0].set_ylabel(f'{pollutant}')
            else:
                axs[i][0].set_ylabel(f'{pollutant}')

    # plt.show()


def fixed_effects(use_index = False):
    offset = 2
    parties = ['Linke', 'Gruene' , 'SPD', 'FDP', 'CDU', 'AfD']
    pollutants = ['CO', 'NO2' , 'O3', 'PM10', 'SO2', 'PM25']
    
    if use_index:
        data = process_data_index(parties, offset)
        data = data.sort_values(by=['City', 'Date'])
        data = data.set_index(['City', 'Date'])

        mod = PanelOLS.from_formula(
            # with _lag WOOLDRIDGE
            'Change ~ Linke + Gruene + SPD + FDP + CDU + AfD + EntityEffects + TimeEffects',
            data
        )

        res = mod.fit()
        print(res.summary)
        

    else:
        for i, pollutant in enumerate(pollutants):
            
            data = process_data(parties, pollutant, offset)
            data = data.sort_values(by=['Air Quality Station EoI Code', 'Date'])
            #data['const'] =1 #for Breusch-Pagan

            data = data.set_index(['Air Quality Station EoI Code', 'Date'])


            mod = PanelOLS.from_formula(
                # with _lag WOOLDRIDGE
                'Change ~ Linke + Gruene + SPD + FDP + CDU + AfD + EntityEffects + TimeEffects',
                data
            )

            res = mod.fit()
            print(res.summary)
            #print(het_breuschpagan(res.resids, data[["Linke","Gruene","SPD","FDP","CDU","AfD",'const']])[1]) # Bresch-Pagan
            #print(acorr_ljungbox(res.resids,lags=[1],return_df =True))


plt.rcParams.update({"figure.dpi": 300})
plt.rcParams.update(bundles.neurips2021(usetex=True, family="serif"))
plt.rcParams.update(figsizes.neurips2021(nrows=2, ncols=2))
plt.rcParams.update(axes.spines(top=False, right=False))
plt.rcParams.update(markers.with_edge())
plt.rcParams.update(cycler.cycler(color=palettes.paultol_muted))

#mulitvariate_regression()
fixed_effects(use_index = False)