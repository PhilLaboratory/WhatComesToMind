import json
import numpy as np
from scipy import stats
import pandas as pd
from pymer4.models import Lmer
import pingouin as pg
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import rcParams
import matplotlib.patches as mpatches
rcParams.update({'figure.autolayout': True})

data_loc = '../clean_data/'


#Plots histogram of category member response counts for each category
#First plots all responses
#Then labeled high and low frequency responses only
def plot_response_counts():
    c = 'blueviolet'

    #get response counts
    with open(data_loc + 'study1/response_counts.json') as f:
        response_counts = json.load(f)
    
    #for all categories
    for cat, res_counts in response_counts.items():
        #sort data
        data = sorted([i for i in res_counts.items() if i[1] > 0], key=lambda x: x[1], reverse=True)
    
        #plot all responses
        labels = [pair[0] for pair in data]
        counts = [pair[1] for pair in data]
        pos = range(len(labels))
        plt.bar(pos, counts, color=c)
        plt.xticks([])
        plt.title(cat.title(), fontweight='bold', fontsize=18)
        plt.ylabel('Response Frequency', fontweight='bold', fontsize=16)
        plt.show()


        #plot just most and least frequent responses
        bottom_data = data[-10:]
        bottom_labels = [pair[0] for pair in bottom_data]
        bottom_counts = [pair[1] for pair in bottom_data]
        top_data = data[:10]
        top_labels = [pair[0] for pair in top_data]
        top_counts = [pair[1] for pair in top_data]
        labels = top_labels + ['','',''] + bottom_labels
        counts = top_counts + [0,0,0] + bottom_counts

        pos = range(len(labels))
        plt.bar(pos, counts, color=c)
        plt.xticks(pos, labels=labels, rotation=50, fontsize=12)
        plt.title(cat.title(), fontweight='bold', fontsize=18)
        plt.ylabel('Response Frequency', fontweight='bold', fontsize=16)
        plt.show()


#Plots zoo animals in 3d portion of feature space
#Colored according to log probability of coming to mind
#Zoo animal locations determined by average subejct ratings
def plot_ratings_3d():
    #average ratings
    with open(data_loc + 'study3/ratings.json') as f:
        ratings = json.load(f)["zoo animals"]
    #response counts
    with open(data_loc + 'study1/response_counts.json') as f:
        response_counts = json.load(f)["zoo animals"]
    
    #selected feature dimensions 
    dims = ['large', 'cute', 'dangerous']
    
    #store zoo animals' location in feature space and log probability of coming to mind
    labels = [k for k in ratings['large'].keys() if response_counts[k] > 0]
    d1,d2,d3,col=[],[],[],[]
    for l in labels:
        d1.append(ratings[dims[0]][l])
        d2.append(ratings[dims[1]][l])
        d3.append(ratings[dims[2]][l])
        col.append(math.log(response_counts[l]/sum(response_counts.values())))
    
    #set labels and plot details
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel(dims[0], fontweight='bold', fontsize='14')
    ax.set_ylabel(dims[1], fontweight='bold',fontsize='14')
    ax.set_zlabel(dims[2], fontweight='bold',fontsize='14')
    ax.set_zlim([1,5])
    p = ax.scatter3D(d1, d2, d3, c=col, cmap=cm.cool)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    plt.xlim([1,5])
    plt.ylim([1,5])
    plt.locator_params(axis="x", nbins=4)
    plt.locator_params(axis="y", nbins=4)
    plt.locator_params(axis="z", nbins=4)
    plt.title("Zoo Animal Feature Space", fontweight='bold',fontsize='18')
    fig.colorbar(p, shrink=0.5)

    #label a few zoo animals
    for i, an in enumerate(labels):
        if an in ['lion', 'elephant', 'penguin', 'snake', 'goat']:
            ax.text(d1[i], d2[i], d3[i], an, fontsize=12)

    plt.show()   


