#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from act.models import Act, Person
from act_ids.models import ActIds
import csv
from act.get_data_prelex import get_adopt_conseil
from act.get_data_oeil import get_nb_lectures
from import_app.get_ids_prelex import get_url_prelex, get_url_content_prelex
from import_app.get_ids_oeil import get_url_oeil, get_url_content_oeil
from django.conf import settings

class Command(NoArgsCommand):
    def handle(self, **options):

        path=settings.PROJECT_ROOT+"/tests/management/commands/"
        error=0
        nb=0
        
        #check adopt_conseil
        headers=["releve_annee", "releve_mois", "no_ordre", "no_celex", "no_unique_type", "nb_lectures", "extracted adopt_conseil", "validated adopt_conseil"]
        writer=csv.writer(open(path+"adopt_conseil.csv", 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(headers)
        
        for act_ids in ActIds.objects.filter(src="index", act__releve_mois=1, act__validated=2, no_unique_type="COD", act__nb_lectures=2):
            act=act_ids.act
            
            if "-" in act_ids.propos_chrono and act_ids.dos_id!=None:
                url=get_url_prelex(act_ids.dos_id)
            else:
                #url saved in the database using the oeil ids in case of a split proposition
                url=act.url_prelex
            url_content=get_url_content_prelex(url)
            extracted_adopt_conseil=get_adopt_conseil(url_content, act.suite_2e_lecture_pe, act.split_propos, act.nb_lectures)
            
            print act.releve_annee, act.releve_mois, act.no_ordre, extracted_adopt_conseil, act.adopt_conseil
            
            row=[act.releve_annee, act.releve_mois, act.no_ordre, act_ids.no_celex, act_ids.no_unique_type, act.nb_lectures, extracted_adopt_conseil, act.adopt_conseil]
            writer.writerow(row)
            
            #~ if str(extracted_adopt_conseil)!=str(act.adopt_conseil):
                #~ error+=1
                #~ if error==3:
                    #~ break
            #~ 
            #~ nb+=1
            #~ if nb==9:
                #~ break
                    
        
        #~ #check nb_lectures
        headers=["releve_annee", "releve_mois", "no_ordre", "no_celex", "no_unique_type", "extracted_nb_lectures", "validated_nb_lectures"]
        writer=csv.writer(open(path+"nb_lectures.csv", 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(headers)
        
        for act_ids in ActIds.objects.filter(src="index", act__validated=2, releve_mois=1).exclude(no_unique_type__in=["COD", "SYN"]):
            act=act_ids.act
            
            url=get_url_oeil(str(act_ids.no_unique_type), str(act_ids.no_unique_annee), str(act_ids.no_unique_chrono))
            url_content=get_url_content_oeil(url)
            extracted_nb_lectures=get_nb_lectures(url_content, act.suite_2e_lecture_pe, act_ids.no_unique_type)
            
            print act.releve_annee, act.releve_mois, act.no_ordre, extracted_nb_lectures, act.nb_lectures
            
            row=[act.releve_annee, act.releve_mois, act.no_ordre, act_ids.no_celex, act_ids.no_unique_type, extracted_nb_lectures, act.nb_lectures]
            writer.writerow(row)
            
            #~ if str(extracted_nb_lectures)!=str(act.nb_lectures):
                #~ error+=1
                #~ if error==3:
                    #~ break
            #~ 
            #~ nb+=1
            #~ if nb==9:
                #~ break


        #check DG
        #~ headers=["dg", "dg_sigle", "year adopt_propos_origine"]
        #~ writer=csv.writer(open(path+"dg.csv", 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        #~ writer.writerow(headers)
        #~ 
        #~ dgs=set()
        #~ for act in Act.objects.filter(validated=2):
            #~ for i in range(1,3):
                #~ dg=getattr(act, "dg_"+str(i))
                #~ if dg!=None:
                    #~ dgs.add((dg.dg.encode("utf-8"), dg.dg_sigle.dg_sigle, act.adopt_propos_origine.year))
        #~ 
        #~ for dg in dgs:
            #~ writer.writerow(dg)
            #~ 
          #~ #check DG
        #~ headers=["dg", "dg_sigle", "year adopt_propos_origine"]
        #~ writer=csv.writer(open(path+"dg.csv", 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        #~ writer.writerow(headers)
        
        
        #check parties (rapps)
        #~ SELECT distinct(party)
        #~ FROM europolix.act_person pe, europolix.act_party pa
        #~ where pe.party_id=pa.id and src="rapp";
        #~ headers=["parties"]
        #~ writer=csv.writer(open(path+"rapp_parties.csv", 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        #~ writer.writerow(headers)
        #~ 
        #~ parties=set()
        #~ for pers in Person.objects.filter(src="rapp"):
            #~ parties.add(pers.party)
        #~ 
        #~ for party in parties:
            #~ writer.writerow([party])
            
