# calculator/templatetags/app_filters.py

from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """
    Checks if a string starts with the given argument.
    Usage: {{ value|startswith:'arg' }}
    """
    return value.startswith(arg)

@register.filter
def cut_prefix(value, arg):
    """
    Removes a prefix from a string if it exists.
    Usage: {{ value|cut_prefix:"prefix " }}
    This is an alternative to the built-in 'cut' filter for clarity with prefixes.
    """
    if value.startswith(arg):
        return value[len(arg):]
    return value