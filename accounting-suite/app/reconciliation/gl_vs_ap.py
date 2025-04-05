# app/reconciliation/gl_vs_ap.py

import pandas as pd
from datetime import datetime
import os

def run_gl_vs_ap_reconciliation(
    data_dir="accounting-suite/data",
    output_dir="accounting-suite/data/outputs"
):
    """
    Performs reconciliation between General Ledger (GL) entries and Accounts Payable (AP) entries.

    Steps:
    - Load GL and AP CSV files
    - Filter AP to include only 'posted' entries
    - Group both datasets by account and period
    - Compare totals and calculate mismatches
    - Print summary stats
    - Save mismatched records to an output CSV

    Args:
        data_dir (str): Path to directory containing input CSV files.
        output_dir (str): Path to directory to write output CSV files.

    Returns:
        dict: A summary of matched and mismatched record counts, and output file path.
    """

    # === Ensure output directory exists ===
    os.makedirs(output_dir, exist_ok=True)

    # === Define input and output file paths ===
    gl_file = f"{data_dir}/gl_entries.csv"
    ap_file = f"{data_dir}/ap_entries.csv"
    date_tag = datetime.now().strftime("%Y-%m-%d")
    output_file = f"{output_dir}/gl_vs_ap_mismatches_{date_tag}.csv"

    # === LOAD DATA ===
    # Read GL and AP files into pandas DataFrames
    gl_df = pd.read_csv(gl_file)
    ap_df = pd.read_csv(ap_file)

    # === FILTER AP TO 'POSTED' ONLY ===
    # We only reconcile finalized (posted) AP entries
    ap_posted = ap_df[ap_df['status'].str.lower() == 'posted']

    # === GROUP AND AGGREGATE BY ACCOUNT + PERIOD ===
    # Group GL data by account and period, summing amounts
    gl_grouped = (
        gl_df.groupby(['account', 'period'])['amount']
        .sum()
        .reset_index()
        .rename(columns={'amount': 'gl_total'})
    )

    # Do the same for AP data
    ap_grouped = (
        ap_posted.groupby(['account', 'period'])['amount']
        .sum()
        .reset_index()
        .rename(columns={'amount': 'ap_total'})
    )

    # === MERGE GL AND AP GROUPS FOR COMPARISON ===
    # Use outer join to ensure no missing records are dropped
    merged = pd.merge(gl_grouped, ap_grouped, on=['account', 'period'], how='outer').fillna(0)

    # === CALCULATE DIFFERENCE BETWEEN GL AND AP ===
    merged['difference'] = merged['gl_total'] - merged['ap_total']

    # Flag matched vs mismatched records using a small rounding threshold
    merged['status'] = merged['difference'].apply(
        lambda x: 'matched' if abs(x) < 0.01 else 'mismatched'
    )

    # === COUNT MATCHED VS MISMATCHED ===
    matched = (merged['status'] == 'matched').sum()
    mismatched = (merged['status'] == 'mismatched').sum()

    # === PRINT SUMMARY ===
    print("=== GL vs AP Reconciliation Summary ===")
    print(f"Matched:    {matched}")
    print(f"Mismatched: {mismatched}")
    print(f"Saved to:   {output_file}")

    # === SAVE MISMATCHED ROWS TO CSV ===
    mismatches = merged[merged['status'] == 'mismatched']
    mismatches.to_csv(output_file, index=False)

    # === RETURN SUMMARY FOR REPORTING OR LOGGING ===
    return {
        "matched": matched,
        "mismatched": mismatched,
        "output_file": output_file
    }
