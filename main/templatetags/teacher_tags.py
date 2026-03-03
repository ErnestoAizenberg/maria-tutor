from django import template

register = template.Library()


@register.filter
def get_page(teacher, page_slug):
    return teacher.get_page(page_slug)
