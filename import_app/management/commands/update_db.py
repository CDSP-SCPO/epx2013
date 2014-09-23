#-*- coding: utf-8 -*-
"""
command to recreate the min_attend instances for validated acts
"""
from django.core.management.base import NoArgsCommand
#new table
from act.models import Verbatim, Status, Country, Act, Person, PartyFamily
from import_app.models import ImportMinAttend, ImportRappPartyFamily
from act_ids.models import ActIds
from act.get_data_others import link_act_min_attend
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
    python manage.py update_db
    """

    def handle(self, **options):

        #~ #update attendance_pdf
        #~ path=settings.MEDIA_ROOT+"/import/"
        #~ years=[str(n) for n in range(2003, 2010)]
        #~ for year in years:
            #~ path_file=path+"RMC_"+year+".csv"
            #~ with open(path_file, 'r') as csv_file_temp:
                #~ #detect delimiter and skip header
                #~ header=csv_file_temp.readline()
                #~ #skip empty lines at the beginning of the file
                #~ while header.strip()=="":
                    #~ header=csv_file_temp.readline()
                #~ delimiter=detect_delim(header)
                #~ reader=csv.reader(csv_file_temp, delimiter=delimiter)
#~
#~
                #~ for row in reader:
                    #~ if row[0].strip()!="":
                        #~ releve_annee=int(row[0])
                        #~ releve_mois=int(row[1])
                        #~ no_ordre=int(row[2])
                        #~ attendance_pdf=row[18].strip().strip(".").lower()
                        #~ if attendance_pdf not in ["", "na"]:
                            #~ print releve_annee, releve_mois, no_ordre
                            #~ try:
                                #~ act=Act.objects.get(releve_annee=releve_annee, releve_mois=releve_mois, no_ordre=no_ordre)
                                #~ act.attendance_pdf=attendance_pdf
                                #~ act.save()
                            #~ except:
                                #~ pass



        #~ path=os.path.dirname(__file__)+"/attendance_pb.csv"
        #~ writer=csv.writer(open(path, 'w'))
        #~ count=0
#~
        #~ min_attends=ImportMinAttend.objects.all()
        #~ for min_attend in min_attends:
             #~ #fill verbatim table
            #~ verbatim, created = Verbatim.objects.get_or_create(verbatim=min_attend.verbatim)
            #~ #fill status table
            #~ try:
                #~ status, created = Status.objects.get_or_create(verbatim=verbatim, country=Country.objects.get(country_code=min_attend.country), status=min_attend.status)
            #~ except Exception, e:
                #~ pbs=ImportMinAttend.objects.filter(verbatim=verbatim, country=min_attend.country)
                #~ header=["releve_annee", "releve_mois", "no_ordre", "no_celex", "verbatim", "country", "status"]
                #~ writer.writerow(header)
                #~ new_status="AB"
                #~ #get the status
                #~ for pb in pbs:
                    #~ if pb.status!="AB":
                        #~ new_status=pb.status
                        #~ print pb.verbatim
#~
                        #~ break
#~
                #~ #update db
                #~ count_local=0
                #~ for pb in pbs:
                    #~ row=[pb.releve_annee, pb.releve_mois, pb.no_ordre, pb.no_celex, pb.verbatim.encode("utf-8"), pb.country, pb.status]
                    #~ writer.writerow(row)
                    #~ if pb.status=="AB":
                        #~ print pb.releve_annee, pb.releve_mois, pb.no_ordre
                        #~ print "verbatim", pb.verbatim
                        #~ print "country", pb.country
                        #~ print "old status", pb.status
                        #~ pb.status=new_status
                        #~ print "new status", pb.status
                        #~ print ""
                        #~ pb.save()
                        #~ count+=1
                        #~ count_local+=1
#~
#~
                #~ #try to save the status again and check that there is no more errors
                #~ if status=="AB":
                    #~ status, created = Status.objects.get_or_create(verbatim=verbatim, country=Country.objects.get(country_code=min_attend.country), status=min_attend.status)
#~
                #~ print count_local, "rows locally updated"
#~
                #~ writer.writerow([""])
#~
        #~ print count, "rows updated"
#~
#~
        #update min_attend for validated acts
        #~ act_ids=ActIds.objects.filter(src="index", act__validated=2)
        #~ for act_id in act_ids:
            #~ print act_id.act
            #~ link_act_min_attend(act_id)

        #trim spaces for no_celex in ImportMinAttend
        #~ for act in ImportMinAttend.objects.all():
            #~ act.no_celex=act.no_celex.strip()
            #~ act.save()

        #update party family of rapporteurs
        for rapp in Person.objects.filter(src="rapp"):
            country=rapp.country
            party=rapp.party
            party_family=ImportRappPartyFamily.objects.get(party=party).party_family
            try:
                PartyFamily.objects.get_or_create(party=party, country=country, party_family=party_family)
            except Exception, e:
                print e
