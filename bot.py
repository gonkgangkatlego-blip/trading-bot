from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/")
def home():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw = request.data.decode("utf-8")

        symbol = "Unknown"
        action = "None"
        price = "N/A"

        for item in raw.split(","):
            if "=" in item:
                key, value = item.split("=", 1)
                key = key.strip()
                value = value.strip()

                if key == "symbol":
                    symbol = value
                elif key == "action":
                    action = value
                elif key == "price":
                    price = value

        message = f"Signal:\n{symbol}\n{action}\n{price}"

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message
        })

        return "OK", 200

    except Exception as e:
        print("ERROR:", e)
        return "Error", 500
