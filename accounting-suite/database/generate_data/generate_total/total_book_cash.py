import pandas as pd
import os

def generate_total(book_path="accounting-suite/data/book_cash.csv",
                    output_path ="accounting-suite/data/total_amount/total_book_cash.csv"
):
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load the book cash CSV
    book_df = pd.read_csv(book_path)

    # Group by bank_account, txn_date, and cleared_flag, then sum the amounts
    grouped = (
        book_df
        .groupby(['bank_account', 'txn_date', 'cleared_flag'])['amount']
        .sum()
        .reset_index()
        .rename(columns={'amount': 'Total_amount'})
    )

    # Add a unique ID column
    grouped.insert(0, 'id', range(1, len(grouped)+ 1))

    # Save the grouped result to CSV
    grouped.to_csv(output_path, index=False)
    print(f"[✓] Totaled book cash saved to: {output_path}")

if __name__ == "__main__":
    generate_total()