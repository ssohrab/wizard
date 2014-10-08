import re
import sys

'''
' Convenience method for reading the entire CSV file at once
'
' return: string containing the whole text file
'''
from market import urlutil, equityutil
from idlelib.IOBinding import encoding
def readTextFile(filePath):

    result = ""
    file = open(filePath, "r")

    if (file):
        result = file.readlines()
    else:
        print ("Failed to open the file: " + filePath)
        sys.exit(1)

    return result

'''
' This method can be used to get all equity symbols from tabulated data, using the given regex.
'
' url: website from which to get the symbols
' regex1: how to find all the symbol groups in the HTML document
' regex2: how to find individual symbols within the group
' suffix: this is needed for some cases such as Yahoo's symbol lookup. i.e. ".V", ".TO"
'
' return: an array which contains all the symbols found.
'''
def extractSymbolsFromWebsite(url, regex1, regex2, encoding, suffix):
    tsxvURLData = urlutil.fetchPlainTextContentFromURL(url, encoding)

    tokens = re.findall(regex1, tsxvURLData)
    
    compiledReg = re.compile(regex2)
    
    i=0
    for token in tokens:
        token = compiledReg.search(token).group() + suffix
        tokens[i] = token
        i += 1
    
    return tokens
    