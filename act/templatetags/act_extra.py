from act.models import PartyFamily, Person
from django.db.models.loading import get_model
#convert unicode to dict
from ast import literal_eval
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
    print val
    return range(val)
