from django import template
register = template.Library()

#template: allows access to a dictionary of dictionary
@register.filter
def ofKey(dic, key):
    if dic:
        return dic.get(key)
    else:
        return ""
