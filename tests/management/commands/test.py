#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User


class Command(NoArgsCommand):
    def handle(self, **options):
        password = User.objects.make_random_password(length=8)
        print password
        #~ user.set_password(password)



