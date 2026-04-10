@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw = request.data.decode("utf-8")
        print("Incoming:", raw)

        # Default values
        symbol = "Unknown"
        action = "None"
        price = "N/A"

        # Parse plain text safely
        if raw:
            parts = raw.split(",")
            for item in parts:
                if "=" in item:
                    key, value = item.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if key == "symbol":
                        symbol = value
                    elif key == "action":
                        action = value
                    elif key == "price":
                        price = value

        message = f"Signal:\n{symbol}\n{action}\n{price}"

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message
        })

        return "OK", 200

    except Exception as e:
        print("ERROR:", str(e))
        return "Error", 500
