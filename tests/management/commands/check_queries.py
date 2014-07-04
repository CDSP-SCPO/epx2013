#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from act.models import Act, CodeSect
import csv
from django.conf import settings

class Command(NoArgsCommand):
    def handle(self, **options):

        #save to file
        check_queries_file=settings.PROJECT_ROOT+"/tests/management/commands/check_queries.csv"
        writer=csv.writer(open(check_queries_file, 'w'))
        
        annee=1998
        code_sect="03"
        
        writer.writerow(["Vérification actes AdoptCSContre=Y pour " + str(annee) + " et le code sectoriel "+code_sect])
        writer.writerow([])
        headers=["releve_annee", "releve_mois", "no_ordre", "cs", "num cs", "nb adopt_cs_contre"]
        writer.writerow(headers)

        #acts of 2000
        acts=Act.objects.filter(validated=2, releve_annee=annee)  
        for act in acts:
            
            for i in range(1, 5):
                cs=getattr(act, "code_sect_"+str(i))
                if cs!=None:
                    cs=cs.code_sect
                    if cs[:2]==code_sect:
                        row=[act.releve_annee, act.releve_mois, act.no_ordre, cs, i, len(act.adopt_cs_contre.all())]
                        writer.writerow(row)
                
            