#For each category, plots each feature's relevance for that category
def plot_ft_relevance():
    c = 'blueviolet'
    #get feature relevance
    with open(data_loc + 'study6/feature_relevance.json') as f:
        ft_relevance = json.load(f)
    for cat in ft_relevance.keys():
        if cat != "zoo animals":
            continue
        data = sorted(ft_relevance[cat].items(), key=lambda x: x[1], reverse=True)
        #plot all responses
        labels = [pair[0] for pair in data]
        for i in range(len(labels)):
            l = labels[i]
            if ", " in l:
                l = l.split(", ")[1]
            if l == "has good hearing":
                l="good hearing"
            if l == "has large feet relative to its body size":
                l="large feet"
            if l == "has long hair":
                l = "long hair"
            labels[i] = l
        counts = [pair[1] for pair in data]
        pos = range(len(labels))
        plt.bar(pos, counts, color=c)
        plt.xticks(pos, labels, rotation=60, fontsize=14)
        plt.title(cat.title(), fontweight='bold', fontsize=26)
        plt.ylabel('Feature Relevance', fontweight='bold', fontsize=18)
        plt.show()


#Takes dictionary with each features' predictiveness of what comes to mind in each category
#Plots scatter plot of feature predictiveness of what comes to mind, and feature relevance
    #Within each category
    #And across categories
#And prints correlations between feature predictiveness and relevance
def plot_ft_predicteveness_vs_relevance(ft_pred):
    c='blueviolet'
    #get feature relevance
    with open(data_loc + 'study6/feature_relevance.json') as f:
        ft_relevance = json.load(f)
    all_pred, all_rel = [], []
    #plot each category individually
    cat_colors = {'zoo animals': 'blue', 'chain restaurants': 'orange', 'vegetables': 'green', 'sports': 'pink', 'kitchen appliances': 'red', 'jobs': 'purple', 'holidays': 'yellow'}
    ft_colors=[]
    for cat in ft_relevance.keys():
        rel, pred, lab = [], [], []
        for k in ft_relevance[cat].keys():
            ft_colors.append(cat_colors[cat])
            rel.append(ft_relevance[cat][k])
            all_rel.append(ft_relevance[cat][k])
            pred.append(ft_pred[cat][k])
            all_pred.append(ft_pred[cat][k])
            #shorten and store ft names as labels
            if ", " in k:
                k = k.split(", ")[1]
            if k == "has good hearing":
                k="good hearing"
            if k == "has large feet relative to its body size":
                k="large feet"
            if k == "has long hair":
                k = "long hair"
            lab.append(k)

        fig = plt.figure()
        ax = plt.axes()
        ax.set_xlabel('Relevance', fontweight='bold', fontsize=15)
        ax.set_ylabel('Predictiveness of What Comes to Mind', fontweight='bold', fontsize=15)
        for i, k in enumerate(lab):
            if k in ['good hearing', 'large feet', 'long hair', 'diurnal','cool']:
                ax.text(rel[i], pred[i]-0.015, '' + k, fontsize=14)
            else:
                ax.text(rel[i], pred[i], ' ' + k, fontsize=14)
        plt.scatter(rel, pred, color=c)
        #obtain m (slope) and b(intercept) of linear regression line
        m, b = np.polyfit(rel, pred, 1)
        rel = np.array(rel)
        #add linear regression line to scatterplot 
        plt.plot(rel, m*rel+b, color=c)
        plt.title(cat.title(), fontweight='bold', fontsize=22)
        plt.show()
        r,p = stats.pearsonr(rel, pred)
        print(cat + ": r=" + str(r) + ", p=" + str(p))
    #plot all categories together
    fig = plt.figure()
    ax = plt.axes()
    ax.set_xlabel('Relevance', fontweight='bold', fontsize=15)
    ax.set_ylabel('Predictiveness of What Comes to Mind', fontweight='bold', fontsize=15)
    plt.scatter(all_rel, all_pred, color=ft_colors)
    #obtain m (slope) and b(intercept) of linear regression line
    m, b = np.polyfit(all_rel, all_pred, 1)
    all_rel = np.array(all_rel)
    #add linear regression line to scatterplot 
    plt.plot(all_rel, m*all_rel+b, color='black')
    patches = []
    for cat, col in cat_colors.items():
        patches.append(mpatches.Patch(color=col, label=cat))
    ax.legend(handles=patches) 
    plt.title("All Categories", fontweight='bold',fontsize=22)
    plt.show()
    r,p = stats.pearsonr(all_rel, all_pred)
    print("overall: r=" + str(r) + ", p=" + str(p))


