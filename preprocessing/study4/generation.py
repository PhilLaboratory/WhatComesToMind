#!/usr/bin/env python3
import json

#returns raw data
def get_raw_data():
    with open('../../raw_data/study4/generation/trials.json') as f:
        temp_data = json.load(f)
    data = []
    #only preprocess the 2 categories for which we gather feature ratings
    for trial in temp_data:
        if trial["cat"] in ["zoo animals you would take with you on a plane", "vegetables that you would use to paint your house"]:
            data.append(trial)
    return data

#clean response by
#   making lower case,
#   taking care of typos,
#   reconciling similar responses into a single response
#returns clean response
def get_clean_response(cat, res):
    res = res.lower().strip()
    if cat == "zoo animals you would take with you on a plane":
        if res in ["chimpanzee"]: res = "chimp"
        elif res in ["orangutang", "orangutange", "orangatan", "arungaton", "orangutans"]: res = "orangutan"
        elif res in ["snakes"]: res = "snake"
        elif res in ["chickens"]: res = "chicken"
        elif res in ["raccoons", "racoon"]: res = "raccoon"
        elif res in ["ground hog"]: res = "groundhog"
        elif res in ["sea otter", "sea otters", "otters"]: res = "otter"
        elif res in ["hippopotamus", "hippopatamus", "hippos"]: res = "hippo"
        elif res in ["aligator", "alligators", "gator", "allegator"]: res = "alligator"
        elif res in ["cheeta", "african cheetah", "cheetahs"]: res = "cheetah"
        elif res in ["anteaters", "ant eater"]: res = "anteater"
        elif res in ["girrafe", "jiraffe", "griraffe", "giraffee"]: res = "giraffe"
        elif res in ["elephants", "elephan", "elepehant", "asian elephants", "elepahnt"]: res = "elephant"
        elif res in ["coati"]: res = "coyote"
        elif res in ["maccaw"]: res = "macaw"
        elif res in ["toucans", "tucan"]: res = "toucan"
        elif res in ["manitee"]: res = "manatee"
        elif res in ["camal", "camals", "camels"]: res = "camel"
        elif res in ["panda bear", "pandas", "panada bear"]: res = "panda"
        elif res in ["crocks", "croc", "crocodiles", 'crocidile']: res = "crocodile"
        elif res in ["gorrila", "gorillas"]: res = "gorilla"
        elif res in ["whales"]: res = "whale"
        elif res in ["bats"]: res = "bat"
        elif res in ["rhinos", "rhinoceros", "rino"]: res = "rhino"
        elif res in ["penguins", "peguin"]: res = "penguin"
        elif res in ["owls"]: res = "owl"
        elif res in ["turtles"]: res = "turtle"
        elif res in ["turtoise"]: res = "tortoise"
        elif res in ["sting rayy"]: res = "stingray"
        elif res in ["butterflies"]: res = "butterfly"
        elif res in ["sharks"]: res = "shark"
        elif res in ["bob cat"]: res = "bobcat"
        elif res in ["sea lions"]: res = "sea lion"
        elif res in ["birds"]: res = "bird"
        elif res in ["ostritch"]: res = "ostrich"
        elif res in ["flamingoes", "flamingos"]: res = "flamingo"
        elif res in ["zebras", "zeebra"]: res = "zebra"
        elif res in ["wolves"]: res = "wolf"
        elif res in ["beare", "bears"]: res = "bear"
        elif res in ["antelopes"]: res = "antelope"
        elif res in ["hyenas"]: res = "hyena"
        elif res in ["polar bears"]: res = "polar bear"
        elif res in ["seals"]: res = "seal"
        elif res in ["lemurs", "lemer"]: res = "lemur"
        elif res in ["opkapi"]: res = "okapi"
        elif res in ["lions"]: res = "lion"
        elif res in ["tigers"]: res = "tiger"
        elif res in ["baby tiger"]: res = "tiger cub"
        elif res in ["baby lion"]: res = "lion cub"
        elif res in ["baby bear"]: res = "bear cub"
        elif res in ["baby giffrae"]: res = "baby giraffe"
        elif res in ["cappabara"]: res = "capybara"
        elif res in ["kuala bear", "koala bear", "kola"]: res = "koala"
        elif res in ["rams"]: res = "ram"
        elif res in ["kangeroo"]: res = "kangaroo"
        elif res in ["cats"]: res = "cat"
        elif res in ["paraket"]: res = "parakeet"
        elif res in ["insects"]: res = "insect"
        elif res in ["chinchila"]: res = "chinchilla"
        elif res in ["lizards"]: res = "lizard"
    elif cat == "vegetables that you would use to paint your house":
        if res in ["cucumber", "cucubmer", "cuecumber"]: res = "cucumbers"
        elif res in ["potato", "patato", "potatos", "pototoe", "pototo", "yukon gold potatoes"]: res = "potatoes"
        elif res in ["yellow squash", "spaghetti squash", "squach", "sqaush", "summer squash", "banana squash"]: res = "squash"
        elif res in ["greenbean", "green bean", "greenbeans", "french green beans"]: res = "green beans"
        elif res in ["tomoato", "tomato", "tomatos", "tomatoe", "tomotto"]: res = "tomatoes"
        elif res in ["bean"]: res = "beans"
        elif res in ["pear"]: res = "pears"
        elif res in ["orange"]: res = "oranges"
        elif res in ["jalapeno", "jalepeno", "jalepeno", "jalopenos", "jalopeno"]: res = "jalapenos"
        elif res in ["grape", "purple grape", "green grape"]: res = "grapes"
        elif res in ["bok choi"]: res = "bok choy"
        elif res in ["chili", "chilis", "red chili", "green chili" "chili pepper", "chilli", "chilli pepper", "chilli peppers"]: res = "chili peppers"
        elif res in ["brocli", "brocolli", "brocoli", "broccili", "broccli", "broccolli"]: res = "broccoli"
        elif res in ["red peppers", "red pepper", "green pepper", "green bell pepper", "yellow bell pepper", "red bell pepper", "orange bell pepper", "pepper", "bell pepper", "bell peppers", "yellow pepper", "orange pepper", "orange peppers", "green pepper", "green peppers"]: res = "peppers"
        elif res in ["bursslsprouts", "brussel sprouts", "brussel sprout" "brussels", "brusslesprout", "brusselsprouts", "brussle sprouts", "burssels"]: res = "brussels sprouts"
        elif res in ["romaine lettuce", "luttice", "iceberg lettuce", "romain"]: res = "lettuce"
        elif res in ["eggpnat", "egg plants"]: res = "eggplant"
        elif res in ["turnip"]: res = "turnips"
        elif res in ["artichoke"]: res = "artichokes"
        elif res in ["spinch"]: res = "spinach"
        elif res in ["peach"]: res = "peaches"
        elif res in ["bananna", "bannana", "banana"]: res = "bananas"
        elif res in ["carrot", "carret", "carrto"]: res = "carrots"
        elif res in ["collards"]: res = "collard greens"
        elif res in ["carrot", "carrott"]: res = "carrots"
        elif res in ["sweet potato", "sweet potatos"]: res = "sweet potatoes"
        elif res in ["zuccini", "zucini", "zuchini", "zuchinni"]: res = "zucchini"
        elif res in ["calliflower", "colliflower", "califlower", "cauiliflower", "cauliflouer"]: res = "cauliflower"
        elif res in ["beet"]: res = "beets"
        elif res in ["radishes", "raddish"]: res = "radish"
        elif res in ["lentil"]: res = "lentils"
        elif res in ["aspagarus", "asparagrus", "apsaragaus", "asapargus", "aparagas"]: res = "asparagus"
        elif res in ["yam"]: res = "yams"
        elif res in ["mushroom"]: res = "mushrooms"
        elif res in ["yam"]: res = "yams"
        elif res in ["black bean"]: res = "black beans"
        elif res in ["kales"]: res = "kale"
        elif res in ["strawberry"]: res = "strawberries"
        elif res in ["wild cabbage", "cabbages", "red cabbage", "cabage"]: res = "cabbage"
        elif res in ["bean sprout"]: res = "sprouts"
        elif res in ["leak", "leek"]: res = "leeks"
        elif res in ["olive"]: res = "olives"
        elif res in ["sugar snap pea", "sugar snap peas" 'chinese pea']: res = "pea pods"
        elif res in ["kidney bean"]: res = "kidney beans"
        elif res in ["scallion"]: res = "scallions"
        elif res in ["rutebaga"]: res = "rutabaga"
        elif res in ["parsnip", "parnsip"]: res = "parsnips"
        elif res in ["pea", "green peas"]: res = "peas"
        elif res in ["onion", "white onions"]: res = "onions"
        elif res in ["pumpkin"]: res = "pumpkins"          
    return res

