import pandas as pd
import random
import os

def generate_budgets(actual_path="accounting-suite/data/actuals.csv",
                                  output_path="accounting-suite/data/budget.csv"):
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load the bank transactions
    if not os.path.exists(actual_path):
        raise FileNotFoundError(f"Missing bank transactions file at: {actual_path}")

    actual_df = pd.read_csv(actual_path)

    # Modify the amounts and cleared flag
    budget_data= []
    for _, row in actual_df.iterrows():
        new_amount = round(row['amount'] + random.uniform(-50, 50), 2)  # Change amount slightly
        budget_data.append({
            'id': row['id'],
            'cost_center': row['cost_center'],
            'account': row['account'],
            'amount': new_amount,
            'period': row['period']
        })

    # Save to CSV
    budget_df = pd.DataFrame(budget_data)
    budget_df.to_csv(output_path, index=False)
    print(f"[✓] Generated book cash entries from bank txns at: {output_path}")

if __name__ == "__main__":
    generate_budgets()

