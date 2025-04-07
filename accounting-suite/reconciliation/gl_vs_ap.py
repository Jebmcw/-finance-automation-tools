import pandas as pd
from datetime import datetime
import os

def run_gl_vs_ap_reconciliation(
    data_dir="accounting-suite/data",
    output_dir="accounting-suite/data/outputs"
):
    os.makedirs(output_dir, exist_ok=True)

    gl_file = f"{data_dir}/gl_entries.csv"
    ap_file = f"{data_dir}/ap_entries.csv"
    date_tag = datetime.now().strftime("%Y-%m-%d")
    output_file = f"{output_dir}/gl_vs_ap_match_report_{date_tag}.csv"

    # Load GL and AP files
    gl_df = pd.read_csv(gl_file)
    ap_df = pd.read_csv(ap_file)

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
