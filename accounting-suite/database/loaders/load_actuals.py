import os
import sys
import pandas as pd

# Add project root so we can import connect.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connect import get_oracle_connection  # your working Thin mode connection

def load_csv_to_oracle(csv_path, table_name):
    conn = get_oracle_connection()
    df = pd.read_csv(csv_path)

    
    cursor = conn.cursor()
    inserted = 0

    for idx, row in df.iterrows():
        try:
            period = pd.to_datetime(row["period"], format="%Y-%m") if pd.notnull(row["period"]) else None
            cursor.execute(f"""
                INSERT INTO {table_name} (id, cost_center, account, period, amount)
                VALUES (:1, :2, :3,TO_DATE(:4, 'YYYY-MM'),:5)
            """, (
                int(row["id"]),
                row["cost_center"],
                row["account"],
                period.strftime("%Y-%m") if period else None,
                float(row["amount"])
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
    csv_file = os.path.join(base_dir, "data", "actuals.csv")

    print(f"📂 Looking for CSV at: {csv_file}")  # Add this line to debug

    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"CSV not found at {csv_file}")
    
    load_csv_to_oracle(csv_file, "actuals")