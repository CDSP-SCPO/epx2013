#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act.models import Act
from act_ids.models import ActIds
from act.get_data_eurlex import *


class Command(NoArgsCommand):

    def handle(self, **options):
        
        #get nb_mots for acts of 2014 NOT YET VALIDATED AND VALIDATE THEM for the statistical analysis
        for act in Act.objects.filter(validated=1, releve_annee=2014):
            print act
            act_ids=ActIds.objects.get(src="index", act=act)
            act.nb_mots=get_nb_mots(act_ids.no_celex)
            act.validated=2
            act.save()

