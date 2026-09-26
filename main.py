import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# настоящие данные от Telegram-бота
TELEGRAM_BOT_TOKEN = "8364020564:AAFHjktRvP45PVU-lKX7OjD8tlwc_Q1pRic"
TELEGRAM_CHAT_ID = "529651568"


def send_telegram_message(text):
    """Функция отправки уведомления в Telegram"""
    if TELEGRAM_BOT_TOKEN == "8364020564:AAFHjktRvP45PVU-lKX7OjD8tlwc_Q1pRic":
        print("Внимание: Не заменено токен или ID чата Telegram в main.py!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/join', methods=['POST'])
def join():
    name = request.form.get('name')
    phone = request.form.get('phone')
    car = request.form.get('car')
    service = request.form.get('service')

    print(f"DEBUG: Заявка получена от {name}, авто: {car}")

    # Пытаемся отправить в Telegram (если токен пустой, просто выведем ошибку в консоль, но сайт не упадет)
    try:
        telegram_text = (
            f"🔥 <b>Nowa zgłoszenie!</b>\n"
            f"👤 {name}\n"
            f"📞 {phone}\n"
            f"🚗 {car}\n"
            f"🛠 {service}"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": telegram_text, "parse_mode": "HTML"}, timeout=3)
    except Exception as e:
        print(f"Telegram error (не влияет на показ страницы): {e}")

    # Возвращаем шаблон благодарности
    return render_template('thanks.html')
@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)