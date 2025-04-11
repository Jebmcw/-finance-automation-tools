import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connect import get_oracle_connection  # your working Thin mode connection

def run_gl_vs_ap_reconciliation():
    conn = get_oracle_connection()
    try:
        date_tag = datetime.now().strftime("%Y_%m_%d")
        new_table_name = f"GL_VS_AP_ENTRIES_{date_tag}"

        project_root = os.path.dirname(os.path.dirname(__file__))
        sql_path = os.path.join(project_root, "schema", "008_create_gl_vs_ap.sql")

        ap_df = pd.read_sql("SELECT id, account, company_code, amount FROM ap_entries", conn)
        ap_df.columns = ap_df.columns.str.lower()  # <-- normalize case
        gl_df = pd.read_sql("SELECT id, account, company_code, amount FROM gl_entries", conn)
        gl_df.columns = gl_df.columns.str.lower()  # <-- normalize case
        

        # Read and execute SQL script
        with open(sql_path, 'r') as file:
            sql = file.read()
            sql = sql.replace("gl_vs_ap", new_table_name)
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

        # No status filter — compare all AP entries
        # Align both datasets to compare top N rows equally
        min_len = min(len(ap_df), len(gl_df))
        ap_trimmed = ap_df.iloc[:min_len].copy().reset_index(drop=True)
        gl_trimmed = gl_df.iloc[:min_len].copy().reset_index(drop=True)

        # Build comparison DataFrame
        result = pd.DataFrame({
            'id': ap_trimmed['id'],
            'account': ap_trimmed['account'],
            'company_code': ap_trimmed['company_code'],
            'ap_amount': ap_trimmed['amount'],
            'gl_amount': gl_trimmed['amount'],
        })

        # Compare amounts exactly
        result['matched'] = result.apply(
            lambda row: 'yes' if row['ap_amount'] == row['gl_amount'] else 'no',
            axis=1
        )



        final_df = result[["id", "account", "company_code", "ap_amount", "gl_amount", "matched"]]

        gl_vs_ap_data = [
            (
                int(row['id']),
                row['account'],
                row['company_code'],
                row['ap_amount'],
                row['gl_amount'],
                row['matched']
            )
            for _, row in final_df.iterrows()
        ]

        # Insert data into new table
        with conn.cursor() as cur:
            insert_sql = f"""
                INSERT INTO {new_table_name}  (id, account,  company_code, ap_amount, gl_amount, matched)
                VALUES (:1, :2, :3, :4, :5, :6)
            """
            cur.executemany(insert_sql, gl_vs_ap_data)

        conn.commit()
        print(f"✅ Inserted {len(gl_vs_ap_data)} rows into {new_table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def download_gl_vs_ap():
    conn = get_oracle_connection()
    match_gl_vs_ap_df = pd.read_sql("SELECT id, account,  company_code, ap_amount, gl_amount, matched FROM GL_VS_AP_ENTRIES_2025_04_10", conn)
    conn.close()
    match_gl_vs_ap_df.columns = match_gl_vs_ap_df.columns.str.lower()

    return {
        "total_entries": len(match_gl_vs_ap_df),
        "matched_count": (match_gl_vs_ap_df["matched"] == "yes").sum(),
        "unmatched_count": (match_gl_vs_ap_df["matched"] == "no").sum(),
    }

if __name__ == "__main__":
   msg = download_gl_vs_ap()
   print(f"✅ Bank vs Book Reconciliation:\nMatched: {msg['matched_count']}, Mismatched: {msg['unmatched_count']}")