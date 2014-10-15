import re
import sys
import market.parser
import market.equityutil
import market.urlutil as util
from collections import OrderedDict

REGEX_FOR_EACH_SYMBOL = "[A-Za-z]+"
REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS = '>[A-Z]+:[A-Z]+<'

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
' regex1: how to find all the symbol groups in the HTML document
' regex2: how to find individual symbols within the group
' suffix: this is needed for some cases such as Yahoo's symbol lookup. i.e. ".V", ".TO"
'
' return: an array which contains all the symbols found. i.e. ["BB", "AAPL", ...]
'''
def extractSymbolsFromWebsite(url, regex1, regex2, encoding, suffix):
    tsxvURLData = util.fetchPlainTextContentFromURL(url, encoding)

    tokens = re.findall(regex1, tsxvURLData)
    
    compiledReg = re.compile(regex2)
    
    i=0
    for token in tokens:
        token = compiledReg.search(token).group() + suffix
        tokens[i] = token
        i += 1
    
    return tokens

'''
' This function reads the given CSV data into a dictionary. i.e. {"Date":[ ], "Open":[ ], ...}
'''
def dictizeCSVData(data):
    result = {}
    
    rows = data.split("\n")
    
    # Read the first row to get the column names
    columnNamesRow = rows[0]
    
    columnNames = columnNamesRow.split(",")
    
    for name in columnNames:
        result[name] = []

    for row in rows[1:]:
        values = row.split(",")
        
        for i in range(0, len(values)):
            result[columnNames[i]].append(values[i])
    
    
    return result

class YahooDataProvider:
    # http://download.finance.yahoo.com/d/quotes.csv?s=GOOG&f=nsl1op&e=.csv
    __baseURL = ""
    __fromDate = [] # [month, day, year]
    __toDate = []
    __interval = ""
    __getAllData = True
    __providerFullURL = ""
    __SYMBOL_INDEX = 0
    __BASE_URL_INDEX = 1
    __INFO_TO_FETCH_INDEX = 2
    __YAHOO_QUOTE_PROPERTY_MAP = OrderedDict([("ask", "a"), ("ask_size", "a5"), ("avg_daily_volume", "a2"), ("bid", "b"),
                                              ("bid_size", "b6"), ("change", "c1"), ("percent_change","p2"), ("day_hight","h"),
                                              ("day_low","g"), ("last_trade","l1"), ("last_trade_size","k3"), ("last_trade_date","d1"),
                                              ("last_trade_time","t1"),("name","n"), ("open","o"), ("year_high","k"), ("year_low","j")])
    
    def __init__(self, dataType, *args):
        
        if (len(args) < 2):
            print("What are you trying to pull here asshole!")
            sys.exit()
        else:
            self.__symbol = args[self.__SYMBOL_INDEX]
            self.__baseURL = args[self.__BASE_URL_INDEX]

        if (len(args) == 2 and dataType == 0):
          self.__providerFullURL = self.__constructFullURLForIntradayData()  
        elif (len(args) == 3 and dataType == 0):
            self.__infoToFetch = args[self.__INFO_TO_FETCH_INDEX]
            self.__getAllData = False
            self.__parent.__providerFullURL = self.__constructFullURLForIntradayData()
        elif (len(args) == 5 and dataType == 1):
            self.__fromDate = args[2]
            self.__toDate = args[3]
            self.__interval = args[4]
            self.__providerFullURL = self.__constructFullURLForEODData()
        

    def __constructFullURLForIntradayData(self):
        f = ""
        result = ""

        if (self.__getAllData):
            # Use the map to get all the needed info
            keys = self.__YAHOO_QUOTE_PROPERTY_MAP.keys()
            
            for k in keys:
                f += self.__YAHOO_QUOTE_PROPERTY_MAP[k]
        else:
            # Use __infoToFetch
            keys = self.__infoToFetch.keys()
            
            for k in keys:
                f += self.__infoToFetch[k]
        
        result = self.__baseURL + "?s=" + self.__symbol + "&f=" + f + "&e=.csv"
        
        return result
    
    def __constructFullURLForEODData(self):
        #http://ichart.yahoo.com/table.csv?s=
        a = self.__fromDate[0] # Month
        b = self.__fromDate[1] # Day
        c = self.__fromDate[2] # Year
        
        d = self.__toDate[0] # Month
        e = self.__toDate[1] # Day
        f = self.__toDate[2] # Year
        
        g = self.__interval
        
        result = self.__baseURL + "?s=" + self.__symbol + "&a=" + a + "&b=" + b + "&c="  + c + "&d=" + d + "&e=" + e + "&f=" + f + "&g=" + g + "&ignore=.csv"
        
        return result

    '''
    ' This method returns the all information specified in __YAHOO_QUOTE_PROPERTY_MAP or what user provides.
    ' 
    ' @return: A dictionary which would contain the same keys as asked by the user and values that were obtained from Yahoo 
    '''
    def getIntraDayData(self):
        retResult = OrderedDict([])
        providerData = util.fetchPlainTextContentFromURL(self.__providerFullURL)
        
        # providerData is in CSV format. Number of elements in providerData should match number of items in __YAHOO_QUOTE_PROPERTY_MAP
        providerDataTokens = providerData.split(",")
        keys = self.__YAHOO_QUOTE_PROPERTY_MAP
        
        if (len(keys) != len(providerDataTokens)):
            print("Something went wrong")
            return {}

        i = 0
        for k in keys:
            retResult[k] = providerDataTokens[i]
            i += 1
        
        return retResult
    
    def getEODData(self):
        #http://ichart.yahoo.com/table.csv?s=BAS.DE&a=0&b=1&c=2000 &d=0&e=31&f=2010&g=w&ignore=.csv
        providerData = util.fetchPlainTextContentFromURL(self.__providerFullURL)
        print(self.__providerFullURL)
        print(providerData)
        print(dictizeCSVData(providerData)['Close'])
