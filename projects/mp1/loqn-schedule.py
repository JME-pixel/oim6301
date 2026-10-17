# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A person ready to buy a house often has to chose between a 15 year or 30 year loan. So my tool would be use by people that want to compare the 30 year loan with the 15 year loan, to see how much difference there is in total interest. The comparison would be easier to see given  interest rate and the length of the payment to see how much more you would pay in the 30 year loan instead of the 15 year loan.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    SO start with the full loan about as the balance. 2Then I need to figure out the total time of the loan.3 Then I need ot figure out the intrest owed on each month based of the current balance, and subtract the principal and interest paid from the balance to get the new balance for the next month. Repeat this process for each month until the loan is paid off. I need to keep track of the total ammount being subtracked because it is what is coming down from one loop to the next loop and it is what determines the remaining balance and therefore the interest calculated in the next iteration of the loop. I will check by comparing total intrest summed from the  month by month shedule versus total interest from (payment x number of months)- loan ammonunt
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    return annual_rates, loan_amount


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    loan_amt = 400000
    term_rates = {30: 0.0703, 15: 0.0642}
    term_choice = 0
    while term_choice != "15" and term_choice != "30":
       print("How many years do you want your payment installment to be 15 or 30? ")
       term_choice = input()
    term_choice = int(term_choice)
    remaining_balance = round(loan_amt,2)
    monthly_rate = round((term_rates[term_choice]/12),2)
    for month_num in range(term_choice*12):
       interest_amt = round(remaining_balance * monthly_rate,2)
       payment_amt = round(loan_amt * monthly_rate / (1 - (1 + monthly_rate) ** -(term_choice*12)),2)
       remaining_balance = round(remaining_balance - payment_amt + interest_amt,2)
    summary = f"Month: {month_num+1}\nPayment: ${payment_amt}\nInterest: ${interest_amt}\nPrincipals: ${payment_amt-interest_amt}\nBalance Left: ${remaining_balance}"
    print(summary)
    return


@app.cell
def _():
    # loan_amount = 400000
    # annual_rates = {30: 0.0703, 15: 0.0642}
    # val = 0
    # while val != "15" and val != "30":
    #    print("How many years do you want your payment installment to be 15 or 30? ")
    #    val = input()
    # val = int(val)
    # balance = round(loan_amount,2)
    # r = round((annual_rates[val]/12),2)
    # for n in range(val*12):
    #    interest = round(balance * r,2)
    #    payment = round(loan_amount * r / (1 - (1 + r) ** -(val*12)),2)
    #    balance = round(balance - payment + interest,2)
    # hello = f"Month: {n+1}\nPayment: ${payment}\nInterest: ${interest}\nPrincipals: ${payment-interest}\nBalance Left: ${balance}"
    # print(hello)
    return


@app.cell(hide_code=True)
def _(annual_rates, loan_amount):
    r30 = annual_rates[30] / 12
    n30 = 30 * 12
    payment30 = round(loan_amount * r30 / (1 - (1 + r30) ** -n30), 2)

    balance30 = loan_amount
    total_interest_30 = 0
    total_paid_30 =0
    for month30 in range(1, n30 + 1):
        interest30 = round(balance30 * r30, 2)
        if month30 == n30:
            principal30 = balance30
            payment_due30 = round(interest30 + principal30, 2)
            balance30 = 0
        else:
            principal30 = round(payment30 - interest30, 2)
            payment_due30 = payment30
            balance30 = round(balance30 - principal30, 2)
        total_interest_30 = round(total_interest_30 + interest30, 2)
        total_paid_30 =round(total_paid_30 + payment_due30, 2)
        print(f"Month: {month30:.2f}\tPayment: ${payment_due30:.2f}\tInterest: ${interest30}\tPrincipal: ${principal30:.2f}\tBalance Left: ${balance30:.2f}")

    total_interest_30
    return n30, payment30, r30, total_interest_30, total_paid_30


