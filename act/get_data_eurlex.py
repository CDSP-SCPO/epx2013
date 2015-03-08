#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get data from Eurlex (data for the statistical analysis)
"""
import re
import urllib
from bs4 import BeautifulSoup
#models
from act.models import CodeSect, DG, DGNb, Person, CodeSect, GvtCompo, PartyFamily
from import_app.views import save_adopt_cs_pc
from import_app.models import ImportAdoptPC
from common.functions import list_reverse_enum, date_string_to_iso
from common.db import save_fk_code_sect, save_get_object, save_get_resp_eurlex
from common.config_file import *
#get pdf file (nb_mots)
import urllib2
#read pdf file (nb_mots)
import tempfile, subprocess
#model as parameter
from django.db.models.loading import get_model
from datetime import datetime

#log file
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


#All the fields are extracted from the "ALL" tab except the directory code section (code_sect and rep_en variables): for some acts, the variables are extracted from the "Procedure" tab, for others they are extracted from the "ALL" tab.


def get_titre_en(soup):
    """
    FUNCTION
    get the titre_en variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    titre_en [string]
    """
    try:
        # <div class="tabContent noStrong" style="padding:6px 30px 6px 13px;"><strong>Regulation (EC) No 1921/2006 of the... </strong>
        return soup.find("div", {"class": "noStrong"}).find("strong").get_text().strip()
    except:
        print "no titre_en!"
        return None

#at the top, below "Procedure"
#not NULL


def get_directory_code(soup_all, soup_his):
    """
    FUNCTION
    get the html code of the directory code part
    PARAMETERS
    soup_all: eurlex url content from the all tab [BeautifulSoup object]
    soup_his: eurlex url content from the his tab [BeautifulSoup object]
    RETURN
    directory code part  [BeautifulSoup object]
    tab: tab where the directory code variables can be found [string]
    """
    #from the ALL tab
    #32010R0023
    #~ <li>
       #~ <b>Directory code: </b>
       #~ <br/>11.30.60.00 <a href="./../../../search.html?type=advanced&amp;CC_1_CODED=11">External relations</a> / <a href="./../../../search.html?type=advanced&amp;CC_2_CODED=1130">Multilateral relations</a> / <a href="./../../../search.html?type=advanced&amp;CC_3_CODED=113060">Multilateral cooperation for protection of the environment, wild fauna and flora and natural resources</a>
       #~ <br/>15.07.00.00 <a href="./../../../search.html?type=advanced&amp;CC_1_CODED=15">Environment, consumers and health protection</a> / <a href="./../../../search.html?type=advanced&amp;CC_2_CODED=1507">Statistics</a>
       #~ <br/>15.10.20.30 <a href="./../../../search.html?type=advanced&amp;CC_1_CODED=15">Environment, consumers and health protection</a> / <a href="./../../../search.html?type=advanced&amp;CC_2_CODED=1510">Environment</a> / <a href="./../../../search.html?type=advanced&amp;CC_3_CODED=151020">Pollution and nuisances</a> / <a href="./../../../search.html?type=advanced&amp;CC_4_CODED=15102030">Monitoring of atmospheric pollution</a>
       #~ <br/>15.10.40.00 <a href="./../../../search.html?type=advanced&amp;CC_1_CODED=15">Environment, consumers and health protection</a> / <a href="./../../../search.html?type=advanced&amp;CC_2_CODED=1510">Environment</a> / <a href="./../../../search.html?type=advanced&amp;CC_3_CODED=151040">International cooperation</a>
    #~ </li>


    # from the HIS tab
    #~ 32010R0023
    #~ <tr>
        #~ <th>Directory code:</th>
        #~ <td id="directoryCodeProc">
            #~ <a id="directoryCodeHistProcHref" href="javascript:;" onclick="toggleHistoricalElements(this,'directoryCodeProc');" class="onlyJsInline" style="float:right;margin-top:3px;"><img src="./../../../images/box-maximize.png" alt="+"></a>
            #~
            #~ <span>15.10.40.00
                #~ <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_1_CODED=15">Environment,     consumers and health protection</a> / <a xmlns="http://www.w3.org/1999/xhtml" href= "./../../../search.html?type=advanced&amp;LP_CC_2_CODED=1510">Environment</a> /
                #~ <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_3_CODED=151040">International cooperation</a>
            #~ </span>
            #~ <br style="display:block;">
            #~
            #~ <span class="hideInJsInline" id="expElement_directory2">11.30.60.00
                #~ <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_1_CODED=11">External relations</a> / <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_2_CODED=1130">Multilateral relations</a> / <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_3_CODED=113060">Multilateral cooperation for protection of the environment, wild fauna and flora and natural resources</a>
            #~ </span>
            #~ <br style="display:block;">
            #~
            #~ <span class="hideInJsInline" id="expElement_directory3">15.10.20.30
                #~ <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_1_CODED=15">Environment, consumers and health protection</a> / <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_2_CODED=1510">Environment</a> / <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_3_CODED=151020">Pollution and nuisances</a> / <a xmlns="http://www.w3.org/1999/xhtml" href="./../../../search.html?type=advanced&amp;LP_CC_4_CODED=15102030">Monitoring of atmospheric pollution</a>
            #~ </span>
        #~ </td>
     #~ </tr>
    tab="ALL"
    try:
        #extraction from the ALL tab
        return soup_his.find("td", {"id": "directoryCodeProc"}).find_all("span"), "HIS"
    except Exception, e :
        print "exception, get_directory_code", e
        try:
            #extraction from the HIS tab
            return soup_all.find(text=re.compile("Directory code:")).find_parent("li"), tab
        except Exception, e :
            print "exception, get_directory_code 2", e

    return None, tab


def get_code_sect(directory_code, tab="ALL"):
    """
    FUNCTION
    get the CodeSect1-4 variables
    PARAMETERS
    directory_code: html source of each directory code [list of BeautifulSoup objects]
    tab: which tab is used to retrieve the variable? [string]
    RETURN
    code_sects: code_sect_* variables [list of CodeSect model instances]
    """
    code_sects=[None for i in range(4)]
    try:
        if tab=="ALL":
            code_sects_temp=directory_code.find_all('br')
            for i in range(len(code_sects_temp)):
                code_sect=code_sects_temp[i].next_sibling.strip()
                code_sects[i]=save_get_object(CodeSect,  {"code_sect": code_sect})

        elif tab=="HIS":
            for i in range(len(directory_code)):
                code_sect=directory_code[i].find(text=True).strip()
                code_sects[i]=save_get_object(CodeSect,  {"code_sect": code_sect})
    except Exception, e:
        print "no code_sect_*!", e

    return code_sects

#first, second, third and fourth code next to "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#first not NULL
#second, third and fourth: can be null


def get_rep_en(directory_code, tab="ALL"):
    """
    FUNCTION
    get the rep_en_1, rep_en_2, rep_en_3 and rep_en_4 variables
    PARAMETERS
    directory_code: html source of each directory code [list of BeautifulSoup objects]
    tab: which tab is used to retrieve the variable? [string]
    RETURN
    rep_ens: rep_en_* variab1es [list of strings]
    """
    rep_ens=["" for i in range(4)]

    try:
        if tab=="ALL":
            links=directory_code.find_all('a')
            delimitors=[]
            #find where 2 variables get separated
            for link in links:
                if link.next_sibling.strip()!="/":
                    delimitors.append(links.index(link)+1)

            #repEn1
            for i in range(delimitors[0]):
                rep_ens[0]+=links[i].get_text()+"; "

            #repEn2
            for i in range(delimitors[0], delimitors[1]):
                rep_ens[1]+=links[i].get_text()+"; "

            #repEn3
            for i in range(delimitors[1], delimitors[2]):
                rep_ens[2]+=links[i].get_text()+"; "

            #repEn4
            for i in range(delimitors[2], len(links)):
                rep_ens[3]+=links[i].get_text()+"; "

        elif tab=="HIS":
            for i in range(len(directory_code)):
                links=directory_code[i].find_all("a")
                for link in links:
                    rep_ens[i]+=link.get_text()+"; "
    except:
        print "less than four rep_en_*"

    #remove trailing "; "
    for i in range(len(rep_ens)):
        rep_ens[i]=rep_ens[i][:-2]

    return rep_ens

#texts in front of the code_sect_1, code_sect_2, code_sect_3 and code_sect_4 variables (n "Directory code:")
#rep_en_1 not NULL
#rep_en_2, rep_en_3, rep_en_4 can be Null


def save_code_agenda(code_sects):
    """
    FUNCTION
    save the code_agenda_* fk variables into the CodeSect model
    PARAMETERS
    code_sects: code_sect_* instances [list of CodeSect model instances]
    RETURN
    None
    """
    #for each code_sect
    for i in range(len(code_sects)):
        instance=code_sects[i]
        save_fk_code_sect(instance, "code_agenda")


def get_type_acte(soup):
    """
    FUNCTION
    get the type_acte variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    type_acte [string]
    """
    #<div class="boxTitle">Miscellaneous information...
    #<div class="tabContent">
    #<li><b>Author: </b>European Parliament, Council of the European Union</li>
    #<li><b>Form: </b>Regulation</li>

    try:
        misc=soup.find(text=re.compile("Miscellaneous information")).find_next("div", {"class": "tabContent"}).find("ul")
        #author part
        author=misc.find("li", text=re.compile("Author:")).get_text().split(":",1)[1].strip().lower()
        #~ print "author", author
        #form part
        form=misc.find("li", text=re.compile("Form:")).get_text().split(":",1)[1].strip().lower()
        #~ print "form", form

        #return acronyms
        author_code=""
        if "european parliament" not in author:
            author_code="CS "
        #decision
        if "decision" in form:
            #framework decision
            if "framework" in form:
                return author_code+"DEC CAD"
            if "addressee" in form:
                if "without" in form:
                    return author_code+"DEC W/O ADD"
                return author_code+"DEC W/ ADD"
            return author_code+"DEC"
        #directive
        if form=="directive":
            return author_code+"DVE"
        #regulation
        elif form=="regulation":
            return author_code+"REG"

        return author+" "+form
    except Exception, e:
        print "no type_acte!", e
        return None

#act type under Miscellaneous data->Author and Miscellaneous data->Form
#not NULL
#List of possible values (acronyms of real values): CS DEC, CS DEC CAD, CS DVE, CS REG, DEC, DVE, REG, CS DEC SUI, DEC SUI.


def get_base_j(soup):
    """
    FUNCTION
    get the base_j variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    base_j [string]
    """
    #~ <li><b>Legal basis: </b>
    #~ <br/>
    #~ <a href="./../../../legal-content/EN/AUTO/?uri=CELEX:12002E251">12002E251</a>
    #~ <br/>
    #~ <a href="./../../../legal-content/EN/AUTO/?uri=CELEX:12002E285">12002E285</a> - P1 </li>
    try:
        #http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32002L0090:EN:NOT
        li=soup.find(text=re.compile("Legal basis:")).find_parent()
        #~ print "li", li
        legal_bases=li.find_all('a')
        var=""
        for legal_base in legal_bases:
            var+=legal_base.get_text().strip()+legal_base.next_sibling.strip()+"; "

        return var[:-2]
    except Exception, e:
        print "no base_j!", e
        return None

#under "Legal basis:"
#not null
#decomposition of the variable:
#~ 1/ 1, 2, 3 ou 4
#~ 2/ 4 chiffres suivants : année de l'acte constituant la base juridique
#~ 3/ "E", "M", "R", "L" ou "D"
#~ 4/ 3 or 4 figures
#~ 5/éventuellement tiret puis au choix:
#~ (
    #~ - "A": followed by figures
    #~ - "P": followed by figures
    #~ - "FR": followed by figures
    #~ - "L": followed by figures
    #~ - "PT": followed by (one figure or one caps letter or one roman figure) and one parenthesis and/or one caps letter and one parenthesis and/or figures and sometimes one parenthesis
#~ ) -> can be repeated


def get_date_doc(soup):
    """
    FUNCTION
    get the date of the act (used for gvt_compo when ProposOrigine="EM", "CONS", "BCE", "CJUE")
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    titre_en [string]
    """
    #<li><b>of document: </b>18/12/2006</li>
    try:
        return date_string_to_iso(soup.find("li", text=re.compile("of document")).get_text().split(":",1)[1].strip())
    except Exception, e:
        print "no date gvt_compo!", e
        return None

#under "Dates"... "of document"
#not NULL


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


def get_nb_mots(no_celex):
    """
    FUNCTION
    get the number of words of the text of the act
    PARAMETERS
    no_celex: no_celex of the act [string]
    RETURN
    nb_mots [string]
    """
    #try html text
    #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:31996R0122&from=EN
    #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32010R0053&from=EN
    src="html"
    url=url_text_act_html
    url=url.replace("NOCELEX", no_celex, 1)
    soup=BeautifulSoup(urllib.urlopen(url))
    nb_mots=0

    try:
        #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32004R0854&from=EN
        #not html version for english -> use the pdf version
        if soup.title.string=="The requested document does not exist. - EUR-Lex":
            print "no english for html text, or no html text -> use pdf"
            src="pdf"
            url=url_text_act_pdf
            url=url.replace("NOCELEX", no_celex, 1)
            file_object=urllib2.urlopen(urllib2.Request(url)).read()
            #~ return None
    except Exception, e:
        #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32006D1982&from=EN
        print "link to 2 documents (STATEMENTS)", e
        return None
        #TODO: SELECT one of the two documents

    #read text of the act from an html document
    if src=="html":
        texts = soup.findAll(text=True)
        visible_texts = filter(visible, texts)
        for text in visible_texts:
            nb_mots+=len(text.split())
    #read text of the act from a pdf document
    else:
        texts=pdf_to_string(file_object)
        for text in texts.split():
            nb_mots+=1

    return nb_mots


    #try pdf doc
    #http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32000D0283(01)&from=EN


def get_adopt_propos_origine(soup, propos_origine):
    """
    FUNCTION
    get the adopt_propos_origine variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    adopt_propos_origine: adopt_propos_origine variable [date]
    """
    adopt_propos_origine=None
    try:
        #(2013-12-45) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32013L0062
        if propos_origine=="COM":
            adopt_propos_origine=soup.find(text=re.compile("Adoption by Commission")).lstrip()[:10]
        #TODO
        #(2014-3-20) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32014L0041
        elif propos_origine=="JAI":
            adopt_propos_origine=get_transm_council(soup, propos_origine)

        #transform dates to the iso format (YYYY-MM-DD)
        adopt_propos_origine=date_string_to_iso(adopt_propos_origine)
    except Exception, e:
        print "no adopt_propos_origine!", e

    return adopt_propos_origine

#~ Date in front of "Adoption by Commission"
#~ not NULL
#~ AAAA-MM-JJ format
#~ ProposOrigine=COM -> date adoption de la proposition par la Commission
#~ ProposOrigine=JAI -> TransmissionConseil date
#~ EM -> not processed because appears only when no_unique_type=CS which concerns non definitive acts (not processed)
#~ ProposOrigine=CONS -> date in pdf document (council path link)


def get_com_proc(soup, propos_origine):
    """
    FUNCTION
    get the com_proc variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    com_proc variable [string]
    """
    try:
        #(2013-12-45) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32013L0062
        if propos_origine=="COM":
            return soup.find("th", text="Decision mode:").find_next('td').get_text().strip()
    except:
        print "no com_proc!"
    return None

#~ in front of "Decision mode"
#~ Possible values:
#~ "Oral Procedure", "Written Procedure", "Empowerment procedure"
#~ Null if ProposOrigine !=COM


def get_dg_1(soup, propos_origine):
    """
    FUNCTION
    get the dg_1 variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    dg_1 variable [string]
    """
    if propos_origine=="COM":
        try:
            #(2013-12-45) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32013L0062
            dg=soup.find("th", text="Leading service:").find_next('td').get_text().strip()
            return dg
        except:
            pass
    return None

#~ in front of "Leading service"
#can be Null


def check_resp_format(names):
    """
    FUNCTION
    check that the names string in parameter matches the resp name format: Firstname(s) LASTNAME(S)
    PARAMETERS
    names: resp name? [string]
    RETURN
    True if names corresponds to a resp and False otherwise [boolean]
    """
    if names is not None:
        names=names.split()
        firstname=False
        lastname=False
        for name in names:
            if name[0].isupper():
                #only caps letters: lastname
                if name[1:].isupper():
                    lastname=True
                #only first letter in caps letter -> firstname
                elif name[1:].islower():
                    firstname=True
            #if at least one first name and one lastname was found -> it is a resp!
            if firstname and lastname:
                return True
            
    return False


def get_dg_2_3(soup, propos_origine):
    """
    FUNCTION
    get the dg_2 and dg_3 variable (if any)
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    dg_2: dg_2 variable [string]
    dg_3: dg_3 variable [string]
    """
    dg_2=None
    dg_3=None
    if propos_origine=="COM":
        try:
            #no problem
            #(1999-4-2) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31999D1296
            
            #problem
            #(2005-7-3) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32005D0600
            #Joint leading service is also used to identify for resp_2 / resp_3)
            #use find_all to get both dg_2 and resp_2 / resp_2
            #take the first item and check if the field format matches a resp
            #if yes, dg_2 is in the second item
            #if no, dg_2 is in the first item
            fields_temp=soup.find_all("th", text="Joint leading service:")
            fields=[]
            #for each field, split it if more than one dg / resp
            for field in fields_temp:
                fields.append(field.find_next('td').get_text().split(";"))
            #check only the first field (there is maximum two Joint leading service on the same page)
            check=check_resp_format(fields[0][0])
            #resp_format, the dg variable is the other item (if any)
            if check:
                if len(fields)>1:
                    dg_2=fields[1][0].strip()
                    dg_3=fields[1][1].strip()
            else:
                #the field doesn't match a responsible, it must be a dg!
                dg_2=fields[0][0].strip()
                dg_3=fields[0][1].strip()
        except Exception, e:
            #~ print "dg_2 except", e
            pass
        
    return dg_2, dg_3

#~ in front of "Leading service"
#can be Null


def get_dgs(dgs):
    """
    FUNCTION
    get the dg instances associated to the dg passed in parameter
    PARAMETERS
    dg: dg 1 or 2 [string]
    RETURN
    dg_instances: list of dg instances [list of DG model instances]
    """
    dg_instances=[]
    many=False
    if dgs is not None and dgs.strip()!="":
        #if there are two possible dgs separated by a semi-column
        #~ print "dgs", dgs
        temp=dgs.split(";")
        for dg in temp:
            dg=dg.strip()
            #if it is a dg_nb, it can refer to more than one DG (manual validation)
            if dg[-1].isdigit():
                try:
                    dg_nb=DGNb.objects.get(dg_nb=dg)
                    #only one dg one many possible dgs?
                    try:
                        instance=DG.objects.get(dg_nb=dg_nb)
                    except Exception, e:
                        #~ print "many possible dgs", e
                        instances=DG.objects.filter(dg_nb=dg_nb)
                        many=True
                except Exception, e:
                    #~ print "get_dgs exception", e
                    instance=None
            #it is a dg
            else:
                try:
                    #dg exists
                    instance=DG.objects.get(dg=dg)
                except Exception, e:
                    #~ print "dg does not exist yet", e
                    #TODO
                    instance=dg

            if many:
                for instance in instances:
                    dg_instances.append(instance)
            else:
                dg_instances.append(instance)

    return dg_instances


def display_dgs(dgs, name):
    """
    FUNCTION
    display dg and dg_sigle variables
    PARAMETERS
    dgs: dg_1 or dg_2 or dg_3 [DG instance]
    name: variable name [string]
    RETURN
    None
    """
    if dgs!=None:
        #get index
        dg_sigle_name="dg_sigle_"+name[-1]
        for dg in dgs:
            #if the dg was found in the database, we have its instance
            if isinstance(dg, DG):
                print name, dg.dg
                print dg_sigle_name, dg.dg_sigle.dg_sigle
            #if the dg was not found in the database, we have the string name found on eurlex (no dg_sigle)
            else:
                print name, dg
                print dg_sigle_name, "dg not found in db so no dg_sigle"
            

def format_resp_name(names):
    """
    FUNCTION
    rewrite  the name of the responsible in the right format (also used for rapporteurs)
    PARAMETERS
    names: full name of the person [string]
    RETURN
    instance: full name of the person, in the right format [string]
    """
    if names is not None:
        #remove trailing "'"
        if names[-1]=="'":
            names=names[:-1]
        #change name format: "Firstname LASTNAME" -> "LASTNAME Firstname"
        names=names.split()
        first_name=last_name=""
        for name in names:
            #get last names
            if name.isupper():
                last_name+=name+" "
            #get first names
            else:
                first_name+=name+" "

        names=last_name+first_name[:-1]

    return names


def get_resp_1(soup):
    """
    FUNCTION
    get the resp_1 variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    resp_1 variable [string]
    """
    try:
        #1999-4-2 http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31999D1296
        resp=soup.find("th", text="Leading person:").find_next('td').get_text().strip()
        return resp
    except:
        pass
    return None

#~ in front of "Leading person"
#can be Null


def get_resp_2_3(soup):
    """
    FUNCTION
    get the resp_2 variable and resp_3 variable (if any)
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    resp_2 variable [string]
    resp_3 variable [string]
    """
    resp_2=None
    resp_3=None
    try:
        #no problem
        #(1999-4-2) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31999D1296
        
        #problem
        #(2005-7-3) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32005D0600
        #Joint leading service is also used to identify for resp_2 / resp_3)
        #use find_all to get both dg_2 and resp_2 / resp_2
        #take the first item and check if the field format matches a resp
        #if yes, resp_2 is in the second item
        #if no, resp_2 is in the first item
        fields_temp=soup.find_all("th", text="Joint leading service:")
        fields=[]
        #for each field, split it if more than one dg / resp
        for field in fields_temp:
            fields.append(field.find_next('td').get_text().split(";"))
        #check only the first field (there is maximum two Joint leading service on the same page)
        check=check_resp_format(fields[0][0])
        #resp_format, the resp variable is the first item
        if check:
            if len(fields)>1:
                resp_2=fields[0][0].strip()
                resp_3=fields[0][1].strip()
        else:
            #the field doesn't match a responsible, the resp is in the second item (if any)
            resp_2=fields[1][0].strip()
            resp_3=fields[1][1].strip()
    except Exception, e:
        print "dg_2 except", e
        pass

    return resp_2, resp_3

#~ in front of "Joint leading service" (IT'S A MISTAKE ON EURLEX, IT SHOULD BE JOINT LEADING PERSON)
#can be Null


def get_resp(resp_name):
    """
    FUNCTION
    get the resp instance of the resp_name variable
    PARAMETERS
    resp_name: name of the responsible list of responsible names [string]
    RETURN
    instance: instance of the resp in parameter [Person instance]
    """
    if resp_name is not None:
        try:
            name=format_resp_name(resp_name)
            return save_get_resp_eurlex(name)
        except Exception, e:
            print "exception", e
    return None


def display_resps(resp, name):
    """
    FUNCTION
    display resp and related variables (name, country, party, party_family)
    PARAMETERS
    resp: resp_1 or resp_2 or resp_3 [Person instance]
    name: variable name [string]
    RETURN
    None
    """
    if resp!=None:
        #get index
        resp_name="resp_"+name[-1]
        country_name="country_"+name[-1]
        party_name="party_"+name[-1]
        party_family_name="party_family_"+name[-1]
        
        #if the resp was found in the database, we have its instance
        if isinstance(resp, Person):
            print resp_name, resp.name
            print country_name, resp.country.country
            print party_name, resp.party.party
            print party_family_name, PartyFamily.objects.get(party=resp.party, country=resp.country).party_family
        #if the dg was not found in the database, we have the string name found on eurlex (no dg_sigle)
        else:
            print resp_name, resp
            print "resp not found in db so there is no related data (country, party, party_family)"


def get_transm_council(soup, propos_origine):
    """
    FUNCTION
    get the transm_council variable
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    transm_council: transm_council variable [date]
    """
    transm_council=None

    #transmision to Council
    if propos_origine!="CONS":
        try:
            #(2014-3-20) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32014L0041 
            transm_council=soup.find(text=re.compile("Transmission to Council")).lstrip()[:10]
            #transform dates to the iso format (YYYY-MM-DD)
            transm_council=date_string_to_iso(transm_council)
        except Exception, e:
            print "pb transm_council Council", e

    if transm_council is None:
        #Transmission to Parliament
        try:
            #(2001-05-03) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32001R0973
            transm_council=soup.find(text=re.compile("Transmission to Parliament")).lstrip()[:10]
            #transform dates to the iso format (YYYY-MM-DD)
            transm_council=date_string_to_iso(transm_council)
        except Exception, e:
            print "pb transm_council Parliament", e

    return transm_council

#date in front of "Transmission to Council"
#not Null (except blank page -> error on page)
#AAAA-MM-JJ format


def get_point_b_tables(soup, propos_origine):
    """
    FUNCTION
    get the html content of the tables concerning each cons_b variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    tables: html content of the tables concerning each cons_b variable [list of BeautifulSoup objects]
    """
    if propos_origine not in ["CONS", "BCE", "EM", "CJUE"]:
        tables=[]
        temps=soup.find_all(text=re.compile('ITEM "B"'))
        for temp in temps:
            tables.append(temp.find_parent("table"))

        return tables

    return None
    

def get_nb_point_b(tables):
    """
    FUNCTION
    get the nb_point_b variable
    PARAMETERS
    tables: html content of the tables concerning each cons_b variable [list of BeautifulSoup objects]
    RETURN
    nb_point: nb_point_b variable [int]
    """
    if tables is not None:
        #(2005-7-3) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32005D0600
        return len(tables)
    return None
    
#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "B"' on the page
#~ not NULL
#~ De 0 a 20
#~ if propos_origine=="CONS" or "BCE", filled manually


def get_date_cons_b(tables):
    """
    FUNCTION
    get the date_cons_b variable
    PARAMETERS
    tables: html content of the tables concerning each cons_b variable [list of BeautifulSoup objects]
    RETURN
    date_cons: date_cons_b variable [int]
    """
    if tables is not None:
        date_cons=""
        for table in tables:
            #(2005-7-3) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32005D0600
            date_cons+=table.find_previous("img", {"alt": "Council of the European Union"}).get_text().lstrip()[:10]+'; '
        #remove last "; "
        if date_cons!="":
            date_cons=date_cons[:-2]

            #convert to amerian format
            return date_string_to_iso(date_cons)
        
    return None
    
#can be Null
#pour chaque point b, date en face du titre du tableau qui contient ITEM "B".
#concatenate all the values, even if redundancy
#~ if propos_origine=="CONS", filled manually


def get_cons_b(tables):
    """
    FUNCTION
    get the cons_b variable
    PARAMETERS
    tables: html content of the tables concerning each cons_b variable [list of BeautifulSoup objects]
    RETURN
    cons_b variable [string]
    """
    if tables is not None:
        cons=""
        for table in tables:
            try:
                #in front of Subject
                #(2005-7-3) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32005D0600
                cons+=table.find("th", text="Subject:").find_next("td").get_text().strip()+'; '
            except:
                cons+="??; "
                #no Subject: below ITEM B, find the number in front of Council session
                #below that number, click on the PRES link, and find the cons variable in the new page below the searched number (at the top of the document)
                
                #TODO
                #(2005-7-3) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31999D1296
                pass
                
        #remove last "; "
        if cons!="":
            cons=cons[:-2]
                
            return cons
        
    return None
  
#can be Null
#in front of SUBJECT, only if the act is processed at B point (preceded by 'ITEM "B" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy
#~ if propos_origine=="CONS", filled manually


def get_split_propos(soup, split_propos):
    """
    FUNCTION
    update the split_propos variable if act not marked as a split proposition and is actually split
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    split_propos: split_propos variable [boolean]
    RETURN
    split_propos: updated split_propos variable [boolean]
    """ 
    #if the act was marked as a split proposition, do nothing
    if not split_propos:
        #otherwise, check if there are many no celex in the Procedure bandeau -> if yes, it is a split propos
        #(1999-1-23) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31999L0003
        try:
            no_celex=soup.find(text=re.compile("Adopted acts:")).find_parent("p").find_all("a")
            if len(no_celex)>1:
                split_propos=True
        except:
            print "no procedure tab!"
            
    return split_propos


def get_date_in_front_of(soup, string):
    """
    FUNCTION
    get the date variable in front of the string field in parameter
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    string: string field to search [string]
    RETURN
    date: searched date [date]
    """
    return soup.find(text=re.compile(string)).lstrip()[:10]
    
    
def get_adopt_conseil(soup, no_unique_type, suite_2e_lecture_pe, split_propos, nb_lectures):
    """
    FUNCTION
    get the adopt_conseil variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    no_unique_type: no_unique_tpye variable [string]
    suite_2e_lecture_pe: suite_2e_lecture_pe variable [boolean]
    split_propos: split_propos variable [boolean]
    nb_lectures: nb_lectures variable [int]
    RETURN
    adopt_conseil: adopt_conseil variable [date]
    """
    adopt_conseil=None

    if no_unique_type=="COD":
        if  nb_lectures==3:
            #in front of "Council decision on 3rd reading"
            #(1996-7-8) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31996D1692
            if not split_propos:
                adopt_conseil=get_date_in_front_of(soup, "Council decision on 3rd reading")
        elif nb_lectures==2:

            if suite_2e_lecture_pe:

                if split_propos:
                    temp=soup.find(text=re.compile("Formal adoption by Council"))
                    table_soup=temp.find_next("table").find_next("table")
                    #date in front of "Formal adoption by Council" IF just before "Signature by the President of the EP and by the President of the Council"
                    #(2001-7-1) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32001R1724
                    if table_soup.find(text=re.compile("Signature by the President of the EP and by the President of the Council")):
                        adopt_conseil=temp.lstrip()[:10]
                    # else date in front of "Approval by the Council of the EP amendments at 2nd reading"
                    #exemple??
                    else:
                        adopt_conseil=get_date_in_front_of(soup, "Approval by the Council of the EP amendments at 2nd reading")

                #date not found with the previous rule
                if adopt_conseil is None:
                    temp=soup.find(text=re.compile("EP opinion on 2nd reading"))
                    table_soup=temp.find_next("table")
                    #date in front of "EP opinion on 2nd reading" IF "Approval without amendment"
                    #(2014-1-1) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32014R0165
                    if table_soup.find(text="Approval without amendment"):
                        adopt_conseil=temp.lstrip()[:10]
                    # "Approval with amendments"
                    #exemple??
                    else:
                        #TO TEST
                        adopt_conseil=get_date_in_front_of(soup, "Council approval on 2nd reading")

            elif not split_propos:
                #date in front of "Approval by the Council of the EP amendments at 2nd reading"
                #(1999-1-8) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31999D0372
                adopt_conseil=get_date_in_front_of(soup, "Approval by the Council of the EP amendments at 2nd reading")


    #if date not found with all the previous rules:
    if adopt_conseil is None:
        #find date in front of one of the following texts
        texts=["Formal adoption by Council", "Adoption common position", "Council approval 1st rdg", "Approval by the Council of the EP position at 1st reading"]
        for text in texts:
            try:
                #(2004-1-1) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32004R0139
                #??
                #??
                #(2014-3-22) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32014R0259
                adopt_conseil=get_date_in_front_of(soup, text)
                break
            except Exception, e:
                print "exception", text, e

    #transform dates to the iso format (YYYY-MM-DD)
    adopt_conseil=date_string_to_iso(adopt_conseil)
    return adopt_conseil

#~ date in front of "Formal adoption by Council" or "Adoption common position" or "Council approval 1st rdg"
#not Null
#~ AAAA-MM-JJ format

#~ Si Suite2LecturePE = Y (ou NbLectures=2) et ProposSplittee=N. Dans ce cas, la date AdoptionConseil=la date qui se trouve en face de la ligne « EP Opinion 2nd rdg » (vérifier qu’à la ligne qui suit dans le même carré, on trouve « Approval without amendment » et que le titre du carré qui suit est bien « Signature by EP and Council »
#~ Exemple : http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619

#~ quand Suite2LecturePE=Y ET quand ProposSplittee=N and nb_lectures=3 -> date in front of Council decision at 3rd rdg (vérifier que le titre du carré qui suit est bien « Signature by EP and Council »)
#~ Example: http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644

# if Suite2LecturePE=Y and split_propos=Y -> to fill manually


def get_point_a_tables(soup, propos_origine):
    """
    FUNCTION
    get the html content of the tables concerning each cons_a variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    tables: html content of the tables concerning each cons_a variable [list of BeautifulSoup objects]
    """
    if propos_origine not in ["CONS", "BCE", "EM", "CJUE"]:
        tables=[]
        temps=soup.find_all(text=re.compile('ITEM "A"'))
        for temp in temps:
            tables.append(temp.find_parent("table"))

        return tables

    return None
    

def get_nb_point_a(tables):
    """
    FUNCTION
    get the nb_point_a variable
    PARAMETERS
    tables: html content of the tables concerning each cons_a variable [list of BeautifulSoup objects]
    RETURN
    nb_point: nb_point_a variable [int]
    """
    if tables is not None:
        #(2014-3-20) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32014L0041
        return len(tables)
    return None
    
#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "A"' on the page
#~ not NULL
#~ De 0 a 20
#~ if propos_origine=="CONS" or "BCE", filled manually


def get_date_cons_a(tables):
    """
    FUNCTION
    get the date_cons_a variable
    PARAMETERS
    tables: html content of the tables concerning each cons_a variable [list of BeautifulSoup objects]
    RETURN
    date_cons: date_cons_a variable [int]
    """
    logger.debug('date_cons_a tables: '+str(tables))
    if tables is not None:
        logger.debug('date_cons_a: tables is not none')
        date_cons=""
        for table in tables:
            logger.debug('date_cons_a table: '+str(table))
            logger.debug('date_cons_a: +1')
            logger.debug('date_cons_a tables.find_previous img: '+str(table.find_previous("img", {"alt": "Council of the European Union"})))
            #(2014-3-20) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32014L0041 
            date_cons+=table.find_previous("img", {"alt": "Council of the European Union"}).get_text().lstrip()[:10]+'; '
            logger.debug('date_cons_a: '+date_cons)
        #remove last "; "
        if date_cons!="":
            logger.debug('date_cons_a: different from ""')
            date_cons=date_cons[:-2]

            #convert to american format
            logger.debug('date_cons_a iso format: '+str(date_string_to_iso(date_cons)))
            return date_string_to_iso(date_cons)
            
    logger.debug('date_cons_a : None!!!!!')
    return None
    
#can be Null
#pour chaque point a, date en face du titre du tableau qui contient ITEM "A".
#concatenate all the values, even if redundancy
#~ if propos_origine=="CONS", filled manually


def get_cons_a(tables):
    """
    FUNCTION
    get the cons_a variable
    PARAMETERS
    tables: html content of the tables concerning each cons_a variable [list of BeautifulSoup objects]
    RETURN
    cons_a variable [string]
    """
    if tables is not None:
        cons=""
        for table in tables:
            try:
                #in front of Subject
                #(2014-3-20) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32014L0041
                cons+=table.find("th", text="Subject:").find_next("td").get_text().strip()+'; '
            except:
                cons+="??; "
                #(1999-1-23) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31999L0003
                #subject can't be found automatically -> to be filled manually
                print "cons_a to be found manually!"
                
        #remove last "; "
        if cons!="":
            cons=cons[:-2]
                
            return cons
        
    return None
  
#can be Null
#in front of SUBJECT, only if the act is processed at B point (preceded by 'ITEM "B" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy
#~ if propos_origine=="CONS", filled manually

#not Null
#in front of SUBJECT, only if the act is processed at A point (preceded by 'ITEM "A" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy


def save_config_cons(code_sect_1):
    """
    FUNCTION
    save the config_cons variable into the CodeSect model
    PARAMETERS
    code_sect_1: code_sect_1 instance [CodeSect model instance]
    RETURN
    None
    """
    print "save_config_cons"
    #~ print "code_sect_1", code_sect_1
    save_fk_code_sect(code_sect_1, "config_cons")


def get_chgt_base_j(soup):
    """
    FUNCTION
    get the cons_a variable
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    chgt_base_j variable [boolean]
    """
    if soup.find(text=re.compile("Change of legal basis")) is not None:
        return True
    return False

    
def get_date_diff(date_1, date_2):
    """
    FUNCTION
    compute the difference between two dates
    PARAMETERS
    date_1: first date [string]
    date_2: second date [string]
    RETURN
    difference between the two dates in parameters  [int]
    """
    excluded_values=[None, "None", ""]
    if date_1 not in excluded_values and date_2 not in excluded_values:
        #transform dates to the iso format (YYYY-MM-DD)
        try:
            date_1=datetime.strptime(date_1, "%Y-%m-%d")
            date_2=datetime.strptime(date_2, "%Y-%m-%d")
            return (date_1 - date_2).days
        except Exception, e:
            print e
            print "The dates are invalid"
            
    return None

#DureeAdoptionTrans (TransmissionConseil - AdoptionProposOrigine)
#DureeProcedureDepuisPropCom (AdoptionConseil – AdoptionProposOrigine)
#DureeProcedureDepuisTransCons (AdoptionConseil – TransmissionConseil)
#DureeTotaleDepuisPropCom (SignPECS – AdoptionProposOrigine)
#DureeTotaleDepuisTransCons (SignPECS – TransmissionConseil) 


def get_duration_fields(fields, sign_pecs):
    """
    FUNCTION
    get all the duration fields: duree_adopt_trans, duree_proc_depuis_prop_com, duree_proc_depuis_trans_cons, duree_tot_depuis_prop_com, duree_tot_depuis_trans_cons
    PARAMETERS
    fields: date fields necessary to compute the durations (from eurlex) [dictionary]
    sign_pecs: sign_pecs variable from oeil [date]
    RETURN
    duration_fields: duration fields [dictionary]
    """
    duration_fields={}
    sign_pecs=str(sign_pecs)
    
      #~ #duree_adopt_trans
    name='duree_adopt_trans'
    duration_fields[name]=get_date_diff(fields['transm_council'], fields['adopt_propos_origine'])
    print name, duration_fields[name]

    #duree_proc_depuis_prop_com
    name='duree_proc_depuis_prop_com'
    duration_fields[name]=get_date_diff(fields['adopt_conseil'], fields['adopt_propos_origine'])
    print name, duration_fields[name]

    #duree_proc_depuis_trans_cons
    name='duree_proc_depuis_trans_cons'
    duration_fields[name]=get_date_diff(fields['adopt_conseil'], fields['transm_council'])
    print name, duration_fields[name]

    #duree_tot_depuis_prop_com
    name='duree_tot_depuis_prop_com'
    duration_fields[name]=get_date_diff(sign_pecs, fields['adopt_propos_origine'])
    #if no sign_pecs
    if duration_fields[name]==None:
        duration_fields[name]=duration_fields['duree_proc_depuis_prop_com']
    print name, duration_fields[name]

    #duree_tot_depuis_trans_cons
    name='duree_tot_depuis_trans_cons'
    duration_fields[name]=get_date_diff(sign_pecs, fields['transm_council'])
    #if no sign_pecs
    if duration_fields[name]==None:
        duration_fields[name]=duration_fields['duree_proc_depuis_trans_cons']
    print name, duration_fields[name]

    return duration_fields


def get_vote_public(adopt_cs_contre, adopt_cs_abs):
    """
    FUNCTION
    return the vote_public variable
    PARAMETERS
    adopt_cs_contre: adopt_cs_contre objet from index [AdoptCsContreAssoc model instance]
    adopt_cs_abs: adopt_cs_abs object from index [AdoptCsAbsAssoc model instance]
    RETURN
    vote_public [boolean]
    """
    adopt_cs_contres=adopt_cs_contre.all()
    adopt_cs_abss=adopt_cs_abs.all()
    if adopt_cs_contres or adopt_cs_abss:
        return True
    return False

#vote_public is True if adopt_cs_contre or adopt_cs_abs has a value


#external table
def save_get_adopt_pc(act, act_ids):
    """
    FUNCTION
    fill the assocation table which links an act to its adopt_pc_contre and adopt_pc_abs variables
    PARAMETERS
    act: instance of an act [Act model instance]
    act_ids: instance of an act ids [ActIds model instance]
    RETURN
    adopt_pc: adopt_pc_contre and adopt_pc_abs variables
    """
    adopt_pc=None
    try:
        #is there a match in the ImportAdoptPC table?
        adopt_pc=ImportAdoptPC.objects.only("adopt_pc_contre", "adopt_pc_abs").get(no_celex=act_ids.no_celex)
        save_adopt_cs_pc(act, "adopt_pc_contre", adopt_pc.adopt_pc_contre)
        save_adopt_cs_pc(act, "adopt_pc_abs", adopt_pc.adopt_pc_abs)
    except Exception, e:
        print "no adopt_pc variables for this act!"

    return adopt_pc


def get_data_eurlex(soups, act_ids):
    """
    FUNCTION
    get all data from the eurlex url
    PARAMETERS
    soups: eurlex url content from the "all" and "his" tab [list of BeautifulSoup objects]
    act_ids: act ids instance [ActIds instance]
    RETURN
    fields: retrieved data from eurlex [dictionary]
    dgs_temp: list of dg names [list of strings]
    resp_names: list of resp names [list of strings]
    """
    fields={}
    act=act_ids.act
    #display in the Act data validation form dg and resp names as written on eurlex
    dg_names=[]
    resp_names=[]

    #ALL TAB
    #<div id="content">
    soup_all=soups[0].find("div", {"id": "content"})

    #HIS tab (Procedure)
    #<div class="tabContent tabContentForDocument">
    soup_his=soups[1].find("div", {"class": "tabContent"})
    #remove script tags
    [s.extract() for s in soup_his('script')]
    

    #titre_en
    name='titre_en'
    fields[name]=get_titre_en(soup_all)
    print name, fields[name]

    #all and his url
    directory_code_soup, tab=get_directory_code(soup_all, soup_his)

    #code_sect_1, code_sect_2, code_sect_3, code_sect_4
    code_sects=get_code_sect(directory_code_soup, tab)

    #code_agenda_1-4
    save_code_agenda(code_sects)

    #print code_sect_* and code_agenda_*
    name='code_sect_'
    for index in xrange(len(code_sects)):
        num=str(index+1)
        #django adds "_id" to foreign keys field names
        fields[name+num+"_id"]=code_sects[index]
        if code_sects[index]!=None:
            print name+num+": ", fields[name+num+"_id"].code_sect
            print 'code_agenda_'+num+": ", fields[name+num+"_id"].code_agenda.code_agenda

    #rep_en_1, rep_en_2, rep_en_3, rep_en_4
    rep_ens=get_rep_en(directory_code_soup, tab)
    name='rep_en_'
    for index in xrange(len(rep_ens)):
        num=str(index+1)
        fields[name+num]=rep_ens[index]
        print name+num+": ", fields[name+num]

    #type_acte
    name='type_acte'
    fields[name]=get_type_acte(soup_all)
    print name, fields[name]

    #~ #base_j
    name='base_j'
    fields[name]=get_base_j(soup_all)
    print name, fields[name]
#~ 
    #date_doc
    name='date_doc'
    fields[name]=get_date_doc(soup_all)
    print name, fields[name]

    #nb_mots
    name="nb_mots"
    fields[name]=get_nb_mots(act_ids.no_celex)
    print name, fields[name]
#~ 
#~ 
    #~ #FROM PRELEX
#~ 
    #~ #adopt_propos_origine
    name='adopt_propos_origine'
    fields[name]=get_adopt_propos_origine(soup_his, act_ids.propos_origine)
    print name, fields[name]
#~ 
    #com_proc
    name='com_proc'
    fields[name]=get_com_proc(soup_his, act_ids.propos_origine)
    print name, fields[name]

    #~ #dg_1, #dg_2, dg_3
    fields["dg_1"]=get_dg_1(soup_his, act_ids.propos_origine)
    fields["dg_2"], fields["dg_3"]=get_dg_2_3(soup_his, act_ids.propos_origine)
    for index in range(nb_dgs):
        index=str(index+1)
        name="dg_"+index
        #dg names as written on eurlex
        dg_names.append(fields[name])
        #DG instances
        fields[name+"_id"]=get_dgs(fields[name])
        display_dgs(fields[name+"_id"], name)

    print "dg_names eurlex", dg_names

    #resp_1, resp_2, res_3
    #~ 
    fields["resp_1"]=get_resp_1(soup_his)
    fields["resp_2"], fields["resp_3"]=get_resp_2_3(soup_his)
    for index in range(nb_resps):
        index=str(index+1)
        name="resp_"+index
        #resp names as written on eurlex
        resp_names.append(fields[name])
        #Person instances
        fields[name+"_id"]=get_resp(fields[name])
        display_resps(fields[name+"_id"], name)
#~ 
    print "resp_names eurlex", resp_names
    #~ 
    #transm_council
    name='transm_council'
    fields[name]=get_transm_council(soup_his, act_ids.propos_origine)
    print name, fields[name]
#~ 
    #~ #point_b html tables
    point_b_tables=get_point_b_tables(soup_his, act_ids.propos_origine)

    #nb_point_b
    name='nb_point_b'
    fields[name]=get_nb_point_b(point_b_tables)
    print name, fields[name]
    
    #date_cons_b
    name='date_cons_b'
    fields[name]=get_date_cons_b(point_b_tables)
    print name, fields[name]

    #~ #cons_b
    name='cons_b'
    fields[name]=get_cons_b(point_b_tables)
    print name, fields[name]

    #~ #check and update split_propos
    name='split_propos'
    fields[name]=get_split_propos(soup_his, act.split_propos)
    print name, fields[name]
#~ 
    #~ #adopt_conseil
    name="adopt_conseil"
    fields[name]=get_adopt_conseil(soup_his, act_ids.no_unique_type, act.suite_2e_lecture_pe, fields['split_propos'], act.nb_lectures)
    print name, fields[name]

    #point_a html tables
    point_a_tables=get_point_a_tables(soup_his, act_ids.propos_origine)

    #nb_point_a
    name='nb_point_a'
    fields[name]=get_nb_point_a(point_a_tables)
    print name, fields[name]
    
    #date_cons_a
    name='date_cons_a'
    fields[name]=get_date_cons_a(point_a_tables)
    print name, fields[name]

    #~ #cons_a
    name='cons_a'
    fields[name]=get_cons_a(point_a_tables)
    print name, fields[name]

    #config_cons
    save_config_cons(act.code_sect_1)
#~ 
#~ 
    #~ #chgt_base_j
    name='chgt_base_j'
    fields[name]=get_chgt_base_j(soup_his)
    print name, fields[name]
#~ 
    #duration fields: duree_adopt_trans, duree_proc_depuis_prop_com, duree_proc_depuis_trans_cons, duree_tot_depuis_prop_com, duree_tot_depuis_trans_cons
    fields.update(get_duration_fields(fields, act.sign_pecs))

    #vote_public
    name='vote_public'
    fields[name]=get_vote_public(act.adopt_cs_contre, act.adopt_cs_abs)
    print name, fields[name]

    #adopt_pc_contre, #adopt_pc_abs
    adopt_pc=save_get_adopt_pc(act, act_ids)
    if adopt_pc!=None:
        print "adopt_pc_contre:", adopt_pc.adopt_pc_contre
        print "adopt_pc_abs:", adopt_pc.adopt_pc_abs

    return fields, dg_names, resp_names
