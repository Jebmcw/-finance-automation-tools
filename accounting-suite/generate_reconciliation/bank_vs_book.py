# app/reconciliation/bank_vs_book.py

import pandas as pd
import os
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connect import get_oracle_connection  # your working Thin mode connection

def run_bank_vs_book_reconciliation(
    verbose=True,
    output_dir="accounting-suite/database/data/outputs",
    amount_tolerance=5.00
):
    os.makedirs(output_dir, exist_ok=True)
    date_tag = datetime.now().strftime("%Y-%m-%d")
    output_file = f"{output_dir}/bank_vs_book_match_report_{date_tag}.csv"

    # Load from database
    conn = get_oracle_connection()
    bank_df = pd.read_sql("SELECT id, bank_account, amount FROM bank_txns", conn)
    bank_df.columns = bank_df.columns.str.lower()  # <-- normalize case
    book_df = pd.read_sql("SELECT id, bank_account, amount FROM book_cash", conn)
    book_df.columns = book_df.columns.str.lower()  # <-- normalize case
    conn.close()

    # Merge on id and bank_account
    merged = pd.merge(
        bank_df[["id", "bank_account", "amount"]],
        book_df[["id", "bank_account", "amount"]],
        on=["id", "bank_account"],
        suffixes=("_bank", "_book"),
        how="inner"
    )

    # Add match flag
    merged["Matched?"] = merged.apply(
        lambda row: "Yes" if row["amount_bank"] == row["amount_book"] else "No",
        axis=1
    )

    # Final output columns
    final_df = merged[["id", "bank_account", "amount_bank", "amount_book", "Matched?"]]

    # Save to CSV
    final_df.to_csv(output_file, index=False)
    
    if verbose:
        print(f"[✓] Match report saved to: {output_file}")
        
    return {
        "total_entries": len(final_df),
        "matched_count": (final_df["Matched?"] == "Yes").sum(),
        "unmatched_count": (final_df["Matched?"] == "No").sum(),
        "output_file": output_file
    }

if __name__ == "__main__":
    run_bank_vs_book_reconciliation()




