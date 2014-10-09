
REGEX_FOR_EACH_SYMBOL = "[A-Za-z]+"
REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS = '>[A-Z]+:[A-Z]+<'


class DataProvider:
    test = "test"
    __providerName = ""
    __providerFullURL = ""
    __infoToFetch = ["symbol", "day_open", "day_close"]
    
    '''
    ' This method uses __infoToFetch to build the needed query parameter for the specific data provider
    ' and return a dictionary containing the same keys as in __infoToFetch with their corresponding values.
    '
    ' return: i.e. {"symbol":"BB.TO", "day_open":5.0, ...}
    '''
    def extractInfo(self):
        pass
    
    '''
    ' This method is specific to the the data provider. Every provider would give access to different financial data
    ' in different format.
    '''
    def extractFinancialData(self):
        pass
    
    def getDefaultInfoArray(self):
        return self.__infoToFetch

    def extractHistoricalDataForSymbols(self):
        pass

class YahooDataProvider(DataProvider):
    # http://download.finance.yahoo.com/d/quotes.csv?s=GOOG&f=nsl1op&e=.csv
    __baseURL = ""

    def __init__(self, baseURL):
        self.__baseURL = baseURL

    def __constructFullURL(self):
        
class Task:
    __parameters = ""
    __methodNameToCall = ""

    def __init__(self, methodName, parameters):
        
        