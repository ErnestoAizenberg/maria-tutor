# Generated by Django 5.2.2 on 2025-06-14 22:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="article",
            name="abstract",
            field=models.CharField(
                blank=True,
                help_text="Brief summary (appears in article listings)",
                max_length=300,
            ),
        ),
    ]
