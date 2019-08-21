# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import DevProject


def makeABCGrammer(className):
    from pyparsing import CaselessLiteral, Char, Combine
    grammer = (CaselessLiteral('unique_ptr<'+className+'>') | CaselessLiteral('shared_ptr<'+className+'>') | Combine(CaselessLiteral(className) + (Char('*')|Char('&'))))
    return grammer

def checkAbcUse(project):
    abc_used = []
    allFiles = project.getFileContents()
    for ABC in project.abstr_base_classes:
        grammer = makeABCGrammer(ABC)
        abc_used.append(grammer.searchString(allFiles).asList())
    return 1 if abc_used else 0

projects = DevProject.AnalyseAllProjects()
inh = 0
role = 0
override = 0
role_not_used = 0
for project in projects:
    inheritance = project.inheritances
    abc = project.abstr_base_classes
    abc_used = checkAbcUse(project)
    ovrd = project.overrides
    if inheritance:
        inh += 1
    if abc:
        role += 1
        if not ovrd:
            override += 1
        if not abc_used:
            role_not_used += 1
print('\nResults for all projects:\n')
print('Number of projects that use inheritance: ' + str(inh))
print('Number of projects that use abstract base classes: ' + str(role) + '...')
print ('... of which ' + str(override) + ' did not use the "override" keyword and ...')
print('... ' +str(role_not_used) + ' did not use the ABC correctly.')