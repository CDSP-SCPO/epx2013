#-*- coding: utf-8 -*-
import urllib
import re
from bs4 import BeautifulSoup

def get_split_propos(soup, split_propos):
    """
    FUNCTION
    update the split_propos variable if wrong from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    split_propos: split_propos variable [boolean]
    RETURN
    split_propos: split_propos variable [boolean]
    """ 
    #if split proposition, do nothing
    if not split_propos:
        #otherwise, check on the prelex bandeau if there are many no celex -> indicated split propos
        #~ print soup.find(text=re.compile("Community legislation in force"))
        nb_no_celex=len(soup.find_all(text=re.compile("Community legislation in force")))
        print "nb no_celex", nb_no_celex
        if nb_no_celex==1:
            split_propos=0
        elif nb_no_celex>1:
            split_propos=1
            
    return split_propos
    
url="prelex_content.html"
soup=BeautifulSoup(urllib.urlopen(url))

#~ print soup

print get_split_propos(soup, 0)
