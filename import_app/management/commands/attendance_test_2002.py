#-*- coding: utf-8 -*-
"""
command to get the min_attend instances for acts with an attendance_pdf url
"""

#PACKAGE TO INSTALL
#poppler-utils

from django.core.management.base import NoArgsCommand
#new table
from import_app.models import ImportMinAttend
from act_ids.models import ActIds
from act.models import Country, Verbatim, Status
import urllib, urllib2, time, os, tempfile, subprocess
from django.db import IntegrityError


def pdf_to_string(file_object):
    """
    FUNCTION
    get the text of a pdf and put it in a string variable
    PARAMETERS
    file_object: pdf file wrapped in a python file object [File object]
    RETURN
    string: extracted text [string]
    """
    pdfData = file_object.read()

    tf = tempfile.NamedTemporaryFile()
    tf.write(pdfData)
    tf.seek(0)

    outputTf = tempfile.NamedTemporaryFile()

    if (len(pdfData) > 0) :
        out, err = subprocess.Popen(["pdftotext", "-layout", tf.name, outputTf.name ]).communicate()
        return outputTf.read()
    else :
        return None


def find_nth(string, substring, n):
    """
    FUNCTION
    return the index of the occurence number n of substring in a string
    PARAMETERS
    string: string to use for the search [string]
    substring: string to be found [string]
    n: number of the occurence [int]
    RETURN
    start: index of the occurence number n [int]
    """
    start = string.find(substring)
    while start >= 0 and n > 1:
        start = string.find(substring, start+len(substring))
        n -= 1
    return start


#CHANGED
def get_participants(string):
    """
    FUNCTION
    extract the participant part from the pdf (just before the ITEMS DEBATED section)
    PARAMETERS
    string: text extracted from the pdf [string]
    RETURN
    string: participant part [string]
    """

    begin=end=-1

    #Belgium
    begin=string.find("%HOJLXP")

    print "begin", begin
    #if no begin found, go to then begin of the string
    if begin==-1:
        begin=0

    #Commission
    end=string.find("&RPPLVVLRQ", begin)

    print "end", end
    #if no end found, go to then end of the string
    if end==-1:
        end=len(string)-begin-1

    return string[begin:end].split('\n')



def capitalized_word(words, display=False):
    """
    FUNCTION
    check if there is at least one capitalized word in a group of words
    PARAMETERS
    words: group of words to check [string]
    RETURN
    True if there is at least one capitalized word, False otherwise [boolean]
    """
    #Micheál MARTIN without Mr or Ms

    #PROVISIO AL VERSIO: http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/envir/99178.pdf
    #not any(char.isdigit() for char in word): discard dates (roman numerals are in upper case)
    if words!="PROVISIO AL VERSIO" and not any(char.isdigit() for char in words):
        words=words.split()
        excluded_list=["EU","EN"]
        for word in words:
            #word.isupper() is what we really want to test
            #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/lsa/111599.pdf
            #len(word)>1: "E" (problem with N of EN)
            if word.isupper() and len(word)>1 and word not in excluded_list:
                if display:
                    print "word", word
                    print "word.isupper()", word.isupper()
                    print "not any(char.isdigit() for char in word)", not any(char.isdigit() for char in word)
                    print "word not in [EU,EN]", word not in ["EU","EN"]
                return True

    return False


def format_country(country):
    return country.split(" ")[0].replace("\x1d", "").strip().replace(":", "")


