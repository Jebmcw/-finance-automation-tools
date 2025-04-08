import pandas as pd
import os

def match_book_cash_from_bank(bank_txns_path="accounting-suite/data/bank_txns.csv"):
    # Make sure the output directory exists

    # Load the bank transactions
    if not os.path.exists(bank_txns_path):
        raise FileNotFoundError(f"Missing bank transactions file at: {bank_txns_path}")

    bank_df = pd.read_csv(bank_txns_path)

    # Modify the amounts and cleared flag
    match_book_data = []
    for _, row in bank_df.iterrows():
        match_book_data.append({
            'id': row['id'],
            'bank_account': row['bank_account'],
            'txn_date': row['txn_date'],
            'amount': row['amount'],
            'description': row['description'],
            'cleared_flag': row['cleared_flag'],
        })

    # Save to CSV
    output_path = os.path.join("accounting-suite","main_app", "static", "outputs", "match_book_cash.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    book_df = pd.DataFrame(match_book_data)
    book_df.to_csv(output_path, index=False)
    print(f"[✓] Generated book cash entries from bank txns at: {output_path}")

    return{
        "rows_written": len(book_df),
        "output_file": output_path
    }

if __name__ == "__main__":
    match_book_cash_from_bank()