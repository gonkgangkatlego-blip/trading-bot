from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ✅ HEALTH CHECK (CRITICAL)
@app.route("/")
def home():
    return "OK", 200


# ✅ WEBHOOK
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(silent=True)  # 👈 IMPORTANT FIX

        if not data:
            return "no data", 200

        # TELEGRAM MESSAGE
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if text == "/start":
                reply = "👋 Welcome to Katlego AI Bot!\n\nWaiting for signals..."
            elif text == "/status":
                reply = "🟢 Bot is running 🚀"
            else:
                reply = text

        # TRADINGVIEW SIGNAL
        else:
            chat_id = CHAT_ID

            symbol = data.get("symbol", "Unknown")
            action = data.get("action", "No action")
            price = data.get("price", "N/A")

            reply = f"🚨 SIGNAL\n\n📊 {symbol}\n📈 Action: {action}\n💰 Price: {price}"

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        requests.post(url, json={
            "chat_id": chat_id,
            "text": reply
        })

        return "ok", 200

    except Exception as e:
        print("ERROR:", str(e))
        return "error", 200
