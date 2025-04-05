import pandas as pd
import random
import os

def generate_actuals(n=100, output_path="accounting-suite/data/actuals.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cost_centers = ['4400', '4500', '4600']
    accounts = ['1000', '2000', '3000']
    periods = ['2024-01', '2024-02', '2024-03']

    data = []
    for i in range(n):
        data.append({
            'id': i + 1,
            'cost_center': random.choice(cost_centers),
            'account': random.choice(accounts),
            'period': random.choice(periods),
            'amount': round(random.uniform(-15000, 20000), 2),
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"[✓] Generated actuals at: {output_path}")

if __name__ == "__main__":
    generate_actuals()
