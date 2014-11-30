#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get data from Eurlex (data for the statistical analysis)
"""
import re
import urllib
from bs4 import BeautifulSoup
from act.models import CodeSect
from common.functions import list_reverse_enum, date_string_to_iso
from common.db import save_fk_code_sect, save_get_object
from common import config_file as conf


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
        if form=="regulation":
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
    #~ print "element", element
    #~ print ""
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    #remove '\n'
    elif element.encode('utf-8').strip()=='':
        return False
    elif re.match('<!--.*-->', element.encode('utf-8')):
        return False
    return True


def get_nb_mots(no_celex):
    """
    FUNCTION
    get the number of words of the text of the act from the eurlex url
    PARAMETERS
    no_celex: no_celex of the act [string]
    RETURN
    nb_mots [string]
    """
    #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:31996R0122&from=EN
    #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32006L0031&from=EN
    #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32010R0053&from=EN
    url=conf.url_text_act
    url=url.replace("NOCELEX", no_celex, 1)
    print url
    soup=BeautifulSoup(urllib.urlopen(url))
    try:
        #page not found
        #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32004R0854&from=EN
        if soup.title.string=="The requested document does not exist. - EUR-Lex":
            print None
            return None
    except Exception, e:
        #http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32006D1982&from=EN
        print "link to 2 documents (STATEMENTS)", e
        return None
    texts = soup.findAll(text=True)
    visible_texts = filter(visible, texts)
    nb_mots=0
    for text in visible_texts:
        nb_mots+=len(text.split())
    print nb_mots
    return nb_mots



def get_data_eurlex(soups, no_celex):
    """
    FUNCTION
    get all data from the eurlex url
    PARAMETERS
    soups: eurlex url content from the all and his tab [list of BeautifulSoup objects]
    no_celex: no_celex of the act [string]
    RETURN
    data: retrieved data from eurlex [dictionary]
    """
    data={}

    #<div id="content">
    soup=soups[0].find("div", {"id": "content"})

    #titre_en
    data['titre_en']=get_titre_en(soup)
    print "titre_en:", data['titre_en']

    #all and his url
    directory_code_soup, tab=get_directory_code(soup, soups[1])

    #code_sect_1, code_sect_2, code_sect_3, code_sect_4
    code_sects=get_code_sect(directory_code_soup, tab)

    #code_agenda_1-4
    save_code_agenda(code_sects)

    #print code_sect_* and code_agenda_*
    for index in xrange(len(code_sects)):
        num=str(index+1)
        #django adds "_id" to foreign keys field names
        data['code_sect_'+num+"_id"]=code_sects[index]
        if code_sects[index]!=None:
            print 'code_sect_'+num+": ", data['code_sect_'+num+"_id"].code_sect
            print 'code_agenda_'+num+": ", data['code_sect_'+num+"_id"].code_agenda.code_agenda

    #rep_en_1, rep_en_2, rep_en_3, rep_en_4
    rep_ens=get_rep_en(directory_code_soup, tab)
    for index in xrange(len(rep_ens)):
        num=str(index+1)
        data['rep_en_'+num]=rep_ens[index]
        print 'rep_en_'+num+": ", data['rep_en_'+num]

    #type_acte
    data['type_acte']=get_type_acte(soup)
    print "type_acte:", data['type_acte']

    #base_j
    data['base_j']=get_base_j(soup)
    print "base_j:", data['base_j']

    #date_doc
    data['date_doc']=get_date_doc(soup)
    print "date_doc:", data['date_doc']

    #nb_mots
    data['nb_mots']=get_nb_mots(no_celex)
    print "nb_mots:", data['nb_mots']

    return data