#Takes response counts for category members in each category
#And ratings for each category member for each feature in each category
#Returns, for each category, each feature's predictiveness of what comes to mind
    #As calculated by correlation between each category member's average rating for that feature
    #And category member's frequency of coming to mind in study 1
def get_ft_predictiveness(response_counts, ratings):
    ft_pred = {}
    #go thru each category
    for cat in ratings.keys():
        ft_pred[cat] = {}
        #go thru each feature
        for ft in ratings[cat].keys():
            #calc correlation between each category member's rating for this feature
            #and category member's frequency of coming to mind
            cat_memb_rating = []
            cat_memb_freq = []
            for cat_memb in ratings[cat][ft].keys():
                #rating
                cat_memb_rating.append(ratings[cat][ft][cat_memb])
                #freq
                cat_memb_freq.append(response_counts[cat][cat_memb])
            ft_pred[cat][ft] = np.corrcoef(cat_memb_rating, cat_memb_freq)[0][1]
    return ft_pred  


#Takes dictionary with each features' predictiveness of what comes to mind in each category
#For each category in keys, plots each feature's predictiveness of what comes to mind in that category
#Features negatively correlated with likelihood of coming to mind plotted in red
def plot_ft_predictiveness(ft_pred):
    #in each category, plot predictiveness of each feature
    for cat in ft_pred.keys():
        #sort data
        data = sorted(ft_pred[cat].items(), key=lambda x: abs(x[1]), reverse=True)
        
        #store predictiveness of each feature
        counts = [abs(pair[1]) for pair in data]

        #shorten and store ft names as labels
        labels = [pair[0] for pair in data]
        for i in range(len(labels)):
            l = labels[i]
            if ", " in l:
                l = l.split(", ")[1]
            if l == "has good hearing":
                l="good hearing"
            if l == "has large feet relative to its body size":
                l="large feet"
            if l == "has long hair":
                l = "long hair"
            labels[i] = l
        
        #color bars by sign of correlation
        colors = []
        for pair in data:
            if pair[1] > 0:
                colors.append('blue')
            else:
                colors.append('red')
        
        #set labels and plot
        pos = range(len(labels))
        plt.bar(pos, counts, color=colors)
        plt.legend(['positive','negative'], fontsize=12)
        plt.xticks(pos, labels, rotation=60, fontsize=12)
        plt.title(cat.title(), fontweight='bold', fontsize=24)
        plt.ylabel('Predictiveness of What Comes to Mind', fontweight='bold', fontsize=16)
        plt.show()


#Runs generalized linear mixed effects regression on intrusion data across categories
#Prints model fit details
def run_intrusions_lmer():
    with open(data_loc + 'study5/responses.json') as f:
        data = json.load(f)
    
    #store model variables
    intrusion, subject, category, feature_dimension, predictive = [], [], [], [], []
    cat_nums = {"zoo animals":1,"chain restaurants":2,"holidays":3}
    for cat, trials in data.items():
        for trial in trials:
            for i in range(len(trial["intrusions"])):
                intrusion.append(trial["intrusions"][i])
                subject.append(trial["subject_id"])
                category.append(cat_nums[cat])
                feature_dimension.append(trial["ft_dimension"])
                predictive.append(int(trial["is_predictive"])+1)
    #convert to df
    my_data = pd.DataFrame({"intrusion":intrusion,"subject":subject,"category":category,"feature_dimension":feature_dimension,"predictive":predictive})
    #fit model and print results
    model = Lmer('intrusion ~ predictive + category + (1|subject) + (predictive|feature_dimension)', data=my_data, family = 'binomial')
    print(model.fit())
    print("overall prob of intrusions for predictive features:", np.mean([intrusion[i] for i in range(len(intrusion)) if predictive[i]]))
    print("overall prob of intrusions for non predictive features:", np.mean([intrusion[i] for i in range(len(intrusion)) if not predictive[i]]))


