from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ENV VARIABLES (Railway)
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_data(as_text=True)

        if not data:
            data = "No message received"

        print("Received:", data)

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": data
        }

        response = requests.post(url, json=payload)
        print("Telegram response:", response.text)

    except Exception as e:
        print("ERROR:", str(e))

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
