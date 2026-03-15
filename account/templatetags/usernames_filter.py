from django import template

register = template.Library()

@register.filter
def mask_username(username):
    if len(username) <= 4:
        return "*" * len(username)
    return username[:2] + "*" * (len(username) - 4) + username[-2:]