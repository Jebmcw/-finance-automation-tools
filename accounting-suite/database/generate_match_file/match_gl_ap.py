import pandas as pd
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import tempfile

from connect import get_oracle_connection  # your working Thin mode connection

def match_generate_gl():
    conn = get_oracle_connection()
    try:
        date_tag = datetime.now().strftime("%Y_%m_%d")
        new_table_name = f"New_GL_{date_tag}"

        project_root = os.path.dirname(os.path.dirname(__file__))
        sql_path = os.path.join(project_root, "schema", "011_create_match_gl_with_ap.sql")

        # Load actuals data
        ap_df = pd.read_sql("SELECT id, account,  company_code, amount, period FROM ap_entries", conn)
        ap_df.columns = ap_df.columns.str.lower()

        # Read and execute SQL script
        with open(sql_path, 'r') as file:
            sql = file.read()
            sql = sql.replace("match_gl_entries", new_table_name)
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
        gl_data = [
            (
                int(row['id']),
                row['account'],
                row['company_code'],
                float(row['amount']),
                row['period']
                
            )
            for _, row in ap_df.iterrows()
        ]

        # Insert data into new table
        with conn.cursor() as cur:
            insert_sql = f"""
                INSERT INTO {new_table_name} (id, account, company_code, amount, period)
                VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'))
            """
            cur.executemany(insert_sql, gl_data)

        conn.commit()
        print(f"✅ Inserted {len(gl_data)} rows into {new_table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def call_match_gl():
    conn = get_oracle_connection()
    match_gl_df = pd.read_sql("SELECT id, account,  company_code, amount, period FROM NEW_GL_2025_04_10", conn)
    conn.close()
    match_gl_df.columns = match_gl_df.columns.str.lower()

    # Save to temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", prefix="match_gl_", mode='w', newline='', encoding='utf-8')
    match_gl_df.to_csv(tmp.name, index=False)
    tmp.close()

    print(f"📎 File ready to download at: {tmp.name}")
    return tmp.name

if __name__ == "__main__":
    call_match_gl()
    #match_generate_gl()
    