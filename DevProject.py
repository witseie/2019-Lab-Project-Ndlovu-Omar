# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 08:13:01 2019

@author: Ashraf
"""
from pyparsing import *
import os
import matplotlib.pyplot as plt
keywords = ['const','class','bool','vector']

def makeGrammer(string):
    keyword = CaselessKeyword(string) + (Optional(FollowedBy("&"))^Optional(FollowedBy("*")))
    value = Suppress('=' + Word(printables))
    datatype = Word(alphas) + (Optional(FollowedBy("&"))^Optional(FollowedBy("*")))
    name = (Optional("&")^Optional("*")) + Word(printables)# + Optional(FollowedBy("("))
    
    Grammer = keyword + name + (Optional(FollowedBy(","))^Optional(FollowedBy(")"))) + Optional(value) + Optional(";")
    Grammer = Grammer.ignore(cppStyleComment)
    return Grammer

def plot(x,y):
    plt.bar(x,y,width = 0.5,label = "Keywords")
    plt.legend()
    plt.xlabel('Keyword')
    plt.ylabel('No. of Occurances')
    plt.title('Keyword Occurences')
    plt.show()

class DevProject:
    def __init__(self, directory):
        self.__directory = directory
        self.__files = self.readFiles()
        self.__results = self.readResults()
    def __repr__(self):
        return str(self.__directory)
    def readFiles(self):
        files = []
        for filename in os.listdir(self.__directory):
            x = File(self.__directory,filename)
            files.append(x)
        return files
    def getFiles(self, index = 'ALL'):
        if index == 'ALL':
            f = self.__files
        else: 
            f = self.__files[index]
        return f
    def getFileContents(self, index = 'ALL'):
        if index == 'ALL':
            contents = []
            for cont in self.__files:
                contents.append(cont.getContents())
        else:
            contents = self.__files[index].getContents()
        return contents
    def readResults(self):
        results = []
        idx = 0
        for keyword in keywords:
            count = 0
            for file in self.__files:
                count += file.getResults(idx).getCount()
            res = Result(keyword,count)
            results.append(res)
            idx+=1
        return results
    def getResults(self):
        return self.__results
        
class File:
    def __init__(self,directory,name):
        self.__name = name
        self.__directory = directory
        self.__contents = self.readContents()
        self.__results = self.readResults()
    def __repr__(self):
        return str(self.__name)
    def readContents(self):
        filename = self.__directory + os.sep + self.__name
        try:
            file_contents = filename.read()
        except AttributeError:
            with open(filename, "r") as f:
                file_contents = f.read()
        return file_contents
    def readResults(self):
        results = []
        for keyword in keywords:
            grammer = makeGrammer(keyword)
            inst = grammer.searchString(self.__contents)
            count = len(inst)
            res = Result(keyword,count,inst)
            results.append(res)
        return results
    def getName(self):
        return str(self.__name)
    def getContents(self):
        return str(self.__contents)
    def getResults(self, index = 'ALL'):
        if index == 'ALL':
            res = self.__results
        else: 
            res = self.__results[index]
        return res

class Result:
    def __init__(self, keyword, count, inst = []):
        self.__keyword = keyword
        self.__count = count
        self.__instances = inst
    def setInst(self,inst):
        self.__instances = inst
        self.__count = len(inst)
    def getCount(self):
        return self.__count
    def getInst(self):
        return self.__instances
    def printResult(self):
        string = 'Instances of use of ' + self.__keyword + ' keyword: ' + str(self.__count)
        print(string)
#For testing purposes:
a = DevProject('D:\Ashraf\Documents\.University_Stuff\.4th Year\ELEN4012 - Lab Project\Parsing\Source Code')
#print('\n')
#for file in x.getFiles():
#    print(file.getName()+'\n')
#    for result in file.getResults():
#        result.printResult()
print('\n')
y = []   
for result in a.getResults():
    y.append(result.getCount())
    result.printResult()
plot(keywords,y)