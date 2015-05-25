#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act_ids.models import ActIds
from import_app.get_ids_eurlex import get_url_eurlex, get_url_content_eurlex
from act.get_data_eurlex import get_adopt_propos_origine


class Command(NoArgsCommand):
    """
    COMMAND
    check empty dates on already validated fields (transm_council, adopt_propos_origin, adopt_council) -> if empty on validation but a value is present in the database, it was manually added -> let's fix this!
    PARAMETERS
    None
    RETURN
    None
    """
    def handle(self, **options):
        
        for act_ids in ActIds.objects.filter(src="index", act__validated=2, act__releve_annee=2013):
            act=act_ids.act
            print act
            print "act.adopt_propos_origine", act.adopt_propos_origine
            
            url=get_url_eurlex(act_ids.no_celex, tab="HIS")
            soup_his=get_url_content_eurlex(url)
            soup_his=soup_his.find("div", {"class": "tabContent"})
            #remove script tags
            [s.extract() for s in soup_his('script')]
            
            adopt_propos_origine=get_adopt_propos_origine(soup_his, act_ids.propos_origine)
            print "adopt_propos_origine", adopt_propos_origine

            if str(adopt_propos_origine)!=str(act.adopt_propos_origine):
                print "DIFFERENT"
                break

