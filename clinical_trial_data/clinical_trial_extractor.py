import json

def date_convert(str):
    """
    Parse the date strings into a format that MySQL can take in
    """
    parse = str.split(', ')
    parse = parse[0].split(' ') + [parse[1]]
    month = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }
    if len(parse[1]) == 1:
        parse[1] = '0' + parse[1]
    ret = parse[2] + '-' + month[parse[0]] + '-' + parse[1]
    return ret

def extract():
    """
    Extract data from the clinicalTrialsJSON.json file. Each row of
    this file corresponds to a person and one of their studies. The
    extracted data is in the form of a dictionary with fields name
    containing the names of everyone involved with the study, aff
    containing all organization involved, works containing all related
    works, start_date, title, bio containing all keywords, and
    name_org containing one pair of person-affilation in this project.
    """
    result = []
    with open('clinicalTrialsJSON.json') as json_file:
        records = json.load(json_file)["people"]
        for rec in records:
            name = rec["OverallOfficialName"].split(", ")
            aff = rec["OverallOfficialAffiliation"].split(", ")
            # works will be an iterator, each element is a tuple of
            # pmids and work type.
            pmids = rec["ReferencePMID"].split(", ")
            pmids = [int(pmid) for pmid in pmids if pmid != '']
            work_types = rec["ReferenceType"].split(", ")
            works = zip(pmids, work_types)
            start_date = date_convert(rec["StudyFirstPostDate"])
            title = rec["OfficialTitle"] if rec["OfficialTitle"] else rec["BriefTitle"]
            # There are several columns for keywords
            bio1 = rec["ConditionBrowseLeafAsFound"].split(", ") +\
                rec["ConditionMeshTerm"].split(", ")
            bio2 = rec["ConditionBrowseLeafName"].split(", ")
            relevance = rec["ConditionBrowseLeafRelevance"].split(", ")
            bio2 = [bio2[idx] for idx in range(min(len(bio2), len(relevance))) if relevance[idx] == "high"]
            bio = bio1 + bio2
            # This will be from the queried person and their aff
            name_org = (rec['AuthorSearchInput'], rec['ResponsiblePartyInvestigatorAffiliation']) if rec['AuthorSearchInput'] and rec['ResponsiblePartyInvestigatorAffiliation'] else None
            result.append({
                'name': name,
                'aff': aff,
                'works': works,
                'start_date': start_date,
                'title': title,
                'bio': bio,
                'name_org': name_org
            })
    return result

if __name__ == '__main__':
    res = extract()
    for pub in res[2]['works']:
        print(pub)