#CHANGED
def format_participants(participants, country_list):
    """
    FUNCTION
    get the participants only from the participants part (remove extra or unreadble characters, blanks, header, footer...)
    keep only countries, ministers' names and verbatims
    PARAMETERS
    participants: text of the participant part split at each line break [list of strings]
    country_list: list of EU countries [list of string]
    RETURN
    new_participants: participants part (countries, ministers' names and verbatims)  [list of strings]
    """
    new_participants=[]

    #~ print "begin participants"
    #~ print participants
    #~ print ""

    #separate 'Mr Didier REYNDERS                  Deputy Prime Minister and Minister for Foreign Affairs,'
    for participant in participants:
        participant=participant.strip()
        #remove empty items
        if participant!="":
            #~ print "participant", participant
            if participant[:2].lower() in ["mr", "ms", "mme"] or capitalized_word(participant):
                for i in range(len(participant)):
                    #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/trans/72370.pdf
                    #long name so only one space between name and verbatim
                    long_name="Ms Melanie SCHULTZ van HAEGEN-MAAS GEESTERANUS"
                    if long_name in participant:
                        #add Mr or Ms
                        new_participants.append(long_name)
                        #add verbatim
                        verbatim_index=participant.index(long_name)+len(long_name)
                        new_participants.append(participant[verbatim_index:].strip())
                        break
                    elif participant[i]==" " and participant[i+1]==" ":
                        #add Mr or Ms
                        new_participants.append(participant[:i].strip())
                        #add verbatim
                        new_participants.append(participant[i:].strip())
                        break
                else:
                    new_participants.append(participant)
            else:
                new_participants.append(participant)

    print "begin new_participants"
    print new_participants
    print ""

    #start the list with the first participant (Belgium)
    for participant in new_participants:
        if format_country(participant)=="%HOJLXP":
            index_belgium=new_participants.index(participant)
            break

    new_participants=new_participants[index_belgium:]

    #~ print "begin new_participants WITH header / footer"
    #~ print new_participants
    #~ print ""

    #if two pages, remove footer and header of separation
    begin=end=-1
    for i in range(len(new_participants)):
        #'Ms Audron MORNIEN', 'Deputy minister for Social Security and Labour', '16611/2/09 REV 2 (en) (Presse 348)                                                                             5', 'E', '30.XI-1.XII.2009', 'Luxembourg:', 'Mr Mars DIBO'
        if any(char.isdigit() for char in new_participants[i].strip()) and format_country(new_participants[i]) not in country_list:
            if begin==-1:
                begin=i
                print "BEGIN OK"
                print new_participants[i].strip()

        #new page starts with a minister's name from a country started on the previous page
        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/gena/87078.pdf
        #or new page starts with a new country
        if begin!=-1 and (new_participants[i].lstrip()[:2].lower() in ["mr", "ms", "mme"] or capitalized_word(new_participants[i], True) or format_country(new_participants[i]) in country_list):
            #~ print "PB"
            #~ print new_participants[i]
            #~ print new_participants[i-5:i+5]
            #~ capitalized_word(new_participants[i], True)
            #~ print ""
            new_participants=new_participants[:begin]+new_participants[i:]
            break
#~
    #~ print "begin new_participants WITHOUT header / footer"
    #~ print new_participants
    #~ print ""

    #stop after last country (uk usually)
    index_uk=len(new_participants)-1
    for participant in new_participants:
        #Commission
        if format_country(participant)=="&RPPLVVLRQ":
            index_uk=new_participants.index(participant)
            break

        if ''.join(participant.split())=="***":
            index_uk=new_participants.index(participant)
            #~ print 'uk ok'
            break
        #~ else:
            #~ print participant.strip()

    new_participants=new_participants[:index_uk]

    #remove "*" before the word "Commission"
    for i, element in reversed(list(enumerate(new_participants))):
        if "*" not in element:
            new_participants=new_participants[:i+1]
            break

    #~ print "new_participants"
    #~ print new_participants
    #~ print ""
    return new_participants


#CHANGED
def get_countries(participants, country_list):
    """
    FUNCTION
    for each country, group together the country name and its ministers' names and verbatims
    PARAMETERS
    participants: list of participants split at each line break [list of strings]
    country_list: list of EU countries [list of string]
    RETURN
    countries: participants with countries and associated ministers grouped together [list of lists of strings / lists]
    """
    print "participants"
    print participants
    print ""
    countries=[]
    for index in range(len(participants)):
        #~ print "participant", participant
        country=format_country(participants[index])
        #problem when conversion from pdf to text
        if country=="etherlands":
            country="Netherlands"
        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/101422.pdf
        #'Ms Michelle GILDERNEW', 'Minister for Agriculture and Rural Development, Northern', 'Ireland']
        #http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/70070.pdf
        #'Portugal :', 'Mr Jaime SILVA', 'Agricultural Counsellor at the Permanent Representation of', 'Portugal', 'Finland :
        if country in country_list and index<len(participants)-1 and format_country(participants[index+1]) not in country_list:
            countries.append([country_list[country], []])
        else:
            countries[-1][1].append(participants[index])

    print "countries"
    print countries
    print ""
    print "nb countries", len(countries)
    print ""
    return countries


