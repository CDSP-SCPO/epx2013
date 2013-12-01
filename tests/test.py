#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib

url="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32007D0722:EN:NOT"
soup=BeautifulSoup(urllib.urlopen(url))
print soup.find("h2", text="Dates").find_next("ul").find(text=re.compile("of document")).strip()[-10:]
