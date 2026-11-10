#!/usr/bin/env python3
"""Generates the synthetic HR policy library for a fictional company, Larkspur Technologies.

Writes one JSON file per article to ./corpus. All content is invented for the prototype.
Usage: python3 scripts/generate_corpus.py
"""

import json
import uuid
from pathlib import Path

COMPANY = "Larkspur Technologies"
OUT = Path(__file__).resolve().parent.parent / "corpus"
NS = uuid.UUID("6f1c2a52-8e0b-4b8e-9a4f-5d2b7c1e9a10")

COUNTRIES = {
    "US": {
        "name": "the United States",
        "short": "United States",
        "currency": "USD",
        "entity": "Larkspur Technologies Inc.",
    },
    "DE": {
        "name": "Germany",
        "short": "Germany",
        "currency": "EUR",
        "entity": "Larkspur Technologies GmbH",
    },
    "IN": {
        "name": "India",
        "short": "India",
        "currency": "INR",
        "entity": "Larkspur Technologies India Pvt. Ltd.",
    },
    "GB": {
        "name": "the United Kingdom",
        "short": "United Kingdom",
        "currency": "GBP",
        "entity": "Larkspur Technologies Ltd",
    },
}

# Each topic: category, display name, fact templates, and per-country parameters.
TOPICS = {
    "parental_leave": {
        "area": "leave",
        "name": "Parental leave",
        "noun": "parental leave",
        "eligibility": [
            "Employees in {country} are eligible for parental leave after {tenure} of continuous employment.",
            "Parental leave applies equally to birth, adoption and surrogacy, and to every parent regardless of gender.",
        ],
        "entitlement": [
            "{entitlement}",
            "Leave can be taken in up to {blocks} separate blocks, and every block must be at least two weeks long.",
            "Parental leave must start within {window} of the birth or placement of the child.",
        ],
        "pay": [
            "During parental leave you receive {pay}.",
            "Your pension contributions and health coverage continue during paid parental leave.",
        ],
        "process": [
            "Leave must be requested in writing at least {notice} before it starts.",
            "Submit the request through the HR portal and attach the expected due date or placement confirmation.",
            "Your manager confirms the dates within five working days of your request.",
        ],
        "table": [
            ("Entitlement", "{entitlement_short}"),
            ("Paid portion", "{paid_short}"),
            ("Notice period", "{notice}"),
            ("Minimum service", "{tenure}"),
        ],
        "params": {
            "US": dict(
                tenure="6 months",
                entitlement="Employees in the United States are entitled to 16 weeks of paid parental leave per child.",
                entitlement_short="16 weeks",
                paid_short="16 weeks at 100% of base salary",
                pay="100% of your base salary for all 16 weeks",
                notice="30 days",
                blocks="two",
                window="12 months",
            ),
            "DE": dict(
                tenure="6 months",
                entitlement="Employees in Germany are entitled to up to 3 years of parental leave per child.",
                entitlement_short="Up to 3 years",
                paid_short="14 weeks topped up to 100% of base salary",
                pay="statutory parental allowance, which Larkspur tops up to 100% of your base salary for the first 14 weeks",
                notice="7 weeks",
                blocks="three",
                window="8 years",
            ),
            "IN": dict(
                tenure="80 days",
                entitlement="Employees in India are entitled to 26 weeks of paid leave for birth mothers and 4 weeks of paid leave for other parents.",
                entitlement_short="26 weeks (birth mother), 4 weeks (other parents)",
                paid_short="All weeks at 100% of base salary",
                pay="100% of your base salary for the full entitlement",
                notice="8 weeks",
                blocks="two",
                window="6 months",
            ),
            "GB": dict(
                tenure="26 weeks",
                entitlement="Employees in the United Kingdom are entitled to up to 52 weeks of parental leave per child.",
                entitlement_short="Up to 52 weeks",
                paid_short="26 weeks enhanced pay",
                pay="100% of your base salary for the first 26 weeks and statutory pay for the following 13 weeks",
                notice="15 weeks",
                blocks="three",
                window="12 months",
            ),
        },
    },
    "annual_leave": {
        "area": "leave",
        "name": "Annual leave",
        "noun": "annual leave",
        "eligibility": [
            "Annual leave accrues from your first day of employment in {country}.",
            "Part-time employees accrue annual leave in proportion to their contracted hours.",
        ],
        "entitlement": [
            "Full-time employees in {country} receive {days} working days of paid annual leave per calendar year.",
            "Up to {carry} unused days can be carried over to the next year and must be used by {carry_deadline}.",
            "Unused days above the carry-over limit are forfeited unless local law requires payment.",
        ],
        "pay": [
            "Annual leave is paid at your normal base salary, including regular allowances.",
            "Holiday pay for variable earnings is calculated on the average of the previous {avg_weeks} weeks.",
        ],
        "process": [
            "Request annual leave in the HR portal at least {notice} before the first day of leave.",
            "Requests of more than ten consecutive working days need approval from your manager and your department head.",
            "Approved leave can be cancelled by you up to two working days before it starts.",
        ],
        "table": [
            ("Annual entitlement", "{days} days"),
            ("Carry-over limit", "{carry} days"),
            ("Carry-over deadline", "{carry_deadline}"),
            ("Notice for requests", "{notice}"),
        ],
        "params": {
            "US": dict(
                days="20", carry="5", carry_deadline="31 March", avg_weeks="12", notice="2 weeks"
            ),
            "DE": dict(
                days="30", carry="10", carry_deadline="31 March", avg_weeks="13", notice="3 weeks"
            ),
            "IN": dict(
                days="24", carry="12", carry_deadline="30 June", avg_weeks="12", notice="2 weeks"
            ),
            "GB": dict(
                days="27", carry="5", carry_deadline="31 March", avg_weeks="52", notice="2 weeks"
            ),
        },
    },
    "sick_leave": {
        "area": "leave",
        "name": "Sick leave",
        "noun": "sick leave",
        "eligibility": [
            "All employees in {country} are covered by this sick leave policy from their first day."
        ],
        "entitlement": [
            "You can take up to {paid_days} working days of paid sick leave per calendar year.",
            "A medical certificate is required for absences longer than {cert_days} consecutive calendar days.",
            "Long-term illness beyond the paid entitlement is handled under the long-term absence process.",
        ],
        "pay": ["Paid sick leave is paid at {sick_pay}.", "{statutory}"],
        "process": [
            "Tell your manager before your usual start time on the first day of absence.",
            "Record the absence in the HR portal on your first day back at the latest.",
            "Upload any medical certificate to the HR portal; it is visible only to HR.",
        ],
        "table": [
            ("Paid sick days", "{paid_days} per year"),
            ("Certificate needed after", "{cert_days} days"),
            ("Sick pay", "{sick_pay_short}"),
        ],
        "params": {
            "US": dict(
                paid_days="10",
                cert_days="3",
                sick_pay="100% of base salary",
                sick_pay_short="100%",
                statutory="Where state law grants more paid sick time, the state entitlement applies.",
            ),
            "DE": dict(
                paid_days="30",
                cert_days="3",
                sick_pay="100% of base salary for up to six weeks per illness",
                sick_pay_short="100% for six weeks",
                statutory="After six weeks, statutory sickness benefit from your health insurer applies.",
            ),
            "IN": dict(
                paid_days="12",
                cert_days="2",
                sick_pay="100% of base salary",
                sick_pay_short="100%",
                statutory="Employees covered by state insurance may also claim sickness benefit.",
            ),
            "GB": dict(
                paid_days="20",
                cert_days="7",
                sick_pay="100% of base salary for the first 20 days",
                sick_pay_short="100% for 20 days",
                statutory="Statutory Sick Pay is included in, not added to, company sick pay.",
            ),
        },
    },
    "bereavement_leave": {
        "area": "leave",
        "name": "Bereavement leave",
        "noun": "bereavement leave",
        "eligibility": [
            "Bereavement leave is available to all employees in {country} from their first day."
        ],
        "entitlement": [
            "You can take up to {close_days} working days of paid leave after the death of a spouse, partner, child or parent.",
            "You can take up to {other_days} working days of paid leave after the death of another family member.",
            "Additional unpaid leave of up to {unpaid} can be agreed with your manager.",
        ],
        "pay": ["Bereavement leave is paid at your normal base salary."],
        "process": [
            "Tell your manager as soon as you reasonably can; no advance notice is required.",
            "Record the leave in the HR portal within {record} of returning to work.",
            "No documentation is required for bereavement leave.",
        ],
        "table": [
            ("Close family", "{close_days} days"),
            ("Other family", "{other_days} days"),
            ("Extra unpaid leave", "Up to {unpaid}"),
        ],
        "params": {
            "US": dict(close_days="5", other_days="3", unpaid="10 days", record="2 weeks"),
            "DE": dict(close_days="5", other_days="2", unpaid="10 days", record="2 weeks"),
            "IN": dict(close_days="7", other_days="3", unpaid="15 days", record="2 weeks"),
            "GB": dict(close_days="5", other_days="3", unpaid="10 days", record="2 weeks"),
        },
    },
    "health_insurance": {
        "area": "benefits",
        "name": "Health insurance",
        "noun": "health insurance",
        "eligibility": [
            "Employees in {country} working at least {min_hours} hours per week are eligible for company health insurance.",
            "Coverage starts {start}.",
        ],
        "entitlement": [
            "{coverage}",
            "Spouses, registered partners and children under {child_age} can be added as dependants.",
            "Annual out-of-pocket costs are capped at {cap} per person.",
        ],
        "pay": [
            "Larkspur pays {employer_share} of the premium for employees and {dependant_share} for dependants.",
            "Your share of the premium is deducted from your monthly salary before tax where local law allows.",
        ],
        "process": [
            "Enroll within {enroll_window} of your start date through the benefits portal.",
            "To add a dependant after a life event, submit the change within 30 days of the event.",
            "Claims are submitted directly to the insurer, not to Larkspur.",
        ],
        "table": [
            ("Employer share (employee)", "{employer_share}"),
            ("Employer share (dependants)", "{dependant_share}"),
            ("Out-of-pocket cap", "{cap}"),
            ("Enrollment window", "{enroll_window}"),
        ],
        "params": {
            "US": dict(
                min_hours="30",
                start="on the first day of the month after your start date",
                coverage="The company plan covers medical, dental and vision care through a national provider network.",
                child_age="26",
                cap="USD 3,000",
                employer_share="90%",
                dependant_share="75%",
                enroll_window="30 days",
            ),
            "DE": dict(
                min_hours="20",
                start="on your first day, as statutory insurance is mandatory",
                coverage="Larkspur adds private supplementary cover for dental and vision care on top of statutory health insurance.",
                child_age="25",
                cap="EUR 600",
                employer_share="100% of the supplementary cover",
                dependant_share="50% of the supplementary cover",
                enroll_window="60 days",
            ),
            "IN": dict(
                min_hours="20",
                start="on your first day",
                coverage="The group medical policy covers hospitalisation up to INR 1,000,000 per family per year.",
                child_age="25",
                cap="INR 50,000",
                employer_share="100%",
                dependant_share="100% for spouse and children, 50% for parents",
                enroll_window="30 days",
            ),
            "GB": dict(
                min_hours="20",
                start="on the first day of the month after your start date",
                coverage="Private medical insurance covers specialist consultations, diagnostics and hospital treatment.",
                child_age="21",
                cap="GBP 250",
                employer_share="100%",
                dependant_share="50%",
                enroll_window="30 days",
            ),
        },
    },
    "retirement_plan": {
        "area": "benefits",
        "name": "Retirement plan",
        "noun": "the retirement plan",
        "eligibility": ["Employees in {country} can join the retirement plan {join}."],
        "entitlement": [
            "Larkspur matches {match}.",
            "Employer contributions vest {vesting}.",
            "You can change your contribution rate {changes}.",
        ],
        "pay": [
            "Contributions are deducted from your salary {tax}.",
            "The plan is administered by an external provider who holds the funds in your name.",
        ],
        "process": [
            "You are enrolled automatically at a {auto_rate} contribution rate unless you opt out within 30 days.",
            "Change your contribution rate or investment choices in the provider's portal.",
            "If you leave Larkspur, your vested balance stays yours and can be transferred.",
        ],
        "table": [
            ("Employer match", "{match_short}"),
            ("Vesting", "{vesting_short}"),
            ("Default contribution", "{auto_rate}"),
        ],
        "params": {
            "US": dict(
                join="from your first day",
                match="100% of your contributions up to 4% of base salary and 50% of the next 2%",
                match_short="Up to 5% of base salary",
                vesting="over three years, one third per year of service",
                vesting_short="3 years, graded",
                changes="at any time",
                tax="before tax in the 401(k) plan, or after tax in the Roth option",
                auto_rate="4%",
            ),
            "DE": dict(
                join="after your probation period",
                match="your deferred compensation by 20% and adds a fixed 3% of base salary",
                match_short="20% of deferrals plus 3% of base salary",
                vesting="immediately",
                vesting_short="Immediate",
                changes="once per calendar year",
                tax="before tax and social security within the statutory limits",
                auto_rate="2%",
            ),
            "IN": dict(
                join="from your first day through the Provident Fund",
                match="12% of basic salary into the Provident Fund",
                match_short="12% of basic salary",
                vesting="immediately",
                vesting_short="Immediate",
                changes="each April for voluntary contributions",
                tax="under the statutory Provident Fund rules",
                auto_rate="12%",
            ),
            "GB": dict(
                join="from your first day",
                match="your contributions up to 6% of base salary",
                match_short="Up to 6% of base salary",
                vesting="immediately",
                vesting_short="Immediate",
                changes="at any time",
                tax="through salary sacrifice, which reduces tax and National Insurance",
                auto_rate="5%",
            ),
        },
    },
    "benefits_enrollment": {
        "area": "benefits",
        "name": "Benefits enrollment",
        "noun": "benefits enrollment",
        "eligibility": [
            "New employees in {country} enroll in benefits within {new_window} of their start date.",
            "Everyone else can change benefits during open enrollment or after a qualifying life event.",
        ],
        "entitlement": [
            "Open enrollment runs every year from {open_start} to {open_end}.",
            "Choices made during open enrollment take effect on {effective}.",
            "Qualifying life events include marriage, divorce, birth or adoption of a child, and loss of other coverage.",
        ],
        "pay": [
            "Benefit costs for the new plan year appear on your first payslip after the effective date."
        ],
        "process": [
            "Make your choices in the benefits portal; changes are not accepted by email.",
            "Report a qualifying life event within 30 days and attach supporting documents.",
            "If you miss open enrollment, your current choices roll over to the next year.",
        ],
        "table": [
            ("New hire window", "{new_window}"),
            ("Open enrollment", "{open_start} to {open_end}"),
            ("Effective date", "{effective}"),
        ],
        "params": {
            "US": dict(
                new_window="30 days",
                open_start="1 November",
                open_end="20 November",
                effective="1 January",
            ),
            "DE": dict(
                new_window="60 days",
                open_start="1 October",
                open_end="31 October",
                effective="1 January",
            ),
            "IN": dict(
                new_window="30 days", open_start="1 March", open_end="20 March", effective="1 April"
            ),
            "GB": dict(
                new_window="30 days",
                open_start="1 November",
                open_end="30 November",
                effective="1 January",
            ),
        },
    },
    "wellbeing_allowance": {
        "area": "benefits",
        "name": "Wellbeing allowance",
        "noun": "the wellbeing allowance",
        "eligibility": [
            "All permanent employees in {country} receive the wellbeing allowance from their first full month."
        ],
        "entitlement": [
            "The allowance is {amount} per calendar year.",
            "It can be used for gym memberships, fitness classes, mental health apps, therapy sessions and sports equipment.",
            "Unused allowance does not carry over to the next year.",
        ],
        "pay": ["Reimbursements are paid with the next monthly salary.", "{tax}"],
        "process": [
            "Submit receipts in the expenses tool under the category Wellbeing.",
            "Claims must be submitted within {claim_window} of purchase.",
            "Claims for the previous year are accepted until {deadline}.",
        ],
        "table": [
            ("Annual allowance", "{amount}"),
            ("Claim window", "{claim_window}"),
            ("Prior-year deadline", "{deadline}"),
        ],
        "params": {
            "US": dict(
                amount="USD 600",
                tax="The allowance is taxable income and is reported on your payslip.",
                claim_window="90 days",
                deadline="31 January",
            ),
            "DE": dict(
                amount="EUR 500",
                tax="Sports and health expenses are paid tax-free up to the statutory limit.",
                claim_window="90 days",
                deadline="31 January",
            ),
            "IN": dict(
                amount="INR 30,000",
                tax="The allowance is taxable unless it is claimed as a tax-exempt reimbursement.",
                claim_window="60 days",
                deadline="15 April",
            ),
            "GB": dict(
                amount="GBP 400",
                tax="The allowance is a taxable benefit and is processed through payroll.",
                claim_window="90 days",
                deadline="31 January",
            ),
        },
    },
    "pay_schedule": {
        "area": "payroll",
        "name": "Pay schedule",
        "noun": "the pay schedule",
        "eligibility": ["This schedule applies to all employees paid through {entity} payroll."],
        "entitlement": [
            "Salaries are paid {frequency}.",
            "{payday}",
            "If payday falls on a weekend or public holiday, pay is made on the previous working day.",
        ],
        "pay": [
            "Payslips are available in the HR portal {payslip}.",
            "Changes submitted after the payroll cut-off on {cutoff} are processed in the following pay run.",
        ],
        "process": [
            "Keep your bank details up to date in the HR portal.",
            "Bank detail changes made after the cut-off take effect in the following pay run.",
            "Contact Payroll through the HR portal if your pay has not arrived by the end of payday.",
        ],
        "table": [
            ("Frequency", "{frequency_short}"),
            ("Payday", "{payday_short}"),
            ("Cut-off", "{cutoff}"),
        ],
        "params": {
            "US": dict(
                frequency="every two weeks on Friday",
                frequency_short="Bi-weekly",
                payday="There are 26 paydays in a typical year.",
                payday_short="Every other Friday",
                payslip="two working days before payday",
                cutoff="the Monday of the pay week",
            ),
            "DE": dict(
                frequency="monthly",
                frequency_short="Monthly",
                payday="Payday is the last working day of each month.",
                payday_short="Last working day",
                payslip="three working days before payday",
                cutoff="the 15th of the month",
            ),
            "IN": dict(
                frequency="monthly",
                frequency_short="Monthly",
                payday="Payday is the last working day of each month.",
                payday_short="Last working day",
                payslip="on payday",
                cutoff="the 20th of the month",
            ),
            "GB": dict(
                frequency="monthly",
                frequency_short="Monthly",
                payday="Payday is the 25th of each month.",
                payday_short="25th of the month",
                payslip="three working days before payday",
                cutoff="the 10th of the month",
            ),
        },
    },
    "payroll_corrections": {
        "area": "payroll",
        "name": "Payroll corrections",
        "noun": "payroll corrections",
        "eligibility": ["Any employee paid through {entity} payroll can request a correction."],
        "entitlement": [
            "Underpayments of more than {threshold} are corrected with an off-cycle payment within {offcycle}.",
            "Smaller underpayments are corrected in the next regular pay run.",
            "Overpayments are recovered from future pay over at least {recovery}, unless you choose to repay sooner.",
        ],
        "pay": ["Corrections are taxed in the period in which they are paid."],
        "process": [
            "Report a suspected error through the HR portal within {report_window} of payday.",
            "Attach the payslip and describe the difference you expect.",
            "Payroll confirms the outcome within five working days.",
        ],
        "table": [
            ("Off-cycle threshold", "{threshold}"),
            ("Off-cycle payment within", "{offcycle}"),
            ("Report within", "{report_window}"),
            ("Overpayment recovery", "Over at least {recovery}"),
        ],
        "params": {
            "US": dict(
                threshold="USD 200",
                offcycle="3 working days",
                recovery="3 pay periods",
                report_window="60 days",
            ),
            "DE": dict(
                threshold="EUR 200",
                offcycle="5 working days",
                recovery="3 months",
                report_window="3 months",
            ),
            "IN": dict(
                threshold="INR 10,000",
                offcycle="5 working days",
                recovery="3 months",
                report_window="60 days",
            ),
            "GB": dict(
                threshold="GBP 150",
                offcycle="5 working days",
                recovery="3 months",
                report_window="60 days",
            ),
        },
    },
    "expense_reimbursement": {
        "area": "payroll",
        "name": "Expense reimbursement",
        "noun": "expense reimbursement",
        "eligibility": [
            "Employees in {country} can claim business expenses approved in advance by their manager."
        ],
        "entitlement": [
            "Meals while travelling are reimbursed up to {meal_cap} per day.",
            "Economy class is the standard for flights under {flight_hours} hours.",
            "Mileage for a personal car is reimbursed at {mileage}.",
        ],
        "pay": ["Approved expenses are reimbursed with the next pay run after approval."],
        "process": [
            "Submit claims in the expenses tool within {claim_window} of the expense.",
            "Itemised receipts are required for any expense over {receipt_threshold}.",
            "Your manager approves claims; claims over {finance_threshold} also need Finance approval.",
        ],
        "table": [
            ("Daily meal cap", "{meal_cap}"),
            ("Mileage rate", "{mileage}"),
            ("Receipts required over", "{receipt_threshold}"),
            ("Claim within", "{claim_window}"),
        ],
        "params": {
            "US": dict(
                meal_cap="USD 75",
                flight_hours="6",
                mileage="the IRS standard rate",
                claim_window="60 days",
                receipt_threshold="USD 25",
                finance_threshold="USD 2,500",
            ),
            "DE": dict(
                meal_cap="EUR 50",
                flight_hours="5",
                mileage="EUR 0.30 per kilometre",
                claim_window="60 days",
                receipt_threshold="EUR 20",
                finance_threshold="EUR 2,000",
            ),
            "IN": dict(
                meal_cap="INR 3,000",
                flight_hours="5",
                mileage="INR 12 per kilometre",
                claim_window="45 days",
                receipt_threshold="INR 1,000",
                finance_threshold="INR 150,000",
            ),
            "GB": dict(
                meal_cap="GBP 50",
                flight_hours="5",
                mileage="GBP 0.45 per mile",
                claim_window="60 days",
                receipt_threshold="GBP 20",
                finance_threshold="GBP 2,000",
            ),
        },
    },
    "overtime": {
        "area": "payroll",
        "name": "Overtime",
        "noun": "overtime",
        "eligibility": [
            "{eligible}",
            "Overtime must be approved by your manager before it is worked, except in emergencies.",
        ],
        "entitlement": [
            "Hours above {threshold} are paid at {rate}.",
            "Work on public holidays is paid at {holiday_rate}.",
            "{toil}",
        ],
        "pay": ["Approved overtime is paid in the pay run after the month in which it was worked."],
        "process": [
            "Record overtime hours in the time tracking tool by the end of each week.",
            "Your manager approves recorded hours by the payroll cut-off.",
            "Unapproved overtime is not paid.",
        ],
        "table": [
            ("Threshold", "{threshold}"),
            ("Overtime rate", "{rate}"),
            ("Public holiday rate", "{holiday_rate}"),
        ],
        "params": {
            "US": dict(
                eligible="Non-exempt employees in the United States are eligible for overtime pay.",
                threshold="40 hours per week",
                rate="1.5 times your hourly rate",
                holiday_rate="2 times your hourly rate",
                toil="Exempt employees are not paid overtime.",
            ),
            "DE": dict(
                eligible="Employees in Germany below the management grade are eligible for overtime compensation.",
                threshold="40 hours per week",
                rate="1.25 times your hourly rate",
                holiday_rate="2 times your hourly rate",
                toil="You can choose time off in lieu instead of pay, at one hour per overtime hour.",
            ),
            "IN": dict(
                eligible="Employees in India below the manager grade are eligible for overtime pay.",
                threshold="48 hours per week",
                rate="2 times your hourly rate",
                holiday_rate="2 times your hourly rate",
                toil="Time off in lieu is not offered in place of statutory overtime pay.",
            ),
            "GB": dict(
                eligible="Employees in the United Kingdom below the manager grade are eligible for overtime pay.",
                threshold="37.5 hours per week",
                rate="1.5 times your hourly rate",
                holiday_rate="2 times your hourly rate",
                toil="You can choose time off in lieu instead of pay, agreed with your manager.",
            ),
        },
    },
}

