'''
given: a name
- pull author ids
- pull works for each author id 
    - store as list in author id dict?
- pull references for each work
    - store in dict
- for any two authors, if list of references meets similarity threshold, add authors to a list
    - if two authors are grouped together are, there references compiled to one list for future comparisons?
    - does this mean the order influences the outcome?
'''

import openalexapi
import requests
import json
import math



test_name_list = [
    "william pao",
    "frederick suchy",
    "malcolm cox",
    "nancy cooke",
    "allan sniderman",
    "vincent dennis",
    "alessandra pernis",
    "john minna",
    "dennis bier",
    "roger pomerantz"
] #names from asci/aap data

class open_alex_AND():
    def __init__(self, author_name):
        self.author_name = author_name
        self.base_url = 'https://api.openalex.org/'
        self.get_referenced_works()
        self.disambiguate_references()


#Getting all author ids through search of first and last name:
    def get_authorIDs(self, name):
        self.listofIDs = []
        page = 1
        full_query= f'https://api.openalex.org/authors?search={name}&page={page}'
        response = requests.get(full_query)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            visualize_data = response.json()
            num_pages = math.ceil(visualize_data['meta']['count']/25)
        
            while page <= num_pages:
                full_query= f'https://api.openalex.org/authors?search={name}&page={page}'
                response = requests.get(full_query)
                response.raise_for_status()  # raises exception when not a 2xx response
                if response.status_code != 204:
                    visualize_data = response.json()
                    for result in visualize_data['results']:
                        openalex_id = result['id'].replace("https://openalex.org/", "")
                        self.listofIDs.append(openalex_id)
                    page += 1 

            print(f'There are {len(self.listofIDs)} author ids for {name}')
            return self.listofIDs

    def get_work_id(self, givenAuthorID):
            page = 'page={}'
            filtered_works_url = f'https://api.openalex.org/works?filter=author.id:{givenAuthorID}&{page}'
            page = 1
            has_more_pages = True
            fewer_than_10000_results = True
            all_worksID = []

            # loop through pages
            while has_more_pages and fewer_than_10000_results:

                # set page value and request page from OpenAlex
                url = filtered_works_url.format(page)
                response = requests.get(url)
                response.raise_for_status()  # raises exception when not a 2xx response
                if response.status_code != 204:
                    page_with_results = response.json()

                    # loop through partial list of results
                    results = page_with_results['results']
                    for i,work in enumerate(results):
                        openalex_id = work['id'].replace("https://openalex.org/", "")
                        all_worksID.append(openalex_id)
                    # next page
                    page += 1

                    # end loop when either there are no more results on the requested page 
                    # or the next request would exceed 15 results
                    per_page = page_with_results['meta']['per_page']
                    has_more_pages = len(results) == per_page
                    fewer_than_10000_results = per_page * page <= 10000
                print(f'There are {len(all_worksID)} works for {givenAuthorID}')
                return (all_worksID)

    def get_refs(self, workId):
        fullquery = self.base_url+'works/'+workId
        response = requests.get(fullquery)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            visualize_data = response.json()
            extra_data = ['doi', 
                    'title', 
                    'display_name', 
                    'publication_year', 
                    'publication_date', 
                    'ids', 
                    'language', 
                    'primary_location', 
                    'type', 
                    'open_access', 
                    'authorships', 
                    'corresponding_author_ids', 
                    'corresponding_institution_ids', 
                    'apc_list', 
                    'apc_paid', 
                    'cited_by_count', 
                    'biblio', 
                    'is_retracted', 
                    'is_paratext', 
                    'concepts', 
                    'mesh', 
                    'locations_count', 
                    'locations', 
                    'best_oa_location', 
                    'grants', 
                    'related_works', 
                    'cited_by_api_url', 
                    'counts_by_year', 
                    'updated_date', 
                    'created_date']
            for key in extra_data:
                visualize_data.pop(key)
            return visualize_data

    def get_referenced_works(self):
        author_ids = self.get_authorIDs(self.author_name)
        works_dict = {}
        self.references_dict = {}
        self.no_references = []
        for id in author_ids:
            works_dict[id] = self.get_work_id(id)
            self.references_dict[id] = []
            for work_id in works_dict[id]:
                refs_list = self.get_refs(work_id)['referenced_works']
                self.references_dict[id] = self.references_dict[id] + refs_list
            if len(self.references_dict[id]) == 0:
                self.no_references.append(id)
    
    def disambiguate_references(self):
        threshold = 0
        self.disamb_dict = {self.listofIDs[0]: {
            "Alternate IDs": [], 
            "References": self.references_dict[self.listofIDs[0]]
            }}
        for ID1 in self.listofIDs:
            print(ID1)
            valid_ID = ID1 not in self.no_references
            for ID2 in self.disamb_dict.keys():
                print(f'testing: {ID2}')
                valid_ID = ID1 != ID2 and valid_ID
                if valid_ID:
                    count = 0
                    for j in self.references_dict[ID1]:
                        for k in self.disamb_dict[ID2]["References"]:
                            if j == k:
                                count += 1
                    if count > threshold*len(self.references_dict[ID1]) and count > threshold*len(self.disamb_dict[ID2]["References"]):
                        self.disamb_dict[ID2]["Alternate IDs"].append(ID1)
                        self.disamb_dict[ID2]["References"] += self.references_dict[ID1]
                        valid_ID = False
                        print(f'{ID2} merged with {ID1}')
            if valid_ID:
                self.disamb_dict[ID1] = {
                    "Alternate IDs": [],
                    "References": self.references_dict[ID1]
                    }

w_pao = open_alex_AND("william pao")
for key in w_pao.disamb_dict.keys():
    print(f'{key} is also {w_pao.disamb_dict[key]["Alternate IDs"]}')

