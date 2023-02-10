# NIH Web Scraping API Instruction
The following is the recommended order of Python files that you should run to get all the data from NIH RePORTER. All are available in the GitHub repository.

1. id_retriever.py needs final_result.json to create true_final_ids.json, true_final_questionable.txt, and true_id_failed.txt
2. nih_request.py needs true_final_ids.json to create final_nih_data.json, final_patent_urls.json, and final_failed_data.txt
3. web_scrap_init.py needs final_patent_urls.json to create final_patent_urls.json and patent_failed_data.txt
4. failed_round2.py needs final_patent_urls.json and patent_failed_data.txt to create second_patent_data.json and second_patent_failed_data.txt
5. publication_retriever.py needs final_nih_data.json to create final_pub_data.json and final_pub_failed_data.txt

Each Python script can be run without any unexpected errors, but they do have some library and file requirements. Namely, everything depends on final_result.json, and this file is in Anh Nguyen’s folder. Alexander Kumar’s folder might also have this file. As for the library, be sure to have json and requests library installed. These two are quite common, so I will go to the less common library. There is only one less known library used, which is selenium, install it using
```
pip install selenium
```
That is all I have about this API, good luck!!
