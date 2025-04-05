import pandas as pd
import os
from datetime import datetime

def run_udget_vs_actual_variance(
        budget_file = "accounting-suite/data/budgets.csv",
        actual_file="accounting-suite/data/actuals.csv",
        output_dir="accounting-suite/data/outputs",
        variance_threshold=0.2 # 20% threshold to flag Large variances
):
    """
    Compares budgeted vs actual amounts by account, period, and cost center.
    Saves a CSV report of variances and flags large discrepancies.
    
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load the CSVs
    budgets = pd.read_csv(budget_file)
    actuals = pd.read_csv(actual_file)

    # Group budgets by account + period + cost_center
    budget_grouped = (
        budgets.groupby(['account','period','cost_center'])['budget_amount']
        .sum()
        .reset_index()
    )

    # Group actuals the same way
    actuals_grouped = (
        actuals.groupby(['account', 'period'])
    )