from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    symbol = data.get("symbol")
    action = data.get("action")
    price = float(data.get("price"))

    # === SETTINGS (YOU CAN CHANGE LATER) ===
    SL_POINTS = 50
    TP_POINTS = 100

    # === CALCULATIONS ===
    if action == "BUY":
        entry = price
        sl = price - SL_POINTS
        tp = price + TP_POINTS

    elif action == "SELL":
        entry = price
        sl = price + SL_POINTS
        tp = price - TP_POINTS

    else:
        return "Invalid action", 400

    # === MESSAGE FORMAT ===
    message = f"""
🚨 SIGNAL

Pair: {symbol}
Type: {action}

Entry: {entry}
SL: {sl}
TP: {tp}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload)

    return "ok", 200


@app.route('/')
def home():
    return "Bot is running"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
