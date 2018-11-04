# import dependencies
import pandas as pd
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)

# read each project URL from csv file
df = pd.read_csv('data/projectURLs.csv', sep=',')
projects = list(df['GitHub link to Repository'])

# chdir to the project repo folder
os.chdir(BASE_PATH + '/repos')

def extract_name(project):
    return project.split('/')[-1]

project_root = os.getcwd()

already_fetched_repo_names = os.listdir(project_root)
print(already_fetched_repo_names)

for project in projects:
    if extract_name(project) in already_fetched_repo_names:
        # pull latest code from the master branch
        print("Pulling latest code from master branch of "+project+" project...")
        repo_names = [name for name in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, name))]
        for repo in repo_names:
            os.chdir(project_root + "/" + repo)
            os.system("git pull origin master")
    else:
        # clone the project
        print("Cloning "+project +" project...")
        os.system('git clone ' + project)
