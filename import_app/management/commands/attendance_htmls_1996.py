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


def get_participants_press(soup):  
    #<div id="contentPressRelease"><pre>
    participants=soup.find("div", {"id": "contentPressRelease"}).find("pre").get_text()
    index_begin=participants.index("Belgium")
    index_end=participants.index("Commission", index_begin)
    participants=participants[index_begin:index_end]
    
    #remove end of participants
    #http://europa.eu/rapid/press-release_PRES-96-45_en.htm
    #For the Commission:
    if participants[-8:]=="For the ":
        participants=participants[:-8].rstrip()
    
    #http://europa.eu/rapid/press-release_PRES-96-75_en.htm
    #http://europa.eu/rapid/press-release_PRES-96-123_en.htm
    temp=participants
    for i in range(len(temp)-1, -1, -1):
        if temp[i].strip()=="" or  temp[i] in ["*", "o"]:
            participants=participants[:-1]
        else:
            break
    #http://europa.eu/rapid/press-release_PRES-96-36_en.htm
    if "- + -" in participants[-7:]: 
        participants=participants[:-7].rstrip()
        
    #~ print "participants"
    #~ print participants
    #~ print ""

    return participants


def extract_html_press(soup, country_list):
    last_country=None
    temp=""
    verbatims_temp=[]
    verbatims=[]
    participants=get_participants_press(soup)
    
    #split countries 
    for word in participants.split():
        word=word.strip()
        if word!="":
            #country
            if len(word)>1 and (word[-1]==":" or (word in country_list or word=="United")):
                if last_country!=None:
                    verbatims_temp.append([last_country, temp[:-1]])
                    temp=""
                last_country=word.replace(":","")
                #~ print "last_country"
                #~ print last_country
            #verbatim
            elif word not in ["Kingdom", ":"]:
                temp+=word+" "
    
    #United Kingdom
    verbatims_temp.append(["United Kingdom", temp[:-1]]) 
    
    #~ print "verbatims_temp"
    #~ print verbatims_temp
    #~ print ""
    
    #for each country, remove minister's name
    for ministers in verbatims_temp:
        index=-1
        country=ministers[0]
        verbatim=ministers[1]
        
        #~ print "verbatim"
        #~ print verbatim
        #~ print ""
        
        #split if more than 1 minister for a country
        ministers = re.split('Mr |Ms |M. |Mme ', verbatim)
        #~ print "ministers"
        #~ print ministers
        #~ print ""
        
        for minister in ministers:
            verbatim_split=minister.split()
            
            for i in range(len(verbatim_split)-1, -1, -1):
                #http://europa.eu/rapid/press-release_PRES-96-69_en.htm
                if verbatim_split[i].isupper() or verbatim_split[i]=="d'AUBERT":
                    index=minister.index(verbatim_split[i])+len(verbatim_split[i])
                    break
            #if not empty p tag
            if index!=-1:
                verbatim=minister[index+1:].strip().replace("\n", " ").replace("  ", " ")
                if verbatim.strip()!="":
                    verbatims.append([country, verbatim])
            
    return verbatims
    

def get_participants_font(soup):
    begin=False
    participants=[]
    
    #~ print soup.find(text=re.compile("The Governments of the Member States")).find_parent("p")
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


def extract_html_font(soup, country_list):
    verbatims=[]
    last_country=None
    participants=get_participants_font(soup)

    for participant in participants:
        participant=participant.get_text().strip()
        #~ print "participant"
        #~ print participant
        #~ print ""
        #Belgium:
        if ":" in participant:
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/008a0015.htm
            #Pour le Portugal
            participant=participant.replace(":", "").replace("Pour le ", "").rstrip()
            #~ print "participant"
            #~ print participant
        
        #country
        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/gena/028a0047.htm ->United&nbsp;Kingdom
        if participant in country_list or "United" in participant:
            last_country=participant
            #~ print "last_country"
            #~ print last_country
            #~ print ''


        #verbatim
        else:
            #~ print "no country"
            #~ print "'"+participant+"'"
        
            part_split=participant.split()
            for i in range(len(part_split)-1, -1, -1):
                if part_split[i].isupper():
                    index=participant.index(part_split[i])+len(part_split[i])
                    #~ print index
                    break
            #if not empty p tag
            if index!=-1:
                verbatim=participant[index+1:].strip().replace("\n", " ").replace("\r", "").replace("  ", " ")
                #~ print "last_country"
                #~ print last_country
                #~ print ''
                if verbatim!="":
                    verbatims.append([last_country, verbatim])

    return verbatims


