import requests
from django.conf import settings
from django.dispatch import Signal, receiver

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
API_URL = f"https://api.telegram.org/bot/{BOT_TOKEN}"

# Определяем кастомные сигналы
command_received = Signal()  # При получении команды
webapp_data_received = Signal()  # При получении данных из WebApp

def send_message(chat_id: int, text: str, reply_markup=None) -> None:
    """Универсальная функция отправки сообщений"""
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup
    }
    requests.post(f"{API_URL}/sendMessage", json=payload)

@receiver(command_received)
def handle_start_command(sender, command, chat_id, **kwargs):
    """Обработчик команды /start"""
    if command == "/start":
        keyboard = {
            "inline_keyboard": [[{
                "text": "Открыть Mini App",
                "web_app": {"url": settings.MINI_APP_URL},
            }]]
        }
        send_message(
            chat_id,
            "Button bellow to open Mini App",
            reply_markup=keyboard
        )

@receiver(webapp_data_received)
def handle_webapp_data(sender, data, chat_id, **kwargs):
    """Обработчик данных из WebApp"""
    send_message(chat_id, f"Даные из Mini App: {data}")
