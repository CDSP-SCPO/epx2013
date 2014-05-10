#-*- coding: utf-8 -*-
import urllib
import re
from bs4 import BeautifulSoup

url="http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2003/0116(CNS)"
soup=BeautifulSoup(urllib.urlopen(url))
print "soup"
print soup
