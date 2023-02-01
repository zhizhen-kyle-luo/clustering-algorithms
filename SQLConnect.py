import mysql.connector
from mysql.connector import Error



def connect_and_query(queries, types, database="test"):
    """
    Input:
        - queries (list of str): The queries to be made to the MySQL
          DB
        - types (list of str): The types of queries we are making
    Output:
        When type == "SELECT", we return the selected rows, otherwise
        we do not return anything.
    Detail:
    queries and types must have the same lengths
    """
    ret = []
    try:
        # Establish connection
        connection = mysql.connector.connect(host='sql.mit.edu',
                                            database='mit-ps+' + database,
                                            user='mit-ps',
                                            passwd='cut18vuk',
                                            charset='utf8')
        if connection.is_connected():
            print("Connection to database established")
            # Do query
            cursor = connection.cursor()
            for idx in range(len(queries)):
                try:
                    cursor.execute(queries[idx])
                except Error as e:
                    print("Error while querying")
                    print(queries[idx])
                    with open('failed_uploads.txt', 'w') as f:
                        f.write(queries[idx])
                    print(e)
                if types[idx] == "SELECT":
                    try:
                        ret.append(cursor.fetchall())
                    except Error as e:
                        print("Error while querying")
                        print(queries[idx])
                        with open('failed_uploads.txt', 'w') as f:
                            f.write(queries[idx])
                        print(e)
                else:
                    try:
                        connection.commit()
                    except Error as e:
                        print("Error while querying")
                        print(queries[idx])
                        with open('failed_uploads.txt', 'w') as f:
                            f.write(queries[idx])
                        print(e)
                
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # Close connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return ret


def insert_query_dict(table_name, fields):
    columns = "("
    entries = "("
    for key, val in fields.items():
        columns += key + ', '
        if isinstance(val, str):
            if '"' in val:
                entries += "'" + val + "', "
            else:
                entries += '"' + val + '", '
        elif val is not None:
            entries += str(val) + ", "
        else:
            entries += "NULL, "
    entries = entries[:-2] + ')'
    columns = columns[:-2] + ')'
    return "INSERT INTO " + table_name + " " + columns + " VALUES " + entries + ";"


def insert_query(table_name, column_names, entry_types, entry):
    """
    Inputs:
        - table_name (str): Name of the table
        - column_names (tuple of strings): Name of the columns in the
          table
        - entry_types (tuple of strings): The way we express the
          entries in the query string
        - entry (tuple): The new entry to the table.
    Outputs:
        return insert query
    Details:
        This function inserts into the table specified by table_name
        a new entry specified by entry. This function expects that
        all of column_names, entry_names, and entry to have the same
        length.
    """
    # Clean entry to make insert query
    modded_entry = "("
    for idx in range(len(entry)):
        if idx != 0:
            modded_entry += ", "
        if entry[idx] is None:
            modded_entry += "NULL"
        elif entry_types[idx] == "num":
            modded_entry += str(entry[idx])
        elif entry_types[idx] == "str":
            modded_entry += ('"' + str(entry[idx]) + '"')
    modded_entry += ")"

    # Clean column_names to make insert query
    modded_column_names = "("
    for idx in range(len(column_names)):
        if idx != 0:
            modded_column_names += ", "
        modded_column_names += str(column_names[idx])
    modded_column_names += ")"

    # Create insert query
    query = "INSERT INTO " + table_name + " " + modded_column_names +\
        " VALUES " + modded_entry + ";"
    
    return query



class UnmergedV1:
    def bioentity(entry):
        column_names = ("origin_database", "name")
        entry_types = ("str", "str")
        return insert_query("Bioentity", column_names, entry_types, entry)
        
    def bio_relation(entry):
        column_names = ("bio_id1", "bio_id2", "relation")
        entry_types = ("num", "num", "str")
        return insert_query("BioRelation", column_names, entry_types, entry)

    def keyword(entry):
        column_names = ("work_id", "bio_id")
        entry_types = ("num", "num")
        return insert_query("Keyword", column_names, entry_types, entry)

    def org(entry):
        column_names = ("origin_database", "name", "funding")
        entry_types = ("str", "str", "num")
        return insert_query("Org", column_names, entry_types, entry)

    def org_alias_id(entry):
        column_names = ("org_id", "alias_id")
        entry_types = ("num", "num")
        return insert_query("OrgAliasID", column_names, entry_types, entry)

    def org_relation(entry):
        column_names = ("org_id1", "org_id2", "relation")
        entry_types = ("num", "num", "str")
        return insert_query("OrgRelation", column_names, entry_types, entry)

    def people(entry):
        column_names = ("origin_database", "email", "phone", "name", "first_name", "middle_name", "last_name", "nih_id")
        entry_types = ("str", "str", "num", "str", "str", "str", "str", "num")
        return insert_query("People", column_names, entry_types, entry)

    def people_alias_id(entry):
        column_names = ("people_id", "alias_id")
        entry_types = ("num", "num")
        return insert_query("PeopleAliasID", column_names, entry_types, entry)

    def people_org(entry):
        column_names = ("people_id", "org_id", "year")
        entry_types = ("num", "num", "num")
        return insert_query("PeopleOrg", column_names, entry_types, entry)

    def people_spec(entry):
        column_names = ("people_id", "bio_id")
        entry_types = ("num", "num")
        return insert_query("PeopleSpec", column_names, entry_types, entry)

    def project(entry):
        column_names = ("origin_database", "title", "start_date")
        entry_types = ("str", "str", "str")
        return insert_query("Project", column_names, entry_types, entry)

    def project_alias_id(entry):
        column_names = ("project_id", "alias_id")
        entry_types = ("num", "num")
        return insert_query("ProjectAliasID", column_names, entry_types, entry)

    def pub_alias_id(entry):
        column_names = ("pub_id", "alias_id")
        entry_types = ("num", "num")
        return insert_query("PubAliasID", column_names, entry_types, entry)
    
    def project_pub(entry):
        column_names = ("project_id", "pub_id")
        entry_types = ("num", "num")
        return insert_query("ProjectPub", column_names, entry_types, entry)

    def publication(entry):
        column_names = ("origin_database", "title", "pmid")
        entry_types = ("str", "str", "num")
        return insert_query("Publication", column_names, entry_types, entry)

    def source(entry):
        column_names = ("work_id", "source")
        entry_types = ("num", "str")
        return insert_query("Source", column_names, entry_types, entry)

    def work(entry):
        column_names = ("project_id", "pub_id")
        entry_types = ("num", "num")
        return insert_query("Work", column_names, entry_types, entry)

    def work_org(entry):
        column_names = ("work_id", "org_id")
        entry_types = ("num", "num")
        return insert_query("WorkOrg", column_names, entry_types, entry)

    def work_people(entry):
        column_names = ("work_id", "people_id")
        entry_types = ("num", "num")
        return insert_query("WorkPeople", column_names, entry_types, entry)



