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
import csv
import os


def get_participants(soup):
    begin=False
    participants=[]
    
    for item in soup.find_all('p'):
        if not begin:
            #start criteria
            if item.text=="Belgium":
                begin=True
                participants.append(item)
        else:
            #stopping criteria
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/gena/07684en8.doc.htm
            if ('*') in item.text:
                break
            participants.append(item)
    
    #~ print "participants"
    #~ print participants
    #~ print ""
    #~ 
    #remove empty items at the end
    while participants[-1].get_text().strip()=="":
        del participants[-1]
    
    #~ print "participants"
    #~ print participants
    #~ print ""
        
    return participants


def extract_html(soup, country_list):
    verbatims=[]
    last_country=""
    participants=get_participants(soup)
    
    #~ print "country_list"
    #~ for country in country_list:
        #~ print country
    #~ print ""
    
    for participant in participants:
        participant=participant.get_text().strip()
        #~ print participant
        
        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/gena/6060en8.htm
        if "UnitedKingdom" in "".join(participant.split()):
            participant="United Kingdom"
            
        #country
        if participant in country_list:
            last_country=participant
        #verbatim
        else:
            index=participant.rfind("\t")
            #if not empty p tag
            if index!=-1:
                verbatim=participant[index+1:]
                verbatims.append([last_country, verbatim])

    print ""
    #~ print verbatims
    for country in verbatims:
        print country[0]+": "+country[1]
    print ""


    return verbatims


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
        acts_ids=ActIds.objects.filter(src="index", act__releve_annee=1997, act__releve_mois=12, act__attendance_pdf__isnull=False)
        
        #write ministers' attendance into a file
        attendance=os.path.dirname(__file__)+"/attendance_1997_dir.csv"
        writer=csv.writer(open(attendance, 'w'))
        header=["releve_annee", "releve_mois", "no_ordre"]
        writer.writerow(header)

        for act_ids in acts_ids:
#~
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/5923en8.htm
            if "htm" in act_ids.act.attendance_pdf[-4:] and "/en/" in act_ids.act.attendance_pdf:

                already_imported=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=True)
                #~ #if the act has been imported and validated already, don't import it again
                if not already_imported:
                    act=act_ids.act
    #~ #~
                    #TEST ONLY
                    #~ act.attendance_pdf=settings.PROJECT_ROOT+"/import_app/management/commands/files/html_dir.html"
                    #~ act.attendance_pdf="http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/gena/6060en8.htm"
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
                    
                    verbatims=None
                    
                    #extraction documents with dir tag, python2.7
                    try:
                        soup.find("table").find(text=re.compile("Belgium"))
                    except Exception, e:
                        try:
                            soup.find("dir")
                            print "dir document", e
                            print "act", act
                            print act.attendance_pdf
                            print ""
                            verbatims=extract_html(soup, country_list)
                        except Exception, e:   
                            print "not a dir doc", e 

#~
                    if verbatims!=None:
                        #~ #remove non validated ministers' attendances
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
                            
                        #log results into a file
                        row=[act.releve_annee, act.releve_mois, act.no_ordre]
                        writer.writerow(row)
            #~ #~
                        
                        print ""
