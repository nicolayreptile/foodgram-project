from django import template

register = template.Library()

@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})

@register.filter
def addid(field, id_value):
    return field.as_widget(attrs={'id': id_value})