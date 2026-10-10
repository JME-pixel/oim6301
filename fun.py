import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _(Review):
    Review
    return


@app.cell
def _():
    orders = [
        {"OrderID": 10248, "ShipCountry": "France"},
        {"OrderID": 10249, "ShipCountry": "Germany"},
    ]
    orders["ShipCountry"]
    return (orders,)


@app.cell
def _(orders):
    orders[1]["OrderID"]
    return


@app.cell
def _(oreders):
    oreders
    return


if __name__ == "__main__":
    app.run()
