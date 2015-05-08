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
import csv



def get_participants(soup):
    begin=False
    participants=[]
    
    begin_participants=soup.find(text=re.compile("The Governments of the Member States")).find_parent("p")
    next_node = begin_participants.find_next('p')
    
    while True:
        #~ print "next_node", next_node
        if 'Commission' in next_node.text:
            break
        else:
            participants.append(next_node)
        
        next_node = next_node.find_next('p')
            
    #~ #remove empty items at the end
    temp=participants[-1].get_text().strip()
    while temp=="" or "*" in temp or "+" in temp:
        del participants[-1]
        temp=participants[-1].get_text().strip()
    
    #~ print "participants"
    #~ print participants
    #~ print ""

    return participants


def extract_html(soup, country_list):
    verbatims=[]
    last_country=""
    participants=get_participants(soup)
     
    for participant in participants:
        participant=participant.get_text().strip()
        #Belgium:
        if participant[-1]==":":
            participant=participant[:-1].rstrip()
        part_split=participant.split()
        
        #country
        if participant in country_list:
            last_country=participant
        
        #verbatim
        else:
            for i in range(len(part_split)-1, -1, -1):
                if part_split[i].isupper():
                    index=participant.index(part_split[i])+len(part_split[i])
                    #~ print index
                    break
            #if not empty p tag
            if index!=-1:
                verbatim=participant[index+1:].strip().replace("\n", " ")
                verbatims.append([last_country, verbatim])

    print ""
    print "verbatims"
    #~ print verbatims
    for country in verbatims:
        print country[0]+": "+country[1]
    print ""


    return verbatims


def html_to_soup(html):
    #~ print html.read()
    #~ return BeautifulSoup(html, 'html.parser')
    #~ return BeautifulSoup(str(html), 'html5lib')
    #~ return BeautifulSoup(html, 'lxml')
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
        
        #get the list of countries from the db
        country_list=Country.objects.values_list('country', flat=True)

        #~ #get all the acts with a non null attendance_path
        #for 1998 or 2001
        acts_ids=ActIds.objects.filter(src="index", act__releve_annee=1997, act__attendance_pdf__isnull=False)
        
        #write ministers' attendance into a file
        attendance=os.path.dirname(__file__)+"/attendance_1997_font.csv"
        writer=csv.writer(open(attendance, 'w'))
        header=["releve_annee", "releve_mois", "no_ordre"]
        writer.writerow(header)

        for act_ids in acts_ids:
#~
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/11825.en8.htm
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/08171.en8.htm
            if "htm" in act_ids.act.attendance_pdf[-4:]:

                already_imported=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=True)
                #~ #if the act has been imported and validated already, don't import it again
                if not already_imported:
                    act=act_ids.act
    #~ #~
                    #TEST ONLY
                    if test and src_file!="db":
                        if src_file=="local":
                            act.attendance_pdf=settings.PROJECT_ROOT+"/import_app/management/commands/files/font.html"
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
                    if not soup.find("dir") and "12241en7.doc.htm" not in act.attendance_pdf and "13140en7.doc.htm" not in act.attendance_pdf and "13370en7.doc.htm" not in act.attendance_pdf and "13138en7.doc.htm" not in act.attendance_pdf and "13373en7.doc.htm" not in act.attendance_pdf:
                        print "font document"
                        verbatims=extract_html(soup, country_list)
                        
                        #TEST ONLY
                        if test:
                            break
                        
                        

                        
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
                            #~ 
                            #~ #log results into a file
                            row=[act.releve_annee, act.releve_mois, act.no_ordre]
                            writer.writerow(row)

                        print ""
                        
