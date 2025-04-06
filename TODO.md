# ✅ Sprint 1 – Week 1 Development Checklist

This checklist breaks down your first week of development into focused, step-by-step tasks.

---

## 📁 Data Validation & Exploration

- [x] **Create `explore_data.py`**
  - [x] Load all `.csv` files using `pandas`
  - [x] Print row counts for each dataset
  - [x] Print total amounts (e.g., GL, bank, budget)
  - [x] Check date ranges and sample values

---

## 🔍 GL vs AP Reconciliation

- [x] **Create `reconcile_gl_vs_ap.py`**
  - [x] Group `gl_entries` by `account + period`
  - [x] Group `ap_entries` by `account + period` where `status == 'posted'`
  - [x] Compare totals and show mismatches
  - [x] Print summary of matched vs unmatched
  - [x] Save differences to a new `.csv` file

---

## 💵 Bank vs Book Reconciliation

- [x] **Create `reconcile_bank_vs_book.py`**
  - [x] Match entries by `bank_account`, `amount ± 0.01`, and `txn_date ± 3 days`
  - [x] Identify unmatched rows in each dataset
  - [x] Show total matched and unmatched amounts
  - [x] Export unmatched rows to a `.csv` file

---

## 📊 Budget vs Actuals Variance

- [x] **Create `variance_budget_actual.py`**
  - [x] Group `budgets.csv` by `account + period + cost_center`
  - [x] Group `actuals.csv` by the same keys
  - [x] Calculate variance and % variance
  - [x] Flag large variances and save to `.csv`

---

## 🧪 One-Click Execution Script

- [x] **Update or create `main.py`**
  - [x] Add functions to call each reconciliation script
  - [x] Print clean, readable summaries for each module
  - [x] Optional: prompt user for module to run

---

## 🖥️ APP: Local Reconciliation Viewer

Build a lightweight local desktop app (using **Tkinter**, **Flask**, or **Electron/React**) that does the following:

- [ ] Load local datasets from `data/`
- [ ] Run reconciliation logic (GL vs AP, Bank vs Book, Budget vs Actuals)
- [ ] Display mismatches in a clean **UI table**
- [ ] Add a **"Run Reconciliation"** button
- [ ] (Optional) Export results to CSV or visualize as a chart
- [ ] Future: Integrate with Oracle database instead of local CSV

📌 Purpose: Help accountants quickly **see, understand, and resolve mismatches** without using the command line.

---


---

## 🗄️ Oracle Database Integration (Post-Week 1 Planning)

- [ ] Set up a **local Oracle database** instance (XE or full)
- [ ] Create tables that mirror each `.csv` file schema
- [ ] Import all CSV files into Oracle tables using Python or SQL*Loader
- [ ] Build Flask integration using `cx_Oracle` or `SQLAlchemy + cx_Oracle`
- [ ] When Flask AI assistant is ready, use it to read/update the Oracle DB automatically
- [ ] Add `.env` or config file for secure DB credentials

This will replace CSV files with a real database as the backend once logic is verified.

---

## 🤖 AI Assistant Development Roadmap

- [ ] **Phase 1:** Build Flask AI assistant that works **only with CSV files**
  - [ ] Accept natural language input via a Flask route or CLI
  - [ ] Use OpenAI to detect mismatches or suggest changes
  - [ ] Automatically update the correct `.csv` file based on logic
  - [ ] Save a log of AI-generated changes for review

- [ ] **Phase 2:** Extend AI assistant to work with **local Oracle database**
  - [ ] Read records from Oracle instead of `.csv`
  - [ ] Perform the same reconciliation or update logic
  - [ ] Commit changes back to the Oracle database
  - [ ] Retain safety checks and change logs

This lets you start fast with file-based automation, then upgrade to full database integration once logic is tested and stable.
