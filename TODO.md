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

- [ ] **Create `variance_budget_actual.py`**
  - [ ] Group `budgets.csv` by `account + period + cost_center`
  - [ ] Group `actuals.csv` by the same keys
  - [ ] Calculate variance and % variance
  - [ ] Flag large variances and save to `.csv`

---

## 🧪 One-Click Execution Script

- [ ] **Update or create `main.py`**
  - [ ] Add functions to call each reconciliation script
  - [ ] Print clean, readable summaries for each module
  - [ ] Optional: prompt user for module to run

---

## 🧹 Output Management

- [ ] Create `data/outputs/` folder (if needed)
- [ ] Save all result `.csv` files there
- [ ] Keep results named by module and date (e.g., `bank_recon_results_2024-04-05.csv`)

---

Track this checklist in VS Code using Markdown Preview or Markdown extensions like:
- Markdown All in One
- Todo Tree


---

## 💡 VS Code Extensions for Managing This Checklist

To track progress inside VS Code without switching tools:

### ✅ Recommended Extensions

- **Markdown All in One**  
  Adds checkbox support, live preview, keyboard shortcuts  
  👉 `yzhang.markdown-all-in-one`

- **Todo Tree**  
  Scans your codebase for `TODO`, `FIXME`, etc., and shows them in a sidebar  
  👉 `Gruntfuggly.todo-tree`

With these, you can check tasks off live as you go — no switching apps or tools.

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
