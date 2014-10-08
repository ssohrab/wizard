
import sys

'''
' Convenience method for reading the entire CSV file at once
'
' return: string containing the whole text file
'''
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
' regex: how to find the symbols in the HTML document
'
' return: an array which contains all the symbols found.
'''
def extractSymbolsFromWebsite(url, regex):
    