GLOBAL_TOPICS = {
    "remote_work": {
        "area": "other",
        "name": "Remote and hybrid work",
        "facts": {
            "Eligibility": [
                "Most roles can work remotely up to three days per week, as agreed with your manager.",
                "Fully remote arrangements need approval from your department head and HR.",
            ],
            "Arrangements": [
                "Working from another country for more than 20 working days per year needs prior approval from HR, because of tax and immigration rules.",
                "A one-time home office allowance is available to fully remote employees, paid in local currency.",
            ],
            "Requesting a change": [
                "Request a new working arrangement in the HR portal.",
                "HR responds to arrangement requests within 10 working days.",
            ],
        },
        "table": [
            ("Remote days per week", "Up to 3"),
            ("Working abroad limit", "20 working days per year"),
            ("HR response time", "10 working days"),
        ],
    },
    "hr_case_handling": {
        "area": "other",
        "name": "How HR handles your case",
        "facts": {
            "Response times": [
                "HR Services responds to a new case within 2 working days.",
                "Urgent pay or coverage issues are answered within 4 working hours.",
                "Cases are closed only after you confirm the answer or 5 working days pass without a reply.",
            ],
            "Escalation": [
                "If you are not satisfied with an answer, reply on the case to ask for escalation to a senior HR partner.",
                "Sensitive matters such as harassment or health concerns are handled by a restricted team and are never shared with your manager without your consent.",
            ],
            "AI assistance": [
                "Some first replies are drafted with AI assistance and are labelled as AI suggestions.",
                "An HR team member reviews every case, and AI never closes a case without human approval.",
            ],
        },
        "table": [
            ("First response", "2 working days"),
            ("Urgent pay or coverage", "4 working hours"),
            ("Auto-close after no reply", "5 working days"),
        ],
    },
    "employee_data_privacy": {
        "area": "other",
        "name": "Employee data privacy",
        "facts": {
            "What we hold": [
                "HR holds your contract, pay, benefits, leave and performance records.",
                "Medical information is stored separately and is visible only to HR staff who need it.",
            ],
            "Retention": [
                "Personnel records are kept for 7 years after employment ends unless local law requires longer.",
                "Case records in the HR portal are kept for 3 years after the case is closed.",
            ],
            "Your rights": [
                "You can request a copy of your personal data through the HR portal.",
                "HR responds to data access requests within 30 days.",
            ],
        },
        "table": [
            ("Personnel records", "7 years after leaving"),
            ("HR case records", "3 years after closure"),
            ("Access requests", "Answered within 30 days"),
        ],
    },
}


