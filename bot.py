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
        data = request.get_json(force=True)

        print("Incoming data:", data)

        symbol = data.get("symbol", "Unknown")
        action = data.get("action", "None")
        price = data.get("price", "N/A")

        message = f"Signal:\n{symbol}\n{action}\n{price}"

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message
        })

        return "OK", 200

    except Exception as e:
        print("ERROR:", str(e))
        return "Error", 500
