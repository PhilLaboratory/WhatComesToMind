#!/usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import stats
import pandas as pd
from pymer4.models import Lmer
import math


#include the extent to which these predictive feature dimensions are independent vs. capturing the same variance.


data_loc = '../clean_data/'

#plot histogram of response counts
def plot_response_counts():
    with open(data_loc + 'study1/response_counts.json') as f:
        response_counts = json.load(f)
    
    #for all categories
    for cat, res_counts in response_counts.items():
        data = sorted(res_counts.items(), key=lambda x: x[1], reverse=True)
    
        #plot all responses
        labels = [pair[0] for pair in data]
        counts = [pair[1] for pair in data]
        pos = range(len(labels))
        plt.bar(pos, counts)
        plt.xticks(pos, labels, rotation=90)
        plt.title(cat, fontweight='bold')
        plt.ylabel('Response Frequency', fontweight='bold')
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
        plt.bar(pos, counts)
        plt.xticks(pos, labels=labels, rotation=30)
        plt.title(cat, fontweight='bold')
        plt.ylabel('Response Frequency', fontweight='bold')
        plt.show()

#plot zoo animals in 3d portion of feature space
def plot_ratings_3d():
    with open(data_loc + 'study3/ratings.json') as f:
        ratings = json.load(f)["zoo animals"]
    with open(data_loc + 'study1/response_counts.json') as f:
        response_counts = json.load(f)["zoo animals"]
    
    #feature dimensions large, cute, dangerous
    dims = ['large', 'cute', 'dangerous']
    
    #for each category member, record position along each ft dimension and ...
    labels = ratings['large'].keys()
    d1,d2,d3,col=[],[],[],[]
    for l in labels:
        d1.append(ratings[dims[0]][l])
        d2.append(ratings[dims[1]][l])
        d3.append(ratings[dims[2]][l])
        #log normalize
        col.append(math.log(response_counts.get(l,0) + 1))

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel(dims[0], fontweight='bold')
    ax.set_ylabel(dims[1], fontweight='bold')
    ax.set_zlabel(dims[2], fontweight='bold')
    ax.set_zlim([1,5])

    #label select category members
    for i, an in enumerate(labels):
        if an in ['lion', 'elephant', 'penguin', 'snake', 'goat', 'beetle']:
            ax.text(d1[i], d2[i], d3[i], an)
    
    ax.scatter3D(d1, d2, d3, c=col, cmap=cm.spring)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.xlim([1,5])
    plt.ylim([1,5])

    plt.locator_params(axis="x", nbins=4)
    plt.locator_params(axis="y", nbins=4)
    plt.locator_params(axis="z", nbins=4)

    plt.title("Zoo Animal Feature Space")
    plt.legend()
    plt.show() 

#for each category, get each feature's predictiveness of what comes to mind
#as calculated by correlation between each category member's location along that feature dimension
#and category member's frequency of coming to mind in study 1
def get_ft_predictiveness():
    ft_pred = {}
    #category members' frequency of coming to mind
    with open(data_loc + 'study1/response_counts.json') as f:
        response_counts = json.load(f)
    #category members' feature ratings
    with open(data_loc + 'study3/ratings.json') as f:
        ratings = json.load(f)
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

#for each category, plot each feature's predictiveness of what comes to mind
#features negative correlated with likelihood of coming to mind plotted in red
def plot_ft_predictiveness():
    #get each feature's predictivenss of what comes to mind
    ft_pred = get_ft_predictiveness()
    for cat in ft_pred.keys():
        data = sorted(ft_pred[cat].items(), key=lambda x: abs(x[1]), reverse=True)
        #plot all responses
        labels = [pair[0] for pair in data]
        counts = [abs(pair[1]) for pair in data]
        colors = []
        for pair in data:
            if pair[1] > 0:
                colors.append('blue')
            else:
                colors.append('red')
        pos = range(len(labels))
        plt.bar(pos, counts, color=colors)
        plt.legend(['positive','negative'])
        plt.xticks(pos, labels, rotation=30)
        plt.title(cat, fontweight='bold')
        plt.ylabel('Predictiveness of what comes to mind', fontweight='bold')
        plt.show()
    
	
