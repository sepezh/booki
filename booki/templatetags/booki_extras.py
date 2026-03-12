"""_
extras filters 

by : https://docs.djangoproject.com/en/5.1/howto/custom-template-tags/
"""

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def combine(value, arg=','):
    """ to combine multi values with a separator """
    return arg.join([str(item) for item in value])

@register.simple_tag(takes_context=True)
def is_librarian(context):
    """ check user is librarian """
    user = context['request'].user
    return user.groups.filter(name='librarian').exists() if user.is_authenticated else False

@register.simple_tag
def get_image_or_default(instance_image, default_image='img/default.png'):
    """ Get model image or use default one """
    if instance_image:
        return instance_image.url
    return settings.STATIC_URL + default_image
