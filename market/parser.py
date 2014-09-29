
import sys

'''
' This method returns a tuple that contains records which match the given column KVP
' Using Dictionary for NVP. e.g. {"Symbol": "BB.TO"}
'''
def extractRecords (fileData, columnNVP):
    result = []
    allMatch = True

    columnIVP = convertNVP2IVP(columnNVP)

    for line in fileData:
        allMatch = True
        lineTokens = line.split(",")
        if (lineTokens):
            for key in columnIVP.keys():
                #print ("value1 = " + lineTokens[key] + ", value2 = " + columnIVP[key])
                if (lineTokens[key] != columnIVP[key]):
                    allMatch = False
                    break

            if (allMatch == True):
                result.append(line)

    return result



'''
' Convenience method for reading the entire CSV file at once
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
' Helper method to get column index by name, from a csv column header row
'''
def getColumnIndexByName(csvData, columnName):
    line = csvData[0]
    
    headersList = line.split(",")
    
    headersList.index(columnName)

    return headersList.index(columnName)

'''
' Helper method, because Python decides to throw an exception as opposed to returning -1 when an element does not exist.
'''
def elementExists(aList, theElement):
    try:
        aList.index(theElement)
        return True
    except ValueError:
        return False

def convertNVP2IVP(theDictionary):
    result = {}
    keys = theDictionary.keys()

    for columnName in keys:
        index = getColumnIndexByName(columnName)
        result.update({index:theDictionary[columnName]})

    return result



