#!/usr/bin/env python3
import json
import numpy as np


#returns raw data
def get_data():
    with open('../../raw_data/study4/ratings/trials.json') as f:
        data = json.load(f)
    return data

#returns data organized by category
def get_clean_data(raw_data):
    clean_data = {}
    for trial in raw_data:
        clean_data[trial["cat"]] = clean_data.get(trial["cat"], [])
        clean_trial = {}
        clean_trial["item"] = trial["item"]
        clean_trial["subject_id"] = trial["row_id"][:-2]
        clean_trial["responses"] = trial["responses"]
        clean_data[trial["cat"]].append(clean_trial)
    return clean_data

#returns average ratings for each item according to each feature, by category
def get_ave_ratings(data):
    ratings = {}
    #iterate thru each category
    for cat, trials in data.items():
        ratings[cat] = {}
        #iterate thru all trials for this category
        for trial in trials:
            it = trial["item"]
            if it in ["baby lion", "baby tiger"]:
                continue
            #list scores for item/feature pair
            for k in trial["responses"].keys():
                ratings[cat][k] = ratings[cat].get(k,{})
                ratings[cat][k][it] = ratings[cat][k].get(it, []) + [trial["responses"][k]]
    #compute mean of lists for item/feature ratings in each category
    for cat, pairs in ratings.items():
        for ft, its in pairs.items():
            for it in its:
                ratings[cat][ft][it] = np.mean(ratings[cat][ft][it])
    return ratings


if __name__ == "__main__":
    #location for clean data
    clean_data_loc = '../../clean_data/study4/'
    #get response data
    data = get_data()
    #store clean data
    clean_data = get_clean_data(data)
    with open(clean_data_loc + 'ratings_responses.json', 'w') as f:
        json.dump(clean_data, f)
    #get and store average ratings from responses
    ratings = get_ave_ratings(clean_data)
    with open(clean_data_loc + 'ratings.json', 'w') as f:
        json.dump(ratings, f)