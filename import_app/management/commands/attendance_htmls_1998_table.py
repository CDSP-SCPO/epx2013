#-*- coding: utf-8 -*-
"""
command to get the min_attend instances for acts with an attendance_pdf url
"""

from django.core.management.base import NoArgsCommand
#new table
from import_app.models import ImportMinAttend
from act_ids.models import ActIds
from act.models import Country, Verbatim, Status
from django.db import IntegrityError
import re
import time
import urllib
import sys
import os
from bs4 import BeautifulSoup
from django.conf import settings


#get the list of countries from the db
countries_db=Country.objects.values_list('country', flat=True)


def extract_html_1(soup):
    verbatims=[]
    country_list=[]
    last_country=""
    pb=False
    end_attendances=False
    #get attendances
    #sometimes two tables for attendances: http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/educ/doc.69170.htm
    attendances_tables=soup.find_all("table")


    #first two tables contain participants
    for attendances_tr in attendances_tables[:2]:

        if end_attendances:
            break

        for tr in attendances_tr.find_all("tr"):
            
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/07677en8.doc.htm
            if tr.find(text=re.compile("In the case of legislative acts"))==None:
            
                #~ print "tr"
                #~ print tr
                #~ print ""
                
                #commission -> end of participants
                try:
                    com=tr.find("font").get_text()
                    #Commission: http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/6894en8.htm
                    if "***" in ''.join(com.split()) or "Commission" in com:
                        end_attendances=True

                except Exception, e:
                    print "commission", e
                    #just belgium without condition below
                    #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/09116-communiqu%C3%A9-1.doc.html
                    if "United Kingdom" in country_list:
                        end_attendances=True

                if end_attendances:
                    break

                try:
                    #country
                    #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/acf8e.htm
                    #<u>Belgium</u>
                    last_country=tr.find("p").get_text().replace(":","").strip()
                    #pb finland http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/trans/doc.69062.htm
                    if last_country=="":
                        #<p>Sweden:</p>
                        last_country=tr.find("u").get_text().strip()
                    if last_country=="United-Kingdom":
                        last_country="United Kingdom"
                    #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/intm/12188.en1.html
                    elif last_country=="Belgique":
                        last_country="Belgium"
                    country_list.append(last_country)
                    #~ print country_list
                except Exception, e:
                    print "no country", e

                #for each minister, get verbatim
                try:
                    #<td valign="TOP" width="58%">
                    verbatims_temp=tr.find("td").find_next("td").find_all("p")
                    for verbatim_soup in verbatims_temp:
                        verbatim=verbatim_soup.get_text()
                        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/intm/09120.en1.html
                        if verbatim.strip()!="":
                            verbatims.append([last_country, verbatim])
                except Exception, e:
                    print "PROBLEM EXTRACTING DOCUMENT", e

    print""
    print "verbatims"
    for country in verbatims:
        print country[0]+": "+country[1]
    print ""

    if "United Kingdom" not in country_list:
        pb=True

    return verbatims, pb



def get_country(tr):
    last_country=""
    try:
        #country
        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/acf8e.htm
        #<u>Belgium</u>
        last_country=tr.find("p").get_text().replace(":","").strip()
        #pb finland http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/trans/doc.69062.htm
        if last_country=="":
            #<p>Sweden:</p>
            last_country=tr.find("u").get_text().strip()
        if last_country=="United-Kingdom":
            last_country="United Kingdom"
        elif ''.join(last_country.split())=="UnitedKingdom":
            last_country="United Kingdom"
        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/intm/12188.en1.html
        elif last_country=="Belgique":
            last_country="Belgium"
        #~ print country_list
    except Exception, e:
        print "no country", e
    
    
    if last_country not in countries_db:
        last_country=""
        
    return last_country


def get_verbatims(tr, last_country, verbatims):
    #for each minister, get verbatim
    try:
        #<td valign="TOP" width="58%">
        verbatims_temp=tr.find("td").find_next("td").find_all("p")
        for verbatim_soup in verbatims_temp:
            verbatim=verbatim_soup.get_text()
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/intm/09120.en1.html
            if verbatim.strip()!="":
                verbatims.append([last_country, verbatim])
    except Exception, e:
        print "PROBLEM EXTRACTING DOCUMENT", e
    return verbatims




def extract_html_2(soup):
    verbatims=[]
    country_list=[]
    last_country=""
    pb=False
    end_attendances=False
    #get attendances
    #sometimes two tables for attendances: http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/educ/doc.69170.htm
    attendances_tables=soup.find_all("table")

    #first two tables contain participants
    for attendances_tr in attendances_tables:

        for tr in attendances_tr.find_all("tr"):
            
             #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/07677en8.doc.htm
            if tr.find(text=re.compile("In the case of legislative acts"))==None:
            
                    #commission -> end of participants
                    try:
                        com=tr.find("font").get_text()
                        #Commission: http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/6894en8.htm
                        if "***" in ''.join(com.split()) or "Commission" in com:
                            end_attendances=True

                    except Exception, e:
                        print "commission", e
                        #just belgium without condition below
                        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/09116-communiqu%C3%A9-1.doc.html
                        if "United Kingdom" in country_list:
                            end_attendances=True

                    if end_attendances:
                        break
                    
                    #country?
                    last_country_temp=get_country(tr)
                    
                    if last_country_temp!="":
                        last_country=last_country_temp
                        country_list.append(last_country)
                    elif len(country_list)>0:
                        #verbatim?
                        #~ print "last_country"
                        #~ print last_country
                        verbatims=get_verbatims(tr, last_country, verbatims)
    

    print""
    print "verbatims"
    for country in verbatims:
        print country[0]+": "+country[1]
    print ""

    if "United Kingdom" not in country_list:
        pb=True
        print country_list
    print "ok"

    return verbatims, pb
    

