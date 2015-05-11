import os
from bs4 import BeautifulSoup

def get_directory_code(soup_all, soup_his):
    """
    FUNCTION
    get the html code of the directory code part
    PARAMETERS
    soup_all: eurlex url content from the all tab [BeautifulSoup object]
    soup_his: eurlex url content from the his tab [BeautifulSoup object]
    RETURN
    directory code part  [BeautifulSoup object]
    tab: tab where the directory code variables can be found [string]
    """
    tab="ALL"
    try:
        #extraction from the ALL tab
        print "his"
        print soup_his.find("td", {"id": "directoryCodeProc"}).find_all("span")
        print ""
        return soup_his.find("td", {"id": "directoryCodeProc"}).find_all("span"), "HIS"
    except Exception, e :
        print "exception, get_directory_code", e
        try:
            #extraction from the HIS tab
            print "all"
            #~ print soup_all.find(text=re.compile("Directory code:")).find_parent("li")
            return soup_all.find(text=re.compile("Directory code:")).find_parent("li"), tab
        except Exception, e :
            print "exception, get_directory_code 2", e

    return None, tab


path="./files/"
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "files/eurlex_his.html"
abs_file_path = os.path.join(script_dir, rel_path)
soup_his=BeautifulSoup(open(abs_file_path).read(), "html.parser").find("div", {"class": "tabContent"})
#remove script tags
[s.extract() for s in soup_his('script')]
directory_code=get_directory_code(soup_his)
print get_rep_en(directory_code)
