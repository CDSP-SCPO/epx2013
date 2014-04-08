#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from act.models import Country, Verbatim, Status
import csv


class Command(NoArgsCommand):
    def handle(self, **options):

        file_path="/var/www/europolix/tests/management/commands/attendance_mistakes.csv"
        with open(file_path, 'r') as csv_file:
            header=csv_file.readline()
            reader=csv.reader(csv_file)
            for row in reader:
                verbatim=row[0].strip()
                country=row[1].strip()
                mistake=row[2].strip()
                correction=row[3].strip()

                #find corresponding acts


        print len("Minister of State at the Department of Enterprise, Trade and Employment, at the Department of Education and Science, and at the Department of Communications, Energy and Natural Resources (with special responsibility for Science, Technology, Innovation, the Information Society and Natural Resources")




