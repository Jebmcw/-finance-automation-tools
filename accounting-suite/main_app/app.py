from flask import Flask, render_template, request
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import reconciliation functions

from reconciliation.gl_vs_ap import run_gl_vs_ap_reconciliation
from reconciliation.bank_vs_book import run_bank_vs_book_reconciliation
from reconciliation.variance_budget_actual import run_budget_vs_actual_variance

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    gl_ap_result = None
    bank_book_result = None
    budget_actual_result = None
    chart_filename = None
    summary_filename= None

    if request.method == "POST":
        if "gl_ap" in request.form:
            gl_ap_result = run_gl_vs_ap_reconciliation()
        if "bank_book" in request.form:
            bank_book_result = run_bank_vs_book_reconciliation()
        if "budget_actual" in request.form:
            budget_actual_result = run_budget_vs_actual_variance()
        if "chart_path" in request.form:
            chart_filename = "reconciliation_chart.png"
        if "summary_path" in request.form:
            summary_filename="reconciliation_summary.png"

    return render_template(
        "index.html",
        gl_ap=gl_ap_result,
        bank_book=bank_book_result,
        budget_actual=budget_actual_result,
        chart_path=chart_filename,
        summary_path=summary_filename
    )

if __name__ == "__main__":
    app.run(debug=True)
