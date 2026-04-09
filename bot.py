from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ENV VARIABLES (Railway)
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/")
def home():
    return {"status": "ok"}, 200


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        if not data:
            return {"error": "No data"}, 400

        text = str(data)

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text
        }

        requests.post(url, json=payload)

        return {"ok": True}, 200

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
