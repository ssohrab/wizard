
REGEX_FOR_EACH_SYMBOL = "[A-Za-z]+"
REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS = '>[A-Z]+:[A-Z]+<'


class DataProvider:
    test = "test"
    __providerName = ""
    __providerBaseURL = ""
    __infoToFetch = ["symbol", "day_open", "day_close"]
    
    '''
    ' This method uses __infoToFetch to build the needed query parameter for the specific data provider
    ' and return a dictionary containing the same keys as in __infoToFetch with their corresponding values.
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


class YahooDataProvider(DataProvider):
    def __init__(self):
        pass
