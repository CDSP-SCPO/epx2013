import urllib
from bs4 import BeautifulSoup


path="http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/acf8e.htm"
soup=BeautifulSoup(urllib.urlopen(path))

attendances_table=soup.find("p", text="The Governments of the Member States and the European Commission were represented as follows:").find_next("table")


print("attendances_tables")
print(attendances_table)
        
        

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
