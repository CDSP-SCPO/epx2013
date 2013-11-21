from django import template
register=template.Library()

@register.filter
def selected_label(value, choices):
	"""
	FUNCTION
	get the text displayed to the user corresponding to the selected item of a drop down list
	PARAMETERS
	value: id of the selected item [int]
	choices: key to use [ChoiceField object]
	RETURN
	text displayed to the user [string]
	"""
	for choice in choices:
		if choice[0]==value:
			return choice[1]
