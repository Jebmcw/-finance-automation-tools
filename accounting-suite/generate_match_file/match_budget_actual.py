import pandas as pd
import random
import os

def match_generate_budgets(actual_path="accounting-suite/data/actuals.csv"):

    # Load the bank transactions
    if not os.path.exists(actual_path):
        raise FileNotFoundError(f"Missing bank transactions file at: {actual_path}")

    actual_df = pd.read_csv(actual_path)

    # Modify the amounts and cleared flag
    budget_data= []
    for _, row in actual_df.iterrows():
        budget_data.append({
            'id': row['id'],
            'cost_center': row['cost_center'],
            'account': row['account'],
            'amount': row['amount'],
            'period': row['period']
        })

    
    # Save to CSV
    output_path = os.path.join("accounting-suite","main_app", "static", "outputs", "match_budget.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    budget_df = pd.DataFrame(budget_data)
    budget_df.to_csv(output_path, index=False)
    print(f"[✓] Generated book cash entries from bank txns at: {output_path}")

    return{
        "rows_written": len(budget_df),
        "output_file": output_path
    }

if __name__ == "__main__":
    match_generate_budgets()