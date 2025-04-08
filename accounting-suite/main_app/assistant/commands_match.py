# assistant/commands.py
import sys
import os
import pandas as pd
import io
import contextlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from generate_match_file.match_book_bank import match_book_cash_from_bank
from generate_match_file.match_budget_actual import match_generate_budgets
from generate_match_file.match_gl_ap import match_generate_gl_entries_from_ap

def match_bank_and_book():
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = match_book_cash_from_bank()
            file_url="/static/outputs/match_book_cash.csv"
        return (
            f"✅ Book cash now matches bank transactions.\n"
            f"- Rows copied: {result['rows_written']}\n"
            f"<a href='{file_url}' download>📥 Download updated CSV</a>"
        )
    except Exception as e:
        return f"❌ Failed to match book to bank: {e}"
    
def match_budget_and_actual():
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = match_generate_budgets()
            file_url="/static/outputs/match_budget.csv"
        return (
            f"✅ Budget now matches actual transactions.\n"
            f"- Rows copied: {result['rows_written']}\n"
            f"<a href='{file_url}' download>📥 Download updated CSV</a>"
        )
    except Exception as e:
        return f"❌ Failed to match book to bank: {e}"
    
def match_gl_and_ap():
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = match_generate_gl_entries_from_ap()
            file_url="/static/outputs/match_gl.csv"
        return (
            f"✅ Gl now matches ap transactions.\n"
            f"- Rows copied: {result['rows_written']}\n"
            f"<a href='{file_url}' download>📥 Download updated CSV</a>"
        )
    except Exception as e:
        return f"❌ Failed to match book to bank: {e}"

if __name__ == "__main__":
    print("🧪 Testing bank vs book reconciliation...\n")
    msg = match_book_cash_from_bank()
    print(msg)




