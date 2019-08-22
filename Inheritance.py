# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import AnalyseProject

projects = AnalyseProject.AnalyseAllProjects()
res = AnalyseProject.ProjectResults()
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
print('\nResults for all projects:\n')
print('Number of projects that used constant functions, variables or arguments: ' + str(res.const))
print('Number of projects that used static functions or variables: ' + str(res.static))
print('Number of projects that used enumerations: ' + str(res.enum))
print('Number of projects that used scoped enumerations: ' + str(res.enum_class))
print('Number of projects that used vectors: ' + str(res.vector))
print('\n')
print('Average number of classes: ' + str(res.classes))
print('Number of projects with number of classes below average: ' + str(res.const_args))
print('Number of projects that used public inheritance: ' + str(res.public_inheritance))
print('Number of projects that use abstract base classes: ' + str(res.abstr_base_classes) + '...')
print ('... of which ' + str(res.override) + ' did not use the "override" keyword and ...')
print('... ' +str(res.abc_used) + ' used the ABC correctly at least once.')