#preprocesses data
#returns clean data
def get_clean_data(data):
    clean_data = []
    for trial in data:
        clean_trial = {}
        clean_trial["subject_id"] = trial["row_id"][:-2]
        #skip participants who responded with non-category members
        if clean_trial["subject_id"]=="62e1ede63f23cc2eb6170242":
            continue
        clean_trial["category"] = trial["cat"]
        clean_responses = []
        #process each response given on this trial
        for res in trial["responses"]:
            if res in ["idk", "na", "none", "n/a", "n'a"]:
                continue
            clean_res = get_clean_response(clean_trial["category"], res)
            #remove repeat responses
            if clean_res not in clean_responses:
                clean_responses.append(clean_res)
        clean_trial["responses"] = clean_responses
        clean_data.append(clean_trial)
    return clean_data


#returns frequency of each response, by category
def get_response_counts(data):
    response_counts = {}
    for trial in data:
        cat = trial["category"]
        response_counts[cat] = response_counts.get(cat, {})
        for res in trial["responses"]:
            response_counts[cat][res] = response_counts[cat].get(res, 0) + 1
    return response_counts


if __name__ == "__main__":
    clean_data_loc = '../../clean_data/study4/'
    data = get_raw_data()
    clean_data = get_clean_data(data)
    with open(clean_data_loc + 'generation_responses.json', 'w') as f:
        json.dump(clean_data, f)
    response_counts = get_response_counts(clean_data)
    with open(clean_data_loc + 'generation_response_counts.json', 'w') as f:
        json.dump(response_counts, f)