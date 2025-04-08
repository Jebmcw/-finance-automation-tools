from flask import Flask, render_template, request, redirect, url_for
import sys
import os

# Add project root to import path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import reconciliation logic
from assistant.prompt_router import get_action_from_prompt
from assistant.commands_match import match_bank_and_book,match_budget_and_actual,match_gl_and_ap
from assistant.commands_reconcile import reconcile_bank_vs_book,reconcile_gl_vs_ap,reconcile_budget_vs_actual
from assistant.commands_chart import reconciliation_chart, summary_table
app = Flask(__name__)

# In-memory session log (note: not thread-safe in production)
chat_log = []

@app.route("/", methods=["GET", "POST"])
def chat():
    global chat_log

    # Clear chat on refresh
    if request.method == "GET":
        chat_log = []

    if request.method == "POST":
        user_input = request.form.get("message", "").strip()
        if not user_input:
            return render_template("chat.html", chat_log=chat_log)

        chat_log.append(f"You: {user_input}")
        action = get_action_from_prompt(user_input)

        # Action dispatch
        if action == "bank_vs_book":
            response = reconcile_bank_vs_book()
        elif action == "gl_vs_ap":
            response = reconcile_gl_vs_ap()
        elif action == "budget_vs_actual":
            response = reconcile_budget_vs_actual()
        elif action == "match_book.csv":
            response = match_bank_and_book()
        elif action == "match_budget.csv":
            response = match_budget_and_actual()
        elif action == "match_gl.csv":
            response = match_gl_and_ap()
        elif action == "reconciliation_chart.png":
            response = reconciliation_chart()
        elif action =="summary_table.png":
            response = summary_table()
        else:
            response = "🤔 Sorry, I didn’t understand that."

        chat_log.append(f"Assistant: {response}")

    return render_template("chat.html", chat_log=chat_log)

@app.route("/clear", methods=["POST"])
def clear_chat():
    global chat_log
    chat_log = []
    return redirect(url_for("chat"))

if __name__ == "__main__":
    app.run(debug=True)