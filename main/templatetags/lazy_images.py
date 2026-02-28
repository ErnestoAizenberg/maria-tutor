import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def lazy_images(value):
    return mark_safe(re.sub(r'<img\s+', r'<img loading="lazy" ', value))
