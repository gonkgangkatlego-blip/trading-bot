from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received:", data)

    try:
        symbol = data.get("symbol", "N/A")
        action = data.get("action", "N/A")
        entry = data.get("entry", data.get("price", "N/A"))

        message = f"Signal:\n{symbol}\n{action}\n{entry}"

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(url, json=payload)
        print("Telegram response:", response.text)

    except Exception as e:
        print("Error:", str(e))

    return {"status": "ok"}, 200
