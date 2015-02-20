#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from common import css


class Command(NoArgsCommand):
    def handle(self, **options):
        print "hello"
        css2=[css, "10"]
        print css2
     
