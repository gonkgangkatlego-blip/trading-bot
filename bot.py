from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ENV VARIABLES (Railway)
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

        # 🔥 GET CHAT ID DYNAMICALLY
        chat_id = data.get("message", {}).get("chat", {}).get("id")

        # 🔥 GET USER MESSAGE
        text = data.get("message", {}).get("text", "")

        # COMMANDS
        if text == "/start":
            reply = "👋 Welcome to Katlego AI Bot!\n\nSend a message or wait for trading signals."
        elif text == "/help":
            reply = "📖 Commands:\n/start - Start bot\n/help - Show help\n/status - Bot status"
        elif text == "/status":
            reply = "🟢 Bot is running and connected 🚀"
        else:
            reply = text  # echo

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
