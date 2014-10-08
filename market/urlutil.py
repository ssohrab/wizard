'''
Created on Sep 3, 2014

@author: ssohrab
'''

import urllib.request


'''
' This method performs an HTTP GET and return the result.
' Don't use this method for fetching binary data or streams.
'
' return: string containing the result
'''
def fetchPlainTextContentFromURL(url):
    response = urllib.request.urlopen(url)
    
    result = response.read().decode("iso-8859-1")
    
    return result
