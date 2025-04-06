# main.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from reconciliation.gl_vs_ap import run_gl_vs_ap_reconciliation
from reconciliation.bank_vs_book import run_bank_vs_book_reconciliation
from reconciliation.variance_budget_actual import run_budget_vs_actual_variance

from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

def run_all_modules():
    os.makedirs("accounting-suite/data/outputs", exist_ok=True)

    summary = []

    # === GL vs AP Reconciliation ===
    gl_ap = run_gl_vs_ap_reconciliation()
    summary.append([
        "GL vs AP",
        gl_ap['matched'],
        gl_ap['mismatched'],
        gl_ap['output_file']
    ])

    # === Bank vs Book Reconciliation ===
    bank = run_bank_vs_book_reconciliation()
    total_unmatched = bank['bank_unmatched'] + bank['book_unmatched']
    summary.append([
        "Bank vs Book",
        "-",
        total_unmatched,
        f"{bank['output_bank']} / {bank['output_book']}"
    ])

    # === Budget vs Actuals Variance ===
    budget = run_budget_vs_actual_variance()
    summary.append([
        "Budget vs Actual",
        budget['total_records'],
        budget['flagged_records'],
        budget['output_file']
    ])

    # === Print as Table ===
    print("\n📊 Reconciliation Summary\n")
    print(tabulate(summary, headers=["Module", "Matched", "Unmatched/Flagged", "Output File"], tablefmt="grid"))

    # === Save as CSV ===
    summary_df = pd.DataFrame(summary, columns=["Module", "Matched", "Unmatched/Flagged", "Output File"])
    csv_path = "accounting-suite/data/outputs/summary_report.csv"
    summary_df.to_csv(csv_path, index=False)
    print(f"\n[✓] Summary saved to {csv_path}")

    # === Bar Chart ===
    show_bar_chart(summary)

def show_bar_chart(summary_data):
    modules = [row[0] for row in summary_data]
    values = [
        int(row[2]) if isinstance(row[2], int) or str(row[2]).isdigit() else 0
        for row in summary_data
    ]

    # === Create pictures folder if not exists ===
    pictures_dir = "accounting-suite/data/pictures"
    os.makedirs(pictures_dir, exist_ok=True)

    # === Plot chart ===
    plt.figure(figsize=(8, 5))
    plt.bar(modules, values)
    plt.title("Unmatched / Flagged Counts per Module")
    plt.ylabel("Count")
    plt.tight_layout()

    # === Save to file ===
    filename = os.path.join(pictures_dir, "reconciliation_chart.png")
    plt.savefig(filename)
    print(f"[✓] Chart saved to {filename}")
    plt.close()
    
if __name__ == "__main__":
    run_all_modules()

