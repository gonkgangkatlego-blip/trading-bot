from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)

    print("Received:", data)

    symbol = data.get("symbol", "Unknown")
    action = data.get("action", "Unknown")

    # Handle BOTH entry and price
    entry = data.get("entry") or data.get("price")

    message = f"Signal:\n{symbol}\n{action}\n{entry}"

    send_telegram(message)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
