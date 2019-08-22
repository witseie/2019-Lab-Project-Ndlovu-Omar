# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 18:35:30 2019

@author: Ashraf
"""
import requests, json, os, getpass
demis = ['2018-project-560895-Linda','2018-project-571133-Kyle','2018-project-714227-Kayla','2018-project-717931-Kishan','2018-project-816424-Conrad','2018-project-837873-Malu']

def main():
    user, pswd, year, max_repos = getInput()
    cloneAllProjects(user, pswd, year, max_repos)

def getRepoNames(user, pswd, year = '2018', max_repos = '100', access_token = '146da8c3ad930d598318a94068fe158c716f6496'):
    cacheDirectory = os.getcwd() +os.sep+r'.cache'
    if not os.path.exists(cacheDirectory):
        os.makedirs(cacheDirectory)
    filename = cacheDirectory + os.sep + 'Repos-' + year + '-max=' + max_repos +'.json'
    if not os.path.exists(filename):
        headers = {
            'Accept': 'application/vnd.github.mercy-preview+json',
            'Content-type': 'application/json',
        }
        params = (
            ('q', 'org:witseie-elen3009 '+ year +'-project-'),
            ('access_token', access_token),
            ('per_page' , max_repos),
        )
        response = requests.get('https://api.github.com/search/repositories', headers=headers, params=params, auth=(user, pswd))
        json_string = response.json()['items']
        with open(filename, 'w') as f:
            json.dump(json_string, f)
    else:
        with open(filename, 'r') as f:
            json_string = json.load(f)
    names = []
    for repo in json_string:
        name = repo['name']
        if ((name not in demis) and ('Demi' not in name)):
            names.append(name)
    return names

def cloneAllProjects(user, pswd, year = '2018', max_repos = '100', directory = os.getcwd() + os.sep + r'Repositories'):
    repos = getRepoNames(user, pswd, year, max_repos)
    repos = str(len(repos))
    print(repos + ' repositories found.')
    cacheDirectory = os.getcwd()+os.sep+r'.cache'
    if not os.path.exists(cacheDirectory):
        os.makedirs(cacheDirectory)
    filename = cacheDirectory + os.sep + 'Repos-' + year + '-max=' + max_repos +'.json'
    with open(filename, 'r') as f:
        json_string = json.load(f)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)    
    for repo in json_string:
        cloneProject(repo)
    print('Done.')
    os.chdir(cacheDirectory)
    os.remove(filename)

def cloneProject(repo):
    name = repo['name']
    if ((name not in demis) and ('Demi' not in name)):
        print('Cloning repository: ' + name)
        os.system('git clone --depth 1 ' + repo['ssh_url'])

def getInput():
    while True:
        user = input('Enter GitHub user name: \n')
        break
    while True:
        pswd = getpass.getpass('Enter GitHub password: ')
        break
    while True:
        year = input('Enter year to search for: ')
        break
    while True:
        max_repos = input('Enter maximum number of repos to search for: ')
        break
    return user, pswd, year, max_repos

if __name__ == '__main__':
    main()
    k = input('Press enter to exit...')