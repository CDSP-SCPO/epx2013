#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from act.get_data_eurlex import get_data_eurlex
from bs4 import BeautifulSoup
from act_ids.models import ActIds
#import files
import os


#files paths
path="./files/"
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
#ALL tab
rel_path = "files/eurlex_all.html"
abs_file_path = os.path.join(script_dir, rel_path)
soup_all=BeautifulSoup(open(abs_file_path).read())
#HIS tab
rel_path = "files/eurlex_his.html"
abs_file_path = os.path.join(script_dir, rel_path)
soup_his=BeautifulSoup(open(abs_file_path).read())

#act ids
act_ids=["2014", "3", "20"]
act_ids=ActIds.objects.get(src="index", act__releve_annee=act_ids[0], act__releve_mois=act_ids[1], act__no_ordre=act_ids[2])



class Command(NoArgsCommand):

    def handle(self, **options):
        #test eurlex import
        print act_ids.act
        fields, dg_names, resp_names=get_data_eurlex([soup_all, soup_his], act_ids)
