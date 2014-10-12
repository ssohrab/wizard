import re
import sys
import runner
import market.urlutil
import market.parser as parser
import market.equityutil as util

COMMAND_TYPE_INDEX = 0
FUNCTION_INFO_INDEX = 1
FUNCTION_NAME_INDEX = 0
FUNCTION_ARGS_INDEX = 1

# symbols = parser.extractSymbolsFromWebsite("http://www.allpennystocks.com/aps_ca/hot_tsxv_stocks.asp",
#                                  equtil.REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS,
#                                  equtil.REGEX_FOR_EACH_SYMBOL,
#                                  "iso-8859-1", ".V")
# print(len(symbols))


while True:
    userInput = input("Enter a command:\n")
    
    if(userInput == "exit"):
        print("Goodbye!\n")
        sys.exit()
    else:
        userInputTokens = userInput.split(":")
        if (len(userInputTokens) == 2):
            commandType = userInputTokens[COMMAND_TYPE_INDEX]
            if(commandType == "fn"):
                # Get the function name and its args
                functionTokens = userInputTokens[FUNCTION_INFO_INDEX].split(";")
                functionName = functionTokens[FUNCTION_NAME_INDEX]
                functionArgs = functionTokens[FUNCTION_ARGS_INDEX]
                print("You are tring to call function " + functionName + " with args: " + functionArgs)
                getattr(runner, functionName)(functionArgs)
                
