from django.apps import apps
from django.db.models import CharField, Q, TextField


def search_models(query, model_names):
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
        except Exception as e:
            print(f"Error searching {model_name}: {str(e)}")
            continue

    return results
