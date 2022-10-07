#!/usr/bin/env python3
import json
import numpy as np


#returns raw data
def get_raw_data():
    with open('../raw_data/study3/trials.json') as f:
        data = json.load(f)
    return data

#returns clean data
#   changes categorical responses to numeric
def get_clean_data(data):
    clean_data = {}
    #iterate thru each category
    for cat, trials in data.items():
        clean_data[cat] = []
        #iterate thru all trials for this category
        for trial in trials:
            clean_trial = {}
            clean_trial["subject_id"] = trial["subject_id"]
            clean_trial["item"] = trial["item"].lower()
            #store scores for item/feature pair in dict
            clean_trial["ratings"] = {}
            for k in trial.keys():
                if k in ["item", "trial_order", "turk_code", "subject_id", "rt", "age", "language", "nationality", "country", "gender", "student", "education"]:
                    continue
                #convert to all numeric responses
                if trial[k] in ["null", "dont know"]:
                    continue
                elif k == "awake":
                    clean_trial["ratings"]["diurnal"] = int(trial[k] == "day")
                    clean_trial["ratings"]["nocturnal"] = int(not(trial[k] == "day"))
                elif k == "diet":
                    for r in ["herbivore", "omnivore", "carnivore"]:
                        clean_trial["ratings"][k + ", " + r] = int(r==trial[k])
                elif k == "type":
                    for r in ["mammal", "fish", "bird", "reptile", "amphibean", "invertibrate"]:
                        clean_trial["ratings"][k + ", " + r] = int(r==trial[k])
                elif trial[k] == "very rarely":
                    clean_trial["ratings"][k] = 0
                elif trial[k] == "rarely":
                    clean_trial["ratings"][k] = 1
                elif trial[k] == "an average amount":
                    clean_trial["ratings"][k] = 2
                elif trial[k] == "often":
                    clean_trial["ratings"][k] = 3
                elif trial[k] == "very often":
                    clean_trial["ratings"][k] = 4
                elif trial[k] == "long":
                    clean_trial["ratings"][k] = 2
                elif trial[k] == "medium":
                    clean_trial["ratings"][k] = 1
                elif trial[k] == "short":
                    clean_trial["ratings"][k] = 0  
                elif trial[k] == "yes":
                    clean_trial["ratings"][k] = 1
                elif trial[k] == "no":
                    clean_trial["ratings"][k] = 0
                else:
                    clean_trial["ratings"][k] = int(trial[k])
            clean_data[cat].append(clean_trial)
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
            #list scores for item/feature pair
            for k in trial["ratings"].keys():
                ratings[cat][k] = ratings[cat].get(k,{})
                ratings[cat][k][it] = ratings[cat][k].get(it, []) + [trial["ratings"][k]]
    #compute mean of lists for item/feature ratings in each category
    for cat, pairs in ratings.items():
        for ft, its in pairs.items():
            for it in its:
                ratings[cat][ft][it] = np.mean(ratings[cat][ft][it])
    return ratings
    

if __name__ == "__main__":
    #location for clean data
    clean_data_loc = '../clean_data/study3/'
    #get raw response data
    data = get_raw_data()
    #clean and store response data
    clean_data = get_clean_data(data)
    with open(clean_data_loc + 'responses.json', 'w') as f:
        json.dump(clean_data, f)
    #get and store average ratings from responses
    ratings = get_ave_ratings(clean_data)
    with open(clean_data_loc + 'ratings.json', 'w') as f:
        json.dump(ratings, f)