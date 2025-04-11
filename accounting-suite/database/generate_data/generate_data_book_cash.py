import pandas as pd
import random
import os

def generate_book_cash_from_bank(bank_txns_path="accounting-suite/data/bank_txns.csv",
                                  output_path="accounting-suite/data/book_cash.csv"):
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load the bank transactions
    if not os.path.exists(bank_txns_path):
        raise FileNotFoundError(f"Missing bank transactions file at: {bank_txns_path}")

    bank_df = pd.read_csv(bank_txns_path)

    # Modify the amounts and cleared flag
    book_data = []
    for _, row in bank_df.iterrows():
        new_amount = round(row['amount'] + random.uniform(-50, 50), 2)  # Change amount slightly
        book_data.append({
            'id': row['id'],
            'bank_account': row['bank_account'],
            'txn_date': row['txn_date'],
            'amount': new_amount,
            'description': row['description'],
            'cleared_flag': row['cleared_flag'],
        })

    # Save to CSV
    book_df = pd.DataFrame(book_data)
    book_df.to_csv(output_path, index=False)
    print(f"[✓] Generated book cash entries from bank txns at: {output_path}")

if __name__ == "__main__":
    generate_book_cash_from_bank()
