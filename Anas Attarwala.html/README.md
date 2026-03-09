# Anas Attar Wala — Coming Soon Website

A fully dynamic, production-ready coming-soon website built with Flask.
Matches the luxury dark gold reference design exactly.

---

## 🚀 HOW TO RUN (3 steps)

### Step 1 — Install Python & Flask
```bash
pip install flask
```

### Step 2 — Run the server
```bash
cd anas-attar
python app.py
```

### Step 3 — Open in browser
```
http://localhost:5000
```

---

## 🔐 Admin Panel

```
URL:      http://localhost:5000/admin
Password: attar2024
```

**What you can edit from admin:**
- ✅ Brand name, tagline, description, badge, promo text
- ✅ Launch date & countdown label (timer updates automatically!)
- ✅ WhatsApp number & Instagram links
- ✅ View all subscriber emails

---

## 📁 Project Structure

```
anas-attar/
├── app.py                    ← Flask server + APIs
├── requirements.txt          ← Just: flask
├── config/
│   ├── site_config.json      ← Edit all content here
│   └── emails.json           ← Auto-created when someone subscribes
├── templates/
│   ├── index.html            ← Main coming-soon page
│   ├── admin.html            ← Admin dashboard
│   └── admin_login.html      ← Admin login
└── static/
    ├── css/style.css         ← All styles
    └── js/app.js             ← Countdown + particles + form
```

---

## 🌐 API Endpoints

| Endpoint | Method | What it does |
|---|---|---|
| `/api/config` | GET | Returns full site config as JSON |
| `/api/countdown` | GET | Returns live countdown data |
| `/api/subscribe` | POST | Saves subscriber email |

---

## ✏️ Changing the Launch Date

**Option 1 — Admin Panel (easiest):**
Go to http://localhost:5000/admin → Launch Date section

**Option 2 — Edit config directly:**
Open `config/site_config.json` and change:
```json
"launch": {
  "date": "2025-08-01T00:00:00"
}
```

---

## 🚢 Deploy to Production

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Set environment variables:
```bash
export SECRET_KEY=your-strong-secret-key
export ADMIN_PASSWORD=your-admin-password
```

---

## 📱 Fully Responsive
- Desktop ✅
- Tablet ✅  
- Mobile ✅

---

## 🔗 Links (update in config/site_config.json)
- WhatsApp: wa.me/917587660797
- Instagram: instagram.com/anasattarwaladotcom
