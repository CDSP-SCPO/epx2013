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
    
    #~ print soup
    next_node=soup.find(text=re.compile("Belgium")).find_parent("p")
     #~ next_node=soup.find(text=re.compile("The Governments of the Member States")).find_next('p')
    #~ print "first"
    #~ print next_node
    #~ print ""
    
    while True:
        #~ print "next_node"
        #~ print next_node
        #~ print ""

        if 'Commission' in next_node.text:
            #~ print "youpi com"
            break
        else:
            participants.append(next_node)

        next_node = next_node.find_next()
    
    #if minister of uk in same tag than commission
    #http://europa.eu/rapid/press-release_PRES-97-19_en.htm
    if "United Kingdom" in participants[-1].text:
        participants.append(next_node.find("li"))
    else:
        for participant in participants[-5:]:
            trouve=False
            if "United Kingdom" in participant.text:
                trouve=True
        if not trouve:
            next_node = next_node.find_next()
            if 'Commission' not in next_node.text:
                participants.append(next_node)
                next_node = next_node.find_next("li")
                participants.append(next_node)

    #remove empty items at the end
    #~ temp=participants[:-1]
    if  "*" in participants[-1].text:
        del participants[-1]
        #~ temp=participants[-1].get_text().strip()
    #~ 
    #~ print "participants"
    #~ print participants
    #~ print ""

    return participants


def extract_html(soup, country_list):
    verbatims=[]
    temp_verbatims_country=[]
    last_country=""
    participants=get_participants(soup)
     
    for participant in participants:
        participant=participant.get_text().strip()
        #~ print "participant"
        #~ print participant
        #~ print ""
        #Belgium:
        if participant.strip()!="" and participant[-1]==":":
            participant=participant[:-1].rstrip()
        part_split=participant.split()
        
        #country
        if participant in country_list:
            if participant!=last_country:
                temp_verbatims_country=[]
            last_country=participant
        
        #verbatim
        else:
            #separate minister's name and verbatim
            for i in range(len(part_split)-1, -1, -1):
                if part_split[i].isupper():
                    index=participant.index(part_split[i])+len(part_split[i])
                    break
            #if not empty p tag, add verbatim
            if index!=-1:
                verbatim=participant[index+1:].strip().replace("\n", " ")
                if verbatim.strip()!="":
                    if len(verbatims)==0:
                        verbatims.append([last_country, verbatim])
                    elif last_country!=verbatims[-1][0] or verbatim!=verbatims[-1][1]:
                        if verbatim not in temp_verbatims_country:
                            verbatims.append([last_country, verbatim])
                            temp_verbatims_country.append(verbatim)
                
#~ 
    print ""
    print "verbatims"
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
        attendance=os.path.dirname(__file__)+"/attendance_1997_press.csv"
        writer=csv.writer(open(attendance, 'w'))
        header=["releve_annee", "releve_mois", "no_ordre"]
        writer.writerow(header)

        for act_ids in acts_ids:
#~
            if "htm" in act_ids.act.attendance_pdf[-4:] and "/nl/" not in act_ids.act.attendance_pdf and act_ids.act.attendance_pdf!="http://europa.eu/rapid/press-release_PRES-97-292_en.htm":

                already_imported=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=True)
                #~ #if the act has been imported and validated already, don't import it again
                if not already_imported:
                    act=act_ids.act
    #~ #~
                    #TEST ONLY
                    if test and src_file!="db":
                        if src_file=="local":
                            act.attendance_pdf=settings.PROJECT_ROOT+"/import_app/management/commands/files/press.html"
                            #open(act.attendance_pdf, encoding='cp1252')
                            html=file(act.attendance_pdf)
                        else:
                            act.attendance_pdf="http://europa.eu/rapid/press-release_PRES-97-19_en.htm"
                            html=urllib.urlopen(act.attendance_pdf)
                    
                    if not test or test and  src_file=="db":
                        act.attendance_pdf=act.attendance_pdf.replace("_pres", "_PRES")
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
#~ 
                    print ""
                        
