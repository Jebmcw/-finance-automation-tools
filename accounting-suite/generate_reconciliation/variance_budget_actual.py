import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connect import get_oracle_connection  # your working Thin mode connection

def run_budget_vs_actual_variance(
    output_dir="accounting-suite/database/data/outputs"
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
    result['Matched?'] = result.apply(
        lambda row: 'yes' if row['actuals_amount'] == row['budget_amount'] else 'no',
        axis=1
    )

    # Save result to CSV
    result.to_csv(output_file, index=False)

    # Print summary
    matched = (result['Matched?'] == 'yes').sum()
    mismatched = (result['Matched?'] == 'no').sum()

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

if __name__ == "__main__":
    run_budget_vs_actual_variance()