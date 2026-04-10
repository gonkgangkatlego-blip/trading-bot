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

        tp = data.get("tp", "N/A")   # ← ADD THIS
        sl = data.get("sl", "N/A")   # ← ADD THI

        message = f"📊 {symbol}\n📉 {action}\n💰 Entry: {entry}\n🎯 TP: {tp}\n🛑 SL: {sl}"

        url = "https://api.telegram.org/bot8621509303:AAENHSD8uaEum2pBWfmG6sc4h9aB3MWy750/sendMessage"
        payload = {
            "chat_id": 5517363052,
            "text": message
        }

        response = requests.post(url, json=payload)
        print("Telegram response:", response.text)

    except Exception as e:
        print("Error:", str(e))

    return {"status": "ok"}, 200
