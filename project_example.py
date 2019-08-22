# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import AnalyseProject#, os


name = r'2018-project-675515-Bradfield-672871-Maboko'
#os.remove(os.getcwd()+os.sep+'.cache'+os.sep+name+'.pkl')
res = AnalyseProject.AnalyseProject(name)

print('Number of classes in the project: ' + str(res.classes))
print('Number of classes using public inheritance: ' + str(res.public_inheritance))
print('Number of abstract base classes: ' + str(res.abstr_base_classes))
print('Number of times ABC was used in code: ' + str(res.abc_used))
print('Number of classes using override functions: ' + str(res.override) + '\n')

print('Number of constant functions, variables or arguments: ' + str(res.const))
if res.const:
    print(str(res.const_funcs) + ' functions, ' + str(res.const_vars) + ' variables and ' + str(res.const_args) + ' arguments.')
print('Number of static functions or variables: ' + str(res.static))
if res.static:
    print(str(res.static_funcs) + ' functions, ' + str(res.static_vars) + ' variables.')
print('Number of enumerations: ' + str(res.enum))
print('Number of scoped enumerations: ' + str(res.enum_class))
print('Number of vectors: ' + str(res.vector))
