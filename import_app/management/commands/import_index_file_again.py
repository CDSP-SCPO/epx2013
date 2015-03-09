#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
#models
from act.models import Act
from act_ids.models import ActIds
from import_app.views import get_save_act_ids
import os
import csv
from django.conf import settings
#adopt vars
from import_app.views import save_adopt_cs_pc, none_or_var


def detect_delim(header):
    """
    FUNCTION
    detect the delimiter of a csv file and return it
    PARAMETERS
    header: first line of a csv file [string]
    RETURN
    delimiter character [char]
    """
    if header.find(";")!=-1:
        #~ print "delimiter=';'"
        return ";"
    if header.find(",")!=-1:
        #~ print "delimiter=','"
        return ","
    #default delimiter (MS Office export)
    return ";"
    

class Command(NoArgsCommand):

    def handle(self, **options):

        #import act_ids already imported with mistakes AND new acts, and devalidate acts with mistakes
        path=settings.MEDIA_ROOT+"/import/"
        #~ path="/home/rom/Documents/jobs/SciencesPo/europolix/import/csv/"
        years=[str(n) for n in range(2014, 2015)]
        for year in years:
            path_file=path+"RMC_"+year+".csv"
            with open(path_file, 'r') as csv_file_temp:
                #detect delimiter and skip header
                header=csv_file_temp.readline()
                #skip empty lines at the beginning of the file
                while header.strip()=="":
                    header=csv_file_temp.readline()
                delimiter=detect_delim(header)
                reader=csv.reader(csv_file_temp, delimiter=delimiter)

                for row in reader:
                    #used to identify the row
                    ids_row={}
                    ids_row["releve_annee"]=int(row[0])
                    ids_row["releve_mois"]=int(row[1])
                    ids_row["no_ordre"]=int(row[2])


                    #if created is True, we just have to save the act data
                    #if created is False, the act was already validated, we have to update its fields and then devalidate it if there is at least one difference IN THE ACT IDS
                    act, created_act=Act.objects.get_or_create(**ids_row)

                    print "act", act
                    if created_act:
                        print "created act"
                    else:
                        print "already exist"
                    

                    #save ActIds model fields and check for differences
                    ids_row={}
                    ids_row["src"]="index"
                    ids_row["act"]=act
                    act_ids, created_actids=ActIds.objects.get_or_create(**ids_row)

                    compare={}
                    compare["no_celex"]=row[7].strip()
                    compare["propos_annee"]=none_or_var(row[8], "int")
                    compare["propos_chrono"]=none_or_var(row[9].replace(" ", ""), "str")
                    compare["propos_origine"]=none_or_var(row[10], "str")
                    compare["no_unique_annee"]=none_or_var(row[11], "int")
                    compare["no_unique_type"]=none_or_var(row[12], "str")
                    compare["no_unique_chrono"]=none_or_var(row[13], "str")

                    #the act ids instance already exist, let's check if the data have changed
                    same=True
                    if not created_act:
                        for field_name, field_value in compare.iteritems():
                            #not the same data -> the act must be validated again
                            if str(getattr(act_ids, field_name)) != str(field_value):
                                print str(getattr(act_ids, field_name)), str(field_value), "DIFFERENT!!!"
                                print "TYPE:", type(getattr(act_ids, field_name)), type(field_value)
                                same=False
                                break
                            
                    act_ids.no_celex=compare["no_celex"]
                    act_ids.propos_annee=compare["propos_annee"]
                    act_ids.propos_chrono=compare["propos_chrono"]
                    act_ids.propos_origine=compare["propos_origine"]
                    act_ids.no_unique_annee=compare["no_unique_annee"]
                    act_ids.no_unique_type=compare["no_unique_type"]
                    act_ids.no_unique_chrono=compare["no_unique_chrono"]
                    

                    #save Act model fields
                    act.titre_rmc=row[3].strip()
                    act.adopt_cs_regle_vote=row[4].strip()
                    if row[14].strip()=="Y":
                        act.split_propos=True
                    if row[15].strip()=="Y":
                       act.suite_2e_lecture_pe=True
                    council_path=row[16].strip().strip(".")
                    if council_path!="":
                        act.council_path=council_path
                    act.notes=row[17].strip()


                    #if the act existed already, delete m2m relations
                    if not created_act:
                        act.adopt_cs_abs.clear()
                        act.adopt_cs_contre.clear()
                    #save adopt_cs variables
                    save_adopt_cs_pc(act, "adopt_cs_abs", row[5])
                    save_adopt_cs_pc(act, "adopt_cs_contre", row[6])

                  

                    #if the act already existed but at least one field was different, devalidate it
                    if not created_act and not same:
                        print "the act need to be validated again!!!"
                        act.validated=0
                        act.save()
                    #~ 
                    #~ #save act_ids
                    act_ids.save()

                    #save act ids on eurlex and oeil
                    ids_row={}
                    ids_row["releve_annee"]=int(row[0])
                    ids_row["releve_mois"]=int(row[1])
                    ids_row["no_ordre"]=int(row[2])
                    get_save_act_ids([ids_row])
