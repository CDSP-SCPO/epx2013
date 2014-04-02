"""
command to recreate the min_attend instances for validated acts
"""
from django.core.management.base import NoArgsCommand
#new table
from import_app.models import ImportMinAttend
from act_ids.models import ActIds
from act.models import Country, Verbatim
import urllib, urllib2, time, os, tempfile, subprocess


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


def get_participants(string):
    """
    FUNCTION
    extract the participant part from the pdf (just before the ITEMS DEBATED section)
    PARAMETERS
    string: text extracted from the pdf [string]
    RETURN
    string: participant part [string]
    """
    begin=-1
    participants=["PARTICIPA(cid:6)TS", "PARTICIPANTS", "PARTICIPA TS"]
    for participant in participants:
        begin=find_nth(string, participant, 2)
        if begin!=-1:
            break
    print "begin", begin
    end=string.find("ITEMS DEBATED", begin)
    print "end", end
    return string[begin:end]



def string_to_file(string, path):
    """
    FUNCTION
    save a string into a txt file
    PARAMETERS
    string: string to save [string]
    path: path of the file to use [string]
    RETURN
    None
    """
    with open(path, "w") as text_file:
        text_file.write(string)


def file_to_string(path):
    """
    FUNCTION
    get the text of a txt file
    PARAMETERS
    path: path of the file to use [string]
    RETURN
    participants: text of the file split at each line break [list of strings]
    """
    with open(path) as string:
        participants=string.read().split('\n')
    return participants


def capitalized_word(words):
    """
    FUNCTION
    check if there is at least one capitalized word in a group of words
    PARAMETERS
    words: group of words to check [string]
    RETURN
    True if there is at least one capitalized word, False otherwise [boolean]
    """
    #Micheál MARTIN without Mr or Ms
    words=words.split()
    for word in words:
        if word.isupper() and word!="EU":
            return True
    return False


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
    #~ for participant in participants:
        #~ print participant

    #separate 'Mr Didier REYNDERS                  Deputy Prime Minister and Minister for Foreign Affairs,'
    for participant in participants:
        participant=participant.strip()
        #~ print "participant", participant
        if participant[:2].lower() in ["mr", "ms"] or capitalized_word(participant):
            for i in range(len(participant)):
                if participant[i]==" " and participant[i+1]==" ":
                    #add Mr or Ms
                    new_participants.append(participant[:i].strip())
                    #add verbatim
                    new_participants.append(participant[i:].strip())
                    break
            else:
                new_participants.append(participant)
        else:
            new_participants.append(participant)

    #start the list with the first participant (Belgium)
    for participant in new_participants:
        if participant.strip() in ["Belgium:", "Belgium :"]:
            index_belgium=new_participants.index(participant)
            break

    new_participants=new_participants[index_belgium:]

    #if two pages, remove footer and header of separation
    begin=end=-1
    for i in range(len(new_participants)):
        #~ print "new_participants[i]", new_participants[i]
        if new_participants[i].strip()=="":
            if begin==-1:
                begin=i
        elif new_participants[i].split(":")[0].strip() in country_list and begin!=-1:
            new_participants=new_participants[:begin]+new_participants[i:]
            break

    print "new_participants", new_participants
    print ""

    #stop after last country (uk usually)
    for participant in new_participants:
        if participant.strip() in ["Commission:", "Commission :"]:
            index_uk=new_participants.index(participant)
            break

    new_participants=new_participants[:index_uk]
    for i, element in reversed(list(enumerate(new_participants))):
        if element.strip()!="" and "*" not in element:
            new_participants=new_participants[:i+1]
            break

    #~ print "new_participants", new_participants
    #~ print ""
    return new_participants


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
    countries=[]
    for participant in participants:
        #~ print "participant", participant
        country=participant.split(":")[0].strip()
        #problem when conversion from pdf to text
        if country=="etherlands":
            country="Netherlands"
        if country in country_list:
            countries.append([country, []])
        else:
            countries[-1][1].append(participant)

    print countries
    print ""
    #~ print "nb countries", len(countries)
    #~ print ""
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
    for country in countries:
        #~ print "country", country
        for minister in country[1]:
            #new minister for the country
            #~ print "minister", minister
            if minister.lstrip()[:2].lower() in ["mr", "ms"] or capitalized_word(minister):
                #~ print "mr ms", minister
                verbatims.append([country[0], ""])
            else:
                #~ print "verbatim", minister
                #for long verbatims in 2 or more lines
                if verbatims[-1][1]=="":
                    separator=""
                else:
                    separator=" "
                verbatims[-1][1]+=separator+minister
            #~ print "verbatims", verbatims
        #~ break

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
        country_list=Country.object.values_list('country', flat=True)

        #get all the acts with a non null attendance_path
        acts_ids=ActIds.objects.filter(src="index").exclude(act__attendance_path__isnull=True)
        for act_ids in acts_ids:
            already_imported=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=True)
            #if the act has been imported and validated already, don't import it again
            if not already_imported:

                act=act_ids.act
                #name of the file
                print ""
                print "act", filename
                print ""

                #get the pdf
                file_object = urllib2.urlopen(act.attendance_path)

                #read the pdf and assign its text to a string
                string=pdf_to_string(file_object)
                string=get_participants(string)
                #~ string_to_file(string, file_path+filename+".txt")

                #format the string variable to get the countries and verbatims only
                #~ participants=file_to_string(file_path+file_name+".txt")
                participants=format_participants(participants, country_list)
                countries=get_countries(participants, country_list)
                verbatims=get_verbatims(countries, country_list)
                #~ break

                #remove non validated ministers' attendances
                ImportMinAttend.objects.filter(no_celex=act_ids.no_celex, validated=False).delete()

                for country in verbatims:
                    status=None
                    #retrieves the status if the verbatim exists in the dictionary
                    try:
                        status=Verbatim.object.get(verbatim=country[1]).status
                    except Exception, e:
                        print "no verbatim", e

                    #add extracted attendances into ImportMinAttend
                    ImportMinAttend.objects.create(releve_annee=act.releve_annee, releve_mois=act.releve_mois, no_ordre=act.no_ordre, no_celex=act_ids.no_celex, country=country[0], verbatim=country[1], status=status)

                #TEST ONLY
                break

                print ""
                print ""
                print ""

