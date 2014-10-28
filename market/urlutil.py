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
def fetchPlainTextContentFromURL(url, encoding="utf-8"):
    try:
        response = urllib.request.urlopen(url)
    except:
        return ''
    
    result = response.read().decode(encoding)
    
    return result
