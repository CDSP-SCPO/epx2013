from django.core.management.base import NoArgsCommand
from django.db import models
from django.db.models import Count
from act.models import Act
from act_ids.models import ActIds
import csv
import os
from django.conf import settings
from collections import OrderedDict

class Command(NoArgsCommand):
    def handle(self, **options):
        years_list=[str(n) for n in range(1996, 2013)]
        titles={}
        nbs=OrderedDict({})

        titles["prelex ids on eurlex"]=OrderedDict({})
        titles["oeil ids on eurlex"]=OrderedDict({})
        titles["eurlex on prelex"]=OrderedDict({})
        titles["oeil ids on prelex"]=OrderedDict({})
        titles["prelex ids on oeil"]=OrderedDict({})
        titles["eurlex ids on oeil"]=OrderedDict({})

        for year in years_list:
            titles["prelex ids on eurlex"][year]=[0,0]
            titles["oeil ids on eurlex"][year]=[0,0]
            titles["eurlex on prelex"][year]=[0,0]
            titles["oeil ids on prelex"][year]=[0,0]
            titles["prelex ids on oeil"][year]=[0,0]
            titles["eurlex ids on oeil"][year]=[0,0]
            nbs[year]=0


        for title in titles:
            for year in titles[title]:
                #~ print ""
                #~ print "YEAR", year
                acts=Act.objects.filter(releve_annee=year)
                nbs[year]=acts.count()
                #~ print "nb", nbs[year]
                for act in acts:
                    index=ActIds.objects.get(act_id=act, src="index")
                    eurlex=ActIds.objects.get(act_id=act, src="eurlex")
                    oeil=ActIds.objects.get(act_id=act, src="oeil")
                    prelex=ActIds.objects.get(act_id=act, src="prelex")
    #~ #~

                    if eurlex.url_exists:
                        if title=="prelex ids on eurlex":
                            #prelex ids on eurlex
                            if eurlex.propos_annee==index.propos_annee and eurlex.propos_chrono==index.propos_chrono and eurlex.propos_origine==index.propos_origine:
                                titles[title][year][0]+=1

                        if title=="oeil ids on eurlex":
                            #oeil ids on eurlex
                            if eurlex.no_unique_annee==index.no_unique_annee and eurlex.no_unique_chrono==index.no_unique_chrono and eurlex.no_unique_type==index.no_unique_type:
                                titles[title][year][0]+=1
    #~ #~
                    if prelex.url_exists:
                        if title=="eurlex on prelex":
                            #eurlex ids on prelex
                            if prelex.no_celex==index.no_celex:
                                titles[title][year][0]+=1
            #~ #~
                        if title=="oeil ids on prelex":
                            #oeils ids on prelex
                            if prelex.no_unique_annee==index.no_unique_annee and prelex.no_unique_chrono==index.no_unique_chrono and prelex.no_unique_type==index.no_unique_type:
                                titles[title][year][0]+=1
    #~ #~
                    if oeil.url_exists:
                        if title=="prelex ids on oeil":
                            #prelex ids on oeil
                            if oeil.propos_annee==index.propos_annee and oeil.propos_chrono==index.propos_chrono and oeil.propos_origine==index.propos_origine:
                                titles[title][year][0]+=1
        #~ #~
                        if title=="eurlex ids on oeil":
                            #eurlex ids on oeil
                            if oeil.no_celex==index.no_celex:
                                titles[title][year][0]+=1

                #percentages
                if nbs[year]!=0:
                    titles[title][year][1]=round(float(titles[title][year][0])/nbs[year],3)
                else:
                    titles[title][year][1]=0

#~ #~
        #write results in file
        path=settings.PROJECT_ROOT+'/tests/management/commands/washington.csv'
        #~ path="/var/www/europolix/tests/management/commands/washington.csv"
        writer=csv.writer(open(path, 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["nombre d'actes par annee"])
        years_list.insert(0, "")
        writer.writerow(years_list)
        nbs_list=[]
        nbs_list.append("")
        for year in nbs:
            nbs_list.append(nbs[year])
        writer.writerow(nbs_list)
#~ #~
        writer.writerow("")
#~ #~
        writer.writerow(["Nombre d'actes corrects"])
        writer.writerow(years_list)
        for title in titles:
            row=[]
            row.append(title)
            for year in titles[title]:
                row.append(titles[title][year][0])
            writer.writerow(row)

        writer.writerow("")

        writer.writerow(["Pourcentage d'actes corrects"])
        writer.writerow(years_list)
        for title in titles:
            row=[]
            row.append(title)
            for year in titles[title]:
                row.append(titles[title][year][1])
            writer.writerow(row)





            #~ self.stdout.write('MODEL: "%s"' % model._meta.db_table)
