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




#All the fields are extracted from the "ALL" tab except the directory code section (code_sect and rep_en variables): for some acts, the variables are extracted from the "Procedure" tab, for others they are extracted from the "ALL" tab.


def get_titre_en(soup):
    """
    FUNCTION
    get the titre_en variable from the eurlex url
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
    get the html code of the directory code part from the eurlex url
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
    get the CodeSect1-4 variables from the eurlex url
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
    get the rep_en_1, rep_en_2, rep_en_3 and rep_en_4 variables from the eurlex url
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
    get the type_acte variable from the eurlex url
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
    get the base_j variable from the eurlex url
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
    get the date of the act (used for gvt_compo when ProposOrigine="EM", "CONS", "BCE", "CJUE") from the eurlex url
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
    get the number of words of the text of the act from the eurlex url
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

    print nb_mots
    return nb_mots


    #try pdf doc
    #http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32000D0283(01)&from=EN



# TO DO

def get_adopt_propos_origine(soup, propos_origine):
    """
    FUNCTION
    get the adopt_propos_origine variable from the eurlex url
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
            adopt_propos_origine=soup.find("div", {"class": "procedureHeader"}).find(text=re.compile("Adoption by Commission")).lstrip()[:10]
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
    get the com_proc variable from the eurlex url
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


def get_dg_1(soup):
    """
    FUNCTION
    get the dg_1 variable from the eurlex url
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
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
    check that the resp_name string in parameter matches the resp name format: Firstname(s) LASTNAME(S)
    PARAMETERS
    names: resp name? [string]
    RETURN
    True if resp_name is a resp and False otherwise [boolean]
    """
    if names is not None:
        names=names.split()
        first_name=0
        last_name=False
        #check format
        for name in names:
            #checking Firstname(s)
            if not last_name:
                if not name[0].isupper() or not name [1:].islower():
                    #it does not match a first name format and no first name was found before -> this is not a responsible!
                    if first_name==0:
                        return False
                    else:
                        #we are now checking last names
                        last_name=True
                else:
                    #this is a first name
                    first_name=1

            #checking LASTNAME(S)
            if last_name and not name.isupper():
                return False

    #if the string matches the responsible name format (none error was detected), return True
    return True


