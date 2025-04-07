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

# 🤖 AI-Powered Accounting Reconciliation Roadmap

A clear plan to evolve from a local CSV-based reconciliation app to an AI-driven, Oracle-integrated enterprise tool.

---

## 🧱 Phase 1: Build the Local Reconciliation App

🔨 Goal: Create a simple desktop or Flask app that:

- [x] Loads local datasets from the `data/` folder
- [x] Runs existing reconciliation logic (GL vs AP, Bank vs Book, Budget vs Actual)
- [x] Prints mismatches as plain text or table output
- [x] Has a **"Run Reconciliation"** button
- [x] Helps users manually inspect results

📌 This is the foundation — just view mismatches in a simple UI.

---

## 🤖 Phase 2: Build AI Assistant to Read CSV Files

🧠 Goal: Make a local Python-based assistant that:

- [ ] Reads datasets in `/data/*.csv`
- [ ] When launched, says **“Yes, I read this”** for each file
- [ ] Doesn’t do analysis yet — just proves file input works
- [ ] Logs what files were read and basic stats (rows, columns)

📌 Verifies AI input is working properly in a testable, observable way.

---

## 🧠 Phase 3: Enable AI to Compare and Reconcile CSVs

🛠️ Now evolve the AI assistant to:

- [ ] Analyze mismatches across CSV files
- [ ] Use existing rules (e.g., GL vs AP by account/period)
- [ ] Suggest corrections or auto-adjust datasets to match
- [ ] Write fixed datasets to `outputs/` and log changes to `outputs/ai_log.csv`

📌 This is the logic core — AI begins doing real accounting cleanup locally.

---

## 🖥️ Phase 4: Add AI into Local App

🎛️ Goal: Bring the AI directly into your local app:

- [ ] Embed the assistant into the interface
- [ ] When AI reads CSVs, show **“✅ AI read X rows from gl_entries.csv”**
- [ ] When mismatches are fixed, show:
  ```
  - AI fixed 6 mismatches between GL and AP
  - 3 records updated in gl_entries.csv
  ```
- [ ] Optionally display diffs or changes in a table

📌 No command line needed — full AI reconciliation from a single button.

---

## 🗄️ Phase 5: Build Local Oracle Database

🧱 Goal: Create a real database backend to replace CSVs:

- [ ] Use Oracle XE or local Docker Oracle
- [ ] Create tables that match `data/*.csv` schemas
- [ ] Import existing CSVs into those tables
- [ ] Validate data and allow SELECT queries

📌 This sets the stage for enterprise-scale data reconciliation.

---

## 🔄 Phase 6: Upgrade AI to Query Oracle

🧠 Now teach the assistant to:

- [ ] Use SQLAlchemy or cx_Oracle to connect to Oracle DB
- [ ] Fetch data from tables instead of reading CSVs
- [ ] Print something like **“✅ Pulled 1,000 rows from oracle.gl_entries”**
- [ ] Print that data to prove access works

📌 Verifies that the AI can talk to your actual accounting backend.

---

## 🧠 Phase 7: AI Reconciliation Against Oracle DB

The final level: make the AI fix Oracle data!

- [ ] AI compares Oracle data across modules
- [ ] Suggests or applies changes via SQL UPDATE
- [ ] All changes logged to `oracle_logs/ai_fixes.sql`
- [ ] Can run in sandbox mode before committing

📌 This is the full AI + DB + App loop — the vision of self-healing accounting pipelines.

---


