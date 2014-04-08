#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from act.models import Country, Verbatim, Status
from import_app.models import ImportMinAttend
import csv


class Command(NoArgsCommand):
    def handle(self, **options):

        #check status errors
        path="/var/www/europolix/tests/management/commands/"
        headers=["releve_annee", "releve_mois", "no_ordre", "no_celex", "verbatim", "country", "status"]
        with open(path+"status_mistakes.csv", 'r') as csv_file:
            status_errors=[]
            header=csv_file.readline()
            status_errors.append(["wrong status"])
            status_errors.append(headers)
            reader=csv.reader(csv_file)

            for row in reader:
                verbatim=row[0].strip()
                country=row[1].strip()
                wrong_status=row[2].strip()
                right_Status=row[3].strip()

                #find corresponding acts
                acts=ImportMinAttend.objects.filter(verbatim=verbatim, country=country, status=wrong_status)
                for act in acts:
                    status_errors.append([act.releve_annee, act.releve_mois, act.no_ordre, act.no_celex, act.verbatim.encode("utf-8"), act.country, act.status])

        #check verbatim <> AB and status= AB
        wrong_ab=[]
        wrong_ab.append(["status=AB and verbatim different from AB"])
        wrong_ab.append(headers)
        acts=ImportMinAttend.objects.filter(status="AB").exclude(verbatim="AB")
        for act in acts:
            wrong_ab.append([act.releve_annee, act.releve_mois, act.no_ordre, act.no_celex, act.verbatim.encode("utf-8"), act.country, act.status])


        #write results inside a file
        writer=csv.writer(open(path+"attendance_problems.csv", 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

        for error in status_errors:
            writer.writerow(error)
        writer.writerow([""])
        for error in wrong_ab:
            writer.writerow(error)


