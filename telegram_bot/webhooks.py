import requests

from django.conf import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
API_URL = f"https://api.telegram.org/bot/{BOT_TOKEN}"

def send_message(chat_id: int, text:str, reply_markup=None) -> None:
    """Send a message with WebApp button"""
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup
    }

    requests.post(f"{API_URL}/sendMessage", json=payload)

def process_telegram_update(update: dict) -> None:
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if text == "/start":
        keyboard = {
            "inline_keyboard": [[
                {
                    "text": "Открыть Mini App",
                    "web_app": {"url": settings.MINI_APP_URL},
                }
            ]]
        }

        send_message(
            chat_id,
            "Button bellow to open Mini App",
            reply_markup = keyboard,
        )
    elif "web_app_data" in message:
        data = message["web_app_data"]
        send_message(chat_id, f"Даные из Mini App: {data}")
