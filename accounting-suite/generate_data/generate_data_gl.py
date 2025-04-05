import pandas as pd
import random
from datetime import datetime, timedelta

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_gl_entries(n=100):
    accounts = ['1000', '2000', '3000']
    data = []
    for _ in range(n):
        data.append({
            'id': _ + 1,
            'account': random.choice(accounts),
            'company_code': random.choice(['1100', '1200']),
            'amount': round(random.uniform(-10000, 10000), 2),
            'period': random.choice(['2024-01', '2024-02', '2024-03']),
        })
    df = pd.DataFrame(data)
    df.to_csv("accounting-suite/data/gl_entries.csv", index=False)

generate_gl_entries()
