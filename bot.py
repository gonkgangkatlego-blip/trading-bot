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
        print("Incoming:", raw)

        symbol = "Unknown"
        action = "None"
        price = "N/A"

        # Parse TradingView plain text
        if raw:
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

        message = f"Signal:\\n{symbol}\\n{action}\\n{price}"

        # Send to Telegram (SAFE — will NOT crash)
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            response = requests.post(url, json={
                "chat_id": CHAT_ID,
                "text": message
            })
            print("Telegram response:", response.text)
        except Exception as tg_error:
            print("Telegram ERROR:", tg_error)

        return "OK", 200

    except Exception as e:
        print("WEBHOOK ERROR:", e)
        return "OK", 200   # IMPORTANT: never crash server
