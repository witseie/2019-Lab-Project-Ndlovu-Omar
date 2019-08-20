# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os, DevProject

def removeComments(string):
    from pyparsing import nestedExpr, dblSlashComment, Suppress
    return (Suppress(nestedExpr('/*','*/') | dblSlashComment)).transformString(string)

def functionGrammer():
    from pyparsing import (oneOf, Word, alphas, alphanums, Combine, Optional, Group, nestedExpr, Suppress, quotedString, cppStyleComment, delimitedList, CaselessKeyword, Char)
    data_type = oneOf("void int short long char float double")
    ident = Word(alphas+'_<', alphanums+':_<>,') + ~Word('\n')
    decl_data_type = Combine(ident + Optional(Word('*')|Word('&'))) | Combine(data_type + Optional(Word('*')|Word('&')))
    arg = Group(decl_data_type + ident)
    LPAR,RPAR = map(Suppress, "()")
    code_body = nestedExpr('{', '}', ignoreExpr=(quotedString | cppStyleComment))
    c_function = (decl_data_type("type")
                  + ident("name")
                  + LPAR + Optional(delimitedList(arg), [])("args") + RPAR
                  + Optional(code_body("body")))
    c_function = c_function.ignore(cppStyleComment)
    virtual_function = CaselessKeyword('virtual') + Group(c_function + Optional(Char('=') + Char('0') + Char(';')))
    virtual_function = virtual_function.ignore(cppStyleComment)
    override_func = c_function + CaselessKeyword('override')
    override_func = override_func.ignore(cppStyleComment)
    return c_function, virtual_function, override_func

def classGrammer():
    from pyparsing import Word, alphas, alphanums, CaselessKeyword, Suppress, Group, nestedExpr, Char, originalTextFor, delimitedList, Optional
    cppName = Word(alphas+':_', alphanums+':_')
    class_keyword = Suppress(CaselessKeyword('class'))
    class_name =  cppName
    class_body = Group(nestedExpr('{', '}') + Char(';'))
    parent_class = Group(Suppress(CaselessKeyword('public')) + class_name)
    inherits =  Suppress(Char(':')) + delimitedList(parent_class)
    scoped_enum = Group(CaselessKeyword('enum') + class_keyword + class_name + class_body)
    
    Grammer = (class_keyword + class_name("name") + Optional(inherits)("parents") + (originalTextFor(class_body)("body")))
    Grammer = Grammer.ignore(scoped_enum)
    return Grammer

repoDirectory = os.getcwd()+os.sep+r'Repositories'
name = r'2018-project-1043475-Mwaniki-1076467-Sethosa'
for name in os.listdir(repoDirectory):
    fileDirectory = repoDirectory + os.sep + name +os.sep + r'game-source-code'
    project = DevProject.DevProject(fileDirectory)
    classList = []
    inheritance = 0
    abc = 0
    ovrd = 0
    c_function, virtual_function, override_func = functionGrammer()
    grammer = classGrammer()
    print(name)
    for file in project.getFiles():
        if file.getName().endswith('.h'):
            cont = removeComments(file.getContents())
            classes = grammer.searchString(cont)
            for cppClass in classes:
                classList.append(cppClass.asList())
                if cppClass.parents:
                    inheritance += 1
                source_code = cppClass.body
                functions = c_function.searchString(source_code).asList()
                abstr_functions = virtual_function.searchString(source_code).asList()
                override_functions = override_func.searchString(source_code).asList()
                if len(functions)==len(abstr_functions) and len(functions) != 0:
                    abc += 1
                if len(override_functions) != 0:
                    ovrd += 1
    print('Number of classes in the project: ' + str(len(classList)))
    print('Number of classes using inheritance: ' + str(inheritance))
    print('Number of abstract base classes: ' + str(abc))
    print('Number of classes using override functions: ' + str(ovrd) + '\n')
    ans = 'Yes.' if inheritance != 0 else 'No.'
    print('Inheritance used?: ' + ans)
    ans = 'Yes.' if abc!=0 else 'No.'
    if ans == 'Yes.' and ovrd==0:
        ans = ans + ' Used incorrectly.'
    print('Role modelling used?: ' + ans +'\n')