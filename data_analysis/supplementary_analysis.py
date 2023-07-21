import json
import numpy as np
from scipy import stats
import pandas as pd
import math
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo
chart_studio.tools.set_credentials_file(username=USER, api_key=API_KEY)
import chart_studio.plotly as py
import plotly.graph_objects as go
import pandas as pd

#run factor analysis on each category
def factor_analysis():
    with open(data_loc + 'study3/ratings.json') as f:
        all_ratings = json.load(f)
    for category in all_ratings.keys():
        ratings = all_ratings[category]
        #remove features highly correlated with other features, or with zero variance (invertibrate)
        if category=="zoo animals":
            ratings.pop("nocturnal")
            ratings.pop("diet, herbivore")
            ratings.pop("water")
            ratings.pop("type, invertibrate")

        df = pd.DataFrame(ratings, columns = ratings.keys())

        #check whether factor analysis is appropriate with bartlett sphericity and kmo
        chi_square_value,p_value=calculate_bartlett_sphericity(df)
        print(chi_square_value, p_value)
        kmo_all,kmo_model=calculate_kmo(df)
        print(kmo_all,kmo_model)

        #get number of factors with eigenvalues >1
        fa = FactorAnalyzer(len(ratings.keys()), rotation=None)
        fa.fit(df)
        ev = fa.get_eigenvalues()[0]
        num_factors = len([v for v in ev if v>1])

        # Create factor analysis object and perform factor analysis
        fa = FactorAnalyzer(num_factors, rotation="varimax", method='ml', use_smc=True)
        fa.fit(df)
        print(category.title())
        print("factor loadings for each feature:")
        cols=['Factor ' + str(i) for i in range(num_factors)]
        loadings = pd.DataFrame(fa.loadings_, columns=cols, index=df.columns)
        print(loadings)

        print("communalities:")
        communalities = fa.get_communalities()
        print(communalities) #how much variance of each var explained by the factors

        print("variance accounted for by factors:")
        variance = fa.get_factor_variance()
        print(variance)

#determine number of factors through eigenvalues or scree plot
def explore_num_factors(df, ratings):
    fa = FactorAnalyzer(len(ratings.keys()), rotation=None)
    fa.fit(df)
    #get eigenvalues
    ev = fa.get_eigenvalues()[0]
    num_factors = len([v for v in ev if v>1])
    # screeplot
    plt.scatter(range(1,df.shape[1]+1),ev)
    plt.plot(range(1,df.shape[1]+1),ev)
    plt.title('Scree Plot')
    plt.xlabel('Factors')
    plt.ylabel('Eigenvalue')
    plt.grid()
    plt.show()


#For each category, prints probability of intrusion at both ends of each feature dimension
#probability calculated as percentage of responses that are intrusions for a subject, averaged across subjects
def get_intrusion_stats():
    with open(data_loc + 'study5/responses.json') as f:
        data = json.load(f)
    
    #in each category, for each feature, store probability of intrusion for each subject
    intrusions = {}
    for cat, trials in data.items():
        intrusions[cat] = {}
        for trial in trials:
            dim = trial["ft_dimension"]
            ft = trial["ft"]
            intrusions[cat][dim] = intrusions[cat].get(dim, {})
            #record probability of intrusion for this subject
            intrusions[cat][dim][ft] = intrusions[cat][dim].get(ft, []) + [np.mean(trial["intrusions"])]

    #store average probability of intrusions for a given feature across subjects
    intrusion_prob = {}
    for cat, ft_dims in intrusions.items():
        intrusion_prob[cat] = {}
        for dim, ft_lists in ft_dims.items():
            intrusion_prob[cat][dim] = intrusion_prob[cat].get(dim, {})
            for ft, lists in ft_lists.items():
                intrusion_prob[cat][dim][ft] = np.mean(intrusions[cat][dim][ft])
    print("probability of intrusion:")
    for cat in intrusion_prob:
        print(cat.title())
        for dims in intrusion_prob[cat].values():
            fts = list(dims.items())
            print(fts[0][0] + ": " + str(round(fts[0][1],2)) + ", " + fts[1][0] + ": " + str(round(fts[1][1],2)))

if __name__ == "__main__":
    data_loc = '../clean_data/'
    
    #print factor analysis over all features in a category
    factor_analysis()

    #print study 5 intrusion data
    get_intrusion_stats()
