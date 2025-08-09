from django import template
from django.db.models import Count

register = template.Library()

@register.filter
def format_group_count(tariffs, format_type):
    """
    Возвращает количество тарифов для указанного типа формата
    Использование в шаблоне: {{ tariffs|format_group_count:"individual" }}
    """
    return tariffs.filter(format_type=format_type).count()

@register.filter
def group_by_format(tariffs):
    """
    Группирует тарифы по формату для отображения в таблице
    Возвращает словарь {format_type: [tariffs]}
    """
    return tariffs.order_by('format_type', 'program_name')