def p(text: str) -> str:
    return f"<p>{text}</p>"


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def table(rows: list[tuple[str, str]], headers=("Item", "Value")) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    return f"<table><tr>{head}</tr>{body}</table>"


def country_article(key: str, spec: dict, code: str) -> dict:
    c = COUNTRIES[code]
    values = dict(
        spec["params"][code], country=c["name"], entity=c["entity"], currency=c["currency"]
    )

    def fill(items):
        return [s.format(**values) for s in items]

    noun, name = spec["noun"], spec["name"]
    html = "".join(
        [
            "<h2>Purpose</h2>",
            p(
                f"This policy explains how {noun} works for employees of {c['entity']} in {c['name']}. It sets out who is eligible, what you are entitled to, how pay is handled, and how to make a request."
            ),
            p(
                f"{COMPANY} wants every employee to understand their entitlements without having to ask. Where this policy and local law differ, the more favourable rule for the employee applies."
            ),
            "<h2>Scope</h2>",
            p(
                f"This policy applies to permanent and fixed-term employees employed by {c['entity']}. It does not apply to contractors, agency workers or interns, who should check their own agreements."
            ),
            ul(
                [
                    f"Full-time employees based in {c['short']}",
                    f"Part-time employees based in {c['short']}, on a pro-rata basis where stated",
                    "Employees on international assignment who remain on the local payroll",
                ]
            ),
            "<h2>Definitions</h2>",
            ul(
                [
                    "Working day means a day you are normally scheduled to work.",
                    "Base salary means your contractual salary before allowances, bonuses and overtime.",
                    "HR portal means the ServiceNow employee portal used for HR requests and cases.",
                    "Manager means the person you report to in the HR system.",
                ]
            ),
            "<h2>Eligibility</h2>",
            *[p(s) for s in fill(spec["eligibility"])],
            p(
                "If you are unsure whether you are eligible, raise a case in the HR portal and HR Services will confirm your eligibility in writing."
            ),
            "<h2>Entitlement</h2>",
            "<h3>Standard entitlement</h3>",
            *[p(s) for s in fill(spec["entitlement"])],
            "<h3>Pay and contributions</h3>",
            *[p(s) for s in fill(spec["pay"])],
            "<h3>Key figures</h3>",
            table([(a, b.format(**values)) for a, b in spec["table"]]),
            "<h2>How to request</h2>",
            *[p(s) for s in fill(spec["process"])],
            p(
                "Keep a copy of any confirmation you receive. Requests made outside the HR portal may be delayed because they cannot be tracked."
            ),
            "<h2>Working with your manager</h2>",
            p(
                "Talk to your manager early about plans that affect your work, so cover can be arranged. Your manager cannot refuse an entitlement set out in this policy, but can discuss timing where business needs allow."
            ),
            p(
                "Managers must treat every request fairly and consistently, and must not ask for more information than this policy requires."
            ),
            "<h2>Interaction with other policies</h2>",
            ul(
                [
                    "Annual leave continues to accrue during periods of paid leave unless local law states otherwise.",
                    "Public holidays that fall during a period of leave are handled under the annual leave policy.",
                    "Benefits continue during paid leave; check the benefits enrollment policy for unpaid leave.",
                ]
            ),
            "<h2>Exceptions and appeals</h2>",
            p(
                "Exceptions to this policy need written approval from the HR Director for the country. If you disagree with a decision made under this policy, you can appeal through the HR portal within 30 days of the decision."
            ),
            p(
                "Appeals are reviewed by an HR partner who was not involved in the original decision, and you receive a written outcome within 20 working days."
            ),
            "<h2>Records and privacy</h2>",
            p(
                "HR keeps records of requests and decisions under this policy in the HR portal. Records are handled under the employee data privacy policy and are visible only to you, your manager where needed, and HR."
            ),
            "<h2>Responsibilities</h2>",
            ul(
                [
                    "Employees submit requests on time and keep their details up to date.",
                    "Managers respond to requests promptly and plan cover.",
                    "HR Services answers questions, processes requests and keeps this policy current.",
                ]
            ),
            "<h2>Contacts</h2>",
            p(
                f"Questions about {noun} go to HR Services through a case in the HR portal. For urgent pay issues, mark the case as urgent."
            ),
            "<h2>Revision history</h2>",
            table(
                [
                    ("2026-01-01", "Annual review; figures confirmed for the new year"),
                    ("2025-04-01", "Policy rewritten in plain language"),
                ],
                headers=("Date", "Change"),
            ),
        ]
    )
    return {
        "title": f"{name} ({c['short']})",
        "meta": f"area:{spec['area']} country:{code}",
        "html": html,
    }


