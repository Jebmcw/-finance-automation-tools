import pandas as pd
import os

def generate_accounts(output_path="accounting-suite/data/accounts.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    accounts = [
        {"account_id": "1000", "name": "Cash", "type": "Asset", "parent_id": ""},
        {"account_id": "2000", "name": "Accounts Payable", "type": "Liability", "parent_id": ""},
        {"account_id": "3000", "name": "Revenue", "type": "Revenue", "parent_id": ""},
    ]

    df = pd.DataFrame(accounts)
    df.to_csv(output_path, index=False)
    print(f"[✓] Generated accounts at: {output_path}")

if __name__ == "__main__":
    generate_accounts()

