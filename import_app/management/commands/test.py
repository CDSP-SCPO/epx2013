#-*- coding: utf-8 -*-

#get pdf file (nb_mots)
import urllib2
import urllib
#read pdf file (nb_mots)
import tempfile, subprocess

#html
from bs4 import BeautifulSoup
import re




def pdf_to_string(file_object):
    """
    FUNCTION
    get the text of a pdf and put it in a string variable
    PARAMETERS
    file_object: pdf file wrapped in a python file object [File object]
    RETURN
    string: extracted text [string]
    """
    tf = tempfile.NamedTemporaryFile()
    tf.write(file_object)
    tf.seek(0)

    outputTf = tempfile.NamedTemporaryFile()

    if (len(file_object) > 0) :
        #-layout: keep layout (not good when names and job titles are split as if they were in two different columns).
        out, err = subprocess.Popen(["pdftotext", "-layout", tf.name, outputTf.name ]).communicate()
        #~ out, err = subprocess.Popen(["pdftotext", tf.name, outputTf.name ]).communicate()
        return outputTf.read()
    else :
        return None


def visible(element):
    """
    FUNCTION
    indicates if the text element in parameter is a real text or is part of html tags / syntax
    PARAMETERS
    element: text to analyze [string]
    RETURN
    string: True if the element contains real text, False otherwise [boolean]
    """
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    #remove '\n'
    elif element.encode('utf-8').strip()=='':
        return False
    elif re.match('<!--.*-->', element.encode('utf-8')):
        return False
    return True



### MAIN ###


#text from pdf file
#~ url="http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32006L0121&from=EN"
#~ #bigest text
#~ url="http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32008R1272&from=EN"
#~ file_object=urllib2.urlopen(urllib2.Request(url)).read()
#~ texts=pdf_to_string(file_object)
#~ nb_mots=0
#~ cpt=0
#~ for text in texts.split():
    #~ nb_mots+=1
    #~ cpt+=1
    #~ if cpt<500:
        #~ print text
#~
#~ print ""
#~ print nb_mots


#text from html file (two documents)
#2006-12-16
url="http://eur-lex.europa.eu/resource.html?uri=cellar:fea6bf93-6db4-473b-b40c-acf92978d6e1.0005.03/DOC_1&format=HTML&lang=EN&parentUrn=CELEX:32006D1982"
soup=BeautifulSoup(urllib.urlopen(url))
texts = soup.findAll(text=True)
visible_texts = filter(visible, texts)
nb_mots=0
for text in visible_texts:
    nb_mots+=len(text.split())
print nb_mots
