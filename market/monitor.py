'''
Created on Sep 3, 2014

@author: ssohrab
'''

import time
import threading
import market.urlutil
import market.csvparser

class Monitor (threading.Thread):
    
    __url = ""
    __pollingIntervals = 30 #In seconds
    __terminateMonitor = False
    
    def __init__(self, url,  pollingIntervals):
        threading.Thread.__init__(self)
        self.__url = url
        self.pollingIntervals = pollingIntervals
    
    def run(self):
        while(not self.__terminateMonitor):
            # Do a lot of shit while we can
            csvData = market.urlutil.fetchPlainTextContentFromURL(self.__url)
            market.csvparser.parseStockData(csvData)
            
            #Chill for a bit
            time.sleep(self.__pollingIntervals)

            