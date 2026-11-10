"""Retrieval quality: recall@5 over 30 labelled questions. Run on demand; it is not a test.

Run against an indexed database and report the number when retrieval changes:
    docker compose run --rm agent python -m evals.retrieval
Prints each miss and exits 1 when recall drops below --min (default 0.9).
"""

import argparse
import sys

from app.search.hybrid import search

# Question, employee country, expected article title.
QUESTIONS = [
    ("How long is parental leave?", "DE", "Parental leave (Germany)"),
    ("How much notice do I need to give before parental leave?", "DE", "Parental leave (Germany)"),
    ("How many weeks of paid parental leave do I get?", "US", "Parental leave (United States)"),
    ("maternity leave weeks", "IN", "Parental leave (India)"),
    ("Is parental leave paid?", "GB", "Parental leave (United Kingdom)"),
    ("How many vacation days do I get per year?", "DE", "Annual leave (Germany)"),
    ("Can I carry over unused holiday to next year?", "US", "Annual leave (United States)"),
    ("When do I need a doctor's note for being ill?", "GB", "Sick leave (United Kingdom)"),
    ("How many paid sick days do I have?", "IN", "Sick leave (India)"),
    (
        "My father passed away, how much time off can I take?",
        "US",
        "Bereavement leave (United States)",
    ),
    ("Can I add my spouse to my health insurance?", "US", "Health insurance (United States)"),
    (
        "What is the out of pocket maximum for medical costs?",
        "GB",
        "Health insurance (United Kingdom)",
    ),
    ("Does the company match 401k contributions?", "US", "Retirement plan (United States)"),
    ("How much does Larkspur contribute to my pension?", "GB", "Retirement plan (United Kingdom)"),
    ("Provident fund contribution", "IN", "Retirement plan (India)"),
    ("When is open enrollment for benefits?", "US", "Benefits enrollment (United States)"),
    ("I got married, can I change my benefits?", "DE", "Benefits enrollment (Germany)"),
    ("Can I expense my gym membership?", "DE", "Wellbeing allowance (Germany)"),
    ("When is payday?", "GB", "Pay schedule (United Kingdom)"),
    ("How often am I paid?", "US", "Pay schedule (United States)"),
    (
        "My salary was wrong this month, how do I get it fixed?",
        "DE",
        "Payroll corrections (Germany)",
    ),
    ("I was overpaid, how will the money be recovered?", "IN", "Payroll corrections (India)"),
    (
        "What is the daily meal limit when travelling?",
        "US",
        "Expense reimbursement (United States)",
    ),
    ("mileage rate for using my own car", "GB", "Expense reimbursement (United Kingdom)"),
    ("Am I paid extra for working more than 40 hours?", "US", "Overtime (United States)"),
    ("Can I take time off instead of overtime pay?", "DE", "Overtime (Germany)"),
    ("How many days a week can I work from home?", "US", "Remote and hybrid work"),
    ("Can I work from another country for a month?", "IN", "Remote and hybrid work"),
    ("How long does HR take to respond to my case?", "GB", "How HR handles your case"),
    ("How long do you keep my personnel records?", "DE", "Employee data privacy"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--min", type=float, default=0.9, help="fail below this recall")
    args = parser.parse_args()

    misses = []
    for question, country, expected in QUESTIONS:
        titles = [r["title"] for r in search(question, country=country, top_k=5)]
        if expected not in titles:
            misses.append((question, expected, titles[:3]))
    recall = 1 - len(misses) / len(QUESTIONS)
    for miss in misses:
        print("MISS", miss)
    print(f"recall@5 = {recall:.2f} over {len(QUESTIONS)} questions")
    return 0 if recall >= args.min else 1


if __name__ == "__main__":
    sys.exit(main())
