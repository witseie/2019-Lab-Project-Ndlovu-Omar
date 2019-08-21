# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 08:13:01 2019

@author: Ashraf
"""
import os, pickle
import numpy as np
import matplotlib.pyplot as plt
keywords = ['const','static','class','enum', 'enum class','vector']
weights = []

def removeComments(string):
    from pyparsing import nestedExpr, dblSlashComment, Suppress
    return (Suppress(nestedExpr('/*','*/') | dblSlashComment)).transformString(string)

def makeGrammer(string):
    from pyparsing import alphanums, Suppress, Optional, CaselessKeyword, Char, Word, cppStyleComment
    cppName = alphanums + ':_<'
    constKeyword = Suppress(Optional(CaselessKeyword("const")))
    keyword = Optional(Char(',')) + constKeyword + Suppress(CaselessKeyword(string)) | Optional(Char('(')) + constKeyword + Suppress(CaselessKeyword(string)) if not string == 'const' else Optional(Char(',')) + Suppress(CaselessKeyword(string)) | Optional(Char('(')) + Suppress(CaselessKeyword(string))
    name =  Word(cppName) + Char(':') + CaselessKeyword('public') | Word(cppName) + Char('{') + CaselessKeyword('public') if string == 'class' else Word(cppName) + Optional(Word(cppName))
    Grammer = keyword + Char("{") | keyword + Char(";") | keyword + Suppress(name) + Optional(Char(';')) if string == 'static' else keyword + Char("{") | keyword + Char(";") | keyword + Suppress(name)
    Grammer = Grammer.ignore(cppStyleComment)
    return Grammer

def makeABCGrammer(className):
    from pyparsing import CaselessLiteral, Char, Combine
    grammer = (CaselessLiteral('unique_ptr<'+className+'>')|CaselessLiteral('shared_ptr<'+className+'>')|Combine(CaselessLiteral(className)+(Char('*')|Char('&'))))
    return grammer

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

c_function, virtual_function, override_func = functionGrammer()

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

cpp_class = classGrammer()

def plot(weights,keyword):
#    if keyword == 'const' or keyword == 'static':
    barWidth = 0.25
 
# set height of bar

# Set position of bar on X axis
    r1 = np.arange(1)
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

# Make the plot
    if keyword == 'const':
        plt.bar(r1, weights[0], color='#7f6d5f', width=barWidth, edgecolor='white', label='as a function')
        plt.bar(r2, weights[1], color='#557f2d', width=barWidth, edgecolor='white', label='as an argument')
        plt.bar(r3, weights[2], color='#2d7f5e', width=barWidth, edgecolor='white', label='as a variable')
    elif keyword == 'static':
        plt.bar(r1, weights[0], color='#7f6d5f', width=barWidth, edgecolor='white', label='as a function')
        plt.bar(r2, weights[2], color='#2d7f5e', width=barWidth, edgecolor='white', label='as a variable')
#    else:
#        plt.bar(r1, weights[0] + weights[1] + weights[2], width=barWidth, edgecolor='white', label='occurances')
# Add xticks on the middle of the group bars
    plt.xlabel('group', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(weights))], [keyword])
    plt.legend()
    if keyword == 'const' or keyword == 'static':
        plt.show()

def AnalyseAllProjects(repoDirectory = os.getcwd()+os.sep+r'Repositories'):
    Projects = []
    for name in os.listdir(repoDirectory):
        Projects.append(AnalyseProject(name))
    return Projects

def AnalyseProject(name, repoDirectory = os.getcwd()+os.sep+r'Repositories', cacheDirectory = os.getcwd()+os.sep+r'.cache'):
    if not os.path.exists(cacheDirectory):
        os.makedirs(cacheDirectory)
    filename =  cacheDirectory+os.sep+name+'.pkl'
    if not os.path.exists(filename):
        Project = DevProject(repoDirectory+os.sep+name+os.sep+'game-source-code')
        print('Analysing ' + name)
        Project.readResults()
        print('Done')
        with open(filename, 'wb') as file_output:
            pickle.dump(Project, file_output, pickle.HIGHEST_PROTOCOL)
    else:
        print('Analysis of '+name+' previously completed. Loading results from cache.')
        with open(filename, 'rb') as file_input:
            Project = pickle.load(file_input)
#    plotProjectResults(Project)
    return Project

def plotProjectResults(project):
    result_count = []
    for result in project.getResults():
        if not (result.getKeyword() == 'const' or result.getKeyword() == 'static'):
            result_count.append(result.getCount())
            plt.bar(result.getKeyword(),result.getCount(),width = 0.5,label = result.getKeyword())
        result.printResult()
    plt.legend()
    plt.xlabel('Keyword', fontweight='bold')
    plt.show()

class DevProject:
    def __init__(self, directory):
        self.__directory = directory
        self.__files = self.readFiles()
        self.__results = []
        self.classes = []
        self.inheritances = []
        self.abstr_base_classes = []
        self.abc_used = []
        self.overrides = 0
    def __repr__(self):
        return str(self.__directory)
    def readFiles(self):
        files = []
        for filename in os.listdir(self.__directory):
            if filename.endswith(".h") or filename.endswith(".cpp"):
                x = File(self.__directory,filename)
                files.append(x)
        return files
    def getFiles(self, index = 'ALL'):
        files = []
        if len(self.__files):
            files = self.__files if index == 'ALL' else self.__files[index]
        return files
    def getFileContents(self, index = 'ALL'):
        if index == 'ALL':
            contents = []
            for cont in self.__files:
                contents.append(cont.getContents())
        else:
            contents = self.__files[index].getContents()
        return contents
    def readFileResults(self):
        for file in self.__files:
            file.readResults()
            if file.getName().endswith('.h'):
                classes = cpp_class.searchString(file.getContents())
                for item in classes:
                    temp = cppClass(item)
                    self.classes.append(temp)
                    if temp.inheritance:
                        self.inheritances.append(temp.name)
                    if temp.abstr_base_class:
                        self.abstr_base_classes.append(temp.name)
                        grammer = makeABCGrammer(temp.name)
                        self.abc_used.append(grammer.searchString(self.getFileContents()).asList())
                    self.overrides += temp.override
    def readResults(self):
        self.readFileResults()
        results = []
        idx = 0
        for keyword in keywords:
            count = 0
            use_cases = [0, 0, 0]
            for file in self.__files:
                count += file.getResults(idx).getCount()
                use_cases[0] +=file.getResults(idx).getUseCases(0)
                use_cases[1] +=file.getResults(idx).getUseCases(1)
                use_cases[2] +=file.getResults(idx).getUseCases(2)
            res = Result(keyword,count)
            res.setUseCases(use_cases)
            results.append(res)
            idx+=1
        self.__results = results
    def getResults(self):
        return self.__results
        
class File:
    def __init__(self,directory,name):
        self.__name = name
        self.__directory = directory
        self.__contents = self.readContents()
        self.__results = []
    def __repr__(self):
        return str(self.__name)
    def readContents(self):
        filename = self.__directory + os.sep + self.__name
        try:
            file_contents = filename.read()
        except AttributeError:
            with open(filename, "r") as f:
                file_contents = f.read()
                file_contents = removeComments(file_contents)
        return file_contents
    def readResults(self):
        results = []
        for keyword in keywords:
            grammer = makeGrammer(keyword)
            inst = grammer.searchString(self.__contents)
            count = len(inst)
            res = Result(keyword,count,inst.asList())
            results.append(res)
        self.__results = results
    def getName(self):
        return str(self.__name)
    def getContents(self):
        return str(self.__contents)
    def getResults(self, index = 'ALL'):
        res = []
        if len(self.__results):
            res = self.__results if index == 'ALL' else self.__results[index]
        return res

class Result:
    def __init__(self, keyword, count, inst = []):
        self.__keyword = keyword
        self.__count = count
        self.__inst = inst
        self.__use_cases = [self.__inst.count([]), self.__inst.count(['(']) + self.__inst.count([',']) , self.__inst.count([';']) + self.__inst.count(['{'])] if self.__keyword == 'static' else [self.__inst.count([';']) + self.__inst.count(['{']) , self.__inst.count(['(']) + self.__inst.count([',']) , self.__inst.count([])]
    def getKeyword(self):
        return self.__keyword
    def getCount(self):
        return self.__count
    def getUseCases(self, index = 'ALL'):
        cases = []
        if len(self.__use_cases):
            cases = self.__use_cases if index == 'ALL' else self.__use_cases[index]
        return cases
    def setUseCases(self,use_cases):
        self.__use_cases = use_cases
    def printResult(self):
        string = 'Instances of use of ' + self.__keyword + ' keyword: ' + str(self.__count)
        print(string)
        print(self.__use_cases)
        plot(self.__use_cases,self.__keyword)
        
class cppClass:
    def __init__(self, parseRes):
        temp = parseRes
        self.name = temp.name
        self.parents = temp.parents.asList() if temp.parents else []
        self.body = temp.body
        self.functions = c_function.searchString(self.body).asList()
        self.abstr_functions = virtual_function.searchString(self.body).asList()
        self.override_functions = override_func.searchString(self.body).asList()
        
        self.inheritance = 1 if self.parents else 0
        self.abstr_base_class = 1 if (len(self.functions)==len(self.abstr_functions) and len(self.functions) != 0) else 0
        self.override = 1 if (len(self.override_functions) != 0) else 0