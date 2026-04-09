from flask import Flask, request
import requests

app = Flask(__name__)

# 🔐 YOUR TELEGRAM DETAILS
TOKEN = "8643871843:AAHednAqzBYqEmKMz3J2HJk81z0v5B9Zj8E"
CHAT_ID = "5517363052"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # ✅ Works with TradingView (text/plain)
        message = request.data.decode("utf-8")

        if not message:
            message = "No message received"

    except Exception:
        message = "Error reading message"

    print("Received:", message)

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    # ✅ SEND + DEBUG
    response = requests.post(url, json=payload)
    print("Telegram response:", response.text)

    return "ok"

if __name__ == "__main__":
    app.run(port=5000)