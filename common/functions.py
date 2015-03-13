"""
common functions to many modules (date, revere list, remove accents)
"""
#manipulates dates
from datetime import date
#remove accents
import unicodedata
import re

def split_fr_date(date_str):
    """
    FUNCTION
    split a date ('DD-MM-YYYY' or 'DD/MM/YYYY') into year, month and day
    PARAMETERS
    date_str: date to split [string]
    RETURN
    year, month and day of the date [int, int, int]
    """
    day=date_str[:2]
    month=date_str[3:5]
    try:
        #date coded on 4 digits
        year=date_str[6:]
    except:
        #date coded on 2 digits
        year=date_str[4:]

    return year, month, day


def date_split_to_iso(year, month, day):
    """
    FUNCTION
    transform a split date to the iso format ('YYYY-MM-DD')
    PARAMETERS
    year, month, day: year, month and day of the date to transform  [int, int, int]
    RETURN
    date in the iso format [string]
    """
    year=int(year)
    month=int(month)
    day=int(day)
    if month>12:
        #month and day are reversed
        temp=month
        month=day
        day=temp
    return date(year, month, day).isoformat()


def date_string_to_iso(string):
    """
    FUNCTION
    transform a string date (American format with "/" or French format) to the iso format ('YYYY-MM-DD')
    PARAMETERS
    string: string date to convert [string]
    RETURN
    date in the iso format [string]
    """
    date=None
    if string is not None:
        try:
            #if separator is "-"
            if "-" in string:
                strings=string.split("-")
            else:
                strings=string.split("/")

            #~ print "strings"
            #~ print strings
                
            #if year is first
            if len(strings[0])==4:
                year, month, day=strings[0], strings[1], strings[2]
            #if year is last
            else:
                #the year must be coded on 4 digits
                year, month, day=strings[2], strings[1], strings[0]
            date=date_split_to_iso(year, month, day)
        except Exception, e:
            print "pb", string
            print "wrong date format", e

    #return None if date string is None
    return date


def list_reverse_enum(string):
    """
    FUNCTION
    reverse a list or string and return it along with the original position of each element
    PARAMETERS
    string: string to analyse [string]
    RETURN
    index: original position of each character [int]
    string: reversed string [string]
    """
    for index in reversed(xrange(len(string))):
        yield index, string[index]


def remove_nonspacing_marks(string):
    """
    FUNCTION
    Decompose the unicode string s and remove non-spacing marks
    PARAMETERS
    string: string to analyse [string]
    RETURN
    string without accents [string]
    """
    return ''.join(c for c in unicodedata.normalize('NFKD', string) if unicodedata.category(c) !='Mn')


def format_rapp_resp_name(names):
    """
    FUNCTION
    rewrite  the name of the rapporteur or responsible in the right format "LASTNAME Firstname"
    PARAMETERS
    names: full name of the person [string]
    RETURN
    instance: full name of the person, in the right format [string]
    """
    if names is not None:
        #remove trailing "'"
        if names[-1]=="'":
            names=names[:-1]
        #change name format: "Firstname LASTNAME" -> "LASTNAME Firstname"
        names=names.split()
        first_name=last_name=""
        for name in names:
            #get last names
            if name.isupper():
                last_name+=name+" "
            #get first names
            else:
                first_name+=name+" "

        names=last_name+first_name[:-1]

    return names


def format_dg_name(old_dg):
    """
    FUNCTION
    format the DG name as "DG ..."
    PARAMETERS
    old_dg: name to format [string]
    RETURN
    new_dg: dg name in the new format [string]
    """
    new_dg=old_dg

    if new_dg not in ["", None]:
        #remove dg / directorate-general at the beginning or end
        pattern = re.compile("dg | dg", re.IGNORECASE)
        new_dg=pattern.sub("", new_dg)
        pattern = re.compile("^directorate-general( for)?( the)?|directorate-general( for)?( the)?$", re.IGNORECASE)
        new_dg=pattern.sub("", new_dg)
        new_dg="DG "+new_dg.strip()
    
    return new_dg
