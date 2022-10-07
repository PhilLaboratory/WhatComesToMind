#!/usr/bin/env python3
import json
import numpy as np


#returns raw data
def get_raw_data():
    with open('../raw_data/study6/trials.json') as f:
        data = json.load(f)
    return data

#returns clean data
def get_clean_data(data):
    clean_data = {}
    #iterate thru each category
    for cat, trials in data.items():
        clean_data[cat] = []
        #iterate thru all trials for this category
        for trial in trials:
            if trial["descriptor"] == "null":
                continue
            clean_trial = {}
            clean_trial["subject_id"] = trial["subject_id"]
            clean_trial["feature"] = trial["descriptor"] 
            #remove repeat responses
            temp_responses = str.split(trial["responses"], ",")
            clean_trial["responses"] = []
            temp_rts = str.split(trial["rt"], ",")
            clean_trial["rts"] = []
            #take care of no response case
            if len(temp_responses)==1 and temp_responses[0]=='':
                clean_trial["responses"] = ['']
                clean_trial["rts"] = ['']
            #otherwise list all non-repeat responses and rts
            else:
                for i, res in enumerate(temp_responses):
                    res = get_clean_response(cat, res)
                    if res not in clean_trial["responses"] and res != '':
                        clean_trial["responses"].append(res)
                        clean_trial["rts"].append(float(temp_rts[i]))
            clean_data[cat].append(clean_trial)
    return clean_data