#For each category, plots intrusion probability for both ends of each feature dimension
def plot_intrusions():
    with open(data_loc + 'study5/responses.json') as f:
        data = json.load(f)
    
    #in each category, for each feature, store probability of intrusion for each subject
    intrusions = {}
    #keep track of which features are predictive to plot correctly
    predictive = []
    for cat, trials in data.items():
        intrusions[cat] = {}
        for trial in trials:
            dim = trial["ft_dimension"]
            ft = trial["ft"]
            if trial["is_predictive"] and ft not in predictive:
                predictive.append(ft)
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
    print(intrusion_prob)
    #plot intrusion probability for each category seperately
    for cat, ft_dims in intrusion_prob.items():
        #store ft names for labels and intrusion probabilities for y coordinates
        labels = []
        y = []
        for dim, ft_probs in ft_dims.items():
            for ft, prob in ft_probs.items():
                if ft in predictive:
                    labels.append(ft)
                    y.append(prob)
            for ft, prob in ft_probs.items():
                if ft not in predictive:
                    labels.append(ft)
                    y.append(prob)
        #arbitrary x coordinate
        x = [0.3,0.8] * int(len(y)/2)

        #plot intrusion probabilities for each feature
        fig, ax = plt.subplots()
        for i in range(0,len(x)-1,2):
            line, = plt.plot([x[i],x[i+1]],[y[i],y[i+1]])#, color=c)
            line.set_label(labels[i] + "-" + labels[i+1])
        plt.scatter(x + [0,1], y + [.65,.65], color=['blue','blue','orange','orange','green','green','red','red','purple','purple', 'white', 'white'])
        
        #set labels
        ax.set_ylabel('Probability of Intrusion',fontweight='bold')
        plt.xticks([0.3,0.8], ['Predictive\nEnd', 'Non Predictive\nEnd'], fontweight='bold')
        plt.title(cat.title(), fontweight='bold')
        plt.legend(loc='upper left')
        plt.show()


#Runs all analyses by default
if __name__ == "__main__":  
    #plot response counts for each category
    plot_response_counts()
    
    #plot zoo animals in 3d portion of feature space
    plot_ratings_3d()
    
    #plot each feature's predictiveness of coming to mind
    with open(data_loc + 'study1/response_counts.json') as f:
        response_counts = json.load(f)
    with open(data_loc + 'study3/ratings.json') as f:
        ratings = json.load(f)
    ft_pred = get_ft_predictiveness(response_counts, ratings)
    plot_ft_predictiveness(ft_pred)
    
    #plot feature predictiveness in ad hoc categories
    with open(data_loc + 'study4/generation_response_counts.json') as f:
        response_counts = json.load(f)
    with open(data_loc + 'study4/ratings.json') as f:
        ratings = json.load(f)
    adhoc_ft_pred = get_ft_predictiveness(response_counts, ratings)
    plot_ft_predictiveness(adhoc_ft_pred)
    
    #plot intrusion probability and print lmer details
    run_intrusions_lmer()
    plot_intrusions()
    
    #plot feature relevance
    plot_ft_relevance()
    
    #plot relationship between feature predictiveness and feature relevance
    #also prints pearson correlation coefficient and p value
    plot_ft_predicteveness_vs_relevance(ft_pred)