# Data Science Analysis: Measuring Impact of Physician-Scientists on Innovation, Research, and Economy

## Database
Current:
OpenSource SQL database called CockroachDB

## Coding Convention
Previously committed code in this GitHub is mostly in ipynb form; this isn't great coding convention. We would like our committed files to be in py form. Feel free to test in ipynb, but please convert to py form before merging into the master branch in our GitHub.

### Unfinished Code

https://docs.google.com/document/d/17AjkavTLgSq9g-ew_HVBQ7thOBMdOWM_NKpEY3MEa5A/edit  <br />
Rule of thumb is to only commit to GitHub if your code is mature, or usable
For other cases, such as your code still being under work, write the code in Google Colab and link it to the above Google Doc.
You are in charge of updating any work you do with a link to the document + brief explanation of what the code does, as well as removing the link and explanation (which you should have transferred as comments to your code) once your code is merged into GitHub.


### GitHub

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
