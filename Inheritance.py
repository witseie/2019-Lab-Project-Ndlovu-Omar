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
    class_keyword = Suppress(CaselessKeyword('class'))
    class_name =  cppName
    class_body = Group(nestedExpr('{', '}') + Char(';'))
    parent_class = Group(Suppress(CaselessKeyword('public')) + class_name)
    inherits =  Suppress(Char(':')) + delimitedList(parent_class)
    scoped_enum = Group(CaselessKeyword('enum') + class_keyword + class_name + class_body)
    
    Grammer = (class_keyword + class_name("name") + Optional(inherits)("parents") + (originalTextFor(class_body)("body")))
    Grammer = Grammer.ignore(scoped_enum)
    return Grammer

fileDirectory = r"D:\Ashraf\Documents\.University_Stuff\.4th Year\ELEN4012 - Lab Project\Parsing\Repositories\2018-project-474233-Hlongwane-1393636-Mukansi\game-source-code"
grammer = classGrammer()

project = DevProject.DevProject(fileDirectory)
classList = []
inheritance = 0
abc = 0
c_function, virtual_function = functionGrammer()

for file in project.getFiles():
    if file.getName().endswith('.h'):
#        print(file.getName())
        cont = removeComments(file.getContents())
        classes = grammer.searchString(cont)
        for cppClass in classes:
#            print(cppClass.name)
            classList.append(cppClass.asList())
            if cppClass.parents:
                inheritance += 1
            source_code = cppClass.body
            functions = c_function.searchString(source_code).asList()
            abstr_functions = virtual_function.searchString(source_code).asList()
            if len(functions)==len(abstr_functions):
                print(cppClass.name + " is an ABC")
                abc += 1
#            else:
#                print("It's not an ABC")
print('Number of classes in the project: ' + str(len(classList)))
print('Number of classes using inheritance: ' + str(inheritance))
print('Number of abstract base classes: ' + str(abc))


        
#for func in a:
#    print("%(name)s (%(type)s) args: %(args)s" % func)
