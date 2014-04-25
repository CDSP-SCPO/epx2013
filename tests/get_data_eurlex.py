#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get data from Eurlex (data for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup


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

#At the top, below "Procedure"
#not NULL


def get_directory_code(soup):
    """
    FUNCTION
    get the html code of the directory code part from the eurlex url
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    directory code part  [BeautifulSoup object]
    """
    #~ 32004D0280
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

    try:
        return soup.find("td", {"id": "directoryCodeProc"}).find_all("span")
    except:
        print "no directory code section!"
        return None


def get_code_sect(directory_code):
    """
    FUNCTION
    get the CodeSect1-4 variables from the eurlex url
    PARAMETERS
    directory_code: html source of each directory code [list of BeautifulSoup objects]
    RETURN
    code_sects: code_sect_* variables [list of CodeSect model instances]
    """
    code_sects=[None for i in range(4)]
    try:
        for i in range(len(directory_code)):
            code_sects[i]=directory_code[i].find(text=True).strip()
    except Exception, e:
        print "no code_sect_*!", e

    return code_sects

#first, second, third and fourth code next to "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#first not NULL
#second, third and fourth: can be null



def get_rep_en(directory_code):
    """
    FUNCTION
    get the rep_en_1, rep_en_2, rep_en_3 and rep_en_4 variables from the eurlex url
    PARAMETERS
    directory_code: html source of each directory code [list of BeautifulSoup objects]
    RETURN
    rep_ens: rep_en_* variab1es [list of strings]
    """
    rep_ens=["" for i in range(4)]

    try:
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
        misc=soup.find(text=re.compile("Miscellaneous information")).find_parent().find_next("div", {"class": "tabContent"})
        #author part
        author=misc.find("b", text=re.compile("Author:")).next_sibling.strip().lower()
        #form part
        form=misc.find("b", text=re.compile("Form:")).next_sibling.strip().lower()

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
    except:
        print "no type_acte!"
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
        li=soup.find_next("b", text=re.compile("Legal basis:")).find_parent('li')
        legal_bases=li.find_all('a')
        var=""
        for legal_base in legal_bases:
            var+=legal_base.get_text().strip()+legal_base.next_sibling.strip()+"; "

        return var[:-2]
    except:
        print "no base_j!"
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
        return soup.find("b", text=re.compile("of document")).next_sibling.strip()
    except Exception, e:
        print "no date gvt_compo!", e
        return None

#under "Dates"... "of document"
#not NULL


def get_data_eurlex(soup, act_ids=None, act=None):
    """
    FUNCTION
    get all data from the eurlex url
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    data: retrieved data from eurlex [dictionary]
    """
    data={}

    #<div id="content">
    soup=soup.find("div", {"id": "content"})

    #titre_en
    data['titre_en']=get_titre_en(soup)
    print "titre_en:", data['titre_en']

    directory_code_soup=get_directory_code(soup)

    #code_sect_1, code_sect_2, code_sect_3, code_sect_4
    code_sects=get_code_sect(directory_code_soup)


    #print code_sect_* and code_agenda_*
    for index in xrange(len(code_sects)):
        num=str(index+1)
        #django adds "_id" to foreign keys field names
        data['code_sect_'+num+"_id"]=code_sects[index]
        if code_sects[index]!=None:
            print 'code_sect_'+num+": ", data['code_sect_'+num+"_id"]

    #rep_en_1, rep_en_2, rep_en_3, rep_en_4
    rep_ens=get_rep_en(directory_code_soup)
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

    return data, None, None
