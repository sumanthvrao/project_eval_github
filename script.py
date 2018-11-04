# import dependencies
import os
import sys
import requests
import json
import pandas as pd
import csv
import time

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)

# Read each project URL from csv file
df = pd.read_csv('data/projectURLs.csv', sep=',')
projects = list(df['GitHub link to Repository'])

def extract_repo(project):
    item = project.split('/')[-1]
    return item

def extract_username(project):
    return project.split('/')[-2]

AUTH_TOKEN = '***************************'

with open ('output/all_stats.csv', 'a') as writeFile:
    writer = csv.writer(writeFile)
    header = ['Github_handle', 'reponame', 'contributions', 'weekcount', 'LOC_addition', 'LOC_deletion']
    writer.writerow(header)
    for project in projects:
        username = extract_username(project)
        reponame = extract_repo(project)
        string = 'https://api.github.com/repos/'+username+'/'+reponame+'/stats/contributors'
        print(string)
        m = requests.get(string, headers={'Authorization': 'token '+AUTH_TOKEN})
        res = json.loads(m.text or m.content)
        for item in res:
            author_name = item['author']['login']
            commit_count = item['total']
            week_count = len(item['weeks'])
            a = 0
            d = 0
            for week in item['weeks']:
                a+= week["a"]
                d+= week["d"]

            row = [author_name, reponame, commit_count, week_count, a, d]
            print(row)
            writer.writerow(row)
