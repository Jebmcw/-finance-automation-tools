import pandas as pd
import random
import os
from datetime import datetime, timedelta

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_bank_txns(n=100, output_path="accounting-suite/data/bank_txns.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    bank_accounts = ['WF001', 'JPMC002']
    descriptions = ['Vendor payment', 'Client deposit', 'Bank fee', 'Interest credit', 'Wire transfer']
    cleared_flags = ['yes', 'no']

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 3, 31)

    data = []
    for i in range(n):
        amount = round(random.uniform(-5000, 10000), 2)
        data.append({
            'id': i + 1,
            'bank_account': random.choice(bank_accounts),
            'txn_date': random_date(start_date, end_date).strftime("%Y-%m-%d"),
            'amount': amount,
            'description': random.choice(descriptions),
            'cleared_flag': random.choice(cleared_flags),
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"[✓] Generated bank transactions at: {output_path}")

if __name__ == "__main__":
    generate_bank_txns()
