#-*- coding: utf-8 -*-

#get pdf file (nb_mots)
import urllib2
#read pdf file (nb_mots)
import tempfile, subprocess



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


### MAIN ###

url="http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32006L0121&from=EN"
#bigest text
#~ url="http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32008R1272&from=EN"
file_object=urllib2.urlopen(urllib2.Request(url)).read()
texts=pdf_to_string(file_object)
nb_mots=0
cpt=0
for text in texts.split():
    nb_mots+=1
    cpt+=1
    if cpt<500:
        print text

print ""
print nb_mots
