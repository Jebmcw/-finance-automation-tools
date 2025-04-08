# assistant/commands.py
import sys
import os
import pandas as pd
import io
import contextlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def reconciliation_chart():
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            file_url="/static/pictures/reconciliation_chart.png"
        return (
            "📊 Reconciliation Chart:<br>"
            f"<img src='{file_url}' width='500'>"
        )
    except Exception as e:
        return f"❌ Failed to match book to bank: {e}"
    
def summary_table():
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            file_url="/static/pictures/summary_table.png"
        return (
        "✅ Here is the summary table:<br>"
        f"<img src='{file_url}' width='500'>"
    )
    except Exception as e:
        return f"❌ Failed to match book to bank: {e}"
    
if __name__ == "__main__":
    print("🧪 Testing bank vs book reconciliation...\n")
    msg = reconciliation_chart()
    print(msg)