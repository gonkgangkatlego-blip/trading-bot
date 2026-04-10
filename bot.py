from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # === SAFETY CHECKS (prevents crashes) ===
    if not data:
        return "No data received", 400

    symbol = data.get("symbol", "Unknown")
    action = data.get("action", "UNKNOWN")

    try:
        price = float(data.get("price", 0))
    except:
        return "Invalid price", 400

    # === SETTINGS ===
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

    # === MESSAGE ===
    message = f"""🚨 SIGNAL

Pair: {symbol}
Type: {action}

Entry: {entry}
SL: {sl}
TP: {tp}
"""

    # === SEND TO TELEGRAM ===
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        return f"Telegram error: {e}", 500

    return "ok", 200


@app.route('/')
def home():
    return "Bot is running"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
