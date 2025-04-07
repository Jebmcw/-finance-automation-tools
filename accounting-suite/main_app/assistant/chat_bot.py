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
from commands import reconcile_bank_vs_book,reconcile_gl_vs_ap

def assistant():
    print("🧠 Reconciliation Assistant Online")
    print("Type something like:\n- 'Match the book and bank'\n- 'Show me the chart'\n- 'Exit'\n")

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

        else:
            print("Assistant: 🤔 Sorry, I didn’t understand that.")

if __name__ == "__main__":
    assistant()
