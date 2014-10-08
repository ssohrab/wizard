import re
import sys
import market.urlutil as util
import market.parser as parser
import market.equityutil as equtil

symbols = parser.extractSymbolsFromWebsite("http://www.allpennystocks.com/aps_ca/hot_tsxv_stocks.asp",
                                 equtil.REGEX_FOR_ALLPENNYSTOCKS_SYMBOLS,
                                 equtil.REGEX_FOR_EACH_SYMBOL,
                                 "iso-8859-1", ".V")
print(symbols)
