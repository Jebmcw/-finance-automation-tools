import pandas as pd
import random
import os

def generate_ap_entries(n=100, output_path="accounting-suite/data/ap_entries.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    vendors = ['V001', 'V002', 'V003']
    accounts = ['2000','3000','4000']  # Payables liability account
    company_codes = ['1100', '1200']
    statuses = ['posted', 'unposted', 'paid']
    periods = ['2024-01', '2024-02', '2024-03']

    data = []
    for i in range(n):
        data.append({
            'id': i + 1,
            'vendor_id': random.choice(vendors),
            'account': random.choice(accounts),
            'company_code': random.choice(company_codes),
            'amount': round(random.uniform(-10000, -1000), 2),  # Payables = negative
            'period': random.choice(periods),
            'status': random.choice(statuses)
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"[✓] Generated AP entries at: {output_path}")

if __name__ == "__main__":
    generate_ap_entries()
