'''
Created on Sep 3, 2014

@author: ssohrab
'''

import threading

class Monitor (threading.Thread):
    
    __uri = ""
    __pollingIntervals = 30 # In seconds
    __terminateMonitor = False
    
    def __init__(self, uri,  pollingIntervals):
        threading.Thread.__init__(self)
        self.uri = uri
        self.pollingIntervals = pollingIntervals
    
    def run(self):
        
        while(not self.__terminateMonitor):
            # Fetch data
            