def get_dg_2_3(soup):
    """
    FUNCTION
    get the dg_2 and dg_3 variable (if any) from the eurlex url
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
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
            #if yes, dg_1 is in the second item
            #if no, dg_1 is in the first item
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
            print "dg_2 except", e
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
    get the resp_1 variable from the eurlex url
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
    get the resp_2 variable and resp_3 variable (if any) from the eurlex url
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    resp_2 variable [string]
    resp_3 variable [string]
    """
    resp_2=None
    resp_3=None
    try:
        #1 dg only (dg_2)
        #(1999-4-2) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:31999D1296
        resps=soup.find("th", text="Leading person:").find_next("th", text="Joint leading service:").find_next('td').get_text().strip()
        #variables separated by a semicolon
        resps=resps.split(";")
        resp_2=resps[0]
        
        #if more than one dg (dg_2 and dg_3)
        #(2005-7-3) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32005D0600
        if len(resps)>1:
            resp_3=resps[1]

    except:
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
    get the transm_council variable from the eurlex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    transm_council: transm_council variable [date]
    """
    transm_council=None
    try:
        #(2014-3-20) http://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:32014L0041 
        if propos_origine!="CONS":
            transm_council=soup.find("div", {"class": "procedureHeader"}).find(text=re.compile("Transmission to Council")).lstrip()[:10]
            #transform dates to the iso format (YYYY-MM-DD)
            transm_council=date_string_to_iso(transm_council)
    except:
        print "pb transm_council"

    return transm_council

#date in front of "Transmission to Council"
#not Null (except blank page -> error on page)
#AAAA-MM-JJ format


def get_nb_point_b(soup, propos_origine):
    """
    FUNCTION
    get the nb_point_b variable from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    nb_point_b: nb_point_b variable [int]
    """
    nb_point_b=None
    try:
        if propos_origine not in ["CONS", "BCE", "EM", "CJUE"]:
            nb_point_b= len(soup.find_all(text=re.compile('ITEM "B"')))
    except:
        print "no nb_point_b!"

    return nb_point_b

#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "B"' on the page
#~ not NULL
#~ De 0 a 20
#~ if propos_origine=="CONS" or "BCE", filled manually


def get_cons_b(soup, propos_origine):
    """
    FUNCTION
    get the cons_b variable from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    cons_b variable [string]
    """
    cons_b=None
    try:
        if propos_origine not in ["CONS", "BCE", "EM", "CJUE"]:
            cons_b_temp=""
            for tables in soup.find_all(text=re.compile('ITEM "B" ON COUNCIL AGENDA')):
                cons_b_temp+=tables.find_parent('table').find(text=re.compile("SUBJECT")).find_next("font", {"size":-2}).get_text().strip()+'; '
            if cons_b_temp!="":
                cons_b=cons_b_temp[:-2]
    except:
        print "no nb_point_b!"

    return cons_b

#can be Null
#in front of SUBJECT, only if the act is processed at B point (preceded by 'ITEM "B" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy
#~ if propos_origine=="CONS", filled manually


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
        nb_no_celex=len(soup.find_all(text=re.compile("Community legislation in force")))
        if nb_no_celex>1:
            print "many no celex"
            split_propos=True
            
    return split_propos
    
    
def get_adopt_conseil(soup, suite_2e_lecture_pe, split_propos, nb_lectures):
    """
    FUNCTION
    get the adopt_conseil variable from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    suite_2e_lecture_pe: suite_2e_lecture_pe variable [boolean]
    split_propos: split_propos variable [boolean]
    nb_lectures: nb_lectures variable [int]
    RETURN
    adopt_conseil: adopt_conseil variable [date]
    """
    adopt_conseil=None

    # if Suite2LecturePE=Y and split_propos=N
    if split_propos==False:
        if suite_2e_lecture_pe or nb_lectures==2:
            try:
                #~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619
                date_table_soup=soup.find("b", text="EP opinion 2nd rdg").find_parent("table")
                # "Approval without amendment"
                if date_table_soup.find(text="Approval without amendment"):
                    #if conditions are met, then get the date
                    adopt_conseil=date_table_soup.find("b").get_text()
                # "Approval with amendment"
                else:
                    date_table_soup=soup.find("b", text="Council approval 2nd rdg").find_parent("table")
                    adopt_conseil=date_table_soup.find("b").get_text()
               
            except Exception, e:
                print "pb AdoptionConseil (case split_propos==0)", e
        elif nb_lectures==3:
            #~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644
            date_table_soup=soup.find("b", text="Council decision at 3rd rdg").find_parent("table")
            #check next table title is "Signature by EP and Council"
            next_table_title=date_table_soup.find_next("table").find(text="Signature by EP and Council")
            #if conditions are met, then get the date
            adopt_conseil=date_table_soup.find("b").get_text()

    # if there is no  2d Lecture at PE
    #~ if no unique type != COD OU nb lectures=1 OU suite_2e_lecture_pe==False:
    if adopt_conseil==None and suite_2e_lecture_pe==False:
        acts=["Formal adoption by Council", "Adoption common position", "Council approval 1st rdg"]
        for act in acts:
            try:
                adopt_conseil=soup.find("a", text=re.compile(act)).find_next('br').next.strip()
                break
            except:
                print "pb", act

    #transform dates to the iso format (YYYY-MM-DD)
    if adopt_conseil!=None:
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


def get_nb_point_a(soup, propos_origine):
    """
    FUNCTION
    get the nb_point_a variable from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    propos_origine: propos_origine variable [string]
    RETURN
    nb_point_a: nb_point_a variable [int]
    """
    nb_point_a=None
    try:
        #~ and propos origine != EM
        if propos_origine not in ["CONS", "BCE", "EM", "CJUE"]:
            nb_point_a=len(soup.find_all(text=re.compile('ITEM "A"')))
    except:
        print "no nb_point_a!"

    return nb_point_a

#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "A"' on the page
#~ not NULL
#~ De 0 a 20
#~ if propos_origine=="CONS" or "BCE", filled manually


def get_council_a(soup):
    """
    FUNCTION
    get the council_a variable from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    RETURN
    council_a: council_a variable [string]
    """
    council_a=None
    try:
        council_a_temp=""
        for tables in soup.find_all(text=re.compile('ITEM "A" ON COUNCIL AGENDA')):
            try:
                council_a_temp+=tables.find_parent('table').find(text=re.compile("SUBJECT")).find_next("font", {"size":-2}).get_text().strip()+'; '
            except Exception, e:
                print "exception council_a", e
                council_a_temp+='None; '
        council_a=council_a_temp[:-2]
    except Exception, e:
        print "no council_a!", e

    return council_a

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


def get_date_diff(date_1, date_2):
    """
    FUNCTION
    compute the difference between two dates
    PARAMETERS
    date_1: first date [date]
    date_2: second date [date]
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
    

    #titre_en
    #~ name='titre_en'
    #~ fields[]=get_titre_en(soup_all)
    #~ print name, fields[name]
