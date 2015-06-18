from django import template

register = template.Library()

# http://stackoverflow.com/questions/2415865/iterating-through-two-lists-in-django-templates
@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)
