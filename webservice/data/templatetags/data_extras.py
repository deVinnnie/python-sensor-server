from django import template

register = template.Library()

@register.simple_tag
def refresh(url, time_delay=5):
    """
    Generates an HTML refresh directive. This tag should be called from within the head of the page.

    Args:
        url: Target url for redirection.
        time_delay: Number of seconds to wait.
    """
    return '<meta http-equiv="refresh" content="' + "{}".format(time_delay) + '; url=' + url +'"/>'