@app.cell
def _(annual_rates, loan_amount):
    r15 = annual_rates[15] / 12
    n15 = 15 * 12
    payment15 = round(loan_amount * r15 / (1 - (1 + r15) ** -n15), 2)

    balance15 = loan_amount
    total_interest_15 = 0
    total_paid_15 = 0
    for month15 in range(1, n15 + 1):
        interest15 = round(balance15 * r15, 2)
        if month15 == n15:
            principal15 = balance15
            payment_due15 = round(interest15 + principal15, 2)
            balance15 = 0
        else:
            principal15 = round(payment15 - interest15, 2)
            payment_due15 = payment15
            balance15 = round(balance15 - principal15, 2)
        total_interest_15 = round(total_interest_15 + interest15, 2)
        total_paid_15 = round(total_paid_15 + payment_due15, 2)
        print(f"Month: {month15}\tPayment: ${payment_due15:.2f}\tInterest: ${interest15:.2f}\tPrincipal: ${principal15:.2f}\tBalance Left: ${balance15:.2f}")

    total_interest_15
    return n15, payment15, r15, total_interest_15, total_paid_15


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(payment15, payment30, total_interest_15, total_interest_30):
    print(f"30-year loan: payment ${payment30:,.2f} per month, total interest ${total_interest_30:,.2f}")
    print(f"15-year loan: payment ${payment15:,.2f} per month, total interest ${total_interest_15:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The 15 year loan cost 797.59 more per month, but saves you  336,906.69 dollars in total interest over the full life of the loan. So if you can afford the higher monthly payment, the 15 year loan is the better choice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(
    loan_amount,
    total_interest_15,
    total_interest_30,
    total_paid_15,
    total_paid_30,
):
    check_30 =round(total_paid_30 - loan_amount, 2)
    check_15 = round(total_paid_15 - loan_amount, 2)
    print(F"30 year:total interest ${total_interest_30:,.2f},check ${check_30:,.2f}")
    print(f"15 year:total interest ${total_interest_15:,.2f},check ${check_15:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I compared total interest summed month-by-month in the schedule against the total of all actual payments made minus the loan amount. For the 30-year loan: $560,942.03 vs $560,942.03. For the 15-year loan: $224,035.34 vs $224,035.34. They agree exactly, confirming the schedule is correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When I first asked the agent to help me check that my total interest was correct, it wrote check_30 = payment30 * n30 - loan_amount, which assumed every single month's payment was the same size. This gave check_30 = 560,937.20, but my schedule's actual total interest was 560,942.03 — a $4.83 gap. I knew something was wrong because these two numbers were supposed to match exactly, and they didn't. The problem was that the last month's payment is not the same as every other month's payment; it's adjusted to exactly pay off whatever balance is left. I fixed it by adding a running total inside my loop, total_paid_30 = round(total_paid_30 + payment_due30, 2), which adds up the real payment made each month, including that different last one. Then I changed the check to total_paid_30 - loan_amount. After that, the check matched the schedule's total interest exactly, $560,942.03 to $560,942.03. This is in the section 6 cells of this notebook, the 30-year amortization loop and the check cell right after it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(loan_amount, n30, payment30, r30, total_interest_30):
    extra_payment = 200

    balance_x30 = loan_amount
    total_interest_x30 = 0
    months_x30 = 0
    for mx30 in range(1, n30 + 1):
        interest_x30 = round(balance_x30 * r30, 2)
        payment_x30 = payment30 + extra_payment
        if payment_x30 >= balance_x30 + interest_x30:
            payment_x30 = round(balance_x30 + interest_x30, 2)
            balance_x30 = 0
        else:
            principal_x30 = round(payment_x30 - interest_x30, 2)
            balance_x30 = round(balance_x30 - principal_x30, 2)
        total_interest_x30 = round(total_interest_x30 + interest_x30, 2)
        months_x30 = mx30
        if balance_x30 == 0:
            break

    months_saved_30 = n30 - months_x30
    interest_saved_30 = round(total_interest_30 - total_interest_x30, 2)
    months_x30, total_interest_x30, months_saved_30, interest_saved_30
    return (extra_payment,)


@app.cell
def _(extra_payment, loan_amount, n15, payment15, r15, total_interest_15):
    balance_x15 = loan_amount
    total_interest_x15 = 0
    months_x15 = 0
    for mx15 in range(1, n15 + 1):
        interest_x15 = round(balance_x15 * r15, 2)
        payment_x15 = payment15 + extra_payment
        if payment_x15 >= balance_x15 + interest_x15:
            payment_x15 = round(balance_x15 + interest_x15, 2)
            balance_x15 = 0
        else:
            principal_x15 = round(payment_x15 - interest_x15, 2)
            balance_x15 = round(balance_x15 - principal_x15, 2)
        total_interest_x15 = round(total_interest_x15 + interest_x15, 2)
        months_x15 = mx15
        if balance_x15 == 0:
            break

    months_saved_15 = n15 - months_x15
    interest_saved_15 = round(total_interest_15 - total_interest_x15, 2)
    months_x15, total_interest_x15, months_saved_15, interest_saved_15
    return


if __name__ == "__main__":
    app.run()
