import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# ENV VARIABLES
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Send message to Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(url, json=payload)
    print("Telegram response:", response.text)


# Home route
@app.route("/")
def home():
    return "Bot is running 🚀"


# TradingView webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("Webhook received:", data)

        symbol = data.get("symbol", "Unknown")
        action = data.get("action", "None")
        price = data.get("price", "N/A")

        message = f"📊 SIGNAL ALERT\n\nSymbol: {symbol}\nAction: {action}\nPrice: {price}"

        send_telegram_message(message)

        return "OK", 200

    except Exception as e:
        print("Error:", e)
        return "Error", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
