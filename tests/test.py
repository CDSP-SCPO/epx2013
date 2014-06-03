#-*- coding: utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup

url="http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2003/0116(CNS)"
print "url", url
html=urllib2.urlopen(url, timeout=10).read()
print "html retrieved"
print html[:100]
soup=BeautifulSoup(html)
print "soup retrieved"
print soup.title
