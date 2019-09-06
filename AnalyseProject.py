# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 12:05:55 2019

@author: Ashraf
"""

import os, pickle, DevProject#Imports, os is for accessing repo directory and for caching with pickle
import numpy as np#For calculation mean and standard deviation of number of classes

def AnalyseProject(name, repoDirectory = os.getcwd()+os.sep+r'Repositories', cacheDirectory = os.getcwd()+os.sep+r'.cache'):
    #A function for Analysing a single project. Takes the name of the repository as an argument and an optional repo directory and cache directory.
    if not os.path.exists(cacheDirectory):#Create the cache directory if it doesn't exist
        os.makedirs(cacheDirectory)
    filename =  cacheDirectory+os.sep+name+'.pkl'#Naming convention for the cache files.
    if not os.path.exists(filename):#If the cache file is not present, then analysis needs to be done.
        Project = DevProject.DevProject(repoDirectory+os.sep+name+os.sep+'game-source-code')#Create a DevProject object for the project.
        print('Analysing ' + name)#Log message
        Project.readResults()#Perform analysis on the project
        print('Done')#Log message
        with open(filename, 'wb') as file_output:
            pickle.dump(Project, file_output, pickle.HIGHEST_PROTOCOL)#Save the cache file of the DevProject object.
    else:#If the cache file exists ... 
        print('Analysis of '+name+' previously completed. Loading results from cache.')
        with open(filename, 'rb') as file_input:
            Project = pickle.load(file_input)#then load the DevProject object from the cache.
    results = GetAnalysisResults(Project)#Collate the results from the DevProject object and return a ProjectResults object.
    return results

def AnalyseAllProjects(repoDirectory = os.getcwd()+os.sep+r'Repositories'):
    #A function for analysing all of the projects. Takes the repo directory as an optional arg.
    projects = []#List for storing the ProjectResults from each project
    classes = []#List used in calculating stats on class usage
    for name in os.listdir(repoDirectory):
        projects.append(AnalyseProject(name))#Gets the ProjectResults for every project in the repo dir
    res = ProjectResults()#Create a ProjectResults object to be returned
    for project in projects:#If a project used a feature, increment the relevant variable
        #Inheritance
        classes.append(project.classes)#Append the number of classes to the list
        if project.public_inheritance:
            res.public_inheritance += 1
        if project.abstr_base_classes:
            res.abstr_base_classes += 1
            if project.override:
                res.override += 1#This is the number of projects that DID use override (changed from did not)
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
        #Use cases
        if project.vector or project.map:
            res.stl += 1
        if project.vector:
            res.vector += 1
        if project.map:
            res.map += 1
        if project.auto:
            res.auto += 1
        if project.shared or project.unique:
            res.pointers += 1#Smart pointers
        if project.shared:
            res.shared += 1
        if project.unique:
            res.unique += 1
        if project.raw and not (project.shared or project.unique):
            res.raw += 1
    res.classes = np.mean(classes)//1#Calculate the mean and normalise as an integer
    std = np.std(classes)//1#Calculate the standard deviation and normalise as integer
    for project in projects:#Grouping projects according to number of classes they have
        below_mean = res.classes - std#One std dev below mean
        above_mean = res.classes + std#One std dev above mean
        if project.classes < below_mean:#Number of projects that had classes below one standard deviation of the mean.
            res.const_args += 1 #Just using an unsused variables instead of creating a dedicated one.
        elif project.classes > above_mean:#no. of proj that had 1 std above mean
            res.const_vars += 1#Reusing unused variable
        elif project.classes < res.classes:#Within 1 std of mean, but less than mean
            res.static_funcs += 1#Reuse unused variable
        elif project.classes > res.classes:#within 1 std of mean but more than mean
            res.const_funcs += 1
    return res

def GetAnalysisResults(project):
    #This function collates the data from a DevProject object and creates and returns a ProjectResults object that represents the analysis data from a single project.
    res = ProjectResults()#Create object
    #Inheritance
    res.classes = len(project.classes)#The number of classes in the project.
    res.public_inheritance = len(project.inheritances)#Number of classes that used public inheritance
    res.abstr_base_classes = len(project.abstr_base_classes)#Abstract base classes in project
    res.abc_used= len(project.abc_used)#Is there a reference or pointer to the ABC in the code?
    res.override = project.overrides#Number of times the override specifier was used
    #Keyword + Use cases
    for result in project.getResults():#Get data from the list of Result objects in the DevProject
        keyword = result.getKeyword()#Member function for returning the name of a Result obj
        #Magic numbers are bad. It might be better to use a dictionary?-->Too much technical debt has been incurred at this point. Noted for future improvement
        if keyword == 'const':
            res.const = result.getCount()#Total number of instances of const
            res.const_funcs = result.getUseCases(0)#functions
            res.const_args = result.getUseCases(1)#Args
            res.const_vars = result.getUseCases(2)#vars
        elif keyword == 'static':
            res.static = result.getCount()#Total number of instances of static
            res.static_funcs = result.getUseCases(0)#functions
            res.static_vars = result.getUseCases(2)#vars
        elif keyword == 'enum':
            res.enum = result.getCount()#No use cases. Includes the enum classes that are used.
        elif keyword == 'enum class':
            res.enum_class = result.getCount()#No use cases
        elif keyword == 'STL':
            res.stl = result.getCount()#Vector, map and auto.
            res.vector = result.getUseCases(0)#vector
            res.map = result.getUseCases(1)#map
            res.auto = result.getUseCases(2)#Although auto does not necessarily belong to STL it is bundled here for convenience sake.
        elif keyword == 'pointers':#Smart pointers and raw pointers
            res.pointers = result.getCount()#includes using arguments that are passed by reference as raw pointer usage
            res.shared = result.getUseCases(0)#shared
            res.unique = result.getUseCases(1)#unique
            res.raw = result.getUseCases(2)#raw
    return res

class ProjectResults:
    #A class that represents the data of an analysis. Used in single projects and all projects
    #There is a variable for each C++ feature outlined in the project spec and proj plan
    def __init__(self):         #single/all
        #inheritance
        self.classes = 0#Number of classes/mean number of classes
        self.public_inheritance = 0#Number of classes that use/number of projects that use
        self.abstr_base_classes = 0#Number of classes that are/number of projects that use
        self.abc_used = 0#Number of times used/number of projects that use
        self.override = 0#Number of times used/number of projects that use
        #keywords
        self.const = 0#Number of times used/number of projects that use
        self.static = 0#Number of times used/number of projects that use
        self.enum = 0#Number of times used/number of projects that use
        self.enum_class = 0#Number of times used/number of projects that use
        self.stl = 0#Number of times used/number of projects that use
        self.pointers = 0#Number of times used/number of projects that use
        #keyword use cases
        #const
        self.const_funcs = 0#Number of times used/number of projects with classes within 1 std of mean but more than mean
        self.const_vars = 0#Number of times used/number of projects with classes 1 std above mean
        self.const_args = 0#Number of times used/number of projects with classes below 1 std of mean.
        #static
        self.static_funcs = 0#Number of times used/number of projects with classes within 1 std of mean, but less than mean
        self.static_vars = 0#Number of times used/unsused var
        #STL
        self.vector = 0#Number of times used/number of projects that use
        self.map = 0#Number of times used/number of projects that use
        self.auto = 0#Number of times used/number of projects that use
        #pointers
        self.shared = 0#Number of times used/number of projects that use
        self.unique = 0#Number of times used/number of projects that use
        self.raw = 0#Number of times used/number of projects that use