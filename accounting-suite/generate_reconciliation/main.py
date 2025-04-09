import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from gl_vs_ap import run_gl_vs_ap_reconciliation
from bank_vs_book import run_bank_vs_book_reconciliation
from variance_budget_actual import run_budget_vs_actual_variance

from tabulate import tabulate
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

def run_all_modules():
    os.makedirs("accounting-suite/database/data/outputs", exist_ok=True)

    summary = []

    # === GL vs AP Reconciliation ===
    gl_ap = run_gl_vs_ap_reconciliation()
    summary.append([
        "GL vs AP",
        gl_ap['matched'],
        gl_ap['mismatched']
    ])

    bank_book = run_bank_vs_book_reconciliation()
    summary.append([
        "Bank vs Book",
        bank_book['matched_count'],
        bank_book['unmatched_count']
       
    ])

    # === Budget vs Actuals Variance ===
    budget = run_budget_vs_actual_variance()
    summary.append([
        "Budget vs Actual",
        budget['matched'],
        budget['mismatched']
       
    ])

    # === Print as Table ===
    print("\n📊 Reconciliation Summary\n")
    print(tabulate(summary, headers=["Module", "Matched", "Unmatched/Flagged"], tablefmt="grid"))

    # === Save as CSV ===
    summary_df = pd.DataFrame(summary, columns=["Module", "Matched", "Unmatched/Flagged"])
    csv_path = "accounting-suite/database/data/outputs/summary_report.csv"
    summary_df.to_csv(csv_path, index=False)
    
    
    # === Bar Chart ===
    show_bar_chart(summary)

    # Table 
    show_table(summary)

def show_bar_chart(summary_data):
    modules = [row[0] for row in summary_data]
    values = [
        int(row[2]) if isinstance(row[2], int) or str(row[2]).isdigit() else 0
        for row in summary_data
    ]

    # === Plot chart ===
    plt.figure(figsize=(8, 5))
    plt.bar(modules, values)
    plt.title("Mismatched")
    plt.ylabel("Total_Number_Mismatched")
    plt.tight_layout()

    # === Save to file ===
    output_path = os.path.join("accounting-suite","main_app", "static", "pictures", "reconciliation_chart.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    print(f"[✓] Chart saved to {output_path}")
    plt.close()

def show_table(data):
    headers = ["Module", "Matched", "Unmatched/Flagged"]

    fig, ax = plt.subplots(figsize=(6, 0.6 * len(data) + 1))
    ax.axis('off')

    table = ax.table(cellText=data, colLabels=headers, cellLoc='center', loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    output_path = os.path.join("accounting-suite","main_app", "static", "pictures", "summary_table.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    return{
        "output_file": output_path
    }

if __name__ == "__main__":
    run_all_modules()