#~ 
    #~ #all and his url
    #~ directory_code_soup, tab=get_directory_code(soup_all, soup_his)
#~ 
    #~ #code_sect_1, code_sect_2, code_sect_3, code_sect_4
    #~ code_sects=get_code_sect(directory_code_soup, tab)
#~ 
    #~ #code_agenda_1-4
    #~ save_code_agenda(code_sects)
#~ 
    #~ #print code_sect_* and code_agenda_*
    #~ name='code_sect_'
    #~ for index in xrange(len(code_sects)):
        #~ num=str(index+1)
        #~ #django adds "_id" to foreign keys field names
        #~ fields[name+num+"_id"]=code_sects[index]
        #~ if code_sects[index]!=None:
            #~ print name+num+": ", fields[name+num+"_id"].code_sect
            #~ print 'code_agenda_'+num+": ", fields[name+num+"_id"].code_agenda.code_agenda
#~ 
    #~ #rep_en_1, rep_en_2, rep_en_3, rep_en_4
    #~ rep_ens=get_rep_en(directory_code_soup, tab)
    #~ name='rep_en_'
    #~ for index in xrange(len(rep_ens)):
        #~ num=str(index+1)
        #~ fields[name+num]=rep_ens[index]
        #~ print name+num+": ", fields[name+num]
#~ 
    #~ #type_acte
    #~ name='type_acte'
    #~ fields[name]=get_type_acte(soup_all)
    #~ print name, fields[name]
#~ 
    #~ #base_j
    #~ name='base_j'
    #~ fields[name]=get_base_j(soup_all)
    #~ print name, fields[name]
#~ 
    #~ #date_doc
    #~ name='date_doc'
    #~ fields[name]=get_date_doc(soup_all)
    #~ print name, fields[name]
#~ 
    #~ #nb_mots
    #~ name="nb_mots"
    #~ fields[name]=get_nb_mots(act_ids.no_celex)
    #~ print name, fields[name]


    #TO DO



    #adopt_propos_origine
    #~ name='adopt_propos_origine'
    #~ fields[name]=get_adopt_propos_origine(soup_his, act_ids.propos_origine)
    #~ print name, fields[name]

    #~ #com_proc
    #~ name='com_proc'
    #~ fields[name]=get_com_proc(soup_his, act_ids.propos_origine)
    #~ print name, fields[name]
#~ 
    #dg_1, #dg_2, dg_3
    #~ fields["dg_1"]=get_dg_1(soup_his)
    #~ fields["dg_2"], fields["dg_3"]=get_dg_2_3(soup_his)
    #~ for index in range(nb_dgs):
        #~ index=str(index+1)
        #~ name="dg_"+index
        #~ #dg names as written on eurlex
        #~ dg_names.append(fields[name])
        #~ #DG instances
        #~ fields[name]=get_dgs(fields[name])
        #~ display_dgs(fields[name], name)
#~ 
    #~ print "dg_names", dg_names
    
