import requests
import json
import sqlite3
from requests.exceptions import Timeout

# Get ID Information
with open('true_final_ids.json') as json_file:
    data = json.load(json_file)
names = list(data.keys())



##################
# Helper Funcitons
##################
def get_json_from_url(url,inp):
    content = get_url(url,inp)
    js = json.loads(content)
    return js

def get_url(url, inp):
    try:
        response = requests.post(url, json = inp)
    except Timeout:
        print('Timeout has been raised.')
        response = requests.post(url, json = inp)
    content = response.content.decode('utf8')
    return content

def name_seperator(name):
    temp = name.split(",")
    x = temp[1].split(" ")[1]
    name = f"{x} {temp[0]}"
    return name
    


# Some storing variables and constants
new_list = []
store = {}
failed = []
count = 0
url_storage = {}
url = "https://api.reporter.nih.gov/v2/projects/search"
url2= "https://api.reporter.nih.gov/v2/publications/search"
print("Found", len(names), "names")

# iterates through each name in the name list and makes a request about their publication and project history
# could be changed to due one giant multiple name querie but this i easier for testing right now
for name in names: 
    store[name] = {}
    url_storage[name] = {}
    count += 1
    try:
        if count % 100 == 0:
            print(str(count) + "/" + str(len(names))) 
        id = data[name]
        keys = id.keys()
        if "first" in keys:
            primary = id["first"]
            test2 = { "criteria": { "pi_profile_ids":[primary] },"exclude_fields": ["terms","abstract_text","pref_terms","phr_text"]}
            json_content = get_json_from_url(url,test2)
            result = json_content["results"]
            meta = json_content["meta"]["search_id"]
            lsearch = f"https:/reporter.nih.gov/search/{meta}/patents"
            url_storage[name]["first"] = lsearch
            store[name]["first"] = result
        if "marked" in keys:
            marked = id["marked"]
            url_storage[name]["marked"] = {}
            store[name]["marked"] = {}
            for mark in marked:
                if mark != id["first"]:
                    test2 = { "criteria": { "pi_profile_ids":[mark] },"exclude_fields": ["terms","abstract_text","pref_terms","phr_text"]}
                    json_content = get_json_from_url(url,test2)
                    result = json_content["results"]
                    meta = json_content["meta"]["search_id"]
                    lsearch = f"https:/reporter.nih.gov/search/{meta}/patents"
                    url_storage[name]["marked"][mark] = lsearch
                    store[name]["marked"][mark] = result
    except:
        print(f"request failed name:{name} count = {count}")
        failed.append(name)

# Write results to JSON
with open('final_nih_data.json', 'w') as fp:
    json.dump(store, fp)
with open('final_patent_urls.json', 'w') as fp:
    json.dump(url_storage, fp)
with open('final_failed_data.txt', 'w') as f:
    for line in failed:
        try:
            f.write(f"{line}\n")
        except:
            print("Cannot write line")
            print(line)
