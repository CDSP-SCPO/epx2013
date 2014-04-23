#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act.models import Act
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
    """
    import attendance_pdf for a specific year / range of years
    """

    def handle(self, **options):

        #update attendance_pdf
        path=settings.MEDIA_ROOT+"/import/"
        #~ path="/home/rom/Documents/jobs/SciencesPo/europolix/import/csv/"
        years=[str(n) for n in range(2001, 2002)]
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
                        attendance_pdf=row[18].strip().strip(".").lower()
                        if attendance_pdf not in ["", "na"]:
                            print releve_annee, releve_mois, no_ordre
                            try:
                                act=Act.objects.get(releve_annee=releve_annee, releve_mois=releve_mois, no_ordre=no_ordre)
                                act.attendance_pdf=attendance_pdf
                                act.save()
                                print act.attendance_pdf
                                print ""
                            except Exception, e:
                                print e
