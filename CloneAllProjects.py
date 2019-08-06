# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 18:35:30 2019

@author: Ashraf
"""
import requests, json, os, getpass
demis = ['2018-project-560895-Linda','2018-project-571133-Kyle','2018-project-714227-Kayla','2018-project-717931-Kishan','2018-project-816424-Conrad','2018-project-837873-Malu']

def main():
    user, pswd = getInput()
    cloneAllProjects(user, pswd)

def cloneAllProjects(user, pswd, access_token = '146da8c3ad930d598318a94068fe158c716f6496', directory = os.getcwd() + os.sep + r'Repositories'):
    filename = os.getcwd() + os.sep + 'Repos.json'
    if not os.path.exists(filename):
        headers = {
            'Accept': 'application/vnd.github.mercy-preview+json',
            'Content-type': 'application/json',
        }
        params = (
            ('q', 'org:witseie-elen3009 2018-project-'),
            ('access_token', ''),
            ('per_page' , '100'),
        )
        response = requests.get('https://api.github.com/search/repositories', headers=headers, params=params, auth=(user, pswd))
        json_string = response.json()['items']
        with open(filename, 'w') as f:
            json.dump(json_string, f)
    else:
        with open(filename, 'r') as f:
            json_string = json.load(f)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)    
    for repo in json_string:
        name = repo['name']
        if name not in demis:
            print('Cloning repository: ' + name)
            os.system('git clone --depth 1 ' + repo['ssh_url'])
    print('Done.')

def getInput():
    while True:
        user = input('Enter GitHub user name: \n')
        break
    while True:
        pswd = getpass.getpass('Enter GitHub password: ')
        break
    return user, pswd

if __name__ == '__main__':
    main()
    k = input('Press enter to exit...')