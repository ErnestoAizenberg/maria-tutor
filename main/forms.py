from django import forms
from django.core.exceptions import ValidationError
import yaml

from .models import Review, Page
from .widgets import YAMLEditorWidget

class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'config_yaml': YAMLEditorWidget(),
        }

    def clean_config_yaml(self):
        yaml_content = self.cleaned_data.get('config_yaml', '')

        if yaml_content:
            try:
                # Validate YAML syntax
                parsed = yaml.safe_load(yaml_content)

                # Optional: Re-dump to standardize formatting
                standardized = yaml.dump(parsed,
                                       default_flow_style=False,
                                       allow_unicode=True,
                                       indent=2,
                                       sort_keys=False)
                return standardized

            except yaml.YAMLError as e:
                raise forms.ValidationError(f"Invalid YAML syntax: {e}")

        return yaml_content


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите поисковый запрос...',
            'class': 'search-input'
        }),
        max_length=100,
        required=True
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["author_name", "achievement", "content", "author_photo_url", "rating"]
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
            "author_photo_url": forms.URLInput(
                attrs={"class": "url-field"}
            ),
        }
        labels = {
            "author_name": "Ваше имя",
            "achievement": "Ваш результат",
            "content": "Текст отзыва",
            "author_photo_url": "Ссылка на Ваше фото (необязательно)",
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
