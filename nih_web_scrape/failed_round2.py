from selenium import webdriver
import requests
import json
from requests.exceptions import Timeout

# Get URLs
with open("final_patent_urls.json") as json_file:
    data = json.load(json_file)
file1 = open('patent_failed_data.txt', 'r')

# Get names
names = []
for line in file1:
     names.append(line.strip())

store = {}
count = 0
failed = []
# Get patent data for each name
for name in names:
    count +=1
    print(count)
    if count % 50 == 0:
        with open('second_patent_data.json', 'w') as fp:
            json.dump(store, fp)
    store[name] = {}
    dic = data[name]
    key = dic.keys()
    if "first" in key:
        try:
            first_url = dic["first"]
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            path = "/usr/local/bin/chromedriver"
            wd = webdriver.Chrome(path, options=option)
            wd.get(first_url)
            result = wd.execute_script("return window.localStorage;")
            result = json.loads(result["patentResults"])
            final = []
            for item in result["results"]:
                temp = (item["patent_id"], item["patent_title"], item["related_projects"], item["core_project_num"])
                final.append(temp)
            store[name]["first"] = final
            if "marked" in key:
                store[name]["marked"] = {}
                ids = dic["marked"].keys()
                for id in ids:
                    url = dic["marked"][id]
                    if url != first_url:
                        wd.get(url)
                        result = wd.execute_script("return window.localStorage;")
                        result = json.loads(result["patentResults"])
                        final = []
                        for item in result["results"]:
                            temp = (item["patent_id"], item["patent_title"], item["related_projects"], item["core_project_num"])
                            final.append(temp)
                        store[name]["marked"][id] = final
        except:
            failed.append(name)
            print("failed")



# Store in JSON
with open('second_patent_data.json', 'w') as fp:
    json.dump(store, fp)
with open('second_patent_failed_data.txt', 'w') as f:
    for line in failed:
        f.write(f"{line}\n")