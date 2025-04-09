import os
import sys

# Add path to the project root to resolve connect.py
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from connect import get_oracle_connection

def run_sql_script(path):
    conn = get_oracle_connection()
    with open(path, 'r') as file:
        sql = file.read()
    try:
        with conn.cursor() as cur:
            # Split on /\n to detect PL/SQL block endings (like SQL*Plus)
            blocks = [s.strip() for s in sql.replace('\r\n', '\n').split('\n/\n') if s.strip()]

            for block in blocks:
                first_word = block.strip().split()[0].upper()

                # Strip trailing semicolon if present
                if first_word not in {"BEGIN", "DECLARE", "CREATE"} and block.endswith(';'):
                    block = block[:-1]
                elif first_word == "CREATE" and block.endswith(';'):
                    block = block[:-1]

                print("Executing block:\n", block)
                cur.execute(block)

            print("✅ Table gl_entries exists, row count:", cur.fetchone()[0])
            cur.execute("SELECT table_name FROM user_tables")
            print("📋 Tables in current schema:", [r[0] for r in cur.fetchall()])

        conn.commit()
        print(f"✅ Executed SQL script: {path}")
    except Exception as e:
        print(f"❌ Error executing script: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    sql_path = os.path.join(project_root, "schema", "006_create_budgets.sql")
    run_sql_script(sql_path)




