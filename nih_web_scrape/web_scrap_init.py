from selenium import webdriver
import requests
import json
from requests.exceptions import Timeout

# get patent URLs
with open("final_patent_urls.json") as json_file:
    data = json.load(json_file)

names = list(data.keys())
store = {}
count = 0
failed = []
print(len(names))
# Get patent info per names
for name in names:
    count +=1
    if count % 100 == 0:
        print(str(count) + "/" + str(len(names)))
    if count % 50 == 0:
        with open('first_patent_data.json', 'w') as fp:
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
with open('first_patent_data.json', 'w') as fp:
    json.dump(store, fp)
with open('patent_failed_data.txt', 'w') as f:
    for line in failed:
        f.write(f"{line}\n")