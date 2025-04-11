import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connect import get_oracle_connection  # your working Thin mode connection

def run_budget_vs_actual_variance(
    output_dir="accounting-suite/data/outputs"
):
    os.makedirs(output_dir, exist_ok=True)
    date_tag = datetime.now().strftime("%Y-%m-%d")
    output_file = f"{output_dir}/budget_vs_actual_match_report_{date_tag}.csv"

    # Load from database
    conn = get_oracle_connection()
    actuals_df = pd.read_sql("SELECT id, cost_center, account, amount FROM actuals", conn)
    actuals_df.columns = actuals_df.columns.str.lower()  # <-- normalize case
    budget_df = pd.read_sql("SELECT id, cost_center, account, amount FROM budget", conn)
    budget_df.columns = budget_df.columns.str.lower()  # <-- normalize case
    conn.close()

    # No status filter — compare all AP entries
    # Align both datasets to compare top N rows equally
    min_len = min(len(actuals_df), len(budget_df))
    actuals_trimmed = actuals_df.iloc[:min_len].copy().reset_index(drop=True)
    budget_trimmed = budget_df.iloc[:min_len].copy().reset_index(drop=True)

    # Build comparison DataFrame
    result = pd.DataFrame({
        'id': actuals_trimmed['id'],
        'cost_center': actuals_trimmed['cost_center'],
        'account': actuals_trimmed['account'],
        'actuals_amount': actuals_trimmed['amount'],
        'budget_amount': budget_trimmed['amount'],
    })

    # Compare amounts exactly
    result['matched'] = result.apply(
        lambda row: 'yes' if row['actuals_amount'] == row['budget_amount'] else 'no',
        axis=1
    )

    # Save result to CSV
    result.to_csv(output_file, index=False)

    # Print summary
    matched = (result['matched'] == 'yes').sum()
    mismatched = (result['matched'] == 'no').sum()

    print("=== GL vs AP Reconciliation (1-to-1 by row) ===")
    print(f"Matched:    {matched}")
    print(f"Mismatched: {mismatched}")
    print(f"Total Rows Compared: {len(result)}")
    print(f"Saved to:   {output_file}")

    return {
        "matched": matched,
        "mismatched": mismatched,
        "total": len(result),
        "output_file": output_file
    }

def load_csv_to_oracle(csv_path, table_name):
    conn = get_oracle_connection()
    df = pd.read_csv(csv_path)

    
    cursor = conn.cursor()
    inserted = 0

    for idx, row in df.iterrows():
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, account,  company_code, ap_amount, gl_amount, matched)
                VALUES (:1, :2, :3,:4,:5,:6)
            """, (
                int(row["id"]),
                row["account"],
                row["company_code"],
                row["ap_amount"],
                row["gl_amount"],
                row["matched"]
            ))
            inserted += 1
        except Exception as e:
            print(f"⚠️ Failed to insert row {idx} (ID {row.get('id')}): {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Loaded {inserted} records from '{csv_path}' into table '{table_name}'.")

def load_csv_to_oracle(csv_path, table_name):
    conn = get_oracle_connection()
    df = pd.read_csv(csv_path)

    
    cursor = conn.cursor()
    inserted = 0

    for idx, row in df.iterrows():
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, cost_center,  account, actuals_amount, budget_amount, matched)
                VALUES (:1, :2, :3,:4,:5,:6)
            """, (
                int(row["id"]),
                row["cost_center"],
                row["account"],
                row["actuals_amount"],
                row["budget_amount"],
                row["matched"]
            ))
            inserted += 1
        except Exception as e:
            print(f"⚠️ Failed to insert row {idx} (ID {row.get('id')}): {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Loaded {inserted} records from '{csv_path}' into table '{table_name}'.")


def run_budget_vs_actual():
    conn = get_oracle_connection()
    try:
        date_tag = datetime.now().strftime("%Y_%m_%d")
        new_table_name = f"BUDGET_VS_ACTUAL_{date_tag}"

        project_root = os.path.dirname(os.path.dirname(__file__))
        sql_path = os.path.join(project_root, "schema", "009_create_budget_vs_actual.sql")

        actuals_df = pd.read_sql("SELECT id, cost_center, account, amount FROM actuals", conn)
        actuals_df.columns = actuals_df.columns.str.lower()  # <-- normalize case
        budget_df = pd.read_sql("SELECT id, cost_center, account, amount FROM budget", conn)
        budget_df.columns = budget_df.columns.str.lower()  # <-- normalize case
        
        # Read and execute SQL script
        with open(sql_path, 'r') as file:
            sql = file.read()
            sql = sql.replace("budget_vs_actual", new_table_name)
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
        min_len = min(len(actuals_df), len(budget_df))
        actuals_trimmed = actuals_df.iloc[:min_len].copy().reset_index(drop=True)
        budget_trimmed = budget_df.iloc[:min_len].copy().reset_index(drop=True)

        # Build comparison DataFrame
        result = pd.DataFrame({
            'id': actuals_trimmed['id'],
            'cost_center': actuals_trimmed['cost_center'],
            'account': actuals_trimmed['account'],
            'actuals_amount': actuals_trimmed['amount'],
            'budget_amount': budget_trimmed['amount'],
        })

        # Compare amounts exactly
        result['matched'] = result.apply(
            lambda row: 'yes' if row['actuals_amount'] == row['budget_amount'] else 'no',
            axis=1
        )

        final_df = result[["id", "cost_center", "account", "actuals_amount", "budget_amount", "matched"]]

        budget_vs_actual_data = [
            (
                int(row['id']),
                row['cost_center'],
                row['account'],
                row['actuals_amount'],
                row['budget_amount'],
                row['matched']
            )
            for _, row in final_df.iterrows()
        ]

        # Insert data into new table
        with conn.cursor() as cur:
            insert_sql = f"""
                INSERT INTO {new_table_name}  (id, cost_center,  account, actuals_amount, budget_amount, matched)
                VALUES (:1, :2, :3, :4, :5, :6)
            """
            cur.executemany(insert_sql, budget_vs_actual_data)

        conn.commit()
        print(f"✅ Inserted {len(budget_vs_actual_data)} rows into {new_table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def download_budget_vs_actual():
    conn = get_oracle_connection()
    match_budget_vs_actual_df = pd.read_sql("SELECT id, cost_center,  account, actuals_amount, budget_amount, matched FROM BUDGET_VS_ACTUAL_2025_04_11", conn)
    conn.close()
    match_budget_vs_actual_df.columns = match_budget_vs_actual_df.columns.str.lower()

    return {
        "total_entries": len(match_budget_vs_actual_df),
        "matched_count": (match_budget_vs_actual_df["matched"] == "yes").sum(),
        "unmatched_count": (match_budget_vs_actual_df["matched"] == "no").sum(),
    }

if __name__ == "__main__":
    #run_budget_vs_actual()
   msg = download_budget_vs_actual()
   print(f"✅ Bank vs Book Reconciliation:\nMatched: {msg['matched_count']}, Mismatched: {msg['unmatched_count']}")



