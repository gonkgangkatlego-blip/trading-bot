from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")

@app.route("/")
def home():
    return {"status": "ok"}, 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        if not data:
            return {"error": "No data"}, 400

        # 👇 Detect TradingView signal OR Telegram message
        if "message" in data:
            # TELEGRAM MESSAGE
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if text == "/start":
                reply = "👋 Welcome to Katlego AI Bot!\n\nWaiting for signals..."
            elif text == "/status":
                reply = "🟢 Bot is running 🚀"
            else:
                reply = text

        else:
            # 🔥 TRADINGVIEW SIGNAL
            chat_id = os.environ.get("CHAT_ID")

            symbol = data.get("symbol", "Unknown")
            action = data.get("action", "No action")
            price = data.get("price", "N/A")

            reply = f"🚨 SIGNAL\n\n📊 {symbol}\n📈 Action: {action}\n💰 Price: {price}"

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": reply
        }

        requests.post(url, json=payload)

        return {"ok": True}, 200

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
