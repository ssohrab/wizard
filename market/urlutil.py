'''
Created on Sep 3, 2014

@author: ssohrab
'''

import urllib.request

def fetchPlainTextContentFromURL(url):
    response = urllib.request.urlopen(url)
    return response.read()
