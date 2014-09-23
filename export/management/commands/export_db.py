#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf import settings
from export.views import get_headers, get_save_acts
import datetime
import logging
import os
import csv


class Command(NoArgsCommand):
    """
    export all the validated acts of the database
    """

    def handle(self, **options):

        dir_server=settings.MEDIA_ROOT+"/export/"
        today = str(datetime.date.today())
        file_name="acts_"+today+".txt"
        #if a file with the same name already exists, we delete it
        if os.path.exists(dir_server+file_name):
            os.remove(dir_server+file_name)
        #get the headers
        excl_fields_act_ids=["id", 'src', "url_exists", 'act']
        excl_fields_act=["id",  'date_doc', "url_prelex", "validated", "validated_attendance"]
        headers=get_headers(excl_fields_act_ids, excl_fields_act)
        #file to write in
        writer=csv.writer(open(dir_server+file_name, 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        #write headers
        writer.writerow(headers)
        #fetch all the acts of the db and save them into the csv file
        get_save_acts(excl_fields_act_ids, excl_fields_act, writer)

        display="csv export: "+ today
        print display
        # Get an instance of a logger
        #~ logger = logging.getLogger(__name__)
        #~ logger.debug(display)
