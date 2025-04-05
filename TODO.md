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

- [ ] **Create `reconcile_gl_vs_ap.py`**
  - [ ] Group `gl_entries` by `account + period`
  - [ ] Group `ap_entries` by `account + period` where `status == 'posted'`
  - [ ] Compare totals and show mismatches
  - [ ] Print summary of matched vs unmatched
  - [ ] Save differences to a new `.csv` file

---

## 💵 Bank vs Book Reconciliation

- [ ] **Create `reconcile_bank_vs_book.py`**
  - [ ] Match entries by `bank_account`, `amount ± 0.01`, and `txn_date ± 3 days`
  - [ ] Identify unmatched rows in each dataset
  - [ ] Show total matched and unmatched amounts
  - [ ] Export unmatched rows to a `.csv` file

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
