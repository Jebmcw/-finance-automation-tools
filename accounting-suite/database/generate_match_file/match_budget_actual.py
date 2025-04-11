import pandas as pd
import os
from datetime import datetime
import sys
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connect import get_oracle_connection  # your working Thin mode connection

def match_generate_budgets():
    conn = get_oracle_connection()
    try:
        date_tag = datetime.now().strftime("%Y_%m_%d")
        new_table_name = f"New_Budget_{date_tag}"

        project_root = os.path.dirname(os.path.dirname(__file__))
        sql_path = os.path.join(project_root, "schema", "012_create_budget_with_actuals.sql")

        # Load actuals data
        actuals_df = pd.read_sql("SELECT id, cost_center, account, amount, period FROM actuals", conn)
        actuals_df.columns = actuals_df.columns.str.lower()

        # Read and execute SQL script
        with open(sql_path, 'r') as file:
            sql = file.read()
            sql = sql.replace("match_budget", new_table_name)
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
        budget_data = [
            (
                int(row['id']),
                row['cost_center'],
                row['account'],
                float(row['amount']),
                row['period']
            )
            for _, row in actuals_df.iterrows()
        ]

        # Insert data into new table
        with conn.cursor() as cur:
            insert_sql = f"""
                INSERT INTO {new_table_name} (id, cost_center, account, amount, period)
                VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'))
            """
            cur.executemany(insert_sql, budget_data)

        conn.commit()
        print(f"✅ Inserted {len(budget_data)} rows into {new_table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def drop_table_if_exists(table_name):
    conn = get_oracle_connection()
    with conn.cursor() as cur:
        try:
            cur.execute(f'DROP TABLE "{table_name}"')
            print(f"✅ Dropped table: {table_name}")
        except Exception as e:
            print(f"⚠️ Could not drop table {table_name}: {e}")


def call_match_budget():
    conn = get_oracle_connection()
    match_budget_df = pd.read_sql("SELECT id, cost_center, account, amount, period FROM NEW_BUDGET_2025_04_10", conn)
    conn.close()
    match_budget_df.columns = match_budget_df.columns.str.lower()

    # Save to temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", prefix="match_budget_", mode='w', newline='', encoding='utf-8')
    match_budget_df.to_csv(tmp.name, index=False)
    tmp.close()

    print(f"📎 File ready to download at: {tmp.name}")
    return tmp.name

if __name__ == "__main__":
    #call_match_budget()
    #match_generate_budgets()
    drop_table_if_exists("GL_VS_AP_2025_04_10")

    
    
    