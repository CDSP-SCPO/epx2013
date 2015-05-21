#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act_ids.models import ActIds
from import_app.get_ids_eurlex import get_url_eurlex, get_url_content_eurlex
from act.get_data_eurlex import get_point_b_tables, get_date_cons_b, get_point_a_tables, get_date_cons_a


class Command(NoArgsCommand):
    """
    COMMAND
    update the date_cons_a and date_cons_b variables for acts validated before the two fields were used
    PARAMETERS
    None
    RETURN
    None
    """
    def handle(self, **options):
        
        for act_ids in ActIds.objects.filter(src="index", act__validated=2, act__date_cons_a__isnull=True, act__date_cons_b__isnull=True):
            act=act_ids.act
            print act
            
            url=get_url_eurlex(act_ids.no_celex, tab="HIS")
            soup_his=get_url_content_eurlex(url)
            soup_his=soup_his.find("div", {"class": "tabContent"})
            #remove script tags
            [s.extract() for s in soup_his('script')]
            
            point_b_tables=get_point_b_tables(soup_his, act_ids.propos_origine)
            act.date_cons_b=get_date_cons_b(point_b_tables)
            print "date_cons_b", act.date_cons_b
            point_a_tables=get_point_a_tables(soup_his, act_ids.propos_origine)
            act.date_cons_a=get_date_cons_a(point_a_tables)
            print "date_cons_a", act.date_cons_a

            act.save()
