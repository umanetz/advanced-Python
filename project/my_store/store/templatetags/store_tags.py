from django import template

register = template.Library()

@register.filter(name='add_space')
def add_space(value):
    return '{0:,}'.format(value).replace(',', ' ')