# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 08:13:01 2019

@author: Ashraf
"""
import os#Imports: os used for accessing files and folders
keywords = ['const','static','enum', 'enum class','vector', 'pointers']#A list of the features. Used by fuctions when performing taks in for loops.

def removeComments(string):
    #Function for removing comments from source code files.
    from pyparsing import nestedExpr, dblSlashComment, Suppress#import the functions needed from pyparsing
    return (Suppress(nestedExpr('/*','*/') | dblSlashComment)).transformString(string)#Remove double slash comments and /* */ block comments

def makeGrammer(string):#Makes a ``grammar" for the searchString() function of pyparsing. Intentionally misspelt to avoid confusion with proper definition of grammar.
    from pyparsing import alphas, alphanums, Suppress, Optional, CaselessKeyword, Char, Word, cppStyleComment
    cppName = Word(alphas+'_<', alphanums+':_<>,') + ~Word('\n')#Definition of a C++ identifier
    constKeyword = Suppress(Optional(CaselessKeyword("const")))#Avoid parsing of the const keyword unless actively searching for it
    keyword = Optional(Char(',')) + constKeyword + Suppress(CaselessKeyword(string)) | Optional(Char('(')) + constKeyword + Suppress(CaselessKeyword(string)) if not string == 'const' else Optional(Char(',')) + Suppress(CaselessKeyword(string)) | Optional(Char('(')) + Suppress(CaselessKeyword(string))
    #A one-size-fits-all definition for all the keywords. does not include classes or stl
    name = cppName + Optional(cppName)#Definition of a function or variable name
    #The grammer returns a "{", ";" or [] based on the use case of the keyword
    Grammer = keyword + Char("{") | keyword + Char(";") | keyword + Suppress(name) + Optional(Char(';')) if string == 'static' else keyword + Char("{") | keyword + Char(";") | keyword + Suppress(name)#As above, so below (one-size-fits-all grammer for all the keywords) 
    Grammer = Grammer.ignore(cppStyleComment)#Ignore comments when looking for the keywords/grammer
    return Grammer

def makeABCGrammer(className):#Makes a definition for Abstract base classes
    from pyparsing import CaselessLiteral, Char, Combine
    grammer = (CaselessLiteral('unique_ptr<'+className+'>')|CaselessLiteral('shared_ptr<'+className+'>')|Combine(CaselessLiteral(className)+(Char('*')|Char('&'))))
    #Based on C++ syntax
    return grammer

def functionGrammer():#Function for different types of functions (normal, virtual, override)
    #Taken directly from examples in pyparsing which has open-source license.
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
    virtual_function = CaselessKeyword('virtual') + Group(c_function + Optional(Char('=') + Char('0') + Char(';')))#Virtual functions are the same except for the virtual keyword and "=0;"
    virtual_function = virtual_function.ignore(cppStyleComment)
    override_func = c_function + CaselessKeyword('override')#Check for override at the end.
    override_func = override_func.ignore(cppStyleComment)
    return c_function, virtual_function, override_func

def classGrammer():#Function for defining the way a class is defined.
    from pyparsing import Word, alphas, alphanums, CaselessKeyword, Suppress, Group, nestedExpr, Char, originalTextFor, delimitedList, Optional
    cppName = Word(alphas+':_', alphanums+':_')#Identifiers
    class_keyword = Suppress(CaselessKeyword('class'))#Keyword
    class_name =  cppName#Class name
    class_body = Group(nestedExpr('{', '}') + Char(';'))#Body
    parent_class = Group(Suppress(CaselessKeyword('public')) + class_name)#Public inheritance
    inherits =  Suppress(Char(':')) + delimitedList(parent_class)#List of parents
    scoped_enum = Suppress(CaselessKeyword('enum') + class_keyword + class_name + class_body)#Ignore enum class when searching
    Grammer = (class_keyword + class_name("name") + Optional(inherits)("parents") + (originalTextFor(class_body)("body")))#Definition
    Grammer = Grammer.ignore(scoped_enum)#See above on scoped_enum
    return Grammer
  
def STLGrammer():#Smart pointers, vectors, maps, auto, and raw pointers all in two definitions. It's a bargain!
    from pyparsing import alphas, alphanums, CaselessLiteral, CaselessKeyword, Char, Word, Suppress, FollowedBy, Optional
    cppName = Suppress(Word(alphas+'_', alphanums+':_,') + ~Word('\n'))
    ptr_grammer = CaselessLiteral('unique_ptr')| CaselessLiteral('shared_ptr') | CaselessLiteral('make_shared') | CaselessLiteral('make_unique') | cppName + ~Char('>') + Char('*') + cppName| cppName + ~Char('>') + Char('&') + cppName
    vec_grammer = CaselessLiteral('vector') + FollowedBy(Char('<')) | CaselessLiteral('vector') + FollowedBy(Char('<') + Optional('std::') + CaselessLiteral('vector')) | CaselessLiteral('map') + FollowedBy(Char('<')) | CaselessKeyword('auto')
    return ptr_grammer, vec_grammer

class DevProject:#This class represents a single Software Development II project.
    def __init__(self, directory):
        self.__directory = directory#Project dir
        self.__files, self.__header_files = self.readFiles()#Get the File objects that represent files
        self.__results = []#List of results
        self.classes = []#Classes in project
        self.inheritances = []#public inheritance
        self.abstr_base_classes = []#names of ABC's
        self.abc_used = []#Were the ABC's referenced in the code?
        self.overrides = 0#Flag for numer of override used in code
    def __repr__(self):
        return str(self.__directory)#python stuff
    def readFiles(self):#Gets the contents of the source code files in the game-source-code directory
        files = []
        h_files = []#header files
        for filename in os.listdir(self.__directory):
            if filename.endswith(".h") or filename.endswith(".cpp"):
                x = File(self.__directory,filename)#Create a File object
                files.append(x)
                if filename.endswith(".h"):
                    h_files.append(x)
        return files, h_files
    def getFiles(self, index = 'ALL'):#Getter function
        files = []
        if len(self.__files):
            files = self.__files if index == 'ALL' else self.__files[index]
        return files
    def getFileContents(self, index = 'ALL'):#Get string of file contents at the index (alphabetical order) or all.
        if index == 'ALL':
            contents = ''
            for cont in self.__files:
                contents+=(cont.getContents())
        else:
            contents = self.__files[index].getContents()
        return contents
    def getHeaderContents(self):#Same as above except for header files.
        contents = ''
        for cont in self.__header_files:
            contents += cont.getContents()
        return contents
    def readFileResults(self):#Get results for the project. Old name, but can't change now.
        cpp_class = classGrammer()
        classes = cpp_class.searchString(self.getHeaderContents())
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
    def readResults(self):#These two functions could have been merged, but I didn't want to break working code.
        ptr_grammer, vec_grammer = STLGrammer()
        self.readFileResults()
        results = []
        for keyword in keywords:
            if keyword == 'vector':
                inst = vec_grammer.searchString(self.getFileContents()).asList()
                count = inst.count(['vector']) + inst.count(['map'])
                use_cases = [inst.count(['vector']), inst.count(['map']), inst.count(['auto'])]
                res = Result('STL',count)
                res.setUseCases(use_cases)
                results.append(res)
            elif keyword == 'pointers':
                inst = ptr_grammer.searchString(self.getFileContents()).asList()
                count = len(inst)
                shared_ptr =  inst.count(['shared_ptr']) + inst.count(['make_shared'])
                unique_ptr = inst.count(['unique_ptr']) + inst.count(['make_unique'])
                raw_ptr = inst.count(['*']) + inst.count(['&'])
                use_cases = [shared_ptr, unique_ptr, raw_ptr]
                res = Result('pointers', count, inst)
                res.setUseCases(use_cases)
                results.append(res)
            else:
                grammer = makeGrammer(keyword)
                inst = grammer.searchString(self.getFileContents())
                count = len(inst)
                res = Result(keyword,count,inst.asList())
                results.append(res)
        self.__results = results
    def getResults(self):#Getter
        return self.__results

class File:#A class that was intended to have results for each file. Now has contents only.
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

class Result:#Results of analysis in the form of vectors and lists. Will be used in AnalyseProject to turn them into usable data.
    def __init__(self, keyword, count, inst = []):
        self.__keyword = keyword
        self.__count = count#number of instances of use
        self.__inst = inst#the actual instances of use returned from pyparsing
        # 0 is functions ([]), 1 is args (["("]) and [","], and 2 is vars ";" for static. for others 0 and 2 are swapped. most return [].
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

class cppClass:#A class that represents a C++ class. It performs analysis on a class after it is parsed.
    def __init__(self, parseRes):
        temp = parseRes
        c_function, virtual_function, override_func = functionGrammer()
        self.name = temp.name
        self.parents = temp.parents.asList() if temp.parents else []#If no parents it's empty
        self.body = temp.body
        self.functions = c_function.searchString(self.body).asList()
        self.abstr_functions = virtual_function.searchString(self.body).asList()
        self.override_functions = override_func.searchString(self.body).asList()
        
        self.inheritance = 1 if self.parents else 0
        self.abstr_base_class = 1 if (len(self.functions)==len(self.abstr_functions) and len(self.functions) != 0) else 0
        self.override = 1 if (len(self.override_functions) != 0) else 0