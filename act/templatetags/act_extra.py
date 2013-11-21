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

@register.simple_tag
def get_related_field(act, field_father, index, field_son):
	"""
	FUNCTION
	get the value of a field from the act model knowing the name of his father and its index (for example "code_sect_", "1" and "code_agenda" for the code_sect_1_id.code_agenda.code_agenda variable)
	PARAMETERS
	act: instance of the data of the act [Act model instance]
	field_father: name of the father field without its index [string]
	index: index of the field [int]
	field_son: name of the son field [string]
	RETURN
	value of the field [string]
	"""
	field=None
	try:
		field=getattr(act, field_father+index+"_id")
		field=getattr(field, field_son)
		field=getattr(field, field_son)
	except Exception, e:
		pass
		#~ print "no act."+field_father+index+"_id", e

	return field


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