def global_article(key: str, spec: dict) -> dict:
    parts = [
        "<h2>Purpose</h2>",
        p(
            f"This policy applies to all {COMPANY} employees worldwide. Country-specific rules are noted where they apply."
        ),
    ]
    for heading, facts in spec["facts"].items():
        parts.append(f"<h2>{heading}</h2>")
        parts.extend(p(f) for f in facts)
    parts += [
        "<h2>Key figures</h2>",
        table(spec["table"]),
        "<h2>Contacts</h2>",
        p("Questions about this policy go to HR Services through a case in the HR portal."),
    ]
    return {
        "title": spec["name"],
        "meta": f"area:{spec['area']} country:GLOBAL",
        "html": "".join(parts),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    articles = []
    for key, spec in TOPICS.items():
        for code in COUNTRIES:
            articles.append((f"{key}:{code}", country_article(key, spec, code)))
    for key, spec in GLOBAL_TOPICS.items():
        articles.append((f"{key}:GLOBAL", global_article(key, spec)))

    for n, (slug, art) in enumerate(articles, start=1):
        number = f"KB{90000 + n:07d}"
        record = {
            "sys_id": uuid.uuid5(NS, slug).hex,
            "number": number,
            "version": 1,
            "workflow_state": "published",
            **art,
        }
        (OUT / f"{number}.json").write_text(json.dumps(record, indent=1))
    print(f"wrote {len(articles)} articles to {OUT}")


if __name__ == "__main__":
    main()
