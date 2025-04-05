import pandas as pd
import random
import os
from datetime import datetime, timedelta

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_book_cash(n=100, output_path="accounting-suite/data/book_cash.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    bank_accounts = ['WF001', 'JPMC002']
    descriptions = ['Vendor payment', 'Client deposit', 'Internal transfer', 'Bank fee accrual', 'Manual journal']
    cleared_flags = ['yes', 'no']

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 3, 31)

    data = []
    for i in range(n):
        amount = round(random.uniform(-5000, 10000), 2)
        # Inject some internal-only items
        desc = random.choices(
            descriptions,
            weights=[0.3, 0.3, 0.2, 0.1, 0.1],
            k=1
        )[0]

        data.append({
            'id': i + 1,
            'bank_account': random.choice(bank_accounts),
            'txn_date': random_date(start_date, end_date).strftime("%Y-%m-%d"),
            'amount': amount,
            'description': desc,
            'cleared_flag': random.choice(cleared_flags),
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"[✓] Generated book cash entries at: {output_path}")

if __name__ == "__main__":
    generate_book_cash()
