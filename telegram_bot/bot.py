import requests
import time

BOT_TOKEN = "8117603297:AAF5nSvrmciw869r6Q1M9wzth1cVGyJPV0s"  # Замените на токен от @BotFather
MINI_APP_URL = "https://mariaseredinskaya.pythonanywhere.com"  # HTTPS обязательно!
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id: int, text: str, reply_markup=None) -> None:
    """Отправляет сообщение с кнопкой WebApp"""
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": reply_markup
    }
    requests.post(f"{API_URL}/sendMessage", json=payload)

def get_updates(offset: int = None) -> list:
    """Получает новые апдейты от Telegram"""
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    response = requests.get(f"{API_URL}/getUpdates", params=params)
    return response.json().get("result", [])

def main():
    print("Бот запущен! Нажми Ctrl+C для остановки.")
    last_update_id = 0

    while True:
        updates = get_updates(last_update_id + 1 if last_update_id else None)

        for update in updates:
            last_update_id = update["update_id"]
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "").strip()

            if text == "/start":
                # Создаем кнопку для Mini App
                keyboard = {
                    "inline_keyboard": [[
                        {
                            "text": "✨ Открыть Mini App",
                            "web_app": {"url": MINI_APP_URL}
                        }
                    ]]
                }
                send_message(
                    chat_id,
                    "🚀 Нажми кнопку ниже, чтобы открыть интерактивное приложение!",
                    reply_markup=keyboard
                )
            elif "web_app_data" in message:
                # Обработка данных из Mini App (если нужно)
                data = message["web_app_data"]["data"]
                send_message(chat_id, f"📲 Данные из Mini App: {data}")

        time.sleep(0.5)  # Пауза между запросами

if __name__ == "__main__":
    main()
