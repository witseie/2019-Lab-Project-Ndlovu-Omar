# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import DevProject
#import pyparsing as pp
from pyparsing import *

def removeComments(string):
    return (Suppress(nestedExpr('/*','*/') | dblSlashComment)).transformString(string)

def functionGrammer():
    data_type = oneOf("void int short long char float double")
    ident = Word(alphas+'_', alphanums+':_')
    decl_data_type = Combine(ident + Optional(Word('*')|Word('&'))) | Combine(data_type + Optional(Word('*')|Word('&')))
#    number = pyparsing_common.number
    arg = Group(decl_data_type + ident)
    LPAR,RPAR = map(Suppress, "()")
    
    code_body = nestedExpr('{', '}', ignoreExpr=(quotedString | cppStyleComment))
    
    c_function = (decl_data_type("type")
                  + ident("name")
                  + LPAR + Optional(delimitedList(arg), [])("args") + RPAR
                  + Optional(code_body("body")))
    c_function = c_function.ignore(cppStyleComment)
    virtual_function = CaselessKeyword('virtual') + c_function
    virtual_function = virtual_function.ignore(cppStyleComment)
    return c_function, virtual_function

def classGrammer():
    cppName = Word(alphas+':_', alphanums+':_')
#    constKeyword = CaselessKeyword("const")
    class_keyword = Suppress(CaselessKeyword('class')) #+ ~PrecededBy(CaselessKeyword('enum'))
    class_name =  cppName
    class_body = nestedExpr('{', '};', ignoreExpr=(cppStyleComment.suppress()))    
    parent_class = Group(Suppress(CaselessKeyword('public')) + class_name)
    inherits =  Suppress(Char(':')) + delimitedList(parent_class)
    scoped_enum = Group(CaselessKeyword('enum') + class_keyword + class_name + class_body)
    
    Grammer = (class_keyword + class_name("name") + Optional(inherits)("parents") + originalTextFor(class_body)("body"))
#    Grammer = originalTextFor(Grammer)
    Grammer = Grammer.ignore(scoped_enum)
    return Grammer

fileDirectory = r"D:\Ashraf\Documents\.University_Stuff\.4th Year\ELEN4012 - Lab Project\Parsing\Repositories\2018-project-474233-Hlongwane-1393636-Mukansi\game-source-code"
grammer = classGrammer()

project = DevProject.DevProject(fileDirectory)
classList = []
inheritance = 0
for file in project.getFiles():
#    if file.getName().endswith('.h'):
    cont = file.getContents()
    classes = grammer.searchString(removeComments(cont))
    for cppClass in classes:
        classList.append(cppClass.asList())
        if cppClass.parents:
            inheritance += 1
print('Number of classes in the project: ' + str(len(classList)))
print('Number of classes using inheritance: ' + str(inheritance))

#c_function, virtual_function = functionGrammer()
#source_code = file.getContents()
#a = c_function.searchString(source_code).asList()
#b=virtual_function.searchString(source_code).asList()
#if len(a)==len(b):
#    print("It's an ABC")
#else:
#    print("It's not an ABC")
        
#for func in a:
#    print("%(name)s (%(type)s) args: %(args)s" % func)
