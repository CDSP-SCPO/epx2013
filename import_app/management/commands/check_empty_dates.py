#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act_ids.models import ActIds
from import_app.get_ids_eurlex import get_url_eurlex, get_url_content_eurlex
from act.get_data_eurlex import get_point_b_tables, get_date_cons_b, get_point_a_tables, get_date_cons_a


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
        
        for act_ids in ActIds.objects.filter(src="index", act__validated=2):
            act=act_ids.act
            print act
            
            url=get_url_eurlex(act_ids.no_celex, tab="HIS")
            soup_his=get_url_content_eurlex(url)
            soup_his=soup_his.find("div", {"class": "tabContent"})
            #remove script tags
            [s.extract() for s in soup_his('script')]
            
            adopt_propos_origine=get_adopt_propos_origine(soup, propos_origine)
            print "adopt_propos_origine", adopt_propos_origine
            print "act.adopt_propos_origine", act.adopt_propos_origine

            if adopt_propos_origine!=act.adopt_propos_origine:
                print "DIFFERENT"
                break
            
            act.save()