def plot_ft_relevance():
    #get feature relevance
    with open(data_loc + 'study6/feature_relevance.json') as f:
        ft_relevance = json.load(f)
    for cat in ft_relevance.keys():
        data = sorted(ft_relevance[cat].items(), key=lambda x: x[1], reverse=True)
        #plot all responses
        labels = [pair[0] for pair in data]
        counts = [pair[1] for pair in data]
        pos = range(len(labels))
        plt.bar(pos, counts)
        plt.xticks(pos, labels, rotation=30)
        plt.title(cat, fontweight='bold')
        plt.ylabel('Feature relevance', fontweight='bold')
        plt.show()

def plot_ft_predicteveness_vs_relevance():
    #get each feature's predictivenss of what comes to mind
    ft_pred = get_ft_predictiveness()
    #get feature relevance
    with open(data_loc + 'study6/feature_relevance.json') as f:
        ft_relevance = json.load(f)
    all_pred, all_rel = [], []
    #plot each category individually
    for cat in ft_relevance.keys():
        rel, pred, lab = [], [], []
        for k in ft_relevance[cat].keys():
            rel.append(ft_relevance[cat][k])
            all_rel.append(ft_relevance[cat][k])
            pred.append(ft_pred[cat][k])
            all_pred.append(ft_pred[cat][k])
            lab.append(k)
        r,p = scatter_lists(rel, pred, lab, 'Relevance', 'Predictiveness of What Comes to Mind', cat)
        print(cat + ": r=" + str(r) + ", p=" + str(p))
    #plot all categories together
    r,p = scatter_lists(all_rel, all_pred, [], 'Relevance', 'Predictiveness of What Comes to Mind', "All Categories")
    print("overall: r=" + str(r) + ", p=" + str(p))
        

#plot scatterplot of values in two lists
#returns pearson r and p value of relationship
def scatter_lists(x, y, lab, x_lab, y_lab, title):
    fig = plt.figure()
    ax = plt.axes()
    ax.set_xlabel(x_lab, fontweight='bold')
    ax.set_ylabel(y_lab, fontweight='bold')
    for i, k in enumerate(lab):
        ax.text(x[i], y[i], ' ' + k)
    plt.scatter(x, y)
    plt.title(title, fontweight='bold')
    plt.show()
    return(stats.pearsonr(x, y))

#for each category, get each feature's predictiveness of what comes to mind
#as calculated by correlation between each category member's location along that feature dimension
#and category member's frequency of coming to mind in study 1
def get_adhoc_ft_predictiveness():
    ft_pred = {}
    #category members' frequency of coming to mind
    with open(data_loc + 'study4/generation_response_counts.json') as f:
        response_counts = json.load(f)
    #category members' feature ratings
    with open(data_loc + 'study4/ratings.json') as f:
        ratings = json.load(f)
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

def plot_adhoc_ft_predictiveness():
    #get each feature's predictivenss of what comes to mind
    ft_pred = get_adhoc_ft_predictiveness()

    for cat in ft_pred.keys():
        data = sorted(ft_pred[cat].items(), key=lambda x: abs(x[1]), reverse=True)
        #plot all responses
        labels = [pair[0] for pair in data]
        counts = [abs(pair[1]) for pair in data]
        colors = []
        for pair in data:
            if pair[1] > 0:
                colors.append('blue')
            else:
                colors.append('red')
        pos = range(len(labels))
        plt.bar(pos, counts, color=colors)
        plt.legend(['positive','negative'])
        plt.xticks(pos, labels, rotation=30)
        plt.title(cat, fontweight='bold')
        plt.ylabel('Predictiveness of what comes to mind', fontweight='bold')
        plt.show()

