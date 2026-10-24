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
    A couple looking to buy a single-family home in Massachusetts wants to narrow down which towns to consider. They have a maximum amount they can spend on a home and a maximum property tax bill they're willing to pay each year. This notebook shows which towns in a chosen county meet both limits, so the couple can see their cheapest options first instead of checking each town one by one.
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

    1. Open the towns endpoint and the history endpoint in my browser to see what fields come back and what type each one is (text, number, etc.).
    2.Decide what makes a town pass: its average home value must be under my budget, and its average tax bill must be under my limit, both for the fiscal year I care about.
    3. Write one function that gets every town in a county, using the total the API reports so I know when I have them all.
    4.Write one function that gets one town's figures for a specific fiscal year, by checking each year in its history instead of assuming the year I want is first in the list.
    5. Loop through every town, pull its figures, skip any town missing data for that year, and count how many I skip. Then keep only the towns under both limits, sorted from cheapest bill to most expensive.

    ///

    ### 2b. Guess code and Which functions will i need
    IN the next cell
    get_all_towns(county) — in: a county name. Out: the list of towns in that county, and the total count the API reports.
    get_town_year(dor_code, year) — in: a town's code and a fiscal year. Out: that town's figures for that year, or nothing if it's missing.
    filter_towns(rows, budget, limit) — in: the list of town figures, a budget, and a tax limit. Out: the towns that pass both limits, cheapest bill first.

    ///

    ### 2c. Which addresses will they request?

    /// admonition | Your addresses
        type: info

    Type here.
     This is a hypothesis: I think they will request wesllsey for the job or middlesex
     https://oim.zhili.dev/ma/towns?county=Middlesex to get every town in the county, and https://oim.zhili.dev/ma/towns/{dor_code}/history once per town, to get each town's figures by year.
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
    # (moved to Section 4)
    return


@app.cell
def _():
    import requests as _dbg2
    _p1 = _dbg2.get("https://oim.zhili.dev/ma/towns", params={"county": "Middlesex", "per_page": 5}, timeout=10).json()
    print(type(_p1["items"][0]["average_single_family_bill_dollars"]))
    _p1
    return


@app.cell
def _():
    import requests as _dbg_requests
    _dbg = _dbg_requests.get("https://oim.zhili.dev/ma/towns/002/history", timeout=10).json()
    print(type(_dbg["years"][20]["residential_rate_per_thousand"]))
    print(_dbg["years"][20])
    _dbg
    return


@app.cell
def _():
    print(type(_p1["items"][0]["average_single_family_bill_dollars"]))
    print(type(_dbg["years"][20]["residential_rate_per_thousand"]))
    print(_dbg["years"][20])
    return


@app.cell
def _():
    # (moved to Section 4)
    return


@app.cell
def _():
    # (moved to Section 5)
    return


@app.cell
def _():
    # (moved to Section 5)
    return


@app.cell
def _():
    # (moved to Section 6)
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
    budget_dollars = 850000
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
    # ---------- Functions ----------
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
        """In: dor_code, fiscal year. Out: that year's figures, or None if not found."""
        r = requests.get(f"{BASE}/ma/towns/{dor_code}/history", timeout=10)
        r.raise_for_status()
        for row in r.json()["years"]:
            if row["fiscal_year"] == year:
                return row
        return None


    def filter_towns(rows, budget, limit):
        """In: town rows, budget, tax limit. Out: passing towns, cheapest bill first."""
        passing = [r for r in rows if r["value"] <= budget and r["bill"] <= limit]
        return sorted(passing, key=lambda r: r["bill"])

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
    # ---------- Run ----------
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
    print(f"Skipped {len(towns) - len(rows)} of {len(towns)} towns: no {fiscal_year} data.")
    return api_total, results, towns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of the towns that pass both limits, cheapest bill first, printed with `print` and f strings with the columns lined up: town, average home value, residential tax rate, average bill. Then one sentence printed from code with an f string, so it changes when the data does.*
    """)
    return


@app.cell
def _(results):
    # Result table.
    print(f"{'Town':<22}{'Avg home value':>16}{'Tax rate':>10}{'Avg bill':>12}")
    print("-" * 60)
    for r in results:
        print(f"{r['town']:<22}${r['value']:>14,.0f}{r['rate']:>10.2f}${r['bill']:>10,.0f}")
    return


@app.cell
def _(budget_dollars, county, results, tax_limit_dollars):
    # One sentence that answers section 1, with the numbers in it.
    if results:
        _best = results[0]
        print(
            f"{len(results)} towns in {county} County fit a ${budget_dollars:,} budget "
            f"and a ${tax_limit_dollars:,} tax limit; the cheapest is {_best['town']} "
            f"at ${_best['bill']:,.0f} a year on a ${_best['value']:,.0f} home."
        )
    else:
        print(
            f"No town in {county} County fits a ${budget_dollars:,} budget "
            f"and a ${tax_limit_dollars:,} tax limit."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second way and shows both numbers. At least one check must run as code. For example: average bill is close to average value times tax rate divided by 1,000, or towns collected equals the total the API reports.*
    """)
    return


