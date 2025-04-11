# 💼 Finance Automation & AI Reconciliation Suite

An end-to-end, AI-enhanced accounting system that reads CSVs, syncs data to Oracle, runs reconciliation logic, and visualizes mismatches with downloadable charts. Includes a full web-based chatbot assistant powered by OpenAI and Flask.

---

## 📦 Features

- 🔁 **Automated Reconciliation**
  - GL vs AP
  - Bank vs Book
  - Budget vs Actuals

- 🧠 **AI Assistant (Chat-Based)**
  - Natural language prompt → system action
  - Automatically triggers data sync, analysis, and CSV downloads
  - OpenAI-powered classifier routes requests

- 🗃 **Oracle Integration**
  - Loads, stores, and reconciles data in real Oracle tables
  - SQL scripts automatically run table setup and inserts
  - Thin or Thick mode connection supported

- 📊 **Charts + Reports**
  - Bar chart and summary table saved to `/static/pictures`
  - All reconciliation mismatches downloadable as CSV

- 🌐 **Flask Web App**
  - Clean HTML/CSS chat interface
  - `/` to chat, `/clear` to reset
  - Assistant prints actions, links, and images

---

## 🧱 Project Structure

```
.
├── accounting-suite/
│   ├── data/                # Synthetic data files
│   ├── schema/              # SQL schema for Oracle tables
│   ├── generate_data_*.py   # Data simulators
│   ├── match_*.py           # Table generation and Oracle loading
│   ├── load_*.py            # CSV-to-Oracle loaders
│   ├── variance_budget_actual.py  # Budget variance logic
│   ├── gl_vs_ap.py, bank_vs_book.py  # Reconciliation logic
│   └── main.py              # Full chart/table summary generator
│
├── assistant/
│   ├── chat_bot.py
│   ├── prompt_router.py
│   ├── commands_match.py
│   ├── commands_chart.py
│   └── commands_reconcile.py
│
├── templates/
│   └── chat.html            # Chatbot frontend (Flask)
├── static/
│   ├── style.css
│   └── pictures/
│       ├── reconciliation_chart.png
│       └── summary_table.png
│
├── connect.py               # Oracle DB connector
├── app.py                   # Flask server
└── TODO.md                  # Completed roadmap
```

---

## ⚙️ Getting Started

### 1. Install Dependencies

```bash
pip install pandas openai flask python-dotenv matplotlib tabulate oracledb
```

### 2. Set Up Oracle Credentials

Update `config/db.env`:

```
ORACLE_USER=your_user
ORACLE_PASS=your_pass
ORACLE_CONNECT_STRING=your_db_low
ORACLE_WALLET_PATH=path_to_wallet
ORACLE_CLIENT_PATH=instantclient_dir
USE_THICK_MODE=true
OPENAI_API_KEY=your_openai_key
```

### 3. Run Everything

```bash
# Generate CSVs
python generate_data_ap_entries.py
...

# Load into Oracle
python load_ap_entries.py
...

# Match + Reconcile + Chart
python main.py
```

---

## 💬 Web Assistant (AI Chat)

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Sample Commands

- `compare budget to actual`
- `gl and ap`
- `match bank to book`
- `print the summary table`
- `overwrite book with bank`

---

## ✅ Current Status

You built:
- [x] Oracle-backed data loaders
- [x] Reconciliation logic
- [x] Chart/table report generators
- [x] Chat assistant w/ NLP routing
- [x] Full Flask frontend
- [x] GPT-powered classifier

---

## 🔮 Next Steps

- [ ] Dataset diff viewer in Flask UI
- [ ] Logging of auto-corrections (CSV + SQL)
- [ ] NLP summary: "why" mismatches happened
- [ ] Dockerize + deploy as internal audit tool

---

Built by a developer who refuses to manually match a single spreadsheet row ever again.