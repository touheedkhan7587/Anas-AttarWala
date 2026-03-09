"""
Anas Attar Wala — Flask App
Run: python app.py
Visit: http://localhost:5000
Admin: http://localhost:5000/admin  (password: attar2024)
"""

import json, os
from datetime import datetime
from functools import wraps
from flask import (Flask, render_template, jsonify,
                   request, redirect, url_for, session, flash)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "anas-luxury-2024")

BASE       = os.path.dirname(__file__)
CFG_PATH   = os.path.join(BASE, "config", "site_config.json")
EMAIL_PATH = os.path.join(BASE, "config", "emails.json")
ADMIN_PASS = os.environ.get("ADMIN_PASSWORD", "attar2024")


# ── helpers ──────────────────────────────────────────────
def load_cfg():
    with open(CFG_PATH, encoding="utf-8") as f:
        return json.load(f)

def save_cfg(data):
    with open(CFG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_emails():
    if not os.path.exists(EMAIL_PATH):
        return []
    with open(EMAIL_PATH, encoding="utf-8") as f:
        return json.load(f)

def add_email(email):
    emails = load_emails()
    if email not in emails:
        emails.append(email)
        with open(EMAIL_PATH, "w", encoding="utf-8") as f:
            json.dump(emails, f, indent=2)
        return True
    return False

def login_required(f):
    @wraps(f)
    def dec(*a, **kw):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*a, **kw)
    return dec


# ── main routes ───────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", cfg=load_cfg())


# ── API ───────────────────────────────────────────────────
@app.route("/api/config")
def api_config():
    return jsonify(load_cfg())

@app.route("/api/countdown")
def api_countdown():
    cfg = load_cfg()
    try:
        launch = datetime.fromisoformat(cfg["launch"]["date"])
    except Exception:
        launch = datetime.now()
    rem = max(0, int((launch - datetime.now()).total_seconds()))
    return jsonify({
        "launch_date": cfg["launch"]["date"],
        "remaining":   rem,
        "days":    rem // 86400,
        "hours":   (rem % 86400) // 3600,
        "minutes": (rem % 3600)  // 60,
        "seconds": rem % 60,
        "launched": rem == 0
    })

@app.route("/api/subscribe", methods=["POST"])
def api_subscribe():
    data  = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"ok": False, "msg": "Please enter a valid email."}), 400
    added = add_email(email)
    msg   = "You're on the list! We'll notify you." if added else "Already subscribed — stay tuned!"
    return jsonify({"ok": True, "msg": msg})


# ── admin ─────────────────────────────────────────────────
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("Wrong password.")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    cfg     = load_cfg()
    emails  = load_emails()
    success = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "brand":
            for k in ("name","tagline","badge","description","promo"):
                cfg["brand"][k] = request.form.get(k, cfg["brand"][k])
            save_cfg(cfg); success = "Brand updated!"

        elif action == "launch":
            cfg["launch"]["date"]  = request.form.get("date",  cfg["launch"]["date"])
            cfg["launch"]["label"] = request.form.get("label", cfg["launch"]["label"])
            save_cfg(cfg); success = "Launch date updated!"

        elif action == "contact":
            for k in ("whatsapp","instagram_url","instagram_handle"):
                cfg["contact"][k] = request.form.get(k, cfg["contact"][k])
            save_cfg(cfg); success = "Contact info updated!"

        cfg = load_cfg()

    return render_template("admin.html", cfg=cfg, emails=emails, success=success)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
