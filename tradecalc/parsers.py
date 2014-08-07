
import sys

class DataExtractor:
    """This class contains utili methods to extract needed data from a CSV file."""

    # List of lines
    __fileData = []

    def __init__(self, filePath):
        self.filePath = filePath
        self.__populateFileData()

    '''
    ' This method returns a tuple that contains records which match the given column KVP
    ' Using Dictionary for NVP. e.g. {"Symbol": "BB.TO"}
    '''
    def extractRecords (self, columnNVP):
        result = []
        allMatch = True

        columnIVP = self.convertNVP2IVP(columnNVP)

        for line in self.__fileData:
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
    ' This method returns the sum
    '''
    def sumValues (self, kvp, valueColumnName):
        valuesSum = 0.0
        resultList = self.extractRecords (kvp)

        valueColumnIndex = self.getColumnIndexByName(valueColumnName)

        for line in resultList:
            # Get the value and accumulate
            value = line.split(",")[valueColumnIndex]
            valuesSum += float(value)

        return valuesSum

    '''
    ' Convenience method for reading the entire CSV file at once
    '''
    def __populateFileData(self):
        if (len(self.__fileData) != 0): return

        file = open(self.filePath, "r")

        if (file):
            self.__fileData = file.readlines() # Allow the file to be reloaded.
        else:
            print ("Failed to open the file: " + self.filePath)
            sys.exit(1)

    '''
    ' This method calculates the return on each trade using the simple formula of ((final - initial)/initial) * 100%.
    ' Dividends are not taken into account here
    '''
    def calculateTradesPerformance(self, nvp, symbolColumnName, valueColumnName):
        trade = []
        result = []
        usedSymbols = []
        symbolColumnIndex = self.getColumnIndexByName(symbolColumnName)
        buyNVP = nvp.copy()
        buyNVP.update({"Action":"Buy"})
        sellNVP = nvp.copy()
        sellNVP.update({"Action":"Sell"})
        
        # In this case we are extracting all the trades.
        tradesList = self.extractRecords (nvp)

        for line in tradesList:
            lineTokens = line.split(",")

            if (self.elementExists(usedSymbols, lineTokens[symbolColumnIndex]) == False):
                usedSymbols.append(lineTokens[symbolColumnIndex])

                buyNVPForSymbol = buyNVP.copy()
                buyNVPForSymbol.update({symbolColumnName:lineTokens[symbolColumnIndex]})
                totalBuyValueForSymbol = self.sumValues(buyNVPForSymbol, valueColumnName)

                sellNVPForSymbol = sellNVP.copy()
                sellNVPForSymbol.update({symbolColumnName:lineTokens[symbolColumnIndex]})
                totalSellValueForSymbol = self.sumValues(sellNVPForSymbol, valueColumnName)
                
                change = ((abs(totalSellValueForSymbol) - abs(totalBuyValueForSymbol)) * 100.0)/abs(totalBuyValueForSymbol)
                print ("Symbol: %s, Bought = $%.2f, Sold = $%.2f, Percent change = %.2f" % (lineTokens[symbolColumnIndex], totalBuyValueForSymbol, totalSellValueForSymbol, change))

    '''
    ' Helper method to get column index by name
    '''
    def getColumnIndexByName(self, columnName):
        line = self.__fileData[0]
        
        headersList = line.split(",")
        
        headersList.index(columnName)

        return headersList.index(columnName)

    '''
    ' Helper method, because Python decides to throw an exception as opposed to returning -1 when an element does not exist.
    '''
    def elementExists(self, aList, theElement):
        try:
            aList.index(theElement)
            return True
        except ValueError:
            return False

    def convertNVP2IVP(self, theDictionary):
        result = {}
        keys = theDictionary.keys()

        for columnName in keys:
            index = self.getColumnIndexByName(columnName)
            result.update({index:theDictionary[columnName]})

        return result