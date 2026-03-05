from typing import List

from django.apps import apps
from django.db.models import CharField, Q, TextField, Model


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
                results.extend(list(search_results))
        except (LookupError, ValueError) as e:
            print(f"Error: Invalid model reference '{model_name}': {str(e)}")
            continue

    return results
