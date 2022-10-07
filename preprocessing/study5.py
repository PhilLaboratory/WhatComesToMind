#!/usr/bin/env python3

import json
import numpy as np


#returns raw data
def get_data():
    with open('../raw_data/study5/trials.json') as f:
        data = json.load(f)
    return data

#returns data organized by category
def get_clean_data(raw_data):
    #note which features are predictive of what comes to mind
    predictive_features = {"zoo animals": ["long-lived", "dangerous", "striking", "large", "cool"], "holidays": ["likes", "time off", "widely celebrated", "think", "romantic"], "chain restaurants": ["many locations", "popular", "cheap", "ordinary", "brightly colored logo"]}
    #and assign unique id to each feature dimension
    feature_dimensions = {"zoo animals": {"large": 1, "small": 1, "dangerous": 2, "harmless": 2, "long-lived": 3, "short-lived": 3, "cool": 4, "boring": 4, "striking": 5, "unremarkable": 5}, "holidays": {'time off':6, 'no time off':6, 'likes':7, 'not likes':7, 'think':8, 'not think':8, 'widely celebrated':9, 'fewest':9, 'romantic':10, 'unromantic':10}, "chain restaurants": {'many locations':11, 'few locations':11, 'popular':12, 'unpopular':12, 'cheap':13, 'expensive':13, 'ordinary':14, 'unique':14, 'brightly colored logo':15,'dull logo':15}} 
    clean_data = {}
    for cat, trials in raw_data.items():
        clean_data[cat] = []
        for trial in trials:
            clean_trial = {}
            clean_trial["response"] = trial["answer"]
            clean_trial["subject_id"] = trial["row_id"]
            clean_trial["considerations"] = trial["considerations"]
            clean_trial["ft"] = trial["ft"]
            clean_trial["is_predictive"] = (clean_trial["ft"] in predictive_features[cat])
            clean_trial["opp_ft"] = trial["opp_ft"]
            clean_trial["ft_ratings"] = trial["ft_dict"]
            clean_trial["opp_ft_ratings"] = trial["opp_ft_dict"]
            clean_trial["ft_dimension"] = feature_dimensions[cat][clean_trial["ft"]]
            clean_trial["intrusions"] = [int(clean_trial["ft_ratings"][c] < 50) for c in clean_trial["considerations"]]
            clean_data[cat].append(clean_trial)
    return clean_data

if __name__ == "__main__":
    #location for clean data
    clean_data_loc = '../clean_data/study5/'
    #get response data
    data = get_data()
    #store clean data
    clean_data = get_clean_data(data)
    with open(clean_data_loc + 'responses.json', 'w') as f:
        json.dump(clean_data, f)