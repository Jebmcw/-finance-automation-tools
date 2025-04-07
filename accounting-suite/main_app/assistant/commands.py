# assistant/commands.py
import sys
import os
import pandas as pd
import io
import contextlib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from generate_reconciliation.gl_vs_ap import run_gl_vs_ap_reconciliation
from generate_reconciliation.bank_vs_book import run_bank_vs_book_reconciliation
from generate_reconciliation.variance_budget_actual import run_budget_vs_actual_variance

def reconcile_bank_vs_book():
    try:
        # Redirect stdout to suppress print()
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = run_bank_vs_book_reconciliation()
        
        return f"✅ Bank vs Book Reconciliation:\nMatched: {result['matched_count']}, Mismatched: {result['unmatched_count']}"
    
    except Exception as e:
        return f"❌ Failed to get match stats: {e}"
    
def reconcile_gl_vs_ap():
    try:
        # Redirect stdout to suppress print()
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = run_gl_vs_ap_reconciliation()

        return f"✅ GL vs AP Reconciliation:\nMatched: {result['matched']}, Mismatched: {result['mismatched']}"
    except Exception as e:
        return f"❌ Failed to get match stats: {e}"

def reconcile_budget_vs_actual():
    try:
        # Redirect stdout to suppress print()
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = run_budget_vs_actual_variance()

        return f"✅ Budget vs Actual Reconciliation:\nMatched: {result['matched']}, Mismatched: {result['mismatched']}"
    except Exception as e:
        return f"❌ Failed to get match stats: {e}"


if __name__ == "__main__":
    print("🧪 Testing bank vs book reconciliation...\n")
    msg = reconcile_budget_vs_actual()
    print(msg)




