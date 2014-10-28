import re
import sys
import runner
import threading
import market.urlutil as url
import market.parser as parser
import market.equityutil as eq


COMMAND_TYPE_INDEX = 0
FUNCTION_INFO_INDEX = 1
FUNCTION_NAME_INDEX = 0
FUNCTION_ARGS_INDEX = 1

'''
' This convenience class allows a method of any instantiated object to run in a separate thread.
'''
class MethodThread(threading.Thread):
    object = None
    methodName = ""
    methodArgs = None
    
    '''
    ' @obj: The instansiated object
    ' @methodName: Name of the method to be called
    ' @methodArgs: A tuple containing parameters to be passed to the method to be called
    '''
    def __init__(self, obj, methodName, *methodArgs):
        threading.Thread.__init__(self)
        self.object = obj
        self.methodName = methodName
        self.methodArgs = methodArgs

    def run(self):
        if (self.methodArgs == None):
            getattr(self.object, self.methodName)()
        else:
            stringToExecute = 'getattr(self.object, self.methodName)'
            
            arguments = ""
            for i in range(0, len(self.methodArgs)):
                arguments += ',self.methodArgs[' + str(i) + ']'
            

            arguments = '(' + arguments[1:] + ')'
            
            stringToExecute += arguments
            
            print('stringToExecute = ' + stringToExecute)
            
            exec(stringToExecute)

def extractSymbolsFromWebsite(args):
    #url, regex1, regex2, suffix
    url = args[0]
    regEx1 = args[1]
    regEx2 = args[2]
    suffix = ''
    
    mt = MethodThread(parser, 'extractSymbolsFromWebsite', url, regEx1, regEx2, suffix)
    mt.start()


def getStatsForSymbols(args):
    symbols = args[0]
    fromDate = args[1]
    toDate = args[2]
    interval = 'd'
    
    # Interval is optional
    if (len(args) == 4):
        interval = args[3]
    
    mt = MethodThread(eq, 'getStatsForSymbols', symbols.split(','), fromDate.split(','), toDate.split(','), interval)
    mt.start()


def getIntraDayDataForSymbol(args):
    if (args[0] == "Yahoo"):
        dp = parser.YahooDataProvider(0, args[1], args[2])
        mt = MethodThread(dp, "getIntraDayData", None)
        mt.start()

def getEODDataForSymbol(args):
    if (args[0] == "Yahoo"):
        symbol = args[1]
        baseURL = args[2]
        fromDate = args[3].split(",")
        toDate = args[4].split(",")
        interval = args[5]
        
        dp = parser.YahooDataProvider(1, symbol, baseURL, fromDate, toDate, interval)
        mt = MethodThread(dp, "getEODData", None)
        mt.start()

def getStatsForSymbolsOnPage(args):
    url = args[0]
    regex1 = args[1]
    regex2 = args[2]
    fromDate = args[3]
    toDate = args[4]
    interval = args[5]
    
    print('Starting thread...')
    
    mt = MethodThread(eq, "getStatsForSymbolsOnPage", url, regex1, regex2, fromDate, toDate, interval)
    mt.start()

while True:
    userInput = input("Enter a command:\n")
    
    userInput = userInput.strip()
    
    if(userInput == "exit"):
        print("Goodbye!\n")
        sys.exit()
    else:
        userInputTokens = userInput.split(">")
        
        if (len(userInputTokens) == 2):
            commandType = userInputTokens[COMMAND_TYPE_INDEX].strip()

            if(commandType == "fn"):
                # Get the function name and its args
                functionTokens = userInputTokens[FUNCTION_INFO_INDEX].split(";")
                functionName = functionTokens[FUNCTION_NAME_INDEX].strip()
                functionArgs = functionTokens[FUNCTION_ARGS_INDEX].strip()
                print("You are trying to call function " + functionName + " with args: " + functionArgs)
                getattr(runner, functionName)(functionArgs.split(" "))
                
                #fn>getIntraDayDataForSymbol;Yahoo BB.TO http://download.finance.yahoo.com/d/quotes.csv (intraday example)
                #fn>getEODDataForSymbol;Yahoo BB.TO http://ichart.yahoo.com/table.csv 9,6,2014 9,13,2014 d (EOD example)
                #fn>getStatsForSymbols;SIO.V,BB.TO 10,1,2014 10,20,2014
                #fn>getStatsForSymbolsOnPage;http://www.allpennystocks.com/aps_ca/hot_tsxv_stocks.asp [A-Z]+:[A-Z]+< [A-Za-z]+ 10,6,2014 10,20,2014 d

