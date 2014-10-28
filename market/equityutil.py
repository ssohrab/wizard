import time
import math
import statistics as stats
import market.parser as parser

'''
 @summary: This method goes through every symbols and obtains the following indicators for the time period and interval: Beta, Sharpe ratio, year low, year high, ...
 
 @param symbolsList: An array of symbols i.e. ['BB.TO', 'SIO.V', ...]
 @param fromDate: Format should be [month, day, year]
 @param toDate: Format should be [month, day, year]
 @param interval: d -> day, w -> week
 
 @return: i.e. {"BB.TO": [<beta>, <Sharpe ratio>, <year low>, <year high>], ...}
'''
def getStatsForSymbols(symbolsList, fromDate, toDate, interval='d'):
    result = {}
        
    for symb in symbolsList:
        print("Getting data for " + symb)
        
        dp = parser.YahooDataProvider(1, symb, parser.BASE_URL_YAHOO_EOD, fromDate, toDate, interval)
        eodData = dp.getEODData()
        
        dp = parser.YahooDataProvider(0, symb, parser.BASE_URL_YAHOO_INTRADAY,
                                      {"year_low":parser.YahooDataProvider.YAHOO_QUOTE_PROPERTY_MAP["year_low"],
                                       "year_high":parser.YahooDataProvider.YAHOO_QUOTE_PROPERTY_MAP["year_high"]})
        
        intradayInfo = dp.getIntraDayData()
        
        # Get the indicators
        print("Getting indicators for " + symb)
        
        tmxSymb = parser.convertFromYahooToTMXSymbol(symb)
        beta = parser.extractBetaForSymbol(parser.BASE_URL_TMX, tmxSymb, parser.REGEX1_FOR_BETA_FROM_TMX, parser.REGEX2_FOR_BETA_FROM_TMX)
        
        sharpeRatio = 'NaN'
        if (len(eodData) > 0 and len(eodData['Adj Close']) >= 3):
            sharpeRatio = calculateSharpeRatio(eodData['Adj Close'], 0)
        
        yearLow = intradayInfo["year_low"]
        yearHigh = intradayInfo["year_high"]
        
        # Put all the data in result
        result[symb] = {"Beta": beta, "Sharpe_Ratio": sharpeRatio, "Year_Low": yearLow, "Year_High": yearHigh}
        
        # Don't hit the server too often too fast
        time.sleep(2)
        
    
    print(result)
    
    return result

def calculateSharpeRatio(inputPrices, riskFreeRate, k=250):
    # First calculate return
    returns = []
    for i in range(1, len(inputPrices)):
        singleReturn = float(inputPrices[i])/float(inputPrices[i-1]) - 1
        returns.append(singleReturn)
    
    # Find mean and std
    meanReturn = stats.mean(returns)
    stdOfReturn = stats.stdev(returns)
    
    # Calculate the Sharpe ratio using formula:
    if (stdOfReturn == 'NaN' or stdOfReturn == 0):
        return 'NaN'
    
    theSharpeRatio = math.sqrt(k) * ((meanReturn - riskFreeRate)/stdOfReturn)
    
    return theSharpeRatio

def getStatsForSymbolsOnPage(url, regex1, regex2, fromDate, toDate, interval='d'):
    print('Calling extractSymbolsFromWebsite')
    symbols = parser.extractSymbolsFromWebsite(url, regex1, regex2, '.V')
    
    print(symbols)
    
    retResult = getStatsForSymbols(symbols, fromDate.split(','), toDate.split(','), interval)
    
    return retResult
