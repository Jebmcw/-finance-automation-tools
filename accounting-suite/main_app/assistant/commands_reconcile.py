import sys
import os
import pandas as pd
import io
import contextlib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.generate_reconciliation.gl_vs_ap import download_gl_vs_ap
from database.generate_reconciliation.bank_vs_book import download_bank_vs_book
from database.generate_reconciliation.variance_budget_actual import download_budget_vs_actual

def reconcile_bank_vs_book():
    try:
        # Redirect stdout to suppress print()
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = download_bank_vs_book()
        
        return f"✅ Bank vs Book Reconciliation:\nMatched: {result['matched_count']}, Mismatched: {result['unmatched_count']}"
    
    except Exception as e:
        return f"❌ Failed to get match stats: {e}"
    
def reconcile_gl_vs_ap():
    try:
        # Redirect stdout to suppress print()
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = download_gl_vs_ap()

        return f"✅ GL vs AP Reconciliation:\nMatched: {result['matched_count']}, Mismatched: {result['unmatched_count']}"
    except Exception as e:
        return f"❌ Failed to get match stats: {e}"

def reconcile_budget_vs_actual():
    try:
        # Redirect stdout to suppress print()
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            result = download_budget_vs_actual()

        return f"✅ Budget vs Actual Reconciliation:\nMatched: {result['matched_count']}, Mismatched: {result['unmatched_count']}"
    except Exception as e:
        return f"❌ Failed to get match stats: {e}"
    
if __name__ == "__main__":
    print("🧪 Testing bank vs book reconciliation...\n")
    msg = reconcile_budget_vs_actual()
    print(msg)