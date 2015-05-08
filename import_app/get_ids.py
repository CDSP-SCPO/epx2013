"""
1/ids and errors retrieval
2/get the urls of European institutions from the ids
3/cross validation between the websites
"""
import get_ids_eurlex as eurlex
import get_ids_oeil as oeil


def check_get_ids_eurlex(no_celex):
    """
    FUNCTION
    check and get all the ids from the eurlex id
    PARAMETERS
    no_celex: no_celex id [string]
    RETURN
    fields: retrieved data from eurlex [dictionary]
    """
    fields={}
    url_eurlex=eurlex.get_url_eurlex(no_celex, "HIS")
    print "eurlex url", url_eurlex
    url_eurlex_content=eurlex.get_url_content_eurlex(url_eurlex)
    #act doesn't exist, problem on page or problem with the Internet connection
    if url_eurlex_content!=False:
        #get data from eurlex
        fields=eurlex.get_ids_eurlex(url_eurlex_content)
        fields['url_exists']=True
    else:
        fields['url_exists']=False
        print "eurlex url does not exist!!"

    return fields


def check_get_ids_oeil(no_unique_type, no_unique_annee, no_unique_chrono):
    """
    FUNCTION
    check and get all the ids from the oeil ids
    PARAMETERS
    no_unique_annee: no_unique_annee id [int]
    no_unique_chrono: no_unique_chrono id [string]
    no_unique_type: no_unique_type id [string]
    RETURN
    fields: retrieved data from oeil [dictionary]
    """
    fields={}
    fields['url_exists']=False
    #1998, 9, 3 ->no_unique_type="ACC" -> no oeil page
    if no_unique_type!="ACC":
        url_oeil=oeil.get_url_oeil(no_unique_type, no_unique_annee, no_unique_chrono)
        print "oeil url", url_oeil
        url_oeil_content=oeil.get_url_content_oeil(url_oeil)
        #act doesn't exist, problem on page or problem with the Internet connection
        if url_oeil_content!=False:
            #~ #get data from oeil
            fields=oeil.get_ids_oeil(url_oeil_content)
            fields['url_exists']=True
        else:
            print "oeil url does not exist!!"
    else:
        #set all the ids to None (in case they were first filled with a value by mistake)
        fields['no_celex']=None
        fields['no_unique_type']=None
        fields['no_unique_annee']=None
        fields['no_unique_chrono']=None
        fields['propos_origine']=None
        fields['propos_annee']=None
        fields['propos_chrono']=None

    return fields
