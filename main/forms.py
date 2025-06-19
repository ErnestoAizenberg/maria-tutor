from django import forms


class ApplicationForm(forms.Form):
    SUBJECT_CHOICES = [
        ("biology", "Биология"),
        ("chemistry", "Химия"),
        ("special", "Спецкурс"),
        ("consultation", "Не знаю, нужна консультация"),
    ]

    name = forms.CharField(max_length=100, required=True, label="Ваше имя")

    email = forms.CharField(max_length=100, required=True, label="Контакт для связи")

    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True, label="Предмет")

    goal = forms.CharField(widget=forms.Textarea, required=True, label="Цель занятий")

    def __init__(self, *args, **kwargs):
        subject_options = kwargs.pop("subject_options", None)
        super().__init__(*args, **kwargs)
        if subject_options:
            self.fields["subject"].choices = subject_options
