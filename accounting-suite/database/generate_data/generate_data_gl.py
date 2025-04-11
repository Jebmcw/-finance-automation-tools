import pandas as pd
import random
import os

def generate_gl_entries_from_ap(
    ap_path="accounting-suite/data/ap_entries.csv",
    gl_output_path="accounting-suite/data/gl_entries.csv",
    noise_range=(-50.00, 50.00)  # how much to offset the amount
):
    os.makedirs(os.path.dirname(gl_output_path), exist_ok=True)

    # Load AP entries
    ap_df = pd.read_csv(ap_path)

    # Create GL entries from AP entries
    gl_rows = []
    for _, row in ap_df.iterrows():
        noisy_amount = round(row['amount'] + random.uniform(*noise_range), 2)
        gl_rows.append({
            'id': row['id'],
            'Vender'
            'account': row['account'],
            'company_code': row['company_code'],
            'amount': noisy_amount,
            'period': row['period']
        })

    gl_df = pd.DataFrame(gl_rows)
    gl_df.to_csv(gl_output_path, index=False)
    print(f"[✓] Generated GL entries from AP (with mismatched amounts): {gl_output_path}")

if __name__ == "__main__":
    generate_gl_entries_from_ap()
