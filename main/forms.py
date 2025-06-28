from django import forms
from django.core.exceptions import ValidationError

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["author_name", "achievement", "content", "author_photo", "rating"]
        widgets = {
            "author_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Как вас зовут? (например: Анна К.)",
                }
            ),
            "achievement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ваш результат (например: ЕГЭ по биологии, 98 баллов)",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Текст вашего отзыва",
                    "rows": 5,
                }
            ),
            "author_photo": forms.FileInput(
                attrs={"class": "form-control-file", "accept": "image/*"}
            ),
        }
        labels = {
            "author_name": "Ваше имя",
            "achievement": "Ваш результат",
            "content": "Текст отзыва",
            "author_photo": "Ваше фото (необязательно)",
        }


class ApplicationForm(forms.Form):
    SUBJECT_CHOICES = [
        ("biology", "Биология"),
        ("chemistry", "Химия"),
        ("special", "Спецкурс"),
        ("consultation", "Не знаю, нужна консультация"),
    ]

    name = forms.CharField(
        max_length=100,
        required=True,
        label="Ваше имя",
        widget=forms.TextInput(attrs={"placeholder": "Иван Иванов"}),
        error_messages={
            "required": "Пожалуйста, введите ваше имя",
            "max_length": "Имя слишком длинное (максимум 100 символов)",
        },
    )

    # Changed from CharField to EmailField for proper validation
    email = forms.EmailField(
        max_length=100,
        required=True,
        label="Контакт для связи",
        widget=forms.EmailInput(attrs={"placeholder": "email@example.com"}),
        error_messages={
            "required": "Пожалуйста, укажите email для связи",
            "invalid": "Пожалуйста, введите корректный email-адрес",
            "max_length": "Email слишком длинный (максимум 100 символов)",
        },
    )

    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        required=True,
        label="Предмет",
        error_messages={
            "required": "Пожалуйста, выберите предмет",
            "invalid_choice": "Выбран недопустимый вариант",
        },
    )

    goal = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Опишите ваши цели обучения...", "rows": 4}
        ),
        required=True,
        label="Цель занятий",
        min_length=10,
        error_messages={
            "required": "Пожалуйста, опишите цель занятий",
            "min_length": "Описание цели слишком короткое (минимум 10 символов)",
        },
    )

    def __init__(self, *args, **kwargs):
        subject_options = kwargs.pop("subject_options", None)
        super().__init__(*args, **kwargs)
        if subject_options:
            self.fields["subject"].choices = subject_options

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if len(name.split()) < 2:
            raise ValidationError("Пожалуйста, введите имя и фамилию")
        return name