def get_verbatims(countries, country_list):
    """
    FUNCTION
    get the final format of the ministers' attendance: remove ministers' name and split the country into as many parts as there are ministers
    PARAMETERS
    participants: list of participants split at each line break [list of strings]
    country_list: list of EU countries [list of string]
    RETURN
    countries: participants with countries and associated ministers grouped together [list of lists of strings / lists]
    """
    verbatims=[]
    #~ print "countries"
    #~ print countries
    #~ print ""

    #check that each country starts with a minister's name, not a verbatim
    #-> pb Belgium with http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/75376.pdf
    #['Belgium', ['Minister, attached to the Minister for Foreign Affairs, with', 'Ms Annemie NEYTS-UTTENBROEK', 'responsibility for Agriculture', 'Mr Jos\xc3\xa9 HAPPART', 'Minister for Agriculture and Rural Affairs (Walloon Region)', 'Ms Vera DUA', 'Minister for the Environment and Agriculture (Flemish Region)']]
    #~ print "countries BEFORE moving ministers", countries
    #~ print ""
    nb_pbs=[0, ""]
    for country in countries:
        first=country[1][0].lstrip()
        #pb
        if first[:2].lower() not in ["mr", "ms", "mme"] or not capitalized_word(first):
            for index in range(len(country[1])):
                if country[1][index].lstrip()[:2].lower() in ["mr", "ms", "mme"] or capitalized_word(country[1][index]):
                    #move the minister to the first place
                    #['Belgium', ['Ms Annemie NEYTS-UTTENBROEK', 'Minister, attached to the Minister for Foreign Affairs, with', 'responsibility for Agriculture', 'Mr Jos\xc3\xa9 HAPPART', 'Minister for Agriculture and Rural Affairs (Walloon Region)', 'Ms Vera DUA', 'Minister for the Environment and Agriculture (Flemish Region)']]
                    country[1].insert(0, country[1].pop(index))
                    nb_pbs[0]+=1
                    nb_pbs[1]+=country[0]+ ";"
                    break
#~
    #~ print 'NB DIFFS', nb_pbs
    #~ print ""
    #~ print "countries AFTER moving ministers", countries
    #~ print ""


    #remove ministers' names and group long verbatims split into more than one item
    for country in countries:
        #~ print "country", country
        for minister in country[1]:
            #new minister for the country
            if minister.lstrip()[:2].lower() in ["mr", "ms", "mme"] or capitalized_word(minister):
                #~ print "mr ms", minister
                verbatims.append([country[0], ""])
            else:
                #~ print "verbatim", minister
                #for long verbatims in 2 or more lines
                #~ print "verbatims", verbatims
                if verbatims[-1][1]=="":
                    separator=""
                else:
                    separator=" "
                verbatims[-1][1]+=separator+minister
            #~ print "verbatims", verbatims
        #~ break

    #~ print "no more ministers' names"
    #~ print verbatims
    #~ print ""

    #remove extra blank spaces
    for country in verbatims:
        country[1]=' '.join(country[1].split())


    #display final result
    for country in verbatims:
        print country[0]+": "+country[1]
    print ""
    print "nb different countries", len(countries)
    print "nb countries", len(verbatims)
    print ""
    return verbatims




class Command(NoArgsCommand):
    """
    for each act, get the pdf of the ministers' attendance, extract the relevant information and import it into ImportMinAttend
    run the command from a terminal: python manage.py attendance.pdf
    """

    def handle(self, **options):

        #get the list of countries from the db
        country_list={}
        country_list["%HOJLXP"]="Belgium"
        country_list["'HQPDUN"]="Denmark"
        country_list["*HUPDQ\\"]="Germany"
        country_list["*UHHFH"]="Greece"
        country_list["6SDLQ"]="Spain"
        country_list[")UDQFH"]="France"
        country_list[",UHODQG"]="Ireland"
        country_list[",WDO\\"]="Italy"
        country_list["/X[HPERXUJ"]="Luxembourg"
        country_list["1HWKHUODQGV"]="Netherlands"
        country_list["$XVWULD"]="Austria"
        country_list["3RUWXJDO"]="Portugal"
        country_list[")LQODQG"]="Finland"
        country_list["6ZHGHQ"]="Sweden"
        country_list["8QLWHG"]="United Kingdom"

        #Commission: &RPPLVVLRQ


        file_path="/var/www/europolix/import_app/management/commands/files/"
        #~ for year in range(2003, 2014):
            #~ file_name=str(year)
        file_name="test"
        print "year", file_name
        file_object=open(file_path+file_name+".pdf",'r')
        #~ file_object = urllib2.urlopen("http://www.consilium.europa.eu/uedocs/cms_data/docs/pressdata/en/agricult/101422.pdf")

        #read the pdf and assign its text to a string
        string=pdf_to_string(file_object)
        participants=get_participants(string)
        #~ print "BEGIN TEST"
        #~ print participants
        #~ print "END TEST"
        #~ print ''

        #format the string variable to get the countries and verbatims only
        #~ participants=file_to_string(file_path+file_name+".txt")
        participants=format_participants(participants, country_list)
        countries=get_countries(participants, country_list)
        verbatims=get_verbatims(countries, country_list)