#clean response by
#   making lower case,
#   taking care of typos,
#   reconciling similar responses into a single response
#returns clean response
def get_clean_response(cat, res):
    res = res.lower().strip()
    if cat == "zoo animals":
        if res in ["chimpanzee"]: res = "chimp"
        elif res in ["orangutang", "orangutange", "orangatan", "orangutans"]: res = "orangutan"
        elif res in ["snakes"]: res = "snake"
        elif res in ["raccoons"]: res = "raccoon"
        elif res in ["sea otter", "sea otters", "otters"]: res = "otter"
        elif res in ["hippopotamus", "hippopatamus", "hippos"]: res = "hippo"
        elif res in ["aligator", "alligators"]: res = "alligator"
        elif res in ["cheeta", "african cheetah", "cheetahs"]: res = "cheetah"
        elif res in ["anteaters"]: res = "anteater"
        elif res in ["girrafe", "jiraffe", "griraffe", "giraffee"]: res = "giraffe"
        elif res in ["elephants", "elephan", "elepehant", "asian elephants", "elepahnt"]: res = "elephant"
        elif res in ["coati"]: res = "coyote"
        elif res in ["manitee"]: res = "manatee"
        elif res in ["camal", "camals", "camels"]: res = "camel"
        elif res in ["panda bear", "pandas"]: res = "panda"
        elif res in ["crocks", "croc", "crocodiles"]: res = "crocodile"
        elif res in ["gorrila", "gorillas"]: res = "gorilla"
        elif res in ["whales"]: res = "whale"
        elif res in ["bats"]: res = "bat"
        elif res in ["bald eagle"]: res = "eagle"
        elif res in ["rhinos", "rhinoceros", "rino"]: res = "rhino"
        elif res in ["penguins"]: res = "penguin"
        elif res in ["owls"]: res = "owl"
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
        elif res in ["lemurs"]: res = "lemur"
        elif res in ["opkapi"]: res = "okapi"
        elif res in ["lions"]: res = "lion"
        elif res in ["tigers"]: res = "tiger"
        elif res in ["cappabara"]: res = "capybara"
        elif res in ["rams"]: res = "ram"
    if cat == "holidays":
        if res in ["4th of july", "4th july", "4ths of july", "forth of july", "july 4", "july 4th", "independence day", "independence day.", "emancipation day", "independance day"]: res = "fourth of july"
        elif res in ["st pattys day", "St, Paticks Day", "st patricks", "st pattys", "st patrciks",  "st patricks day", "st patrick day"]: res = "st. patrick's day"
        elif res in ["new years eve", "new year", "NYE"]: res = "new years eve"
        elif res in ["mlk", "mlk day", "martin luther king day", "martin luther kings birthday", "martin luther king, jr. day", "martin luther king", "martin luther king jr day", "martin luther king jr. birthday", "birthday of martin luther", "martin luther king, jr"]: res = "martin luther king jr. day"
        elif res in ["columbus", "columbus day", "columbus day." "columbus day "]: res = "christopher columbus day"
        elif res in ["chirstmas", "christmas day", "christmasq"]: res = "christmas"
        elif res in ["memorial", "memorial day."]: res = "memorial day"
        elif res in ["ressurrection dayeaster"]: res = "easter"
        elif res in ["kwansa", "kwanzaa", "kwanaaaza"]: res = "kwanza"
        elif res in ["veterens day", "veterons day", "veteran day", "veterensday"]: res = "veterans day"
        elif res in ["st. valentines day", "valetines day", "valentine", "valentines", "valentine day", "velentines day"]: res = "valentines day"
        elif res in ["washingtons birthday"]: res = "presidents day"
        elif res in ["thanksgiving day", "thanks giving"]: res = "thanksgiving"
        elif res in ["honaka", "chanukah", "hanukah", "hanakah", "hanuakah", "hannukkah", "hauneca", "chananaukah", "hannukah", "channukah"]: res = "hanukkah"
        elif res in ["chinese new years", "lunar new year"]: res = "chinese new year"
        elif res in ["my birthday", "birthday"]: res = "bithdays"
        elif res in ["holloween", "haloween", "all hallows eve"]: res = "halloween"
        elif res in ["columbus day", "colombus day"]: res = "christopher columbus day"
        elif res in ["labor day.", "labor dy"]: res = "labor day"
        elif res in ["diwahli"]: res = "diwali"
    elif cat == "jobs":
        if res in ["mailman", "mail person", "mail delivery person", "mailperson", "mail carrier", "postal worker", "postal service", "mail delivery worker", "delivery driver", "postman", "delievery driver"]: res = "mail carrier"
        elif res in ["garbage person", "garbage pickup", "trash collector", "trashman", "garbageperson","garbage truck driver", "garbageman", "garbage man"]: res = "garbage collector"
        elif res in ["fireman","fireperson", "fire fighter"]: res = "firefighter"
        elif res in ["waitress", "server", "waiter", "waitstaff"]: res = "waitstaff"
        elif res in ["footballer"]: res = "football player"
        elif res in ["office"]: res = "office worker"
        elif res in ["marketing"]: res = "marketer"
        elif res in ["cook"]: res = "chef"
        elif res in ["police man", "cop", "police", "policeman", "officer", "sheriff"]: res = "police officer"
        elif res in ["dishwasher"]: res = "busboy"
        elif res in ["bank teller", "banking"]: res = "banker"
        elif res in ["actress"]: res = "actor"
        elif res in ["it"]: res = "information technology"
        elif res in ["retail clerk", "office clerk"]: res = "clerk"
        elif res in ["construction", "builder", "constuction"]: res = "construction worker"
        elif res in ["cleaner", "custodian"]: res = "janitor"
        elif res in ["supreme court judge", 'circuit judge']: res = "judge"
        elif res in ["office assistant", "admin assistant"]: res = "administrative assistant"
        elif res in ["vet", "vetrinarian"]: res = "veterinarian"
        elif res in ["assembly line work", "factory"]: res = "factory worker"
        elif res in ["housekeeper"]: res = "maid"
        elif res in ["linesman"]: res = "lineman"
        elif res in ["repariman", "repair man"]: res = "repairman"
        elif res in ["trucker"]: res = "truck driver"
        elif res in ["call center", "customer service agent", "customer service rep", "customer service" "customer support person"]: res = "customer service representative"
        elif res in ["personal assistant"]: res = "assistant"
        elif res in ["science"]: res = "scientist"
        elif res in ["film director"]: res = "director"
        elif res in ["grocery store clerk"]: res = "cashier"
        elif res in ["ele ctrician", "electrican"]: res = "electrician"
        elif res in ["dentists"]: res = "dentist"
        elif res in ["data analyst"]: res = "analyst"
        elif res in ["agriculture"]: res = "farmer"
        elif res in ["hairdresser", "hair stylist", "esthetician"]: res = "beautician"
        elif res in ["nursh"]: res = "nurse"
        elif res in ["accounting"]: res = "accountant"
        elif res in ["sex worker"]: res = "prostitute"
        elif res in ["auditer"]: res = "auditor"
        elif res in ["mechanics"]: res = "mechanic"
        elif res in ["communicatoins"]: res = "commuications"
        elif res in ["professional athlete"]: res = "athlete"
        elif res in ["taxi"]: res = "taxi driver"
    elif cat == "chain restaurants":
        if res in ["kfc"]: res = "kentucky fried chicken"
        elif res in ["chiles", "chillis"]: res = "chilis"
        elif res in ["tgif", "fridays", "tgifridays", "tgi friday", "t g i fridays"]: res = "tgi fridays"
        elif res in ["outback"]: res = "outback steakhouse"
        elif res in ["burgerking", "burga king"]: res = "burger king"
        elif res in ["chic fil a", "chickfila", "chick-fil-a", "chic-fil-a", "chick fila", "chik-fil-a", "chikafila", "chick filette", "chikfila", "chik fil a"]: res = "chick fil a"
        elif res in ["mcd", "macdonalds", "mcdoanlds", "mcdonals", "mc donalds", "mc ds"]: res = "mcdonalds"
        elif res in ["five guys burgers", "5 guys", "five guys and fries"]: res = "five guys"
        elif res in ["panera bread", "pananera"]: res = "panera"
        elif res in ["olive garen"]: res = "olive garden"
        elif res in ["red loster"]: res = "red lobster"
        elif res in ["windys", "wendy"]: res = "wendys"
        elif res in ["chopotle", "chipolte", "chipoltle"]: res = "chipotle"
        elif res in ["pizzahut", "pozza hut"]: res = "pizza hut"
        elif res in ["lil ceasars"]: res = "little ceasars"
        elif res in ["applebee", "apple bees", "applebys"]: res = "applebees"
        elif res in ["macaronni grill"]: res = "macaroni grill"
        elif res in ["ruby tuesday"]: res = "ruby tuesdays"
        elif res in ["bonefish"]: res = "bonefish grill"
        elif res in ["taco ball", "taobell", "tacobell"]: res = "taco bell"
        elif res in ["cracker barrell", "crackerbarrel"]: res = "cracker barrel"
        elif res in ["jack and box"]: res = "jack in the box"
        elif res in ["p.f. changs", "p.f. changes"]: res = "pf changs"
        elif res in ["domino"]: res = "dominos"
        elif res in ["arby"]: res = "arbys"
        elif res in ["sonic drive in"]: res = "sonic"
    elif cat == "sports":
        if res in ["horse riding", "horse racing"]: res = "horseback riding"
        elif res in ["car racing", "formula 1", "race car driver", "formular one", "nas car", "f1 racing", "race car driving", "stock car racing", "nascar", "auto racing", "formula 1 ", "f1"]: res = "racecar driving"
        elif res in ["racketball", "raquetball"]: res = "racquetball"
        elif res in ["table tennis"]: res = "ping pong"
        elif res in ["skating", "speed skating"]: res = "ice skating"
        elif res in ["mma"]: res = "boxing"
        elif res in ["swim"]: res = "swimming"
        elif res in ["ice hockey", "hickey", "hocky"]: res = "hockey"
        elif res in ["basket ball", "baskeball"]: res = "basketball"
        elif res in ["cycling", "bicycling", "bicylcing", "bmx"]: res = "biking"
        elif res in ["snowboard"]: res = "snowboarding"
        elif res in ["ultimate frisbee"]: res = "frisbee"
        elif res in ["cheer"]: res = "cheerleading"
        elif res in ["la crosse", "lacross", "laccross"]: res = "lacrosse"
        elif res in ["soccor", "scooer", "socker", "soccar"]: res = "soccer"
        elif res in ["tennnis"]: res = "tennis"
        elif res in ["volley ball", "volly ball", "vollyball", "valley ball"]: res = "volleyball"
        elif res in ["bastketball"]: res = "basketball"
        elif res in ["badmington", "badmitton", "batmitton", "badmitten"]: res = "badminton"
        elif res in ["foot ball", "american football"]: res = "football"
        elif res in ["soft ball"]: res = "softball"
        elif res in ["wwe"]: res = "wrestling"
        elif res in ["dancing"]: res = "dance"
    elif cat == "kitchen appliances":
        if res in ["stand mixer", "hand mixer", "standing mixer", "mixer", "kitchenaid mixer", "cake mixer"]: res = "electric mixer"
        elif res in ["instapot", "insta pot", "instant pot"]: res = "pressure cooker"
        elif res in ["fridge", "refrigerator", "refridgerator", "refriderator", "fridgerator"]: res = "refrigerator"
        elif res in ["overn", "convection oven", "over"]: res = "oven"
        elif res in ["coffee pot", "coffeee maker", "coffee machine", "coffeemaker"]: res = "coffee maker"
        elif res in ["garbade disposal", "disposal"]: res = "garbage disposal"
        elif res in ["waffle maker", "waffel iron"]: res = "waffle iron"
        elif res in ["air frier", "airfryer"]: res = "air fryer"
        elif res in ["dish washer", "plate washer", "wishwasher"]: res = "dishwasher"
        elif res in ["food processer", "processor", "processer"]: res = "food processor"
        elif res in ["crock pot", "crockpot", "slower cooker", "slowcooker", "qcrock pot"]: res = "slow cooker"
        elif res in ["pinini maker"]: res = "panini press"
        elif res in ["fryer", "deep fat fryer"]: res = "deep fryer"
        elif res in ["microwave over", "micowave", "microvawe", "microwave oven"]: res = "microwave"
        elif res in ["electric tea kettle", "electric kettle", "electronic kettle", "hot water kettle"]: res = "kettle"
        elif res in ["rice steamer", "rice maker"]: res = "rice cooker"
        elif res in ["electric can opener"]: res = "can opener"
        elif res in ["stovetop"]: res = "stove"
        elif res in ["fruit juicer"]: res = "juicer"
        elif res in ["grinder"]: res = "coffee grinder"
        elif res in ["oven toaster"]: res = "toaster oven"
        elif res in ["faucet"]: res = "sink"
    elif cat == "vegetables":
        if res in ["cucumber", "cuecumber"]: res = "cucumbers"
        elif res in ["potato", "patato", "potatos", "pototo"]: res = "potatoes"
        elif res in ["greenbean", "green bean", "greenbeans", "french green beans"]: res = "green beans"
        elif res in ["tomoato", "tomato", "tomatos", "tomatoe", "tomotto"]: res = "tomatoes"
        elif res in ["bean"]: res = "beans"
        elif res in ["brocli", "brocolli", "brocoli", "broccili", "broccli", "broccolli"]: res = "broccoli"
        elif res in ["bursslsprouts", "brussel sprouts", "brussel sprout" "brussels", "brusslesprout", "brusselsprouts", "brussle sprouts", "burssels"]: res = "brussels sprouts"
        elif res in ["eggpnat"]: res = "eggplant"
        elif res in ["turnip"]: res = "turnips"
        elif res in ["carrot", "carret"]: res = "carrots"
        elif res in ["collards"]: res = "collard greens"
        elif res in ["carrot", "carrott"]: res = "carrots"
        elif res in ["sweet potato"]: res = "sweet potatoes"
        elif res in ["zuccini", "zuchini", "zuchinni"]: res = "zucchini"
        elif res in ["calliflower", "colliflower", "cauiliflower", "cauliflouer"]: res = "cauliflower"
        elif res in ["beet"]: res = "beets"
        elif res in ["radishes", "raddish"]: res = "radish"
        elif res in ["lentil"]: res = "lentils"
        elif res in ["aspagarus", "asparagrus", "aparagas"]: res = "asparagus"
        elif res in ["yam"]: res = "yams"
        elif res in ["mushroom"]: res = "mushrooms"
        elif res in ["yam"]: res = "yams"
        elif res in ["black bean"]: res = "black beans"
        elif res in ["kales"]: res = "kale"
        elif res in ["wild cabbage", "red cabbage"]: res = "cabbage"
        elif res in ["bean sprout"]: res = "sprouts"
        elif res in ["leak", "leek"]: res = "leeks"
        elif res in ["olive"]: res = "olives"
        elif res in ["sugar snap pea", 'chinese pea']: res = "snap peas"
        elif res in ["kidney bean"]: res = "kidney beans"
        elif res in ["scallion"]: res = "scallions"
        elif res in ["rutebaga"]: res = "rutabaga"
        elif res in ["parsnip", "parnsip"]: res = "parsnips"
        elif res in ["pea"]: res = "peas"
        elif res in ["onion"]: res = "onions"        
    return res

