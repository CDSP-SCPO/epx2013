#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act.models import Act, Country
import os
import csv
import re
from django.conf import settings
import sys


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


def save_adopt_cs(instance, field, values, writer):
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
        value=value.strip()
        if value!="":
            field_instance=getattr(instance, field)
            try:
                country=Country.objects.get(country_code=value)

                #check if the country does not exist already for the given adopt_cs variable and act
                if country not in field_instance.all():
                    
                    #save the country in the database
                    field_instance.add(country)
                    
                    #log inserted variables into a file
                    row=[instance.releve_annee, instance.releve_mois, instance.no_ordre, "", "", "no"]
                    if field=="adopt_cs_abs":
                        row[3]=value
                    else:
                        row[4]=value
                    if instance.validated==2:
                        row[5]="yes"
                    writer.writerow(row)
                else:
                    print instance, field, value, "already saved :)."
            except Exception, e:
                print "problem", instance, field, value, ": ", e
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

class Command(NoArgsCommand):
    """
    import adopt_cs variables if not already imported
    """

    def handle(self, **options):

        #read index files
        path=settings.MEDIA_ROOT+"/import/"
        
        #write new adopt_cs variables into a file
        adopt_cs_file=os.path.dirname(__file__)+"/adopt_cs.csv"
        writer=csv.writer(open(adopt_cs_file, 'w'))
        header=["releve_annee", "releve_mois", "no_ordre", "adopt_cs_abs", "adopt_cs_contre", "validated?"]
        writer.writerow(header)
        
        years=[str(n) for n in range(1996, 2013)]
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
                            act=Act.objects.get(releve_annee=releve_annee, releve_mois=releve_mois, no_ordre=no_ordre)
                            
                            #save adopt_cs variables if not already in the database
                            save_adopt_cs(act, "adopt_cs_abs", row[5], writer)
                            save_adopt_cs(act, "adopt_cs_contre", row[6], writer)
                        except Exception, e:
                            print "problem act", releve_annee, releve_mois, no_ordre, "already validated?", e
                      
                    #~ #TESTS ONLY
                    #~ if row[5].strip()!="" or row[6].strip()!="":
                        #~ break
                #~ break
                      
