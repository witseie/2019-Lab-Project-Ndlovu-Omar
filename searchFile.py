import os
from pyparsing import *
import matplotlib.pyplot as plt

def searchFileGrammer(file_or_filename, grammer):
        """
        Execute the keyword (string) search on the given file or filename.
        If a filename is specified (instead of a file object),
        the entire file is opened, read, and closed before parsing.
        May be called with optional
        ``maxMatches`` argument, to clip searching after 'n' matches are found.        
        """
        try:
            file_contents = file_or_filename.read()
        except AttributeError:
            with open(file_or_filename, "r") as f:
                file_contents = f.read()
        try:
            return grammer.searchString(file_contents)
        except ParseBaseException as exc:
            if ParserElement.verbose_stacktrace:
                raise
            else:
                # catch and re-raise exception from here, clears out pyparsing internal stack trace
                raise exc

def makeGrammer(string):
    cppName = alphanums + ':_()<>'
    if string != 'const':
        keyword = Optional(Char(',')) + Optional(CaselessKeyword("const")) + CaselessKeyword(string) | Optional(Char('(')) + Optional(CaselessKeyword("const")) + CaselessKeyword(string)
    else:
        keyword = Optional(Char(',')) + CaselessKeyword(string) | Optional(Char('(')) + CaselessKeyword(string)
    name =  Word(cppName) + Optional(Word(cppName))
    Grammer = keyword + Char("{") | keyword + Char(";") | keyword + name
    Grammer = Grammer.ignore(cppStyleComment)
    return Grammer

def searchFile(file_or_filename, string):
        """
        Execute the keyword (string) search on the given file or filename.
        If a filename is specified (instead of a file object),
        the entire file is opened, read, and closed before parsing.
        May be called with optional
        ``maxMatches`` argument, to clip searching after 'n' matches are found.        
        """
        try:
            file_contents = file_or_filename.read()
        except AttributeError:
            with open(file_or_filename, "r") as f:
                file_contents = f.read()
        try:
            return OneOrMore(CaselessKeyword(string).ignore(cppStyleComment)).searchString(file_contents)
        except ParseBaseException as exc:
            if ParserElement.verbose_stacktrace:
                raise
            else:
                # catch and re-raise exception from here, clears out pyparsing internal stack trace
                raise exc
def checkKeywords(file_or_filename, string):
    """
    Returns the number of occurances of a keyword in a given file or filename.
    """
    output = searchFile(file_or_filename, string)
    return len(output)

def plot(x,y):
    plt.bar(x,y,width = 0.5,label = "Keywords")
    plt.legend()
    plt.xlabel('keyword')
    plt.ylabel('count')
    plt.title('Keyword Occurences')
    plt.show()
    
keywords = ['const','class','enum','bool', 'vector']
#
directory = "D:\Ashraf\Documents\.University_Stuff\.4th Year\ELEN4012 - Lab Project\Parsing\Source Code"

x = []
use_cases =[]
for keyword in keywords:
#for file in files:
    count = 0
    for filename in os.listdir(directory):
        #print('Checking file: ' + filename)
        file = directory+os.sep+filename
        #count += checkKeywords(file,keyword)
        y = searchFileGrammer(file,makeGrammer(keyword))
        print(y)
        use_cases.append(y)
        count += len(y)
    x.append(count)
    print('Instances of use of ' + keyword + ' keyword: ' + str(count))
plot(keywords,x)

