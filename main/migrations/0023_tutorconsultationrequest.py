# Generated migration for TutorConsultationRequest model

from django.core.validators import EmailValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0022_teacher_avatar2_teacher_education_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TutorConsultationRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Полное имя репетитора",
                        max_length=300,
                        verbose_name="Имя репетитора",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Email для связи",
                        max_length=300,
                        validators=[EmailValidator()],
                        verbose_name="Email",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        help_text="Контактный телефон (необязательно)",
                        max_length=50,
                        verbose_name="Телефон",
                    ),
                ),
                (
                    "question",
                    models.TextField(
                        help_text="Описание вопроса или проблемы, с которой нужна помощь",
                        max_length=2000,
                        verbose_name="Вопрос/проблема",
                    ),
                ),
                (
                    "experience_years",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Количество лет работы репетитором",
                        null=True,
                        verbose_name="Опыт работы (лет)",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "is_processed",
                    models.BooleanField(
                        default=False,
                        help_text="Была ли обработана заявка",
                        verbose_name="Обработано",
                    ),
                ),
                (
                    "processed_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Дата обработки",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Внутренние заметки администратора",
                        max_length=1000,
                        verbose_name="Заметки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на консультацию для репетиторов",
                "verbose_name_plural": "Заявки на консультацию для репетиторов",
                "ordering": ["-created_at"],
            },
        ),
    ]
