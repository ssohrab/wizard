'''
Created on Sep 3, 2014

@author: ssohrab
'''

import urllib.request


def fetchPlainTextContentFromURL(url):
    response = urllib.request.urlopen(url)
    
    result = response.read().decode("iso-8859-1")
    
    return result
