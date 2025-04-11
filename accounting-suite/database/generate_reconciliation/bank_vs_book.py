# app/reconciliation/bank_vs_book.py

import pandas as pd
import os
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connect import get_oracle_connection  # your working Thin mode connection

def run_bank_vs_book_reconciliation():
    conn = get_oracle_connection()
    try:
        date_tag = datetime.now().strftime("%Y_%m_%d")
        new_table_name = f"BOOK_VS_BANK_{date_tag}"

        project_root = os.path.dirname(os.path.dirname(__file__))
        sql_path = os.path.join(project_root, "schema", "007_create_bank_vs_book.sql")

        bank_df = pd.read_sql("SELECT id, bank_account, amount FROM bank_txns", conn)
        bank_df.columns = bank_df.columns.str.lower()  # <-- normalize case
        book_df = pd.read_sql("SELECT id, bank_account, amount FROM book_cash", conn)
        book_df.columns = book_df.columns.str.lower()  # <-- normalize case
        # Read and execute SQL script
        with open(sql_path, 'r') as file:
            sql = file.read()
            sql = sql.replace("bank_vs_book", new_table_name)
        with conn.cursor() as cur:
            blocks = [s.strip() for s in sql.replace('\r\n', '\n').split('\n/\n') if s.strip()]
            for block in blocks:
                first_word = block.strip().split()[0].upper()
                if block.endswith(';'):
                    block = block[:-1]

                if first_word == "CREATE" and "TABLE" in block.upper():
                    try:
                        tokens = block.split()
                        table_index = tokens.index("TABLE") + 1
                        table_name = tokens[table_index].strip('"').strip()
                        cur.execute(f'DROP TABLE {table_name}')
                        print(f"🧹 Dropped existing table: {table_name}")
                    except Exception as drop_err:
                        print(f"⚠️ Could not drop table (likely doesn't exist): {drop_err}")

                print("🚀 Executing block:\n", block)
                cur.execute(block)

            cur.execute("SELECT table_name FROM user_tables")
            print("📋 Tables in current schema:", [r[0] for r in cur.fetchall()])

        conn.commit()
        print(f"✅ Executed SQL script: {sql_path}")

        # Merge on id and bank_account
        merged = pd.merge(
            bank_df[["id", "bank_account", "amount"]],
            book_df[["id", "bank_account", "amount"]],
            on=["id", "bank_account"],
            suffixes=("_bank", "_book"),
            how="inner"
        )

        # Add match flag
        merged["matched"] = merged.apply(
            lambda row: "Yes" if row["amount_bank"] == row["amount_book"] else "No",
            axis=1
        )

        # Final output columns
        final_df = merged[["id", "bank_account", "amount_bank", "amount_book", "matched"]]

        # Prepare data
        bank_vs_book_data = [
            (
                int(row['id']),
                row['bank_account'],
                row['amount_bank'],
                float(row['amount_book']),
                row['matched']

            )
            for _, row in final_df.iterrows()
        ]

        # Insert data into new table
        with conn.cursor() as cur:
            insert_sql = f"""
                INSERT INTO {new_table_name} (id, bank_account, amount_bank, amount_book, matched)
                VALUES (:1, :2, :3, :4, :5)
            """
            cur.executemany(insert_sql, bank_vs_book_data)

        conn.commit()
        print(f"✅ Inserted {len(bank_vs_book_data)} rows into {new_table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def download_bank_vs_book():
    conn = get_oracle_connection()
    match_bank_vs_book_df = pd.read_sql("SELECT id, bank_account, amount_bank, amount_book,  matched FROM BOOK_VS_BANK_2025_04_10", conn)
    conn.close()
    match_bank_vs_book_df.columns = match_bank_vs_book_df.columns.str.lower()

    return {
        "total_entries": len(match_bank_vs_book_df),
        "matched_count": (match_bank_vs_book_df["matched"] == "Yes").sum(),
        "unmatched_count": (match_bank_vs_book_df["matched"] == "No").sum(),
    }

if __name__ == "__main__":
   #run_bank_vs_book_reconciliation()
    result = download_bank_vs_book()
    