def html_to_soup(html):
    #~ print html.read()
    return BeautifulSoup(html, 'html.parser')
    #~ return BeautifulSoup(str(html), 'html5lib')
    #~ return BeautifulSoup(html, 'lxml')
    return BeautifulSoup(html)

    

class Command(NoArgsCommand):
    """
    for each act, get the pdf of the ministers' attendance, extract the relevant information and import it into ImportMinAttend
    run the command from a terminal: python manage.py attendance.pdf
    """

    def handle(self, **options):

        src_file="url"
        src_file="db"
        test=False
        doc=None
        url=None
        urls={}
        
        #~ test=True
        #~ src_file="local"
        #~ 
        #get the list of countries from the db
        country_list=Country.objects.values_list('country', flat=True)

        #~ #get all the acts with a non null attendance_path
        #for 1998 or 2001
        acts_ids=ActIds.objects.filter(src="index", act__releve_annee=1996, act__attendance_pdf__isnull=False)
        
        #write ministers' attendance into a file
        attendance=os.path.dirname(__file__)+"/attendance_1996.csv"
        writer=csv.writer(open(attendance, 'w'))
        header=["releve_annee", "releve_mois", "no_ordre"]
        writer.writerow(header)

        for act_ids in acts_ids:
            
            if act_ids.act.attendance_pdf not in ["1938 ENERGY", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/008a0015.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/001a0022.htm", "http://europa.eu/rapid/press-release_PRES-96-217_en.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/001a0023.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/lsa/017a0007.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/trans/019a0005.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/gena/028a0048.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/008a0016.htm","http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/011a0007.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/001a0024.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/008a0017.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/lsa/013a0004.htm", "http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/001a0025.htm"]:
                
                ok=False
                doc=None
                
                #new attendance html page
                if act_ids.act.attendance_pdf not in urls:
#~
                    #we retrieve only english documents (other languages -> to be filled manually)
                    #http://europa.eu/rapid/press-release_PRES-96-189_en.htm
                    #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/11825.en8.htm
                    if "_PRES" in act_ids.act.attendance_pdf:
                        if "_en.htm" in act_ids.act.attendance_pdf[-7:]:
                            doc="press"
                            #~ url="http://europa.eu/rapid/press-release_PRES-96-8_en.htm"
                    elif "uedocs" in act_ids.act.attendance_pdf and "/en/" in act_ids.act.attendance_pdf:
                        doc="font"
                        #~ url="http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/008a0015.htm" 

                    
                    if doc!=None:
                        already_imported=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=True)
                        #~ #if the act has been imported and validated already, don't import it again
                        if not already_imported:
                            act=act_ids.act
            #~ #~
                            #TEST ONLY
                            if test:
                                if src_file=="local":
                                    #TEST ONLY
                                    doc="press"
                                    doc="font"
                                    
                                    #~ act.attendance_pdf=settings.PROJECT_ROOT+"/import_app/management/commands/files/1996_"+doc+".html"
                                    html=file(act.attendance_pdf)
                                elif src_file=="url":
                                    act.attendance_pdf=url
                            
                            if "html" not in locals():
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


                            #http://europa.eu/rapid/press-release_PRES-96-189_en.htm
                            if  doc=="press":
                                print "press document"
                                verbatims=extract_html_press(soup, country_list)
                            else:
                                #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/ecofin/11825.en8.htm -> font document
                                print "font document"
                                verbatims=extract_html_font(soup, country_list)
                            
                            urls[act.attendance_pdf]=verbatims
                            ok=True
                            
            
                #html page already retrieved
                else:
                    already_imported=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=True)
                     #~ #if the act has been imported and validated already, don't import it again
                    if not already_imported:
                        act=act_ids.act
                        
                        print ""
                        print "act", act
                        print act.attendance_pdf
                        print ""
                        
                        verbatims=urls[act.attendance_pdf]
                        ok=True
                        print
                
                
                #if the verbatims have been extracted
                if ok:

                    print "verbatims"
                    for country in verbatims:
                        print country[0]+": "+country[1]
                    print ""
    
                    #remove non validated ministers' attendances
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
                        
                        #log results into a file
                        #~ row=[act.releve_annee, act.releve_mois, act.no_ordre]
                        #~ writer.writerow(row)
                    
                    print ""
                
                
                 #TEST ONLY
                if test:
                    break
                        

#PBS
#no mr
#http://europa.eu/rapid/press-release_PRES-96-130_en.htm

#pb parser
#~ see above

#~ ENERGY PDF

#~ FOREIGN LANGUAGES