def run_intrusions_lmer():
    with open(data_loc + 'study5/responses.json') as f:
        data = json.load(f)
    intrusion, subject, category, feature_dimension, predictive = [], [], [], [], []
    cat_nums = {"zoo animals":1,"chain restaurants":2,"holidays":3}
    for cat, trials in data.items():
        for trial in trials:
            for i in range(len(trial["intrusions"])):
                intrusion.append(trial["intrusions"][i])
                subject.append(trial["subject_id"])
                category.append(cat_nums[cat])
                feature_dimension.append(trial["ft_dimension"])
                predictive.append(int(trial["is_predictive"]))
    my_data = pd.DataFrame({"intrusion":intrusion,"subject":subject,"category":category,"feature_dimension":feature_dimension,"predictive":predictive})
    model = Lmer('intrusion ~ predictive + category + (1|subject) + (predictive|feature_dimension)', data=my_data, family = 'binomial')
    print(model.fit())


def plot_intrusions():
    with open(data_loc + 'study5/responses.json') as f:
        data = json.load(f)
    intrusions = {}
    #in each category, for each feature, for each response, list 1 for intrusion and 0 otherwise
    #keep track of which features are predictive
    predictive = []
    for cat, trials in data.items():
        intrusions[cat] = {}
        for trial in trials:
            dim = trial["ft_dimension"]
            ft = trial["ft"]
            if trial["is_predictive"] and ft not in predictive:
                predictive.append(ft)
            intrusions[cat][dim] = intrusions[cat].get(dim, {})
            intrusions[cat][dim][ft] = intrusions[cat][dim].get(ft, []) + trial["intrusions"]
    #probability that response is an intrusion for each feature
    intrusion_prob = {}
    for cat, ft_dims in intrusions.items():
        intrusion_prob[cat] = {}
        for dim, ft_lists in ft_dims.items():
            intrusion_prob[cat][dim] = intrusion_prob[cat].get(dim, {})
            for ft, lists in ft_lists.items():
                intrusion_prob[cat][dim][ft] = np.mean(intrusions[cat][dim][ft])
    
    #plot each category seperately
    for cat, ft_dims in intrusion_prob.items():
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

        #probs
        x = [0.3,0.8] * int(len(y)/2)

        fig, ax = plt.subplots()
        plt.scatter(x, y, color=['blue','blue','orange','orange','green','green','red','red','purple','purple'])
        #plt.scatter(x + [0,1], y + [.7,.7], color=['blue']*10 + ['red']*10 + ['green'] * 10 + ['white']*2)#color=['blue','blue','orange','orange','green','green','red','red','purple','purple','white','white'])
        #plt.scatter(x, y)#, color=['blue','blue','white','white','white','white','white','white','white','white'])
        #ax.boxplot([[y[0], y[2], y[4], y[6], y[8]], [y[1], y[3], y[5], y[7], y[9]]], positions=[0.3,0.8],whis=(0, 100))
        ax.set_ylabel('Probability of Intrusion',fontweight='bold')
        #for i, txt in enumerate(labels):
        #    ax.annotate(txt, (x[i], y[i]))
        #plt.scatter(x,y)
        for i in range(0,len(x)-1,2):
        #for i in range(0,2,2):
            #c=['blue','red','green'][(i>9)+(i>19)]
            line, = plt.plot([x[i],x[i+1]],[y[i],y[i+1]])#, color=c)
            line.set_label(labels[i] + "-" + labels[i+1])
        plt.xticks([0.3,0.8], ['Predictive\nEnd', 'Non Predictive\nEnd'], fontweight='bold')
        #plt.xticks([])
        plt.title(cat, fontweight='bold')
        plt.legend(loc='upper left')
        plt.show()


if __name__ == "__main__":
    
    #plot response counts for each category
    #plot_response_counts()

    #3d plot for ratings
    plot_ratings_3d()
    """
    #plot each feature's predictiveness of coming to mind
    plot_ft_predictiveness()

    #plot feature relevance
    plot_ft_relevance()

    #plot relationship between feature predictiveness and feature relevance
    #also prints pearson correlation coefficient and p value
    plot_ft_predicteveness_vs_relevance()
    
    #ad hoc
    #get_adhoc_ft_predictiveness()
    plot_adhoc_ft_predictiveness()

    #intrusions
    #run_intrusions_lmer()
    plot_intrusions()
    """