from django.apps import AppConfig
from django.db.models import BigAutoField

class TelegramBotConfig(AppConfig):
    default_auto_field = BigAutoField
    name = 'telegram_bot'

    def ready(self):
        from . import signals #noqa
