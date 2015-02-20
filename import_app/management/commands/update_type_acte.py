#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act.models import Act
from act_ids.models import ActIds
from import_app.get_ids_eurlex import get_url_eurlex, get_url_content_eurlex
from act.get_data_eurlex import *


class Command(NoArgsCommand):

    def handle(self, **options):
        
        #get type_act for acts of 2014 NOT YET VALIDATED AND VALIDATE THEM for the statistical analysis
        for act in Act.objects.filter(type_acte__isnull=True, validated=2, releve_annee=2014):
            print act
            #url content
            no_celex=ActIds.objects.get(src="index", act=act).no_celex
            url=get_url_eurlex(no_celex)
            soup=get_url_content_eurlex(url)
            #type acte
            act.type_acte=get_type_acte(soup)
            act.save()

