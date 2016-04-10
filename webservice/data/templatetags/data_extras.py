from django import template

register = template.Library()

@register.simple_tag
def refresh(url, time_delay=5):
    return '<meta http-equiv="refresh" content="' + "{}".format(time_delay) + '; url=' + url +'"/>'