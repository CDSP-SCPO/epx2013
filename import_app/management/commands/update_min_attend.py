#-*- coding: utf-8 -*-
"""
command to recreate the min_attend instances for validated acts
"""
from django.core.management.base import NoArgsCommand
#new table
from act.models import Verbatim, Status, Country, Act
from import_app.models import ImportMinAttend
from act_ids.models import ActIds
from act.get_data_others import save_get_min_attend
import os
import csv
from django.conf import settings


class Command(NoArgsCommand):
    """
    run the command in a terminal
    
    python manage.py update_min_attend
    """

    def handle(self, **options):

        #pb duplicate ReleveAnnee=2008, ReleveMois=3, NoOrdre=31

        #~ #update min_attend for validated acts
        act_ids=ActIds.objects.filter(src="index", act__validated=2).exclude(act__releve_annee=2008, act__releve_mois=3, act__no_ordre=31)
        for act_id in act_ids:
            print act_id.act
            save_get_min_attend(act_id)
