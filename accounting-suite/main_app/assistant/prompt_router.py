# assistant/prompt_router.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_action_from_prompt(user_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a classifier. Only respond with ONE of these action labels based on the user's request:\n"
                    "- bank_vs_book → Reconcile and compare bank transactions to book cash\n"
                    "- gl_vs_ap → Reconcile general ledger entries to accounts payable\n"
                    "- budget_vs_actual → Compare budgeted values to actual spending\n"
                    "- match_book.csv → Overwrite book cash file to match bank transactions\n"
                    "- match_budget.csv → Overwrite budget file to match actual file\n"
                    "- match_gl.csv → Overwrite gl file to match ap file\n"
                    "- reconciliation_chart.png → Print out the reconciliation chart"
                    "- summary_table.png → Print out the summary table"
                    "- unknown → If the request doesn’t match any of the above"
                )
            },
            {"role": "user", "content": user_prompt}
        ]
    )

    raw=response['choices'][0]['message']['content'].strip().lower()

    if "overwrite book" in user_prompt or "force book" in user_prompt or "update book" in user_prompt:
        return "match_book.csv"
    
    elif "overwrite budget" in user_prompt or "force budget" in user_prompt or "update budget" in user_prompt:
        return "match_budget.csv"
    
    elif "overwrite gl" in user_prompt or "force gl" in user_prompt or "update gl" in user_prompt:
        return "match_gl.csv"
    
    elif raw in ["bank_vs_book", "gl_vs_ap", "budget_vs_actual", "match_book.csv", "match_budget.csv", "match_gl.csv", "reconciliation_chart.png", "summary_table.png"]:
        return raw
    
    else:
        return "unknown"
    
if __name__ == "__main__":
    while True:
        prompt = input("Prompt: ")
        label = get_action_from_prompt(prompt)
        print(f"Action: {label}")
