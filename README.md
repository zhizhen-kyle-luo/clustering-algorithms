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
