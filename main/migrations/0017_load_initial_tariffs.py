from django.db import migrations, transaction
from django.utils.text import slugify
import time

def create_initial_tariffs(apps, schema_editor):
    Tariff = apps.get_model('main', 'Tariff')
    Teacher = apps.get_model('main', 'Teacher')

    TARIFFS_DATA = [
        # (format_type, format_display, program_name, price, price_unit, is_group_format)
        ('individual', 'Индивидуально', 'ОГЭ', 1600, '₽/час', False),
        ('individual', 'Индивидуально', 'ЕГЭ', 1800, '₽/час', False),
        ('individual', 'Индивидуально', 'Олимпиады', 2000, '₽/час', False),
        ('pair', 'Парные', 'ОГЭ/школьная программа', 1200, '₽/час', True),
        ('pair', 'Парные', 'ЕГЭ', 1400, '₽/час', True),
        ('group', 'Групповые', 'ОГЭ (3-5 чел)', 700, '₽/час', True),
        ('async', 'Асинхронное', 'ОГЭ', 600, '₽/неделя', False),
        ('async', 'Асинхронное', 'ЕГЭ', 800, '₽/неделя', False),
    ]

    try:
        with transaction.atomic():
            for teacher in Teacher.objects.all():
                for data in TARIFFS_DATA:
                    base_slug = slugify(f"{teacher.name}-{data[0]}-{data[2]}")
                    unique_slug = base_slug
                    counter = 1

                    # Проверяем уникальность slug
                    while Tariff.objects.filter(slug=unique_slug).exists():
                        unique_slug = f"{base_slug}-{counter}"
                        counter += 1

                    Tariff.objects.create(
                        teacher=teacher,
                        format_type=data[0],
                        format_display=data[1],
                        program_name=data[2],
                        price=data[3],
                        price_unit=data[4],
                        is_group_format=data[5],
                        slug=unique_slug  # Уникальный slug для каждой записи
                    )
    except Exception as e:
        print(f"Ошибка при создании тарифов: {e}")
        raise

def reverse_tariffs(apps, schema_editor):
    Tariff = apps.get_model('main', 'Tariff')
    Tariff.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ("main", "0016_tariff"),
    ]

    operations = [
        migrations.RunPython(
            create_initial_tariffs,
            reverse_tariffs,
            atomic=True
        )
    ]
