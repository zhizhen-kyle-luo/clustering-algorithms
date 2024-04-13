import csv


def str_list_parser(inp):
    """
    Given a string with format "['text', 'texttwo']" return a list
    ['text', 'texttwo']
    """
    if len(inp) < 3:
        return []
    idx = 1
    res = []
    while True:
        quote = inp[idx]
        new_affil = ''
        idx += 1
        while inp[idx] != quote:
            new_affil += inp[idx]
            idx += 1
        idx += 3
        res.append(new_affil)
        if idx >= len(inp):
            break
    return res


def extract():
    """
    Extract the data from asci_aap_data.csv in the form of a dictionary
    """
    print()
    print("Extracting from asci_aap_data.csv")
    # Extract in the form of a list of records
    with open('asci_aap_data.csv', encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        ret = []
        for row in csv_reader:
            if len(row) < 1:
                continue
            if row[0] == "year":
                print("Found column names")
                continue
            record = {
                "year": int(row[0]) if row[0] else None,
                "first_name": row[1] if row[1] else None,
                "middle_name": row[2] if row[2] else None,
                "last_name": row[3] if row[3] else None,
                "phone": int(row[4]) if row[4] != "FALSE" and row[4] != "" and row[4] != "False" else None,
                "email": row[5] if row[5] else None,
                "affiliation": str_list_parser(row[6]),
                "original specialization": str_list_parser(row[7]),
                "modified specializationmemoriam": str_list_parser(row[8]),
                "unactive": row[9],
                "organization": row[10],
                "email_affiliation": str_list_parser(row[11]),
                "umbrella_aff": str_list_parser(row[12]),
                "related_aff": str_list_parser(row[13]),
                "umbrella_spec": str_list_parser(row[14]),
                "related_spec": str_list_parser(row[15]),
                "Id_num": str_list_parser(row[16]),
                "kumu_num": row[17]
            }
            ret.append(record)
    return ret

if __name__ == "__main__":
    pass
