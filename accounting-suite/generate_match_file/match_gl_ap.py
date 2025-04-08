import pandas as pd
import random
import os

def match_generate_gl_entries_from_ap(ap_path="accounting-suite/data/ap_entries.csv"):

    # Load AP entries
    ap_df = pd.read_csv(ap_path)

    # Create GL entries from AP entries
    gl_rows = []
    for _, row in ap_df.iterrows():
        gl_rows.append({
            'id': row['id'],
            'Vender'
            'account': row['account'],
            'company_code': row['company_code'],
            'amount': row['account'],
            'period': row['period']
        })
    # Save to CSV
    gl_output_path = os.path.join("accounting-suite","main_app", "static", "outputs", "match_gl.csv")
    os.makedirs(os.path.dirname(gl_output_path), exist_ok=True)

    gl_df = pd.DataFrame(gl_rows)
    gl_df.to_csv(gl_output_path, index=False)
    print(f"[✓] Generated GL entries from AP (with mismatched amounts): {gl_output_path}")

    return{
        "rows_written": len(gl_df),
        "output_file": gl_output_path
    }
if __name__ == "__main__":
    match_generate_gl_entries_from_ap()