@app.cell
def _(api_total, results, towns):
    # Check 1: does the API's bill match value x rate / 1000, for the cheapest town?
    if results:
        _top = results[0]
        number_a = _top["bill"]
        number_b = _top["value"] * _top["rate"] / 1000
        print(f"{_top['town']}: API bill = ${number_a:,.2f}   value x rate / 1000 = ${number_b:,.2f}")
        print(f"Agree? {abs(number_a - number_b) < 1}")

    # Check 2: did we collect every town the API reports for the county?
    print(f"Towns collected: {len(towns)}   API total: {api_total}   Agree? {len(towns) == api_total}")
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
    The first version of filter_towns used or instead of and between the budget and tax checks, and sorted with reverse=True. That meant a town could pass by meeting only one limit instead of both, and the most expensive towns were listed first instead of last. The first version of get_town_year also always returned years[0], which is not necessarily fiscal year 2026 — it just grabbed whatever row happened to be first.

    **What I changed:**
    I changed or to and so a town only passes if it meets both the budget and the tax limit. I changed reverse=True to leave off reverse so the cheapest bill comes first. I changed get_town_year to loop through the years and return the row where fiscal_year actually matches the year I asked for, returning None if it's missing.

    **How I knew:**
    The sentence in Section 5 didn't match the question in Section 1 — a couple wants towns under both limits, not towns with the cheapest bill regardless of price, or towns sorted worst first. Also, my check in Section 6 (API bill vs. value times rate divided by 1,000) would have used whatever year years[0] pointed to, which wasn't guaranteed to be 2026.

    **Where (commit or cell):**
    the scratch cell under 'My Trying code' versus the Section 4 Functions cell
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

    **Name:** get_all_towns

    **Goes in:**a county name, like "Middlesex"

    **Comes out:** two things together:the list of towns in that county, and the total number the API says exists for that county.

    **One line I had to ask about:**
      return data["items"], data["pagination"]["total"] ; this returns two values at once, separated by a comma. When you call the function with towns, api_total = get_all_towns(county), Python hands the first value to towns and the second to api_total. (One line to note: returning more than one value from a function.)
    ///

    ### 8b. Function two

    /// admonition | Your answer
        type: info

    **Name:** filter_towns

    **Goes in:** the list of town records, the budget, and the tax limit.

    **Comes out:** a shorter list, keeping only towns within both limits, ordered from cheapest bill to most expensive.

    **One line I had to ask about:**  passing = [r for r in rows if r["value"] <= budget and r["bill"] <= limit] — this builds the filtered list in one line instead of a for loop with an if and an append. (One line to note: this is called a list comprehension — a compact way of writing a for loop that builds a list.)

    ///

    ### 8c. Prediction

    *Choose one change, such as another county, another budget or another rule. Changing one value in the Inputs cell is enough. Write what you expect to change in the answer. Then commit with the message `mp2: prediction`.*

    /// admonition | My prediction (write before running)
        type: warning

    **The change:** raising budget_dollars to 850000

    **What I expect:**more towns should pass, since the budget limit is now looser and the tax limit is unchanged AND I'd expect the list to grow but the cheapest town (Malden) to stay the same, since it was already well under the old budget.

    ///

    ### 8d. What happened

    *Make the change, run it, then write what happened and whether it matched.*

    /// admonition | Result
        type: success

    **What happened:**
     Raising the budget to $850,000 increased the list from 12 towns to 14. Woburn and Burlington were added — both have home values between $700,000 and $850,000 — but the cheapest town stayed Malden at $4,952/year, since it was already well under both the old and new budget.
    **Did it match my prediction? Yes or no, and why:**  the list grew as expected, and Malden stayed the cheapest, just as I guessed.

    ///
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    *What you tried past the main task, what you found, and where it is in the notebook.*

    /// admonition | Your answer
        type: info

    **What I tried:**

    Type here.

    **What I found:**

    Type here.

    **Where it is in the notebook:**

    Type here.

    ///
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    *About how many hours this project took you outside class, as one number. It is not graded.*

    /// admonition | Your answer
        type: info

    I spent 15 hours on this
    ///
    """)
    return


if __name__ == "__main__":
    app.run()
