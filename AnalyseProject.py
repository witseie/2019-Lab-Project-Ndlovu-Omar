# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 12:05:55 2019

@author: Ashraf
"""

import os, pickle, DevProject

def AnalyseProject(name, repoDirectory = os.getcwd()+os.sep+r'Repositories', cacheDirectory = os.getcwd()+os.sep+r'.cache'):
    if not os.path.exists(cacheDirectory):
        os.makedirs(cacheDirectory)
    filename =  cacheDirectory+os.sep+name+'.pkl'
    if not os.path.exists(filename):
        Project = DevProject.DevProject(repoDirectory+os.sep+name+os.sep+'game-source-code')
        print('Analysing ' + name)
        Project.readResults()
        print('Done')
        with open(filename, 'wb') as file_output:
            pickle.dump(Project, file_output, pickle.HIGHEST_PROTOCOL)
    else:
        print('Analysis of '+name+' previously completed. Loading results from cache.')
        with open(filename, 'rb') as file_input:
            Project = pickle.load(file_input)
    results = GetAnalysisResults(Project)
    return results

def AnalyseAllProjects(repoDirectory = os.getcwd()+os.sep+r'Repositories'):
    projects = []
    for name in os.listdir(repoDirectory):
        projects.append(AnalyseProject(name))
    res = ProjectResults()
    for project in projects:
        #Inheritance
        res.classes += project.classes
        if project.public_inheritance:
            res.public_inheritance += 1
        if project.abstr_base_classes:
            res.abstr_base_classes += 1
            if not project.override:
                res.override += 1#This is the number of projects that did NOT use override
            if project.abc_used:
                res.abc_used += 1
        #Keywords
        if project.const:
            res.const += 1
        if project.static:
            res.static += 1
        if project.enum:
            res.enum += 1
        if project.enum_class:
            res.enum_class += 1
        if project.vector:
            res.vector += 1
        #No use cases for all projects
    res.classes = res.classes//len(projects)
    for project in projects:
        if project.classes < res.classes:#Number of projects with below average number of classes
            res.const_args += 1 #Just using an unsused variable instead of creating a dedicated one
    return res

def GetAnalysisResults(project):
    res = ProjectResults()
    #Inheritance
    res.classes = len(project.classes)
    res.public_inheritance = len(project.inheritances)
    res.abstr_base_classes = len(project.abstr_base_classes)
    res.abc_used= len(project.abc_used)
    res.override = project.overrides
    #Keyword + Use cases
    for result in project.getResults():
        keyword = result.getKeyword()
        if keyword == 'const':
            res.const = result.getCount()
            res.const_funcs = result.getUseCases(0)
            res.const_args = result.getUseCases(1)
            res.const_vars = result.getUseCases(2)
        elif keyword == 'static':
            res.static = result.getCount()
            res.static_funcs = result.getUseCases(0)
            res.static_vars = result.getUseCases(2)
        elif keyword == 'enum':
            res.enum = result.getCount()
        elif keyword == 'enum class':
            res.enum_class = result.getCount()
        elif keyword == 'vector':
            res.vector = result.getCount()
    return res

class ProjectResults:#For each C++ feature outlined in the project spec and proj plan
    def __init__(self):
        #inheritance
        self.classes = 0
        self.public_inheritance = 0
        self.abstr_base_classes = 0
        self.abc_used = 0
        self.override = 0
        #keywords
        self.const = 0
        self.static = 0
        self.enum = 0
        self.enum_class = 0
        self.vector = 0
        #keyword use cases
        self.const_funcs = 0
        self.const_vars = 0
        self.const_args = 0
        self.static_funcs = 0
        self.static_vars = 0