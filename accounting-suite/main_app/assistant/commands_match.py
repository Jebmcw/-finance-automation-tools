# assistant/commands.py
import sys
import os
import pandas as pd
import io
import contextlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from database.generate_match_file.match_book_bank import call_match_book
from database.generate_match_file.match_budget_actual import call_match_budget
from database.generate_match_file.match_gl_ap import call_match_gl

def match_bank_and_book():
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            token = call_match_book()
            file_url=f"/download/{token}"
        return (
            f"✅ Book cash now matches bank transactions.\n"
            f"<a href='{file_url}' download>📥 Download updated CSV</a>"
        )
    except Exception as e:
        return f"❌ Failed to match book to bank: {e}"
    
def match_budget_and_actual():
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = call_match_budget()
            file_url=result
        return (
            f"✅ Budget now matches actual transactions.\n"
            f"<a href='{file_url}' download>📥 Download updated CSV</a>"
        )
    except Exception as e:
        return f"❌ Failed to match budget to actual: {e}"
    
def match_gl_and_ap():
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = call_match_gl()
            file_url=result
        return (
            f"✅ Gl now matches ap transactions.\n"
            f"<a href='{file_url}' download>📥 Download updated CSV</a>"
        )
    except Exception as e:
        return f"❌ Failed to match gl to ap: {e}"

if __name__ == "__main__":
    print("🧪 Testing bank vs book reconciliation...\n")
    msg = match_bank_and_book()
    print(msg)




