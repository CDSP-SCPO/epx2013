#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from act.models import Act


class Command(NoArgsCommand):

    def handle(self, **options):

        stop=False
        for act in Act.objects.filter(validated=2):
            #~ if stop:
                #~ break
            for index in range(8):
                var="group_vote_"+str(index)
                votes=getattr(act, var)
                if votes is not None:
                    for number, vote in enumerate(votes.split(";")):
                        #cohesion column
                        #~ print vote
                        if number==7 and vote not in [None, "None", ""] and float(vote)>100:
                            print act
                            print var
                            print vote
                            #~ stop=True
                            #~ break
                
                
