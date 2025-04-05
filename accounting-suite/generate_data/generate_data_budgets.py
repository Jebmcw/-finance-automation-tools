import pandas as pd
import random
import os

def generate_budgets(n=100, output_path="accounting-suite/data/budgets.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cost_centers = ['4400', '4500', '4600']
    accounts = ['1000', '2000', '3000']
    periods = ['2024-01', '2024-02', '2024-03']

    data = []
    for i in range(n):
        acc = random.choice(accounts)
        # Revenue is positive, expense/payable accounts are negative
        amount = round(random.uniform(5000, 20000), 2) if acc == '3000' else round(random.uniform(-15000, -1000), 2)
        data.append({
            'id': i + 1,
            'cost_center': random.choice(cost_centers),
            'account': acc,
            'period': random.choice(periods),
            'budget_amount': amount,
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"[✓] Generated budgets at: {output_path}")

if __name__ == "__main__":
    generate_budgets()