#returns ease of response to each feature, normalized within each category
#ease of response for a feature measured as average ease of response across all trials
#in which participants name category members with that feature
#ease of response measured for a single trial as sum of reciprocals of the response time for each response given
def get_ft_relevance(data):
    ease_of_res = {}
    #iterate thru each category
    for cat, trials in data.items():
        ease_of_res[cat] = {}
        #iterate thru all trials for this category and compute trial ease of response
        for trial in trials:
            ft = trial["feature"]
            #ease of response is 0 if no responses given
            if len(trial["rts"])==1 and trial["rts"][0]=="":
                trial_ease_of_res = 0
            #otherwise sum reciprocal response times
            else:
                trial_ease_of_res = sum([(1/rt) for rt in trial["rts"]])
            ease_of_res[cat][ft] = ease_of_res[cat].get(ft, []) + [trial_ease_of_res]
    #compute mean of trial ease of response lists for each feature in each category
    for cat, ft_eors in ease_of_res.items():
        for ft, eors in ft_eors.items():
            ease_of_res[cat][ft] = np.mean(eors)
    #normalize within each category
    relevance = {}
    for cat, ft_eor in ease_of_res.items():
        relevance[cat] = {}
        for ft, eor in ft_eor.items():
            relevance[cat][ft] = eor/max(ease_of_res[cat][x] for x in ease_of_res[cat].keys())
    return relevance


if __name__ == "__main__":
    #location for clean data
    clean_data_loc = '../clean_data/study6/'
    #get raw response data
    data = get_raw_data()
    #clean and store response data
    clean_data = get_clean_data(data)
    with open(clean_data_loc + 'responses.json', 'w') as f:
        json.dump(clean_data, f)
    #get and store average normalized ease of response to each feature
    ft_relevance = get_ft_relevance(clean_data)
    with open(clean_data_loc + 'feature_relevance.json', 'w') as f:
        json.dump(ft_relevance, f)
