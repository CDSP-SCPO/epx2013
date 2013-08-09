from django import template
register = template.Library()

#get the value of the selected item from a drop down list (value displayed to the user)
@register.filter
def selected_label(value, choices):
	for src in choices:
		if src[0]==value:
			return src[1]

	#~ return [label for value, label in form.fields[field].choices if value in form[field].value()]
