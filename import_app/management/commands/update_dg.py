#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
#models
from act.models import Act, DG
import re
from common.config_file import nb_dgs


class Command(NoArgsCommand):

    def handle(self, **options):
        #make uniform the list of dg:
        #"Administration", "DG Administration", "Administration DG", "Directorate-General for the Administration":  same DG!
        #only one DG needed: "DG Administration" (all the DGs must start with "DG")

        #store old and new dg names
        dgs={}
        print "get old and new values"
        for dg in DG.objects.all():
            new_dg=dg.dg
            #remove dg / directorate-general at the beginning or end
            pattern = re.compile("dg | dg", re.IGNORECASE)
            new_dg=pattern.sub("", new_dg)
            pattern = re.compile("^directorate-general( for)?( the)?|directorate-general( for)?( the)?$", re.IGNORECASE)
            new_dg=pattern.sub("", new_dg)
            new_dg="DG "+new_dg.strip()
            #add to the dictionary of dgs to update if the name has changed
            if dg.dg != new_dg:
                dgs[dg.dg.encode("utf-8")]=new_dg.encode("utf-8")
                print dg.dg.encode("utf-8") + " -> " + new_dg.encode("utf-8")


        #~ #update database (dg in Act model, DG model and dg_nb)
        print "update DG model"
        for old_value, new_value in dgs.iteritems():
            old_dg=DG.objects.get(dg=old_value)
    
            #~ #update DG model: add new DGs (DG model with dg_sigle)
            new_dg=DG.objects.get_or_create(dg=new_value, defaults={"dg_sigle": old_dg.dg_sigle})
#~ 
            #NO NEED because all dgs with numbers are linked to dg with a correct name already
            #update dg_nb association: get dgs with nb linked to the current dg and associate them with the new dg
            for dg_nb in old_dg.dg_nb.all():
                print dg_nb.dg
                new_dg.dg_nb.add(dg_nb)

            #remove old links
            old_dg.dg_nb.clear()
#~ 
        #update Act model and all their dgs
        print "update Act model"
        for act in Act.objects.all():
            for index in range(1, nb_dgs+1):
                #if the act has a reference to an old dg, update it
                field_name="dg_"+str(index)
                dg=getattr(act, field_name)
                if dg is not None and dg.dg in dgs:
                    setattr(act, field_name, DG.objects.get(dg=dgs[dg.dg]))
                    print str(act)+": "+ dg.dg+" -> "+ dgs[dg.dg]
#~ 
            #~ #save the modifications if any
            act.save()
#~ 
        #~ #remove old DGs
        print "delete old dgs from DG model"
        for dg in DG.objects.all():
            if dg.dg[:2] != "DG":
                dg.delete()
