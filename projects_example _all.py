# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import AnalyseProject

res = AnalyseProject.AnalyseAllProjects()

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