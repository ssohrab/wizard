import re
import sys
import market.urlutil as util
import market.csvparser as parser
import market.equityutil as equtil

#market.urlutil.fetchPlainTextContentFromURI("http://download.finance.yahoo.com/d/quotes.csv?s=GOOG&f=nsl1op&e=.csv")

#result = market.csvparser.parseStockData('"BLACKBERRY LIMITE","BB.TO",11.44,"9/26/2014","3:59pm"')

#print(result)

tsxvURLData = util.fetchPlainTextContentFromURL("http://www.allpennystocks.com/aps_ca/hot_tsxv_stocks.asp")
#print(urlData.encode("utf-8"))


compiledReg = re.compile(equtil.REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS)
tokens = compiledReg.findall(tsxvURLData)

compiledReg = re.compile(r"[A-Za-z]+")

i=0
for token in tokens:
    token = compiledReg.search(token).group() + ".V"
    tokens[i] = token
    i += 1

print(tokens)

#equtil.parseEquityInfo(tokens);

#print(tokens)

#str = "<a href='sdfsdf'>sfsf</a> <a href='test'>testingURL</a> "
#tokens = str.search("<a href=")
#compiledObj = re.compile(">.*</a>\s{1}?")
#filtered = compiledObj.findall(str)


#print(filtered)
#print(tokens[1])


#util.parseHTML(urlData)

'''
monitorStock = market.monitor.Monitor("http://download.finance.yahoo.com/d/quotes.csv?s=BB.TO&f=nsl1d1t1&e=.csv", 30)
monitorStock.start()
'''