from django import template
from django.db.models import QuerySet
from django.db.models.query import EmptyQuerySet
from typing import Union

from main.models import Tariff

register = template.Library()


@register.filter
def format_group_count(tariffs: Union[QuerySet[Tariff], None], format_type: str) -> int:
    """
    Return count of tariffs for a given format type.

    Args:
        tariffs: QuerySet of Tariff objects or None
        format_type: String representing the format type to filter by

    Returns:
        int: Number of tariffs matching the format type, or 0 if tariffs is None
    """
    if tariffs is None:
        return 0
    return tariffs.filter(format_type=format_type).count()


@register.filter
def group_by_format(
    tariffs: Union[QuerySet[Tariff], None],
) -> Union[QuerySet[Tariff], EmptyQuerySet]:
    """
    Orders tariffs by format and program name.

    Args:
        tariffs: QuerySet of Tariff objects or None

    Returns:
        QuerySet[Tariff]: Ordered QuerySet of tariffs, or empty QuerySet if input is None
    """
    if tariffs is None:
        return Tariff.objects.none()
    return tariffs.order_by("format_type", "program_name")
