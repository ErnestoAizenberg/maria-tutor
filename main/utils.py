import logging
from typing import List

from django.apps import apps
from django.db.models import CharField, Q, TextField, Model

logger = logging.getLogger(__name__)


def search_models(query: str, model_names: List[str]) -> List[Model]:
    """
    Search through multiple Django models for a given query string.

    Args:
        query: The search string to look for
        model_names: List of model names in 'app_label.ModelName' format

    Returns:
        List of model instances that match the search query
    """
    results = []

    for model_name in model_names:
        try:
            model = apps.get_model(model_name)
        except (LookupError, ValueError) as e:
            logger.warning("Invalid model reference '%s': %s", model_name, e)
            continue

        text_fields = [
            field.name
            for field in model._meta.get_fields()
            if isinstance(field, (CharField, TextField))
        ]

        if text_fields:
            q_objects = Q()
            for field in text_fields:
                q_objects |= Q(**{f"{field}__icontains": query})

            search_results = model.objects.filter(q_objects)
            results.extend(search_results)

    return results
