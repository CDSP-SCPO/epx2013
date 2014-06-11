#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act.models import Act, Country
import os
import csv
import re
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


def save_adopt_cs(instance, field, values):
    """
    FUNCTION
    save the coutries for adopt_cs_contre, adopt_cs_abs
    PARAMETERS
    instance: instance of the act [Act model instance]
    field: name  of the field (adopt_cs_contre, adopt_cs_abs) [string]
    values: countries [list of strings]
    RETURN
    None
    """
    #countries separated by a comma or a semi-column
    values=re.split(';|,',values)
    
    #the instance must have an id to add many to many fields
    #~ instance.save()
    for value in values:
        if value!="":
            field_instance=getattr(instance, field)
            try:
                field_instance.add(Country.objects.get(pk=value.strip()))
                print instance
                print "saving", field, value
                print ""
            except Exception, e:
                print field+" already exists!", e

class Command(NoArgsCommand):
    """
    import adopt_cs variables for non-validated acts if not imported yet (1997 only)
    """

    def handle(self, **options):

        #update attendance_pdf
        path=settings.MEDIA_ROOT+"/import/"
        #year 1997 only
        years=[str(n) for n in range(1997, 1998)]
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
                        releve_annee=int(row[0])
                        releve_mois=int(row[1])
                        no_ordre=int(row[2])
                        
                        try:
                            #discard already validated acts
                            act=Act.objects.get(releve_annee=releve_annee, releve_mois=releve_mois, no_ordre=no_ordre, validated__lt=2)
                            
                            #save adopt_cs variables if not already in the database
                            save_adopt_cs(act, "adopt_cs_abs", row[5])
                            save_adopt_cs(act, "adopt_cs_contre", row[6])
                        except Exception, e:
                            print "act", releve_annee, releve_mois, no_ordre, "already validated!", e
                        
                        
                      
