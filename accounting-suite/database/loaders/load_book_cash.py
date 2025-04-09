import os
import sys
import pandas as pd

# Add project root so we can import connect.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connect import get_oracle_connection  # your working Thin mode connection

def load_csv_to_oracle(csv_path, table_name):
    conn = get_oracle_connection()
    df = pd.read_csv(csv_path)

    # Parse txn_date column explicitly
    if "txn_date" in df.columns:
        df["txn_date"] = pd.to_datetime(df["txn_date"], errors="coerce")
    
    cursor = conn.cursor()
    inserted = 0

    for idx, row in df.iterrows():
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, bank_account, txn_date, amount, description, cleared_flag)
                VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6)
            """, (
                int(row["id"]),
                row["bank_account"],
                row["txn_date"].strftime("%Y-%m-%d") if pd.notnull(row["txn_date"]) else None,
                float(row["amount"]),
                row["description"],
                row["cleared_flag"]
            ))
            inserted += 1
        except Exception as e:
            print(f"⚠️ Failed to insert row {idx} (ID {row.get('id')}): {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Loaded {inserted} records from '{csv_path}' into table '{table_name}'.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_file = os.path.join(base_dir, "data", "book_cash.csv")

    print(f"📂 Looking for CSV at: {csv_file}")  # Add this line to debug

    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"CSV not found at {csv_file}")
    
    load_csv_to_oracle(csv_file, "book_cash")