class MergedV1:
    def bioentity(entry):
        column_names = ("name")
        entry_types = ("str")
        return insert_query("Bioentity", column_names, entry_types, entry)
        
    def bio_relation(entry):
        column_names = ("bio_id1", "bio_id2", "relation")
        entry_types = ("num", "num", "str")
        return insert_query("BioRelation", column_names, entry_types, entry)

    def citation(entry):
        column_names = ("work_id1", "work_id2", "relation")
        entry_types = ("num", "num", "str")
        return insert_query("Citation", column_names, entry_types, entry)

    def keyword(entry):
        column_names = ("work_id", "bio_id")
        entry_types = ("num", "num")
        return insert_query("Keyword", column_names, entry_types, entry)
        
    def org(entry):
        column_names = ("name", "funding")
        entry_types = ("str", "num")
        return insert_query("Org", column_names, entry_types, entry)
        
    def org_alias_name(entry):
        column_names = ("org_id", "alias_name")
        entry_types = ("num", "str")
        return insert_query("OrgAliasName", column_names, entry_types, entry)

    def org_relation(entry):
        column_names = ("org_id1", "org_id2", "relation")
        entry_types = ("num", "num", "str")
        return insert_query("OrgRelation", column_names, entry_types, entry)

    def people(entry):
        column_names = ("email", "phone", "name", "first_name", "middle_name", "last_name", "nih_id")
        entry_types = ("str", "num", "str", "str", "str", "str", "num")
        return insert_query("People", column_names, entry_types, entry)
        
    def people_alias_name(entry):
        column_names = ("people_id", "alias_name")
        entry_types = ("num", "str")
        return insert_query("PeopleAliasName", column_names, entry_types, entry)
        
    def people_org(entry):
        column_names = ("people_id", "org_id", "year")
        entry_types = ("num", "num", "num")
        return insert_query("PeopleOrg", column_names, entry_types, entry)
        
    def people_relation(entry):
        column_names = ("people_id1", "people_id2", "relation")
        entry_types = ("num", "num", "str")
        return insert_query("PeopleRelation", column_names, entry_types, entry)

    def people_spec(entry):
        column_names = ("people_id", "bio_id")
        entry_types = ("num", "num")
        return insert_query("PeopleSpec", column_names, entry_types, entry)
        
    def project(entry):
        column_names = ("title")
        entry_types = ("str")
        return insert_query("Project", column_names, entry_types, entry)
        
    def project_alias_name(entry):
        column_names = ("project_id", "alias_name")
        entry_types = ("num", "str")
        return insert_query("ProjectAliasName", column_names, entry_types, entry)
    
    def project_pub(entry):
        column_names = ("project_id", "pub_id")
        entry_types = ("num", "num")
        return insert_query("ProjectPub", column_names, entry_types, entry)
        
    def pub_alias_name(entry):
        column_names = ("pub_id", "alias_name")
        entry_types = ("num", "str")
        return insert_query("PubAliasName", column_names, entry_types, entry)
        
    def publication(entry):
        column_names = ("title", "pmid")
        entry_types = ("str", "num")
        return insert_query("Publication", column_names, entry_types, entry)
        
    def work(entry):
        column_names = ("project_id", "pub_id")
        entry_types = ("num", "num")
        return insert_query("Work", column_names, entry_types, entry)
        
    def work_org(entry):
        column_names = ("work_id", "org_id")
        entry_types = ("num", "num")
        return insert_query("WorkOrg", column_names, entry_types, entry)
        
    def work_people(entry):
        column_names = ("work_id", "people_id")
        entry_types = ("num", "num")
        return insert_query("WorkPeople", column_names, entry_types, entry)

    

if __name__ == "__main__":
    pass