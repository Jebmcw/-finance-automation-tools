# app/reconciliation/bank_vs_book.py

import pandas as pd
from datetime import datetime, timedelta
import os

def run_bank_vs_book_reconciliation(
    data_dir="accounting-suite/data",
    output_dir="accounting-suite/data/outputs",
    date_tolerance_days=7,
    amount_tolerance=5.00
):
    """
    Reconciles bank transactions with internal book cash transactions.

    Matching logic:
    - Match on `bank_account`
    - `amount` within ± amount_tolerance
    - `txn_date` within ± date_tolerance_days

    Args:
        data_dir (str): Folder path where input CSVs live
        output_dir (str): Where to save unmatched rows
        date_tolerance_days (int): Tolerance window for matching dates
        amount_tolerance (float): Allowed rounding difference for amount

    Returns:
        dict: Count of matched and unmatched rows
    """

    os.makedirs(output_dir, exist_ok=True)

    # === File paths ===
    bank_file = f"{data_dir}/bank_txns.csv"
    book_file = f"{data_dir}/book_cash.csv"
    date_tag = datetime.now().strftime("%Y-%m-%d")
    bank_unmatched_file = f"{output_dir}/unmatched_bank_txns_{date_tag}.csv"
    book_unmatched_file = f"{output_dir}/unmatched_book_cash_{date_tag}.csv"

    # === Load both datasets ===
    bank_df = pd.read_csv(bank_file, parse_dates=["txn_date"])
    book_df = pd.read_csv(book_file, parse_dates=["txn_date"])

    # Add flags to track match status
    bank_df["matched"] = False
    book_df["matched"] = False

    # === Loop through bank txns and try to match ===
    for i, bank_row in bank_df.iterrows():
        for j, book_row in book_df.iterrows():
            if bank_row["bank_account"] != book_row["bank_account"]:
                continue
            if abs(bank_row["amount"] - book_row["amount"]) > amount_tolerance:
                continue
            if abs((bank_row["txn_date"] - book_row["txn_date"]).days) > date_tolerance_days:
                continue
            # Match found
            bank_df.at[i, "matched"] = True
            book_df.at[j, "matched"] = True
            break

    # === Get unmatched rows ===
    unmatched_bank = bank_df[bank_df["matched"] == False].drop(columns="matched")
    unmatched_book = book_df[book_df["matched"] == False].drop(columns="matched")

    # === Print Summary ===
    total_bank = len(bank_df)
    total_book = len(book_df)
    matched_bank = total_bank - len(unmatched_bank)
    matched_book = total_book - len(unmatched_book)

    print("=== Bank vs Book Reconciliation Summary ===")
    print(f"Total bank rows:     {total_bank}")
    print(f"Matched bank rows:   {matched_bank}")
    print(f"Unmatched bank rows: {len(unmatched_bank)}")
    print(f"Total book rows:     {total_book}")
    print(f"Matched book rows:   {matched_book}")
    print(f"Unmatched book rows: {len(unmatched_book)}")

    # === Save unmatched ===
    unmatched_bank.to_csv(bank_unmatched_file, index=False)
    unmatched_book.to_csv(book_unmatched_file, index=False)

    return {
        "bank_total": total_bank,
        "book_total": total_book,
        "bank_unmatched": len(unmatched_bank),
        "book_unmatched": len(unmatched_book),
        "output_bank": bank_unmatched_file,
        "output_book": book_unmatched_file
    }
