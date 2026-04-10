import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route("/")
def home():
    return "Bot running"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Try JSON first
        data = request.get_json(silent=True)

        if data:
            print("JSON data received:", data)
            symbol = data.get("symbol", "Unknown")
            action = data.get("action", "None")
            price = data.get("price", "N/A")

        else:
            # Handle plain text (TradingView fallback)
            raw = request.data.decode("utf-8")
            print("Raw data received:", raw)

            parts = {}
            for item in raw.split(","):
                if "=" in item:
                    key, value = item.split("=", 1)
                    parts[key.strip()] = value.strip()

            symbol = parts.get("symbol", "Unknown")
            action = parts.get("action", "None")
            price = parts.get("price", "N/A")

        message = f"Signal:\n{symbol}\n{action}\n{price}"

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        response = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message
        })

        print("Telegram response:", response.text)

        return "OK", 200

    except Exception as e:
        print("ERROR:", str(e))
        return "Error", 500
