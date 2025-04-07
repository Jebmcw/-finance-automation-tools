# app/reconciliation/bank_vs_book.py

import pandas as pd
import os
from datetime import datetime

def run_bank_vs_book_reconciliation(
    data_dir="accounting-suite/data",
    output_dir="accounting-suite/data/outputs",
    amount_tolerance=5.00
):
    """
    Reconciles bank transactions with book cash entries by comparing
    rows with the same ID and bank_account. Outputs all rows with match status.

    Output CSV columns: id, bank_account, amount_bank, amount_book, Matched?
    """

    os.makedirs(output_dir, exist_ok=True)

    bank_file = f"{data_dir}/bank_txns.csv"
    book_file = f"{data_dir}/book_cash.csv"
    date_tag = datetime.now().strftime("%Y-%m-%d")
    output_file = f"{output_dir}/bank_vs_book_match_report_{date_tag}.csv"

    # Load data
    bank_df = pd.read_csv(bank_file)
    book_df = pd.read_csv(book_file)

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
    print(f"[✓] Match report saved to: {output_file}")

    return {
        "total_entries": len(final_df),
        "matched_count": (final_df["Matched?"] == "Yes").sum(),
        "unmatched_count": (final_df["Matched?"] == "No").sum(),
        "output_file": output_file
    }






