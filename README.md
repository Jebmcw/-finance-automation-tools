# Accounting Reconciliation & Reporting Suite

This is a modular Python project that simulates core enterprise accounting workflows using mock data. It focuses on reconciliation, reporting, and optional AI-assisted queries to emulate real-world systems like those used at Weatherford and similar enterprise environments.

---

## 📁 Project Structure

```
accounting-suite/
├── app/                      # Core application logic
│   ├── __init__.py
│   ├── reconciliation.py     # Reconciliation logic (GL vs AP, Bank, Budget)
│   ├── ai_interface.py       # OpenAI query processing
│   └── database.py           # DB setup and utility functions
├── data/                     # Mock data CSVs
│   ├── gl_entries.csv
│   ├── ap_entries.csv
│   ├── bank_txns.csv
│   ├── budgets.csv
│   ├── actuals.csv
│   └── accounts.csv
├── notebooks/                # Jupyter notebooks for data exploration
├── static/                   # For future frontend assets
├── templates/                # HTML templates (optional for Flask UI)
├── main.py                   # Flask app entry point
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 📌 2-Day MVP Plan

### Core Features
- [x] Reconcile GL vs AP
- [x] Reconcile Bank vs Book Cash
- [x] Compare Budget vs Actuals
- [x] Chart of Accounts setup
- [x] Basic Flask API (e.g., `/reconcile`, `/summary`)
- [x] Optional: AI interface for natural-language queries

### Tools & Libraries
- Python 3.10+
- Flask
- Pandas
- SQLite (or PostgreSQL for later scaling)
- OpenAI API (for natural language input)
- Jinja2 (optional, if you build a frontend)

Install with:
```
pip install -r requirements.txt
```

---

## 📈 Example Endpoints

- `POST /reconcile`  
  Trigger reconciliation by module (e.g., "bank", "ap_gl").

- `POST /ai-query`  
  Accepts natural-language prompts to generate SQL or explain variances.

---

## 🚀 Future Plans (Stretch Goals)

- Fixed Assets tracking + depreciation logic
- Inventory module with item flow + cost tracking
- Intercompany reconciliation and elimination logic
- Change management tracking (audit logs, approval workflow)
- Frontend interface (React or HTML templates)
- Export reports to Excel or PDF
- Role-based access/authentication

---

## 📞 Contact

For demo or collaboration inquiries, contact: *Your Name / Email*



---

## ⚙️ Automation Design

This project is intended to run **locally on your computer** as a Flask app or script. Most key accounting tasks can be automated with a **single button press** from a simple UI or script command.

### 🔘 Button Automation Overview

| Task                        | Automation Description                            |
|----------------------------|----------------------------------------------------|
| Reconcile GL vs AP         | 🔘 One-click to compare GL and AP summaries        |
| Reconcile Bank vs Book     | 🔘 One-click to match bank vs internal transactions|
| Budget vs Actuals Report   | 🔘 One-click to generate variance report           |
| AI Query Interface         | 🔘 Ask natural questions, get structured responses |
| Load Mock Data             | 🔘 Auto-load sample CSVs into the database         |

You can later build a small web UI or CLI interface where each function runs at the push of a button.

