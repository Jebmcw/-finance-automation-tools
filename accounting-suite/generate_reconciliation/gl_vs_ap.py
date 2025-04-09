import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.connect import get_oracle_connection  # your working Thin mode connection

def run_gl_vs_ap_reconciliation(
    output_dir="accounting-suite/database/data/outputs"
):
    os.makedirs(output_dir, exist_ok=True)
    date_tag = datetime.now().strftime("%Y-%m-%d")
    output_file = f"{output_dir}/gl_vs_ap_match_report_{date_tag}.csv"

    # Load from database
    conn = get_oracle_connection()
    ap_df = pd.read_sql("SELECT id, account, company_code, amount FROM ap_entries", conn)
    ap_df.columns = ap_df.columns.str.lower()  # <-- normalize case
    gl_df = pd.read_sql("SELECT id, account, company_code, amount FROM gl_entries", conn)
    gl_df.columns = gl_df.columns.str.lower()  # <-- normalize case
    conn.close()

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
    result['Matched?'] = result.apply(
        lambda row: 'yes' if row['ap_amount'] == row['gl_amount'] else 'no',
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
    run_gl_vs_ap_reconciliation()