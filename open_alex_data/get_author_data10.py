import openalexapi
import requests
import json
import math
import csv
import pandas as pd

class open_alex_AND():
    def __init__(self, author_name):
        self.author_name = author_name
        self.base_url = 'https://api.openalex.org/'
        self.get_authorIDs()
        self.get_work_id()
        self.get_work_details()
        self.clean_data()
        self.get_details()

    #Getting all author ids through search of first and last name:
    def get_authorIDs(self):
        self.listofIDs = []
        page = 1
        visualize_data = {}  # Initialize with an empty dictionary
            
        while True:
            full_query = f'https://api.openalex.org/authors?search={self.author_name}&page={page}'
            response = requests.get(full_query)
            visualize_data = response.json()
                
            for result in visualize_data['results']:
                openalex_id = result['id'].replace("https://openalex.org/", "")
                self.listofIDs.append(openalex_id)
                
            page += 1
            if page > math.ceil(visualize_data['meta']['count'] / 25):
                break

        print(f'There are {len(self.listofIDs)} author ids for {self.author_name}')

    def get_work_id(self):
        self.works_dict = {}
        for aID in self.listofIDs:
            page = 'page={}'
            filtered_works_url = f'https://api.openalex.org/works?filter=author.id:{aID}&{page}'
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
                self.works_dict[aID] = all_worksID
            print(f'{aID} has {len(self.works_dict[aID])} works')

    def get_work_details(self):
        self.institutions_dict = {}
        self.references_dict = {}
        self.no_references = []
        self.coauthors_dict = {}
        self.concepts_dict = {}
        self.years_dict = {}
        for aID in self.listofIDs:
            self.institutions_dict[aID] = []
            self.references_dict[aID] = []
            self.coauthors_dict[aID] = []
            self.concepts_dict[aID] = []
            self.years_dict[aID] = []
            for wID in self.works_dict[aID]:
                fullquery = self.base_url+'works/'+wID
                response = requests.get(fullquery)
                response.raise_for_status()  # raises exception when not a 2xx response
                if response.status_code != 204:
                    visualize_data = response.json()

                    if len(visualize_data['referenced_works']) == 0 and len(visualize_data['authorships']) < 2:
                        pass
                    
                    else:
                        refs_list = visualize_data['referenced_works']
                        for ref in refs_list:
                            ref = ref.replace("https://openalex.org/", "")
                            self.references_dict[aID] += [ref]
                            if len(self.references_dict[aID]) == 0:
                                self.no_references += [aID]
                        
                        concepts_list = visualize_data['concepts']
                        for concept in concepts_list:
                            finalConcept = concept['display_name']
                            if finalConcept not in self.concepts_dict[aID]:
                                self.concepts_dict[aID] += [finalConcept]
                        
                        coauthors_list = visualize_data['authorships']
                        for coauthor in coauthors_list:
                            firstDict = coauthor['author']
                            if firstDict['id'].replace("https://openalex.org/", "") == aID:
                                secondDict = coauthor['institutions']
                                if len(secondDict) != 0:
                                    for i in range(len(secondDict)):
                                        institution = secondDict[i]["id"]
                                        if institution != None:
                                            institution = secondDict[i]["id"].replace("https://openalex.org/", "")
                                            self.institutions_dict[aID] += [institution]
                            else:
                                if firstDict['display_name'] != None:
                                    name = firstDict['display_name'].lower()
                                    parts = name.split()
                                    if len(parts) == 3:
                                        # if the name has a middle name, remove it
                                        parts.pop(1)
                                    finalName = " ".join(parts)
                                    if finalName not in self.coauthors_dict[aID]:
                                        self.coauthors_dict[aID] += [finalName]

                        year = int(visualize_data['created_date'].split("-")[0])
                        if len(self.years_dict[aID]) == 0:
                            self.years_dict[aID] = [year, year]
                        else:
                            if year < self.years_dict[aID][0]:
                                self.years_dict[aID][0] = year
                            elif year > self.years_dict[aID][1]:
                                self.years_dict[aID][1] = year

    def clean_data(self):
        self.no_info = []
        for aID in self.listofIDs:
            no_institutions = len(self.institutions_dict[aID]) == 0
            no_concepts = len(self.concepts_dict[aID]) == 0
            no_coauthors = len(self.coauthors_dict[aID]) == 0
            no_references = len(self.references_dict[aID]) == 0
            if no_institutions and no_concepts and no_coauthors and no_references:
                self.listofIDs.remove(aID)
                for dict in [self.institutions_dict, self.concepts_dict, self.coauthors_dict, self.references_dict, self.years_dict]:
                    dict.pop(aID)
                self.no_info.append(aID)
        print(f'There are {len(self.no_info)} IDs without enough information. There are {len(self.listofIDs)} remaining.')

    def get_details(self):
        self.details = {}
        for aID in self.listofIDs:
            self.details[aID] = {}
            self.details[aID]["Institution"] = self.institutions_dict[aID]
            self.details[aID]["Concepts"] = self.concepts_dict[aID]
            self.details[aID]["Coauthors"] = self.coauthors_dict[aID]
            self.details[aID]["References"] = self.references_dict[aID]
            self.details[aID]["Years"] = self.years_dict[aID]
