# assistant/chat_bot.py

import openai
import os
import sys
from dotenv import load_dotenv

# Load env and path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Import intent router + commands
from prompt_router import get_action_from_prompt
from commands_reconcile import reconcile_bank_vs_book,reconcile_gl_vs_ap,reconcile_budget_vs_actual
from commands_match import match_bank_and_book, match_gl_and_ap, match_budget_and_actual
from commands_chart import reconciliation_chart, summary_table

def assistant():
    print("🧠 Reconciliation Assistant Online")
    print("Type something like:\n- 'Match the book and bank'\n- 'gl and ap data'\n- 'compare budget and actuals'\n- 'update the book file with bank numbers'\n- 'Print out the reconciliation chart'\n 'Print out the summary table'\n 'Exit'\n")

    while True:
        user_input = input("You: ").strip().lower()
        if user_input in ["exit", "quit"]:
            print("Assistant: Goodbye.")
            break

        action = get_action_from_prompt(user_input)

        if action == "bank_vs_book":
            print("Assistant:", reconcile_bank_vs_book())

        elif action == "gl_vs_ap":
            print("Assistant:", reconcile_gl_vs_ap())

        elif action == "budget_vs_actual":
            print("Assistant:", reconcile_budget_vs_actual())

        elif action == "match_book.csv":
            print("Assistant:", match_bank_and_book())

        elif action == "match_budget.csv":
            print("Assistant:", match_gl_and_ap())

        elif action == "match_gl.csv":
            print("Assistant:", match_budget_and_actual())

        elif action == "summary_table.png":
            print("Assistant:", summary_table())

        elif action == "reconciliation_chart.png":
              print("Assistant:", reconciliation_chart())

        else:
            print("Assistant: 🤔 Sorry, I didn’t understand that.")

if __name__ == "__main__":
    assistant()