#~ 
    #~ #resp_1, resp_2, res_3
    
    #~ fields["resp_1"]=get_resp_1(soup_his)
    #~ fields["resp_2"], fields["resp_3"]=get_resp_2_3(soup_his)
    #~ for index in range(nb_resps):
        #~ index=str(index+1)
        #~ name="resp_"+index
        #~ #resp names as written on eurlex
        #~ resp_names.append(fields[name])
        #~ #Person instances
        #~ fields[name]=get_resp(fields[name])
        #~ display_resps(fields[name], name)

    #~ print "resp_names", resp_names

    
    #transm_council
    fields['transm_council']=get_transm_council(soup_his, act_ids.propos_origine)
    print "transm_council:", fields['transm_council']
#~ 
    #~ #nb_point_b
    #~ fields['nb_point_b']=get_nb_point_b(soup, act_ids.propos_origine)
    #~ print "nb_point_b:", fields['nb_point_b']
#~ 
    #~ #cons_b
    #~ fields['cons_b']=get_cons_b(soup, act_ids.propos_origine)
    #~ print "cons_b:", fields['cons_b']

    #~ 
    #~ #check and update split_propos
    #~ fields['split_propos']=get_split_propos(soup, act.split_propos)
    #~ print "split_propos:", fields['split_propos']
#~ 
    #~ #adopt_conseil
    #~ fields['adopt_conseil']=get_adopt_conseil(soup, act.suite_2e_lecture_pe, fields['split_propos'], act.nb_lectures)
    #~ print "adopt_conseil:", fields['adopt_conseil']
#~ 
    #~ #nb_point_a
    #~ fields['nb_point_a']=get_nb_point_a(soup, act_ids.propos_origine)
    #~ print "nb_point_a:", fields['nb_point_a']
#~ 
    #~ #council_a
    #~ fields['council_a']=get_council_a(soup)
    #~ print "council_a:", fields['council_a']
#~ 
    #~ #config_cons
    #~ save_config_cons(act.code_sect_1_id)
#~ 
    #~ #duree_adopt_trans
    #~ fields['duree_adopt_trans']=get_date_diff(fields['transm_council'], fields['adopt_propos_origine'])
    #~ print "duree_adopt_trans:", fields['duree_adopt_trans']
#~ 
    #~ #duree_proc_depuis_prop_com
    #~ fields['duree_proc_depuis_prop_com']=get_date_diff(fields['adopt_conseil'], fields['adopt_propos_origine'])
    #~ print "duree_proc_depuis_prop_com:", fields['duree_proc_depuis_prop_com']
#~ 
    #~ #duree_proc_depuis_trans_cons
    #~ fields['duree_proc_depuis_trans_cons']=get_date_diff(fields['adopt_conseil'], fields['transm_council'])
    #~ print "duree_proc_depuis_trans_cons:", fields['duree_proc_depuis_trans_cons']
#~ 
    #~ #duree_tot_depuis_prop_com
    #~ fields['duree_tot_depuis_prop_com']=get_date_diff(str(act.sign_pecs), fields['adopt_propos_origine'])
    #~ #if no sign_pecs
    #~ if fields['duree_tot_depuis_prop_com']==None:
        #~ fields['duree_tot_depuis_prop_com']=fields['duree_proc_depuis_prop_com']
    #~ print "duree_tot_depuis_prop_com:", fields['duree_tot_depuis_prop_com']
#~ 
    #~ #duree_tot_depuis_trans_cons
    #~ fields['duree_tot_depuis_trans_cons']=get_date_diff(str(act.sign_pecs), fields['transm_council'])
    #~ #if no sign_pecs
    #~ if fields['duree_tot_depuis_trans_cons']==None:
        #~ fields['duree_tot_depuis_trans_cons']=fields['duree_proc_depuis_trans_cons']
    #~ print "duree_tot_depuis_trans_cons:", fields['duree_tot_depuis_trans_cons']
#~ 
    #~ #vote_public
    #~ fields['vote_public']=get_vote_public(act.adopt_cs_contre, act.adopt_cs_abs)
    #~ print "vote_public:", fields['vote_public']
#~ 
    #~ #adopt_pc_contre, #adopt_pc_abs
    #~ adopt_pc=save_get_adopt_pc(act, act_ids)
    #~ if adopt_pc!=None:
        #~ print "adopt_pc_contre:", adopt_pc.adopt_pc_contre
        #~ print "adopt_pc_abs:", adopt_pc.adopt_pc_abs

    return fields, dg_names, resp_names
