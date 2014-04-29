#-*- coding: utf-8 -*-
"""
command to get the min_attend instances for acts with an attendance_pdf url
"""

#PACKAGE TO INSTALL
#poppler-utils

from django.core.management.base import NoArgsCommand
#new table
from import_app.models import ImportMinAttend
from act_ids.models import ActIds
from act.models import Country, Verbatim, Status
import urllib
from django.db import IntegrityError
import re
import time
from bs4 import BeautifulSoup
from django.conf import settings


def extract_html(soup):
    verbatims=[]
    country_list=[]
    last_country=""
    pb=False
    end_attendances=False
    #get attendances
    #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/5923en8.htm
    #<P>The Governments of the Member States and the European Commission were represented as follows:</P>
    begin=soup.find("p", text="The Governments of the Member States and the European Commission were represented as follows:")
    print "begin", begin
    #<P ALIGN="CENTER">* * *</P>
    #<b>Commission</b>
    print soup
    end=soup.find_all(text=re.compile("Commission"))
    print "end", end

    #~ print "attendances_tables"
    #~ print attendances_tables
    #~ print ""
    #~ print "len tables"
    #~ print len(attendances_tables)

    #~ for attendances_tr in attendances_tables[1:]:
        #~ print attendances_tr
        #~ print ""
#~ 
        #~ if end_attendances:
            #~ break
#~ 
        #~ for tr in attendances_tr.find_all("tr"):
#~ 
            #~ #commission -> end of participants
            #~ try:
                #~ com=tr.find("font").get_text()
                #~ if "***" in ''.join(com.split()):
                    #~ end_attendances=True
#~ 
            #~ except Exception, e:
                #~ print "commission", e
                #~ #just belgium without condition below
                #~ #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/09116-communiqu%C3%A9-1.doc.html
                #~ if "United Kingdom" in country_list:
                    #~ end_attendances=True
#~ 
            #~ if end_attendances:
                #~ break
#~ 
            #~ try:
                #~ #country
                #~ last_country=tr.find("u").get_text().replace(":","").strip()
                #~ #pb finland http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/trans/doc.69062.htm
                #~ if last_country=="":
                    #~ last_country=tr.find("p").find_next("p").get_text().replace(":","").strip()
                #~ if last_country=="United-Kingdom":
                    #~ last_country="United Kingdom"
                #~ #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/intm/12188.en1.html
                #~ elif last_country=="Belgique":
                    #~ last_country="Belgium"
                #~ country_list.append(last_country)
            #~ except Exception, e:
                #print "no country", e
                #~ pass
#~ 
                #~ #for each minister, get verbatim
                #~ try:
                    #~ verbatims_temp=tr.find("td").find_next("td").find_all("p")
                    #~ for verbatim_soup in verbatims_temp:
                        #~ verbatim=verbatim_soup.get_text()
                        #~ #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/intm/09120.en1.html
                        #~ if verbatim.strip()!="":
                            #~ verbatims.append([last_country, verbatim])
                #~ except Exception, e:
                    #~ print "PROBLEM EXTRACTING DOCUMENT", e

    print ""
    #~ print verbatims
    for country in verbatims:
        print country[0]+": "+country[1]
    print ""

    if "United Kingdom" not in country_list:
        pb=True

    return verbatims, pb


class Command(NoArgsCommand):
    """
    for each act, get the pdf of the ministers' attendance, extract the relevant information and import it into ImportMinAttend
    run the command from a terminal: python manage.py attendance.pdf
    """

    def handle(self, **options):

        #get the list of countries from the db
        country_list=Country.objects.values_list('country', flat=True)
        nb_pbs=0

        #delete not validated acts
        #~ ImportMinAttend.objects.filter(validated=False).delete()

        #~ #get all the acts with a non null attendance_path
        acts_ids=ActIds.objects.filter(src="index", act__releve_annee=1998, act__attendance_pdf__isnull=False)

        for act_ids in acts_ids:
#~
            if "htm" in act_ids.act.attendance_pdf[-4:]:

                already_imported=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=True)
                #~ #if the act has been imported and validated already, don't import it again
                if not already_imported:
                    act=act_ids.act
    #~ #~
                    #TEST ONLY
                    act.attendance_pdf=settings.PROJECT_ROOT+"/import_app/management/commands/files/html.html"
                    #~ act.attendance_pdf="http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/09116-communiqu%c3%a9-1.doc.html"
    #~
                    print ""
                    print "act", act
                    print act.attendance_pdf
                    print ""
    #~
                    #~ #get the pdf
                    try:
                        soup = BeautifulSoup(urllib.urlopen(act.attendance_pdf), 'html.parser')
                    except Exception, e:
                        #wait a few seconds
                        print e
                        print ""
                        time.sleep(3)
                        soup = BeautifulSoup(urllib.urlopen(act.attendance_pdf), 'html.parser')


                    #~ print 'soup'
                    #~ print soup
                    #~ print ""

                    #TODO: extract html page
                    verbatims, pb=extract_html(soup)
                    if pb:
                        nb_pbs+=1
#~
#~ #~
                    #~ #remove non validated ministers' attendances
                    #~ ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=False).delete()
        #~
                    #~ for country in verbatims:
                        #~ status=None
                        #~ #retrieves the status if the verbatim exists in the dictionary
                        #~ try:
                            #~ verbatim=Verbatim.objects.get(verbatim=country[1])
                            #~ status=Status.objects.get(verbatim=verbatim, country=Country.objects.get(country=country[0])).status
                        #~ except Exception, e:
                            #pass
                            #~ print "no verbatim", e
        #~
                        #~ #add extracted attendances into ImportMinAttend
                        #~ try:
                            #~ ImportMinAttend.objects.create(releve_annee=act.releve_annee, releve_mois=act.releve_mois, no_ordre=act.no_ordre, no_celex=act_ids.no_celex, country=Country.objects.get(country=country[0]).country_code, verbatim=country[1], status=status)
                        #~ except IntegrityError as e:
                            #pass
                            #~ print "integrity error", e
        #~ #~
                    #TEST ONLY
                    break

                    print ""

        print "nb pbs", nb_pbs


