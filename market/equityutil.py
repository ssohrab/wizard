'''
Created on Sep 28, 2014

@author: ssohrab
'''

import market.csvparser as parser

REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS = '>[A-Z]+:[A-Z]+<'

'''
' This method calculates the return on each trade using the simple formula of ((final - initial)/initial) * 100%.
' Dividends are not taken into account here
'''
def calculateTradesPerformance(nvp, symbolColumnName, valueColumnName):
    usedSymbols = []

    symbolColumnIndex = getColumnIndexByName(symbolColumnName)
    buyNVP = nvp.copy()
    buyNVP.update({"Action":"Buy"})
    sellNVP = nvp.copy()
    sellNVP.update({"Action":"Sell"})
    
    # In this case we are extracting all the trades.
    tradesList = extractRecords (nvp)

    for line in tradesList:
        lineTokens = line.split(",")

        if (elementExists(usedSymbols, lineTokens[symbolColumnIndex]) == False):
            usedSymbols.append(lineTokens[symbolColumnIndex])

            buyNVPForSymbol = buyNVP.copy()
            buyNVPForSymbol.update({symbolColumnName:lineTokens[symbolColumnIndex]})
            totalBuyValueForSymbol = sumValues(buyNVPForSymbol, valueColumnName)

            sellNVPForSymbol = sellNVP.copy()
            sellNVPForSymbol.update({symbolColumnName:lineTokens[symbolColumnIndex]})
            totalSellValueForSymbol = sumValues(sellNVPForSymbol, valueColumnName)
            
            change = ((abs(totalSellValueForSymbol) - abs(totalBuyValueForSymbol)) * 100.0)/abs(totalBuyValueForSymbol)
            print ("Symbol: %s, Bought = $%.2f, Sold = $%.2f, Percent change = %.2f" % (lineTokens[symbolColumnIndex], totalBuyValueForSymbol, totalSellValueForSymbol, change))

'''
' This method returns the sum
'''
def sumValues (csvRecords, kvp, valueColumnName):
    valuesSum = 0.0
    
    valueColumnIndex = getColumnIndexByName(valueColumnName)

    for line in csvRecords:
        # Get the value and accumulate
        value = line.split(",")[valueColumnIndex]
        valuesSum += float(value)

    return valuesSum

'''
' This method parses out data from the CSV input and returns a JSON object
' containing key-value-pairs.
' Format f=nsl1d1t1 => {"name":value, "symbol":value, "price":value, "date":value, "time":value}
'''
def parseEquityInfo(csvData):
    csvDataArray = csvData.split(',')
    name = csvDataArray[0][1:len(csvDataArray[0])-1]
    symbol = csvDataArray[1][1:len(csvDataArray[1])-1]
    price = csvDataArray[2]
    date = csvDataArray[3][1:len(csvDataArray[3])-1]
    time = csvDataArray[4][1:len(csvDataArray[4])-2]
    
    formattedString = '"name":"{0}", "symbol":"{1}", "price":{2}, "date":"{3}", "time":"{4}"'.format(name, symbol, price, date, time)
    
    result = "{" + formattedString + "}"
    
    return result  
