import numpy as np
import json

"""
Clean data
"""
def get_clean_data(trials):
    new_data = []
    for d in trials:
        #exclude subjects who did not respond with a single zoo animal
        if d["subject_id"] in [33, 72]:
            continue
        d2 = d
        d2["answer"] = parse(d["answer"])
        consid = []
        for c in d["considerations"]:
            c = parse(c)
            if c not in ["na","n a","n/a", "n/an"]:
                consid.append(c)
        d2["considerations"] = list(set(consid + [d2["answer"]]))
        new_data.append(d2)
    return new_data

"""
Parses response to combine highly similar responses
"""
def parse(res): 
    res = res.lower().strip()
    if res in ["chimpanzee", "chimps"]: res = "chimp"
    elif res in ["orangutang", "orangutange", "orangatan", "orangutans"]: res = "orangutan"
    elif res in ["snakes"]: res = "snake"
    elif res in ["raccoons", "racoon"]: res = "raccoon"
    elif res in ["sea otter", "sea otters", "otters"]: res = "otter"
    elif res in ["hippopotamus", "hippopatamus", "hippos"]: res = "hippo"
    elif res in ["aligator", "alligators"]: res = "alligator"
    elif res in ["cheeta", "african cheetah", "cheetahs"]: res = "cheetah"
    elif res in ["anteaters"]: res = "anteater"
    elif res in ["koala bear", "koalas"]: res = "koala"
    elif res in ["gazelles"]: res = "gazelle"
    elif res in ["girrafe", "jiraffe", "griraffe", "geraffee", "girafe", "giraffee", "giraffes"]: res = "giraffe"
    elif res in ["elephants", "elephan", "elepehant", "asian elephants", "elepahnt"]: res = "elephant"
    elif res in ["coati"]: res = "coyote"
    elif res in ["insects/spiders"]: res = "bugs"
    elif res in ["manitee"]: res = "manatee" 
    elif res in ["camal", "camals", "camels"]: res = "camel"
    elif res in ["panda bear", "pandas"]: res = "panda"
    elif res in ["crocks", "croc", "crocodiles"]: res = "crocodile"
    elif res in ["gorrila", "gorillas", "gorrilla"]: res = "gorilla"
    elif res in ["whales"]: res = "whale"
    elif res in ["bats"]: res = "bat"
    elif res in ["lizards"]: res = "lizard"
    elif res in ["bald eagle", "eagles"]: res = "eagle"
    elif res in ["rhinos", "rhinoceros", "rino"]: res = "rhino"
    elif res in ["penguins", "the penguins"]: res = "penguin"
    elif res in ["owls"]: res = "owl"
    elif res in ["turtoise"]: res = "tortoise"
    elif res in ["turtles", "i would take them to see the turtles"]: res = "turtle"
    elif res in ["parrots"]: res = "parrot"
    elif res in ["sting rayy"]: res = "stingray"
    elif res in ["butterflies"]: res = "butterfly"
    elif res in ["monkeys", "monkey.", "monkey's", "monkies", "i would take them to see the monkeys. all kids like monkeys and i think they would keep the kids entertained."]: res = "monkey"
    elif res in ["sharks", "shaek"]: res = "shark"
    elif res in ["bob cat"]: res = "bobcat"
    elif res in ["sea lions"]: res = "sea lion"
    elif res in ["the fish"]: res = "fish"
    elif res in ["birds", "i would take them to see one of the smaller birds", "birds in the aviary", "i'd take them to the bird exhibit"]: res = "bird"
    elif res in ["ostritch"]: res = "ostrich"
    elif res in ["flamingoes", "flamingos"]: res = "flamingo"
    elif res in ["zebras", "zeebra"]: res = "zebra"
    elif res in ["wolves"]: res = "wolf"
    elif res in ["lepoard"]: res = "leopard"
    elif res in ["beare", "bears"]: res = "bear"
    elif res in ["antelopes"]: res = "antelope"
    elif res in ["hyenas"]: res = "hyena"
    elif res in ["polar bears"]: res = "polar bear"
    elif res in ["seals"]: res = "seal"
    elif res in ["reptile house", "reptiles"]: res = "reptile"
    elif res in ["peacocks"]: res = "peacock"
    elif res in ["bison"]: res = "buffalo"
    elif res in ["lemurs"]: res = "lemur"
    elif res in ["opkapi"]: res = "okapi"
    elif res in ["lions"]: res = "lion"
    elif res in ["tigers"]: res = "tiger"
    elif res in ["cappabara"]: res = "capybara"
    elif res in ["rams"]: res = "ram"
    elif res in ["arctic fox", "artic fox"]: res = "fox"
    elif res in ["ducks"]: res = "duck"
    elif res in ["mir cat", "meerkats", "meer cats"]: res = "meerkat"
    elif res in ["red pandas"]: res = "red panda"
    elif res in ["prairie dogs"]: res = "prairie dog"
    if res=="bear": res="grizzly bear"
    return res

"""
Returns count of each response
"""
def get_response_counts(data):
    counts = {}
    for trial in data:
        res = trial["answer"]
        counts[res] = counts.get(res, 0) + 1
    return counts

"""
Returns count of each consideration
"""
def get_consideration_counts(data):
    counts = {}
    for trial in data:
        for c in trial["considerations"]:
            counts[c] = counts.get(c, 0) + 1
    return counts


if __name__ == "__main__":
    clean_data_loc = '../clean_data/study7/'

    with open('../raw_data/study7/trials.json') as f:
        trials = json.load(f)

    clean_data = get_clean_data(trials)

    with open(clean_data_loc + 'responses.json', 'w') as f:
        json.dump(clean_data, f)
    
    consideration_counts = get_consideration_counts(clean_data)
    with open(clean_data_loc + 'consideration_counts.json', 'w') as f:
        json.dump(consideration_counts, f)
    
    response_counts = get_response_counts(clean_data)
    with open(clean_data_loc + 'response_counts.json', 'w') as f:
        json.dump(response_counts, f)