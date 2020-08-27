from django import template
register = template.Library()


def index(value, arg):
    arg = int(arg)
    return value[arg]


def li(value):
    return list(value)


register.filter('index', index)
