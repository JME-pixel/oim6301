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
    The people who would us this are people who want to buy a house. Also if they want to be the most finacially responsible they can use this.
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


app._unparsable_cell(
    r"""
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}our inputs.
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    val = 0
    while val != "15" and val != "30":
        print("How many years do you want your payment installment to be 15 or 30? ")
        val = input()
    val = int(val)
    balance = round(loan_amount,2)
    r = round((annual_rates[val]/12),2)
    for n in range(val*12):
        interest = round(balance * r,2)
        payment = round(loan_amount * r / (1 - (1 + r) ** -(val*12)),2)
        balance = round(balance - payment + interest,2)
        hello = f"Month: {n+1}\nPayment: ${payment}\nInterest: ${interest}\nPrincipals: ${payment-interest}\nBalance Left: ${balance}"
        print(hello)
    return annual_rates, interest, loan_amount


@app.cell(hide_code=True)
def _(annual_rates, interest, loan_amount):
    # 30-year loan schedule
    r30 = annual_rates[30] / 12
    n30 = 30 * 12
    payment30 = round(loan_amount * r30 / (1 - (1 + r30) ** -n30), 2)

    balances = loan_amount
    total_interest_30 = 0
    for month in range(1, n30 + 1):
        interests = round(balances * r30, 2)
        if month == n30:
            principal = balances
            payments = round(interests + principal, 2)
            balance = 0
        else:
            principal = round(payment30 - interest, 2)
            payments = payment30
            balances = round(balances - principal, 2)
        total_interest_30 = round(total_interest_30 + interests, 2)
        print(f"Month: {month}\nPayment: ${payments}\nInterest: ${interest}\nPrincipal: ${principal}\nBalance Left: ${balances}")

    total_interest_30
    return


@app.cell
def _(annual_rates, loan_amount):
    # 15-year loan schedule
    r15 = annual_rates[15] / 12
    n15 = 15 * 12
    payment15 = round(loan_amount * r15 / (1 - (1 + r15) ** -n15), 2)

    balance15 = loan_amount
    total_interest_15 = 0
    for month in range(1, n15 + 1):
        interest = round(balance15 * r15, 2)
        if month == n15:
            principal = balance15
            payment = round(interest + principal, 2)
            balance15 = 0
        else:
            principal = round(payment15 - interest, 2)
            payment = payment15
            balance15 = round(balance15 - principal, 2)
        total_interest_15 = round(total_interest_15 + interest, 2)
        print(f"Month: {month}\nPayment: ${payment}\nInterest: ${interest}\nPrincipal: ${principal}\nBalance Left: ${balance15}")

    total_interest_15
    return (interest,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
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
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
