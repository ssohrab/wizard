import re
import sys
import market.urlutil as util
from collections import OrderedDict

REGEX_FOR_EACH_SYMBOL = "[A-Za-z]+"
REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS = '>[A-Z]+:[A-Z]+<'
REGEX1_FOR_BETA_FROM_TMX = ">Beta:</td>\s*<td.*>\d\.\d*</td>"
REGEX2_FOR_BETA_FROM_TMX = "\d+\.*\d+"
REGEX1_FOR_VOLUME = ">[\d,]+</[tdTD]{2}>"
REGEX2_FOR_VOLUME = "[\d,]+"

BASE_URL_YAHOO_EOD = "http://ichart.yahoo.com/table.csv"
BASE_URL_YAHOO_INTRADAY = "http://download.finance.yahoo.com/d/quotes.csv"
BASE_URL_TMX = "http://web.tmxmoney.com/quote.php?qm_symbol="
BASE_URL_ALLPENNYSTOCKS_TSV = "http://www.allpennystocks.com/aps_ca/hot_tsxv_stocks.asp"

yahooToTMXMap = {".V":":TSV", ".TO":":TSX"}

def convertFromYahooToTMXSymbol(symbol):
    tokens = symbol.split('.')
    tmxSuffix = yahooToTMXMap['.' + tokens[1]]
    resultSymbol = tokens[0] + tmxSuffix
    
    return resultSymbol

'''
 @summary: Convenience method for reading the entire CSV file at once

 @return: string containing the whole text file
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


def extractSymbolsFromWebsite(url, regex1, regex2, suffix, encoding='iso-8859-1'):
    '''
     @summary: This method can be used to get all equity symbols from tabulated data, using the given regex.
     
     @param url: website from which to get the symbols
     @param regex1: how to find all the symbol groups in the HTML document
     @param regex2: how to find individual symbols within the group
     @param suffix: this is needed for some cases such as Yahoo's symbol lookup. i.e. ".V", ".TO"
     
     @return: An array which contains all the symbols found. i.e. ["BB", "AAPL", ...]
    '''
    theURLData = util.fetchPlainTextContentFromURL(url, encoding)
    
    retResult = extractSymbolFromHTMLString(theURLData, regex1, regex2, suffix)
    
    print(retResult)
    
    return retResult


def extractSymbolFromHTMLString(htmlString, regex1, regex2, suffix):
    tokens = re.findall(regex1, htmlString)
    
    compiledReg = re.compile(regex2)
    
    i=0
    for token in tokens:
        token = compiledReg.search(token).group() + suffix
        tokens[i] = token
        i += 1
    
    return tokens

'''
 @return: A dictionary i.e. {"BB.TO":<volume>,....}
'''
def extractSymbolsAndVolumesFromWebsite(url, regEx1Vol, regEx2Vol, regEx1Sym, regEx2Sym, encoding="utf-8"):
    result = OrderedDict([])
    theURLData = util.fetchPlainTextContentFromURL(url, encoding)

    symbolsArray = extractSymbolFromHTMLString(theURLData, regEx1Sym, regEx2Sym, ".V")
    
    allTDVolumes = re.findall(regEx1Vol, theURLData)
    
    compiledRegEx = re.compile(regEx2Vol)
    
    i = 0
    for sym in symbolsArray:
        valueWithComma = compiledRegEx.search(allTDVolumes[i]).group()
        valueAsInt = int(re.sub("[,]", "", valueWithComma))
        result[sym] = valueAsInt
        i += 1
    
    return result

def extractBetaForSymbol(url, symbol, regEx1, regEx2, encoding="ISO-8859-1"):
    print("Beta URL: " + url + symbol)
    data = util.fetchPlainTextContentFromURL(url + symbol, encoding)

    res = re.search(regEx1, data)
    
    if (res == None):
        return 'NaN'
    
    res = res.group()
    value = re.search(regEx2, res).group()

    return value

'''
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
    __infoToFetch = None # Must be a dictionary
    __getAllData = True
    __providerFullURL = ""
    __SYMBOL_INDEX = 0
    __BASE_URL_INDEX = 1
    __INFO_TO_FETCH_INDEX = 2
    YAHOO_QUOTE_PROPERTY_MAP = OrderedDict([("ask", "a"), ("avg_daily_volume", "a2"), ("bid", "b"),
                                            ("change", "c1"), ("percent_change","p2"), ("day_high","h"),
                                            ("day_low","g"), ("last_trade","l1"), ("last_trade_size","k3"), ("last_trade_date","d1"),
                                            ("last_trade_time","t1"),("name","n"), ("open","o"), ("year_high","k"), ("year_low","j")])
    
    '''
    ' dataType: 0 for intraday, 1 for EOD data
    '''
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
            self.__providerFullURL = self.__constructFullURLForIntradayData()
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
            keys = self.YAHOO_QUOTE_PROPERTY_MAP.keys()
            
            for k in keys:
                f += self.YAHOO_QUOTE_PROPERTY_MAP[k]
        else:
            # Use __infoToFetch
            keys = self.__infoToFetch.keys()
            
            for k in keys:
                f += self.__infoToFetch[k]
        
        result = self.__baseURL + "?s=" + self.__symbol + "&f=" + f + "&e=.csv"
        
        return result
    
    def __constructFullURLForEODData(self):
        #http://ichart.yahoo.com/table.csv
        a = str(int(self.__fromDate[0]) - 1) # Month
        b = self.__fromDate[1] # Day
        c = self.__fromDate[2] # Year
        
        d = str(int(self.__toDate[0]) - 1) # Month
        e = self.__toDate[1] # Day
        f = self.__toDate[2] # Year
        
        g = self.__interval
        
        result = self.__baseURL + "?s=" + self.__symbol + "&a=" + a + "&b=" + b + "&c="  + c + "&d=" + d + "&e=" + e + "&f=" + f + "&g=" + g + "&ignore=.csv"
        
        return result

    '''
     @summary: This method returns the all information specified in __YAHOO_QUOTE_PROPERTY_MAP or what user provides.
     
     @return: A dictionary which would contain the same keys as asked by the user and values that were obtained from Yahoo 
    '''
    def getIntraDayData(self):
        retResult = OrderedDict([])
        providerData = util.fetchPlainTextContentFromURL(self.__providerFullURL)
        
        # providerData is in CSV format. Number of elements in providerData should match number of items in __YAHOO_QUOTE_PROPERTY_MAP
        providerDataTokens = providerData.split(",")
        
        if (self.__getAllData):
            keys = self.__YAHOO_QUOTE_PROPERTY_MAP
        else:
            keys = self.__infoToFetch
        
        
        if (len(keys) != len(providerDataTokens)):
            print("Something went wrong")
            return {}

        i = 0
        for k in keys:
            retResult[k] = providerDataTokens[i].strip()
            i += 1
        
        return retResult
    
    def getEODData(self):
        #http://ichart.yahoo.com/table.csv?s=BAS.DE&a=0&b=1&c=2000 &d=0&e=31&f=2010&g=w&ignore=.csv
        print('Request URL = ' + self.__providerFullURL)
        providerData = util.fetchPlainTextContentFromURL(self.__providerFullURL)

        if (providerData == ''):
            return {}
        
        return dictizeCSVData(providerData)
