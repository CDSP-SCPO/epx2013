#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act_ids.models import ActIds
    

class Command(NoArgsCommand):


    def handle(self, **options):

        for act in ActIds.objects.filter(src="index"):
            print act.releve_annee, act.releve_mois, act.no_ordre
            act.no_celex=act.no_celex.strip()
            act.save()
