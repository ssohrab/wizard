import math
import statistics as stats
import market.parser as parser
from market.parser import YahooDataProvider

'''
 @summary: This method goes through every symbols and obtains the following indicators for the time period and interval: Beta, Sharpe ratio, year low, year high, ...
 
 @param symbolsList: 
 @param fromDate: Format should be [month, day, year]
 @param toDate: Format should be [month, day, year]
 @param interval: d -> day, w -> week
 
 @return: i.e. {"BB.TO": [<beta>, <Sharpe ratio>, <year low>, <year high>], ...}
'''
def recommendFromSymbols(symbolsList, fromDate, toDate, interval):
    dp = YahooDataProvider(1, symb, parser.BASE_URL_YAHOO_EOD, fromDate, toDate, "d")
    pass

def calculateSharpeRatio(inputPrices, riskFreeRate, k=250):
    # First calculate return
    returns = []
    for i in range(1, len(inputPrices)):
        singleReturn = inputPrices[i]/inputPrices[i-1] - 1
        returns.append(singleReturn)
    
    # Find mean and std
    meanReturn = stats.mean(returns)
    stdOfReturn = stats.stdev(returns)
    
    # Calculate the Sharpe ratio using formula:
    theSharpeRatio = math.sqrt(k) * ((meanReturn - riskFreeRate)/stdOfReturn)
    
    return theSharpeRatio