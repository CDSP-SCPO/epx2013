#-*- coding: utf-8 -*-
"""
command to recreate the min_attend instances for validated acts
"""
from django.core.management.base import NoArgsCommand
from act.models import Person, PartyFamily
from import_app.models import ImportRappPartyFamily


class Command(NoArgsCommand):
    """
    python manage.py update_db
    """

    def handle(self, **options):

        i=0
        #update party family of rapporteurs
        for rapp in Person.objects.filter(src="rapp"):
            i+=1
            print "i", i
            print "name", rapp.name
            country=rapp.country
            party=rapp.party
            try:
                party_family=ImportRappPartyFamily.objects.get(party=party).party_family
                PartyFamily.objects.get_or_create(party=party, country=country, party_family=party_family)
            except Exception, e:
                print e
