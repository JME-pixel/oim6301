# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "requests",
# ]
# ///
"""Mini Project 2: Where the Tax Bill Is Lowest.
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
    # Mini Project 2: Where the Tax Bill Is Lowest

    A couple wants a single family home in one Massachusetts county, within a budget, with a property tax bill under a limit. This notebook finds the towns that fit both, cheapest bill first, and can be rerun for another county or budget.

    Data: the course API, built from the state's Division of Local Services. Endpoints are listed at `oim.zhili.dev/ma` and every field is described at `oim.zhili.dev/docs`.

    Save it in your course repository as `projects/mp2/property-tax-finder.py` and open it with `uv run marimo edit`. Keep the headings. Double click a box to type your answer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*

    /// admonition | Your answer
        type: info


    ///
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *First, open the API address in your browser and read what comes back. Then write your plan before you ask your agent anything.*

    ### 2a. Steps, in order (five lines or more)

    /// admonition | Your steps
        type: info

    1. Type here.
    2.
    3.
    4.
    5.

    ///

    ### 2b. Which functions will your tool need?

    *For each: what goes in and what comes out.*

    /// admonition | Your functions
        type: info

    | Function | Goes in | Comes out |
    |---|---|---|
    | | | |
    | | | |
    | | | |

    ///

    ### 2c. Which addresses will they request?

    /// admonition | Your addresses
        type: info

    Type here.

    ///

    ### 2d. How will you know you have every record?

    /// admonition | Your answer
        type: info

    Type here.

    ///

    ### 2e. Which check will you use in section 6, and which two numbers should agree?

    /// admonition | Your check
        type: info

    Check:

    Number A:

    Number B:

    ///

    *Commit this notebook with the message `mp2: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every input goes in the cell below and nowhere else, so changing one value changes every result after it.
    """)
    return


@app.cell
def _():
    # Your inputs.
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Your functions first, then the code that uses them. Add as many cells as you need.

    *Needed: every town in the county (all pages), each town's figures for `fiscal_year` from its history, and a filter for both limits.*
    """)
    return


@app.cell
def _():
    import requests

    # Function 1: get every town in the county, all pages.

    # Function 2: get one town's figures for fiscal_year.

    # Function 3: keep the towns that pass both limits.
    return


@app.cell
def _():
    # Run your functions with the inputs above.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of the towns that pass both limits, cheapest bill first, printed with `print` and f strings with the columns lined up: town, average home value, residential tax rate, average bill. Then one sentence printed from code with an f string, so it changes when the data does.*
    """)
    return


@app.cell
def _():
    # Result table.
    return


@app.cell
def _():
    # One sentence that answers section 1, with the numbers in it.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second way and shows both numbers. At least one check must run as code. For example: average bill is close to average value times tax rate divided by 1,000, or towns collected equals the total the API reports.*
    """)
    return


@app.cell
def _():
    # Number A:
    # Number B:
    # Print both and whether they agree.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | What the check shows
        type: info

    Do the two numbers agree? If not, why?

    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as is. What did it give you, what did you change, and how did you know? Point to the commit or the cell. If the agent got it right the first time: what did you do to verify that? Pointing to your check in section 6 is enough.*

    /// admonition | Your answer
        type: info

    **What it gave me:**

    **What I changed:**

    **How I knew:**

    **Where (commit or cell):**

    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    *Pick two functions your agent wrote or helped write. For each, say in your own words what goes in, what comes out, and one line you had to ask about.*

    ### 8a. Function one

    /// admonition | Your answer
        type: info

    **Name:**

    **Goes in:**

    **Comes out:**

    **One line I had to ask about:**

    ///

    ### 8b. Function two

    /// admonition | Your answer
        type: info

    **Name:**

    **Goes in:**

    **Comes out:**

    **One line I had to ask about:**

    ///

    ### 8c. Prediction

    *Choose one change, such as another county, another budget or another rule. Changing one value in the Inputs cell is enough. Write what you expect to change in the answer. Then commit with the message `mp2: prediction`.*

    /// admonition | My prediction (write before running)
        type: warning

    **The change:**

    **What I expect:**

    ///

    ### 8d. What happened

    *Make the change, run it, then write what happened and whether it matched.*

    /// admonition | Result
        type: success

    **What happened:**

    **Did it match my prediction? Yes or no, and why:**

    ///
    """)
    return


if __name__ == "__main__":
    app.run()
