#-*- coding: utf-8 -*-
from act.models import PartyFamily, Person
from django.db.models.loading import get_model
#convert unicode to dict
from ast import literal_eval
#compare dg
from common.functions import format_dg_name, format_rapp_resp_name
from django import template
register=template.Library()

@register.filter
def get_value(dic, key):
    """
    FUNCTION
    get the value associated to a key in a dictionary (in a template,it is imposible to access a dictionary of dictionary)
    PARAMETERS
    dic: dictionary to use [dictionary of strings]
    key: key to use  [string]
    RETURN
    value [string]
    """
    if dic:
        #python dictionary passed from the view to the template: when page is reloaded, it is converted to unicode object!
        if isinstance(dic, unicode):
            dic=literal_eval(dic)
        return dic.get(key) 
        
    else:
        return ""


@register.simple_tag
def get_related_field(model_name, value_pk, name_son):
    """
    FUNCTION
    get the related field of a selected value in a drop down list (code_agenda for code_sect, party and country for a person, dg_sigle for a dg)
    PARAMETERS
    model_name: name of the model of the mother table [string]
    value_pk: value of the field of the mother table [int]
    name_son: name of the son field [string]
    RETURN
    instance of the son field [model instance]
    """
    field=None
    try:
        model=get_model('act', model_name)
        field=getattr(model.objects.get(pk=value_pk), name_son)
        field=getattr(field, name_son)
    except Exception, e:
        #~ print "pb get_related_field", e
        pass

    return field


@register.simple_tag
def get_party_family(pers_id):
    """
    FUNCTION
    get the party family variable from the pers id in parameter
    PARAMETERS
    pers_id: id of the person to get the party family from [id]
    RETURN
    party_family variable [string]
    """
    try:
        pers=Person.objects.get(id=pers_id)
        return PartyFamily.objects.get(party=pers.party, country=pers.country).party_family
    except Exception, e:
        print e
        return None


@register.filter
def numeric_loop(val):
    """
    FUNCTION
    use a numeric loop in template
    PARAMETERS
    val: number of iterations [int]
    RETURN
    range: for loop [list of integers]
    """
    return range(val)


@register.filter
def compare_dgs(dg_1, dg_2):
    """
    FUNCTION
    compare the dgs passed in parameter: return True if they are the same and False otherwise
    PARAMETERS
    dg_1: name of the first dg to compare [string]
    dg_2: name of the second dg to compare [string]
    RETURN
    True if the dgs are the same and False otherwise [boolean]
    """
    if dg_1 is None and dg_2 is None:
        return True
        
    if dg_1 is not None and dg_2 is not None:
        dg_1=format_dg_name(dg_1)
        dg_2=format_dg_name(dg_2)
        #2014-2-1: Value found on eurlex: European Anti-Fraud Office; Value found on oeil: European Anti-Fraud Office (OLAF).
        if dg_1 == dg_2 or dg_1 in dg_2 or dg_2 in dg_1:
            return True
            
    return False


@register.filter
def compare_resps(resp_1, resp_2):
    """
    FUNCTION
    compare the resps passed in parameter: return True if they are the same and False otherwise
    PARAMETERS
    resp_1: name of the first resp to compare [string]
    resp_2: name of the second resp to compare [string]
    RETURN
    True if the resps are the same and False otherwise [boolean]
    """
    if resp_1 is None and resp_2 is None:
        return True
        
    if resp_1 is not None and resp_2 is not None:
        resp_1=format_rapp_resp_name(resp_1)
        resp_2=format_rapp_resp_name(resp_2)
        #2014-2-1: Value found on eurlex: Algirdas Gediminas ŠEMETA; Value found on oeil: ŠEMETA Algirdas.
        if resp_1 == resp_2 or resp_1 in resp_2 or resp_2 in resp_1:
            return True
            
    return False
