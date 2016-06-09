from django import template

register = template.Library()

@register.filter(name='get_item')
def get_due_date_string(dictionary, key):
    return dictionary[key]
