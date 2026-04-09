import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# 🔐 ENV VARIABLES (set these in Railway)
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 📩 Send message to Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

# 🏠 Home route (just to check server is alive)
@app.route('/')
def home():
    return "Bot is running ✅"

# 🤖 Telegram webhook (for /start etc.)
@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_telegram_message("👋 Welcome to Katlego AI Bot!\nWaiting for signals...")
        elif text == "/help":
            send_telegram_message("📘 Commands:\n/start - Start bot\n/help - Help menu")

    return "OK"

# 📊 TradingView webhook
@app.route('/webhook', methods=['POST'])
def tradingview_webhook():
    try:
        data = request.get_json()

        # Handle raw string JSON (TradingView sometimes does this)
        if not data:
            data = json.loads(request.data)

        symbol = data.get("symbol", "Unknown")
        action = data.get("action", "Signal")
        price = data.get("price", "")

        # Clean symbol (optional)
        symbol = symbol.replace("USD", "")

        # Format message
        if action.upper() == "BUY":
            emoji = "📈🔥"
        elif action.upper() == "SELL":
            emoji = "📉❌"
        else:
            emoji = "📊"

        message = f"""{emoji} {symbol} {action.upper()}

💰 Price: {price}

⚡ Check chart before entry
"""

        send_telegram_message(message)

        return "OK"

    except Exception as e:
        print("ERROR:", e)
        return "ERROR"

# ▶️ Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
