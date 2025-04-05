# Accounting Reconciliation & Reporting Suite

This is a modular Python project that simulates enterprise-level accounting reconciliation tasks using mock data. It targets the key issues faced by accounting teams (like at Weatherford), including manual reconciliations, poor variance visibility, and lack of automation.

---

## 📁 Project Structure

```
accounting-suite/
├── app/
│   ├── __init__.py
│   ├── reconciliation.py
│   ├── ai_interface.py
│   └── database.py
├── data/
│   ├── gl_entries.csv
│   ├── ap_entries.csv
│   ├── bank_txns.csv
│   ├── book_cash.csv
│   ├── budgets.csv
│   ├── actuals.csv
│   └── accounts.csv
├── generate_data/
│   ├── generate_data_gl.py
│   ├── generate_data_ap_entries.py
│   ├── generate_data_bank_txns.py
│   ├── generate_data_book_cash.py
│   ├── generate_data_budgets.py
│   ├── generate_data_actuals.py
│   └── generate_data_accounts.py
├── notebooks/
├── static/
├── templates/
├── main.py
├── requirements.txt
└── README.md
├── app/
│   ├── __init__.py
│   ├── reconciliation.py
│   ├── ai_interface.py
│   └── database.py
├── data/
│   ├── gl_entries.csv
│   ├── ap_entries.csv
│   ├── bank_txns.csv
│   ├── book_cash.csv
│   ├── budgets.csv
│   ├── actuals.csv
│   └── accounts.csv
├── notebooks/
├── static/
├── templates/
├── main.py
├── requirements.txt
└── README.md
```

---

## 📌 What This Project Solves

- Reconciliation between GL and subsystems (e.g., AP)
- Bank reconciliation (book cash vs. bank transactions)
- Budget vs. Actual variance tracking
- Dataset setup for automation
- Foundation for integrating AI and dashboard tools (like Power BI)

---

## ✅ Week 1 Sprint Plan: Start Here

### 🎯 Goal: Get data loaded and basic accounting checks working.

| Task | What You Do |
|------|-------------|
| ✅ `explore_data.py` | Load CSVs and print counts, totals, and sample rows |
| ⏳ `reconcile_gl_vs_ap.py` | Compare AP totals to GL AP account by period |
| ⏳ `reconcile_bank_vs_book.py` | Match bank vs. book entries by amount + date |
| ⏳ `variance_budget_actual.py` | Compare budget vs. actual by cost center/account |
| ⏳ `main.py` | Runs the 3 scripts above from one place |

This gives you a working demo for common pain points using real logic.

---

## ⚙️ Automation Design

This project runs **locally** on your computer and is designed to allow **one-click execution** via script or UI.

| Task                        | Button Does...                                   |
|----------------------------|--------------------------------------------------|
| Reconcile GL vs AP         | Run a check between GL totals and AP postings    |
| Reconcile Bank vs Book     | Match book cash vs bank statement                |
| Budget vs Actuals Report   | Show over/under budget per account/period        |
| Load Mock Data             | Auto-load CSVs into memory or DB                 |
| (Optional) AI Interface    | Use GPT-4 to explain mismatches or generate SQL  |

---

## 🔮 Future Features (Stretch Goals)

- Add fixed asset depreciation logic
- Inventory and asset management mock logic
- Intercompany balances + eliminations
- Change management logging
- Frontend UI (Flask or React)
- Power BI integration
- AI-enhanced accounting Q&A

---

## 📞 Contact

For questions or demo inquiries: *Your Name / Email*