def html_to_soup(html):
    #~ print "html"
    #~ print html.read()
    #~ return BeautifulSoup(html, 'html.parser')
    #~ return BeautifulSoup(str(html), 'html5lib')
    return BeautifulSoup(html, 'lxml')
    return BeautifulSoup(html)

    

class Command(NoArgsCommand):
    """
    for each act, get the pdf of the ministers' attendance, extract the relevant information and import it into ImportMinAttend
    run the command from a terminal: python manage.py attendance.pdf
    """

    def handle(self, **options):

        pbs=[]
        src_file="url"
        src_file="db"
        test=False
        
        #~ test=True
        #~ src_file="local"
        
        #delete not validated acts
        #~ ImportMinAttend.objects.filter(validated=False).delete()

        #~ #get all the acts with a non null attendance_path
        #for 1998 or 2001
        acts_ids=ActIds.objects.filter(src="index", act__releve_annee=2001, act__attendance_pdf__isnull=False)

        for act_ids in acts_ids:
#~
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/11825.en8.htm
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/08171.en8.htm
            if "htm" in act_ids.act.attendance_pdf[-4:] and "/fr/" not in act_ids.act.attendance_pdf and "/it/" not in act_ids.act.attendance_pdf:

                already_imported=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=True)
                #~ #if the act has been imported and validated already, don't import it again
                if not already_imported:
                    table_doc=False
                    act=act_ids.act
    #~ #~
                    #TEST ONLY
                    if test and src_file!="db":
                        if src_file=="local":
                            act.attendance_pdf=settings.PROJECT_ROOT+"/import_app/management/commands/files/html_table.html"
                            #open(act.attendance_pdf, encoding='cp1252')
                            html=file(act.attendance_pdf)
                        else:
                            act.attendance_pdf="http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/09116-communiqu%c3%a9-1.doc.html"
                            html=urllib.urlopen(act.attendance_pdf)
                    
                    if not test:
                        html=urllib.urlopen(act.attendance_pdf)
    #~
                    print ""
                    print "act", act
                    print act.attendance_pdf
                    print ""
    #~
                    #~ #get the pdf
                    try:
                        soup=html_to_soup(html)
                    except Exception, e:
                        #wait a few seconds
                        print e
                        print ""
                        time.sleep(3)
                        soup=html_to_soup(html)


                    #~ #extraction documents with table
                    try:
                        tr=None
                        #~ print soup.find("table").
                        tables=soup.find_all("table")
                        for table in tables:
                            belgium=table.find(text=re.compile("Belgium"))
                            if belgium!=None:
                                tr=table.find("tr")
                                break
                        
                        
                        #~ if soup.find("table").find(text=re.compile("In the case of legislative acts"))!=None:
                            #~ tr=soup.find("table").find_next("table")
                        #~ else:
                            #~ tr=soup.find("table")
                        
                        #~ print tr
                            
                        #~ tr=tr.find_parent("tr")
                        tds=tr.find_all("td")
                        nb=0
                        for td in tds:
                            if td.get_text().strip()!="":
                                nb+=1
                            if nb>1:
                                table_doc=1
                                break
                            
                        if table_doc!=1:
                            table_doc=2

                        #~ verbatims=tr.find("td").find_next("td").find_all("p")
                        #~ print verbatims
                        #~ for verbatim in verbatims:
                            #~ verbatim=verbatim.get_text().strip()
                            #~ print "verbatim"
                            #~ print verbatim
                            #~ if verbatim!="" and "Belgium" not in verbatim:
                                   #~ #country and verbatim in one tr
                                    #~ table_doc=1
                                    #~ print "table_doc=1"
                                    #~ break
                        #~ if table_doc!=1:
                            #~ #country and verbatim in two different tr
                            #~ table_doc=2
                            #~ print "table_doc=2"
                    except Exception, e:
                        print "dir document", e
                        #~ break
                        
                        
                    if table_doc==1:
                        print "extract_html_1"
                        verbatims, pb=extract_html_1(soup)
                    elif table_doc==2:
                        print "extract_html_2"
                        verbatims, pb=extract_html_2(soup)
                                        
                        
                    if table_doc!=False:
                        if pb:
                            pbs.append(act)
                        
                        #remove non validated ministers' attendances
                        ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=False).delete()
            #~ #~
                        for country in verbatims:
                            status=None
                            #retrieves the status if the verbatim exists in the dictionary
                            try:
                                verbatim=Verbatim.objects.get(verbatim=country[1])
                                status=Status.objects.get(verbatim=verbatim, country=Country.objects.get(country=country[0])).status
                            except Exception, e:
                                #~ #pass
                                print "no verbatim", e
            #~ #~
                            #add extracted attendances into ImportMinAttend
                            try:
                                ImportMinAttend.objects.create(releve_annee=act.releve_annee, releve_mois=act.releve_mois, no_ordre=act.no_ordre, no_celex=act_ids.no_celex, country=Country.objects.get(country=country[0]).country_code, verbatim=country[1], status=status)
                            except IntegrityError as e:
                                #~ #pass
                                print "integrity error", e
            #~
                        #TEST ONLY
                        if test:
                            break

                        print ""
                        
                    
          
        print ""
        print "pbs"
        print  pbs
        print ""
