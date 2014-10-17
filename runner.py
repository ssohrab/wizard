import re
import sys
import runner
import threading
import market.urlutil as url
import market.parser as parser


COMMAND_TYPE_INDEX = 0
FUNCTION_INFO_INDEX = 1
FUNCTION_NAME_INDEX = 0
FUNCTION_ARGS_INDEX = 1

'''
' This convenience class allows a method of any instantiated object to run in a separate thread.
'''
class MethodThread(threading.Thread):
    __object = None
    __methodName = ""
    __methodArgs = None
    
    '''
    ' @obj: The instansiated object
    ' @methodName: Name of the method to be called
    ' @methodArgs: A tuple containing parameters to be passed to the method to be called
    '''
    def __init__(self, obj, methodName, methodArgs=None):
        threading.Thread.__init__(self)
        self.__object = obj
        self.__methodName = methodName
        self.__methodArgs = methodArgs

    def run(self):
        if (self.__methodArgs == None):
            print(self.__object)
            getattr(self.__object, self.__methodName)()
        else:
            getattr(self.__object, self.__methodName)(self.__methodArgs)


# symbols = parser.extractSymbolsFromWebsite("http://www.allpennystocks.com/aps_ca/hot_tsxv_stocks.asp",
#                                  equtil.REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS,
#                                  equtil.REGEX_FOR_EACH_SYMBOL,
#                                  "iso-8859-1", ".V")
# print(len(symbols))

# parser.extractSymbolsAndVolumesFromWebsite("http://www.allpennystocks.com/aps_ca/hot_tsxv_stocks.asp",
#                                            ">[\d,]+</[tdTD]{2}>", "[\d,]+", parser.REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS, parser.REGEX_FOR_EACH_SYMBOL, "iso-8859-1")



def getIntraDayDataForSymbol(args):
    if (args[0] == "Yahoo"):
        print("calling getIntraDayData")
        dp = parser.YahooDataProvider(0, args[1], args[2])
        mt = MethodThread(dp, "getIntraDayData")
        mt.start()

def getEODDataForSymbol(args):
    if (args[0] == "Yahoo"):
        symbol = args[1]
        baseURL = args[2]
        fromDate = args[3].split(",")
        toDate = args[4].split(",")
        interval = args[5]
        
        dp = parser.YahooDataProvider(1, symbol, baseURL, fromDate, toDate, interval)
        mt = MethodThread(dp, "getEODData")
        mt.start()
        

while True:
    userInput = input("Enter a command:\n")
    
    if(userInput == "exit"):
        print("Goodbye!\n")
        sys.exit()
    else:
        userInputTokens = userInput.split(">")
        print(userInputTokens)
        if (len(userInputTokens) == 2):
            commandType = userInputTokens[COMMAND_TYPE_INDEX]

            if(commandType == "fn"):
                # Get the function name and its args
                functionTokens = userInputTokens[FUNCTION_INFO_INDEX].split(";")
                functionName = functionTokens[FUNCTION_NAME_INDEX]
                functionArgs = functionTokens[FUNCTION_ARGS_INDEX]
                print("You are trying to call function " + functionName + " with args: " + functionArgs)
                getattr(runner, functionName)(functionArgs.split(" "))
                
                #fn>getIntraDayDataForSymbol;Yahoo BB.TO http://download.finance.yahoo.com/d/quotes.csv (intraday example)
                #fn>getEODDataForSymbol;Yahoo BB.TO http://ichart.yahoo.com/table.csv 9,6,2014 9,13,2014 d (EOD example)
                

