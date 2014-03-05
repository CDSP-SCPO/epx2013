#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib

def contains_digits(d):
    _digits = re.compile('\d')
    return bool(_digits.search(d))


propos_origine="COM"

if contains_digits(d):
    print "digit"
else
    print "no digit"
