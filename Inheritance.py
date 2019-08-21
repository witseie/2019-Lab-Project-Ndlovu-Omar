# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import DevProject

projects = DevProject.AnalyseAllProjects()
inh = 0
role = 0
override_not_used = 0
abc_used_projects = 0
for project in projects:
    inheritance = project.inheritances
    abc = project.abstr_base_classes
    abc_used = len(project.abc_used)
    ovrd = project.overrides
    if inheritance:
        inh += 1
    if abc:
        role += 1
        if not ovrd:
            override_not_used += 1
        if abc_used:
            abc_used_projects += 1
print('\nResults for all projects:\n')
print('Number of projects that used public inheritance: ' + str(inh))
print('Number of projects that use abstract base classes: ' + str(role) + '...')
print ('... of which ' + str(override_not_used) + ' did not use the "override" keyword and ...')
print('... ' +str(abc_used_projects) + ' used the ABC correctly at least once.')