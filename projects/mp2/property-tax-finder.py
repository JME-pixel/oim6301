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
    The person who would use this is a person who is looking for jobs and trying to see where they want to live in Massachusetts. Then they are trying to calculate the net income they get from their paycheck to be able to budget for their living expenses in that area.

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
    2.I am going to look at the API and see what type of data is in the data set and the structure my code and AI need for the format.
    3. Then I am going to make sure I usethe right API to get the question right.
    4. I am also going to probably create a for loop for the code to loop through the records returned by the API to make sure it hits the budget limit
    5. The I am going to puch check makrs in place

    ///

    ### 2b. Guess code
    IN the next cell


    ///

    ### 2c. Which addresses will they request?

    /// admonition | Your addresses
        type: info

    Type here.
     This is a hypothesis: I think they will request wesllsey for the job or middlesex
    ///

    ### 2d. How will you know you have every record?

    /// admonition | Your answer
        type: info

    Type here. I will Know because I will pull it from the APIand check that the number of records I collect matches the total count reported by the API, either in the response metadata or by paging until no more records are returned.

    ///

    ### 2e. Which check will you use in section 6, and which two numbers should agree?

    /// admonition | Your check
        type: info

    Check:

    Number A:The average bill the API reports for a town in fiscal year 2026.

    Number B:That same town’s average home value times its residential tax rate, divided by 1,000.



    ///

    *Commit this notebook with the message `mp2: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My Tryng code.
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    # ---------- Work: functions ----------
    import requests

    BASE = "https://oim.zhili.dev"


    def get_all_towns(county):
        """In: county name. Out: (list of towns, total the API reports)."""
        r = requests.get(
            f"{BASE}/ma/towns",
            params={"county": county, "per_page": 100},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        return data["items"], data["pagination"]["total"]


    def get_town_year(dor_code, year):
        """In: dor_code, fiscal year. Out: that year's figures."""
        r = requests.get(f"{BASE}/ma/towns/{dor_code}/history", timeout=10)
        r.raise_for_status()
        return r.json()["years"][0]


    def filter_towns(rows, budget, limit):
        """In: town rows, budget, tax limit. Out: passing towns, cheapest bill first."""
        passing = [r for r in rows if r["value"] <= budget or r["bill"] < limit]
        return sorted(passing, key=lambda r: r["bill"], reverse=True)

    return filter_towns, get_all_towns, get_town_year


@app.cell
def _(
    budget_dollars,
    county,
    filter_towns,
    fiscal_year,
    get_all_towns,
    get_town_year,
    tax_limit_dollars,
):
    # ---------- Work: run ----------
    towns, api_total = get_all_towns(county)

    rows = []
    for t in towns:
        figures = get_town_year(t["dor_code"], fiscal_year)
        if figures is None:
            continue
        value = figures["average_single_family_value_dollars"]
        rate = figures["residential_rate_per_thousand"]
        bill = figures["average_single_family_bill_dollars"]
        if value is None or rate is None or bill is None:
            continue
        rows.append({"town": t["name"], "value": value, "rate": rate, "bill": bill})

    results = filter_towns(rows, budget_dollars, tax_limit_dollars)
    print(f"Skipped {len(towns) - len(rows)} towns with missing {fiscal_year} data")
    return api_total, results, towns


@app.cell
def _(results):
    # ---------- Answer: table ----------
    print(f"{'Town':<22}{'Avg home value':>16}{'Tax rate':>10}{'Avg bill':>12}")
    print("-" * 60)
    for r in results:
        print(f"{r['town']:<22}${r['value']:>14,.0f}{r['rate']:>10.2f}${r['bill']:>10,.0f}")
    return


@app.cell
def _(budget_dollars, county, results, tax_limit_dollars):
    if results:
        _best = results[0]
        print(
            f"{len(results)} towns in {county} County fit a ${budget_dollars:,} budget "
            f"and a ${tax_limit_dollars:,} tax limit; the cheapest is {_best['town']} "
            f"at ${_best['bill']:,.0f} a year on a ${_best['value']:,.0f} home."
        )
    else:
        print(
            f"No town in {county} County fits ${budget_dollars:,} "
            f"and ${tax_limit_dollars:,}."
        )
    return


@app.cell
def _(api_total, results, towns):
    # ---------- Check (section 6) ----------
    if results:
        _top = results[0]
        _computed = _top["value"] * _top["rate"] / 1000
        print(f"API bill: ${_top['bill']:,.2f}   value x rate / 1000: ${_computed:,.2f}")

    print(f"Collected: {len(towns)}   API total: {api_total}")
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
    return budget_dollars, county, fiscal_year, tax_limit_dollars


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
