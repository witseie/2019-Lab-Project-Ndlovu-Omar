# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import AnalyseProject, os

res = AnalyseProject.AnalyseAllProjects()
flist = os.listdir(os.getcwd()+os.sep+r'Repositories')

print('\nResults for all projects:\n')
print('Number of projects being analysed: ' + str(len(flist)))
print('Number of projects that used constant functions, variables or arguments: ' + str(res.const))
print('Number of projects that used static functions or variables: ' + str(res.static))
print('Number of projects that used enumerations: ' + str(res.enum))
print('Number of projects that used scoped enumerations: ' + str(res.enum_class))
print('Number of projects that used vectors: ' + str(res.vector))
print('Number of projects that used maps: ' + str(res.map))
print('Number of projects that used the "auto" keyword: ' + str(res.auto))
print('Number of projects that used smart pointers: ' + str(res.pointers))
print('Number of projects that used shared pointers: ' + str(res.shared))
print('Number of projects that used unique pointers: ' + str(res.unique))
print('Number of projects that used only raw pointers: ' + str(res.raw))
print('Number of projects that used the override keyword: ' + str(res.override))

print('\n')
print('Average (mean) number of classes: ' + str(res.classes//1))
print('Number of projects with classes below one standard deviation of the mean: ' + str(res.const_args))
print('Number of projects with classes within one standard deviation below the mean: ' + str(res.static_funcs))
print('Number of projects with classes within one standard deviation above the mean: ' + str(res.const_funcs))
print('Number of projects with classes above one standard deviation of the mean: ' + str(res.const_vars))
print('Number of projects that used public inheritance: ' + str(res.public_inheritance))
print('Number of projects that use abstract base classes: ' + str(res.abstr_base_classes) + '...')
print('... of which ' +str(res.abc_used) + ' used the ABC correctly at least once.')
