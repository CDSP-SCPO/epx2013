from act.models import PartyFamily
from django.db.models.loading import get_model
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
		return dic.get(key)
	else:
		return ""


@register.filter
def get_instance(act, field):
	"""
	FUNCTION
	get the instance associated to the field given in parameter (for example act and "adopt_cs_contre")
	PARAMETERS
	act: instance of the data of the act [Act model instance]
	field: name of the field to get [string]
	RETURN
	instance of the field [Act model instance]
	"""
	try:
		return getattr(act, field)
	except Exception, e:
		print "get_instance pb", e
		return None


@register.simple_tag
def get_related_field(model_name, value_pk, name_son):
	field=None
	try:
		model=get_model('act', model_name)
		field=getattr(model.objects.get(pk=value_pk), name_son)
		field=getattr(field, name_son)
	except Exception, e:
		print "pb get_field", e
		pass

	return field


@register.simple_tag
def get_party_family(country, party):
	"""
	FUNCTION
	get the party family variable of a country and party given in parameters
	PARAMETERS
	country: country instance [Country model instance]
	party: party instance [Party model instance]
	RETURN
	party_family variable [string]
	"""
	return PartyFamily.objects.get(country=country, party=party).party_family
