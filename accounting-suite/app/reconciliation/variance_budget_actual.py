import pandas as pd
import os
from datetime import datetime

def run_budget_vs_actual_variance(
        budget_file = "accounting-suite/data/budgets.csv",
        actual_file="accounting-suite/data/actuals.csv",
        output_dir="accounting-suite/data/outputs",
        variance_threshold=0.2 # 20% threshold to flag Large variances
):
    """
    Compares budgeted vs actual amounts by account, period, and cost center.
    Saves a CSV report of variances and flags large discrepancies.

    Parameters:
        budget_file (str): Path to the budgets CSV file
        actual_file(str): Path to the actuals CSV file
        out_dir (str): Directory to save output CSV file
        variance_threshold (float): Threshold to flag large % variances

        Returns:
            dict: Summary of results
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load the CSV data into pandas DataFrames
    budgets = pd.read_csv(budget_file)
    actuals = pd.read_csv(actual_file)

    # Group budgets by account + period + cost_center
    budget_grouped = (
        budgets.groupby(['account','period','cost_center'])['budget_amount']
        .sum()
        .reset_index()
    )

    # Group by same keys and sum actuals
    actuals_grouped = (
        actuals.groupby(['account', 'period', 'cost_center'])['amount']
        .sum()
        .reset_index()
        .rename(columns= {'amount': 'actual_amount'})
    )

    # Outer join so we don't drop missing entries
    merged = pd.merge(
        budget_grouped,
        actuals_grouped,
        on=['account','period','cost_center'],
        how='outer'
    ).fillna(0) # Fill in missing values with 0

    # CALCULATE VARIANCE
    merged['variance']=merged['actual_amount'] - merged['budget_amount']

    # Calculate percentage variance (hanfle divide-by-zero carefully)
    merged['percent_variance'] = merged.apply(
        lambda row: (row['variance'] / abs(row['budget_amount'])) if row['budget_amount'] != 0 else 0,
        axis = 1
    )

    # FLAG LARGE VARIANCES
    merged['flagged']=merged['percent_variance'].abs() >= variance_threshold

    # SAVE TO CSV
    date_tag = datetime.now().strftime("%Y-%m-%d")
    output_file = f"{output_dir}/budget_vs_actuals_variance_{date_tag}.csv"
    merged.to_csv(output_file, index=False)

    # === PRINT SUMMARY ===
    flagged_count = merged['flagged'].sum()
    print("=== Budget vs Actuals Variance Report ===")
    print(f"Total records analyzed: {len(merged)}")
    print(f"Records flagged (>{variance_threshold*100:.0f}%): {flagged_count}")
    print(f"Output saved to: {output_file}")

    # === RETURN A SUMMARY DICTIONARY ===
    return {
        'total_records': len(merged),
        'flagged_records': int(flagged_count),
        'output_file': output_file
    }

# Run if script is called directly
if __name__ == "__main__":
    run_budget_vs_actual_variance()