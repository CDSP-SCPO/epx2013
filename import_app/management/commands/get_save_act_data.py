#-*- coding: utf-8 -*-
"""
command to retrieve data on eurlex and oeil automatically and validate the act
"""
from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User
from act.models import Act
from history.models import History

from common.db import get_act_ids
from act.views import get_urls, get_data, check_multiple_dgs, store_dg_resp
from act.get_data_others import get_data_others


def set_empty_dg(dg):
    if dg in [[], [None], [None, None]] :
        return None
    return dg

class Command(NoArgsCommand):
    """
    python manage.py get_data
    """

    def handle(self, **options):
        
        #~ acts_to_validate=[]
        #~ acts_to_validate.append([2003, 10, 1])
        #~ acts_to_validate.append([2003, 10, 9])
        #~ acts_to_validate.append([2003, 10, 10])
        #~ 
        #~ for act_ids in acts_to_validate:
            
            #~ act=Act.objects.get(releve_annee=act_ids[0], releve_mois=act_ids[1], no_ordre=act_ids[2])

        #import and "validate" acts not yet validated by experts
        for act in Act.objects.filter(validated=1):
            
            #the act has not been validated yet
            if act.validated==1:
                
                #retrieve the act ids for each source
                act_ids=get_act_ids(act)

                #"compute" the url of the eurlex and oeil page
                urls=get_urls(act_ids["index"])

                #get data on oeil
                fields, dg_names_oeil, resp_names_oeil=get_data("oeil", act_ids, urls["url_oeil"])
                act.__dict__.update(fields)
    
                #get data on eurlex
                fields, dg_names_eurlex, resp_names_eurlex=get_data("eurlex", act_ids, urls["url_eurlex"])
                act.__dict__.update(fields)
                

                #pb empty dgs (empty list instead of None)
                fields["dg_1_id"]=set_empty_dg(fields["dg_1_id"])
                fields["dg_2_id"]=set_empty_dg(fields["dg_2_id"])
                fields["dg_3_id"]=set_empty_dg(fields["dg_3_id"])
                act.__dict__.update(fields)
                
                #~ #store dg/resp from eurlex and oeil to be displayed as text in the template
                act=store_dg_resp(act, dg_names_eurlex, dg_names_oeil, "dg")[0]
                act=store_dg_resp(act, resp_names_eurlex, resp_names_oeil, "resp")[0]

                #~ #check multiple values for dgs with numbers
                act=check_multiple_dgs(act)[1]

                #set value for releve_mois_init
                act.releve_mois_init=act.releve_mois
                   
                #update opal, min_attend
                get_data_others(act_ids["index"], act)
               
                #validate the act
                act.validated=2
                
                #set false to empty booleans
                if act.modif_propos==None:
                    act.modif_propos=False
                
                print "act"
                fields= act.__dict__
                for field, value in fields.items():
                    print field, value
                
                #save the act
                print act.__dict__
                act.save()
                
                print "the act", act, "has been validated :)."
                print ""
                
                #add entry in history
                History.objects.create(action="add", form="data", act=act, user=User.objects.get(username="romain.lalande"))
            
            else:
                print "the act", act, "has already been validated!!"
                print ""
