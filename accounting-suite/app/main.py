from reconciliation.gl_vs_ap import run_gl_vs_ap_reconciliation
from reconciliation.bank_vs_book import run_bank_vs_book_reconciliation


if __name__ == "__main__":
    result = run_gl_vs_ap_reconciliation()
    print(result)
    result = run_bank_vs_book_reconciliation()
print(result)