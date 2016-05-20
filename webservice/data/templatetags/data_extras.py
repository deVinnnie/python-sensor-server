from django import template

register = template.Library()

@register.simple_tag
def refresh(url, time_delay=5):
    """"
    Generates an HTML refresh directive. This tag should be called from within the head of the page.

    Args:
        url: Target url for redirection.
        time_delay: Number of seconds to wait.
    """
    return '<meta http-equiv="refresh" content="' + "{}".format(time_delay) + '; url=' + url +'"/>'


@register.filter
def is_archived(alerts):
    """
    Filters the given array and returns a new array with only alerts that are archived.

    Args:
        alerts: An array containing serialiezd representations of Alert objects.
    """
    result = []
    for alert in alerts:
        if(alert['archived']):
            result.append(alert)
    return result

@register.filter
def is_active(alerts):
    """
    Filters the given array and returns a new array with only alerts that are active (NOT archived).

    Args:
        alerts: An array containing serialiezd representations of Alert objects.
    """
    result = []
    for alert in alerts:
        if(not alert['archived']):
            result.append(alert)
    return result