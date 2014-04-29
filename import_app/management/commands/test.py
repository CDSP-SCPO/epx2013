import urllib
from bs4 import BeautifulSoup

url="http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/5923en8.htm"
soup=BeautifulSoup(urllib.urlopen(url), 'html.parser')

for item in soup.find_all('p'):
    if item.text.startswith('Commission'):
        break
    else:
        print item.text
        
        

#WORKS WITH PYTHON3

#~ from urllib.request import urlopen
#~ from bs4 import BeautifulSoup
#~ 
#~ url="http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/5923en8.htm"
#~ soup=BeautifulSoup(urlopen(url))
#~ 
#~ for item in soup.find_all('p'):
    #~ if item.text.startswith('Commission'):
        #~ break
    #~ else:
        #~ print(item.text)
