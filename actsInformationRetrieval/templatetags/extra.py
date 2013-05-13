from django import template
register = template.Library()

@register.filter
def ofKey(dic, key):
    if dic:
        return dic.get(key)
    else:
        return ""
