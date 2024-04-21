import requests
import json
from requests.exceptions import Timeout

with open('final_nih_data.json') as json_file:
    data = json.load(json_file)
names = list(data.keys())



##################
# Helper Functions
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
    


new_list = []
store = {}
failed = []
count = 0
url= "https://api.reporter.nih.gov/v2/publications/search"
print(len(names), "names found")
# iterates through each name in the name list and makes a request about their publication and project history
# could be changed to due one giant multiple name querie but this i easier for testing right now
for name in names: 
    try:
        count += 1
        if count % 10 == 0:
            print(str(count) + "/" + str(len(names)))
        if count % 200 == 0:
            with open('final_pub_data.json', 'w') as fp:
                json.dump(store, fp)
            with open('final_pub_failed_data.txt', 'w') as f:
                for line in failed:
                    f.write(f"{line}\n")
        store[name] = {}
        if "first" in data[name].keys():
            store[name]["first"] = {}
            projects = data[name]["first"]
            for project in projects:
                num = project["core_project_num"]
                test1 = {"criteria": {"core_project_nums": [num]} }
                json_content = get_json_from_url(url,test1)
                result = json_content["results"]
                store[name]["first"][num] = result
        if "marked" in data[name].keys():
            store[name]["marked"] = {}
            for mark in data[name]["marked"].keys():
                projects = data[name]["marked"][mark]
                store[name]["marked"][mark] = {}
                for project in projects:
                    num = project["core_project_num"]
                    test1 = {"criteria": {"core_project_nums": [num]} }
                    json_content = get_json_from_url(url,test1)
                    result = json_content["results"]
                    store[name]["marked"][mark][num] = result
    except:
        failed.append(name)
        print("FAILED")              

# Store in JSON
with open('final_pub_data.json', 'w') as fp:
    json.dump(store, fp)
with open('final_pub_failed_data.txt', 'w') as f:
    for line in failed:
        f.write(f"{line}\n")
