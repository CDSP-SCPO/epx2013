#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act.models import Act
from import_app.views import get_save_act_ids
import os
import csv
from django.conf import settings

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

        #update act_ids due to a problem on eurlex, oeil or prelex (click on actualisation button on act_ids form for a range of acts)
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
                    if row[0].strip()!="":
                        ids_row={}
                        ids_row["releve_annee"]=int(row[0])
                        ids_row["releve_mois"]=int(row[1])
                        ids_row["no_ordre"]=int(row[2])
                        print ids_row["releve_annee"], ids_row["releve_mois"], ids_row["no_ordre"]
                        #actualisation button -> use acts ids retrieval from the import module
                        get_save_act_ids([ids_row])
