# Data Science Analysis: Measuring Impact of Physician-Scientists on Innovation, Research, and Economy

## Database

We are currently working with the MIT SIPB MySQL Database service, which allows 100MB of total storage for free.
The following is the instruction for accessing the database through MIT SIPB’s webpage that you can use to add or drop entire databases:

1. Open http://sql.mit.edu/main/do/index
2. Around the top right corner of the page, there are two choices for logging-in, choose the SQL Password option.
3. Enter the username (mit-ps) and password (cut18vuk).
4. You should see something like the following if you did everything right.

To interact with a specific database, it is suggested that we should use phpMyAdmin, and to do that, you open the following link.

https://sql.scripts.mit.edu/phpMyAdmin/index.php?db=&table=&server=1&target=&token=c5b17600b2fb3b32e70c89903ec66b38

After that, you enter the same username and password.

We currently are using the UnmergedV1 database for our project.

## Uploading Scripts

The repository is organized in the following way. At the root directory, there are the SQLConnect.py, UnmergedV1.sql, and this read me file. The SQLConnect.py is used as a library for the uploading scripts to help with the process of querying to the database that we use, while the UnmergedV1.sql can be used to re-initialize an empty version of the UnmergedV1 database.

Aside from these files, there are folders in the repository. With the exceptions of _pycache_ and demo, each folder contains files and data that are used to upload data from online databases to our MySQL database.

### SQLConnect.py

In SQLConnect.py, there are several functions and classes that can help you with querying the database. The first and most useful one would be connect_and_query, which is a function that takes in a list of queries, another list containing the kind of queries being made, and the name of the database that we are querying to in str. Note that the two lists must be of same sizes, and both are lists of strings.

The next is the insert_query_dict, which helps you make MySQL INSERT queries. The inputs contain the name of the targetted table in string, and a dictionary mapping table fields to the values that you want to insert. The table fields are strings, while values can be numbers, strings, or None. Use numbers when you are inserting numeric values, None when you want to leave a field blank, and strings otherwise. Some fields in our tables are ID fields that will autofill itself, do not include these fields in the input's dictionary.

There is also the insert_query function, which was an older version of the insert_query_dict. Instead of using a dictionary to represent the input, this function takes in a tuple of the name of the fields, a tuple of the values to be inserted, and a tuple of the type of values for the fields. All these tuples have the same length so that we can correspond each field with a value and a type. There are two types, represented by strings, "num" which suggests that the values are numeric and that the values should not be encapsulated by quotes, and "str" which suggests otherwise. It is recommended that you switch to using insert_query_dict from now on as this function tends to be less straight-forward to use.

Finally, there are two classes, each with numerous methods. Each class corresponds to one database, and each method in it corresponds to a table in the database. Each method's purpose was to take in entries, and output an INSERT query to insert the entries to the table that corresponds to the method.

## GitHub

For collaboration, you need to first create a local copy of the repository in the following way
1. Make a GitHub account if you have not. Once you have an account, message the owner of the repository about your account name to add you to the collaborator.
2. Go to https://github.com/aaronk2002/physician-scientists, press Fork at the top right corner to create a new repo for your account that is a fork of the main repo, beyond this let's refer to this repo as the forked repo
3. Once you created a new fork, choose a folder on your device, open it on VSCode, and run the following on your terminal
```
git clone <URL of the forked repository>.git
cd <the new folder that appeared>
```
Now you are in a local version of the repository that is on your device. Next, for uploading changes from local repository to GitHub repository, follow the next set of instructions:
1. After making some changes, run the following on your terminal
```
git add .
git commit -m “Some text to tell other collaborator what you changed”
git push
```
2. Go to your forked repository, go to the Pull Request tab, and press New pull request.
3. Make the pull request.
4. After that you should be able to perform merge pull request. You may want to not immediately do this, other people may want to look at the changes first. If everyone is on board with the changes, go ahead and perform a merge pull request. Note that merging occasionally does not work due to a merge conflict, and if none occurs, the process should run smoothly, and you technically do not need any other person’s approval to merge, it’s just best practice to do so. Once merged, your changes should be applied to the GitHub repository.
