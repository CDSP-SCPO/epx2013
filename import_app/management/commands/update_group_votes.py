#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from act.models import Act
from act.get_data_others import save_get_group_votes


class Command(NoArgsCommand):
    """
    COMMAND
    update the group votes variables: for each act with group votes imported in temporary tables only, this command imports them in the real database too
    PARAMETERS
    None
    RETURN
    None
    """
    def handle(self, **options):
        
        for act in Act.objects.filter(validated=2):
            print act
            save_get_group_votes(act)

