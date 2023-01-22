import json
import requests
from requests.exceptions import Timeout
# loads name-data list
with open('final_result.json') as json_file:
    data = json.load(json_file)
name_list = data.keys()
questionable = []
dic = {}



##################
# Helper Functions
##################
def name_seperator_middle(name):
    """
    takes a name and returns the first last and middle name
    """
    temp = name.split(",")
    last = temp[0]
    new = temp[1].split(" ")
    first = new[1]
    middle = new[2]
    return first,last, middle

def name_seperator(name):
    """
    takes a name and returns the first and last name
    """
    temp = name.split(",")
    last = temp[0]
    new = temp[1].split(" ")
    first = new[1]
    return first,last

def name_change(name):
    """
    changes name to first last string
    """
    temp = name.split(",")
    x = temp[1].split(" ")[1]
    name = f"{x} {temp[0]}"
    return name

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



url = "https://api.reporter.nih.gov/v2/projects/search"
count = 0
time_out = False
failed = []
print(len(name_list), "people found")
for name in name_list:
    dic[name] = {}
    count += 1
    try:
        if count % 100 == 0:
            print(str(count) + "/" + str(len(name_list)))

        # Separate name
        sep_name = name_change(name)
        if data[name]["Middle name"] != "None":
            mid = True
        else:
            mid = False    
        try:
            first, last, middle = name_seperator_middle(name)
        except:
            first,last = name_seperator(name)
        if mid:
            middle = data[name]["Middle name"]
        
        # Request
        req = {
            "criteria":
            {
                "fiscal_years":[],
                "pi_names": [{"any_name": sep_name}]
            },
            "include_fields": ["Organization",
                    "PrincipalInvestigators"],
            "offset":0,
            "limit": 10
        }
        json_content = get_json_from_url(url,req)

        # Get results
        result = json_content["results"]
        org = data[name]["Affiliation(s)"].lower()
        done = False
        marked = []
        flag = False

        # Find all possible IDs
        for item in result:
            for invest in item["principal_investigators"]:
                temp_first = invest["first_name"]
                temp_last = invest["last_name"]
                prof = invest["profile_id"]
                if prof == None:
                    continue
                if temp_first.lower() in name.lower() and temp_last.lower() in name.lower():
                    org_name = item["organization"]["org_name"]
                    if org_name != None:
                        if org == org_name.lower():
                            if "first" in dic[name].keys():
                                if dic[name]["first"] != prof:
                                    marked.append(dic[name]["first"])
                                    dic[name]["first"] = prof 
                            else:
                                dic[name]["first"] = prof
                            done = True
                            break
                    if mid:
                        temp_mid = invest["middle_name"]
                        if temp_mid:
                            if temp_mid[0].lower() == middle[0].lower():
                                if "first" in dic[name].keys():
                                    if dic[name]["first"] != prof:
                                        marked.append(prof)
                                else:
                                    dic[name]["first"] = prof
                                break
                        else:
                            if prof not in marked:
                                marked.append(prof)
                    else:
                        if not marked:
                            marked.append(prof)
                        else:
                            if prof not in marked:
                                marked.append(prof)
                                if name not in questionable:
                                    questionable.append(name)
                            break
            if done:
                if marked:
                    dic[name]["marked"] = list(set(marked))
                break
            else:
                if len(set(marked)) == 1 and "first" not in dic[name].keys() :
                    dic[name]["first"] = marked[0]
                else:
                    if marked:
                        dic[name]["marked"] = list(set(marked))
                        if name not in questionable:
                            questionable.append(name)
    except:
        print("failed")
        failed.append(name)
        print(count)
        print(name)

# Put data into JSON
if time_out:
    print("run again")
else:
    with open('true_final_ids.json', 'w') as fp:
        json.dump(dic, fp)
    with open('true_final_questionable.txt', 'w') as f:
        for line in questionable:
            f.write(f"{line}\n")
    with open('true_id_failed.txt', 'w') as f:
        for line in failed:
            try:
                f.write(f"{line}\n")
            except:
                print("Failed to write")
                print(line)
