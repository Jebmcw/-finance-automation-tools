import pandas as pd
import os
from datetime import datetime
import sys
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from connect import get_oracle_connection  # your working Thin mode connection

def match_generate_book():
    conn = get_oracle_connection()
    try:
        date_tag = datetime.now().strftime("%Y_%m_%d")
        new_table_name = f"New_Book_{date_tag}"

        project_root = os.path.dirname(os.path.dirname(__file__))
        sql_path = os.path.join(project_root, "schema", "010_create_match_book_with_bank.sql")

        # Load actuals data
        bank_df = pd.read_sql("SELECT id, bank_account, txn_date, amount, description, cleared_flag FROM bank_txns", conn)
        bank_df.columns = bank_df.columns.str.lower()

        # Read and execute SQL script
        with open(sql_path, 'r') as file:
            sql = file.read()
            sql = sql.replace("match_book_cash", new_table_name)
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

        # Prepare data
        book_data = [
            (
                int(row['id']),
                row['bank_account'],
                row['txn_date'],
                float(row['amount']),
                row['description'],
                row['cleared_flag']
            )
            for _, row in bank_df.iterrows()
        ]

        # Insert data into new table
        with conn.cursor() as cur:
            insert_sql = f"""
                INSERT INTO {new_table_name} (id, bank_account, txn_date, amount, description,cleared_flag)
                VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4,  :5, :6)
            """
            cur.executemany(insert_sql, book_data)

        conn.commit()
        print(f"✅ Inserted {len(book_data)} rows into {new_table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def call_match_book():
    conn = get_oracle_connection()

    df = pd.read_sql(
        "SELECT id, bank_account, txn_date, amount, description, cleared_flag FROM NEW_BOOK_2025_04_10", 
        conn
    )
    conn.close()

    if df.empty:
        raise ValueError("Query returned no rows!")

    df.columns = df.columns.str.lower()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', newline='', encoding='utf-8')
    df.to_csv(tmp.name, index=False)
    tmp.close()

    return tmp.name  # or token if you're mapping it to a UUID

if __name__ == "__main__":

    #match_generate_book()
    call_match_book()
    #drop_table_if_exists("MATCH_BUDGET")