from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ENV VARIABLES (Railway)
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        message = request.data.decode("utf-8")
        if not message:
            message = "No message received"
    except Exception as e:
        message = f"Error reading message: {str(e)}"

    print("Received:", message)

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Telegram error:", str(e))

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
