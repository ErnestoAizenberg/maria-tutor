from .signals import command_received, webapp_data_received


def process_telegram_update(update: dict) -> None:
    """Основной обработчик входящих обновлений"""
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if text:
        command_received.send(
            sender=process_telegram_update,
            command=text,
            chat_id=chat_id
        )
    elif "web_app_data" in message:
        webapp_data_received.send(
            sender=process_telegram_update,
            data=message["web_app_data"],
            chat_id=chat_id
        )
