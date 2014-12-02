#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act.models import Act
from act_ids.models import ActIds
from act.get_data_eurlex import *


class Command(NoArgsCommand):

    def handle(self, **options):

        for act in Act.objects.filter(nb_mots__isnull=True, validated=2):
            print act
            act_ids=ActIds.objects.get(src="index", act=act)
            act.nb_mots=get_nb_mots(act_ids.no_celex)
            act.save()

