"""
common functions to many modules (date, revere list, remove accents)
"""
#manipulates dates
from datetime import date
#remove accents
import unicodedata

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
    date in the iso format [date]
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
    date in the iso format [date]
    """
    if string!=None:
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
        return date_split_to_iso(year, month, day)
    else:
        return None


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
