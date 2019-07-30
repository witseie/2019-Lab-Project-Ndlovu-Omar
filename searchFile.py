import sys
from pyparsing import *

def searchFile(file_or_filename, string, maxMatches=sys.maxsize):
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
            return OneOrMore(CaselessKeyword(string).ignore(cppStyleComment)).searchString(file_contents, maxMatches)
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
    
keywords = ['const','class','enum','enum class','bool','namespace','shared_ptr']
#
x = []
for keyword in keywords:
#for file in files:
    count = 0
    for filename in os.listdir(os.getcwd()):
    #print('Checking file: ' + filename)
        count += checkKeywords(filename,keyword)
    x.append(count)
    print('Instances of use of ' + keyword + ' keyword: ' + str(count))
plot(keywords,x)

