#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act_ids.models import ActIds
    

class Command(NoArgsCommand):


    def handle(self, **options):

        for act_ids in ActIds.objects.filter(src="index"):
            act=act_ids.act
            print act.releve_annee, act.releve_mois, act.no_ordre
            act_ids.no_celex=act_ids.no_celex.strip()
            act_ids.save()
