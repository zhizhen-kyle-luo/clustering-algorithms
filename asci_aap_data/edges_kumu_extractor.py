import csv

def extract():
    """
    Extract the data from edges_kumu.csv in the form of a dictionary
    """
    print()
    print("Extracting from edges_kumu.csv")
    # Extract in the form of a list of records
    with open('edges_kumu.csv', encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        ret = []
        relation_type = set()
        for row in csv_reader:
            if len(row) < 1:
                continue
            if row[0] == "From":
                print("Found column names")
                continue
            record = {
                "entity1": row[0],
                "entity2": row[1],
                "type": row[2],
                "strength": int(row[3])
            }
            relation_type.add(row[2])
            ret.append(record)
    print(relation_type)
    return ret



if __name__ == "__main__":
    data  = extract()
    print(data[-1])