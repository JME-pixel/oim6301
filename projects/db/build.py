import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    return duckdb, mo, pl


@app.cell
def _(duckdb, mo):
    mo.md("""
    # Babson Bean Café: Build the Database

    This notebook builds `database.duckdb` from nothing every time it runs, using the CSV files in `data/`.
    The as_of date for the whole project is **2026-11-07**.
    """)

    database = mo.notebook_dir() / "database.duckdb"
    data_dir = mo.notebook_dir() / "data"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, data_dir, database


@app.cell
def _(mo):
    mo.md("""
    ## The Tables

    The next cell deletes the old database file, then opens a new one, creates the seven tables and the view, loads the CSV files and closes the file again. Parents are created and loaded before the tables that point at them.
    """)
    return


@app.cell
def _(data_dir, database, duckdb, mo):
    # Start from nothing: delete the old database file (and its log file, if any).
    if database.exists():
        database.unlink()
    _wal = database.with_name(database.name + ".wal")
    if _wal.exists():
        _wal.unlink()

    with duckdb.connect(database) as _con:
        _con.sql("""
            CREATE TABLE members (
                member_id      INTEGER PRIMARY KEY,
                first_name     VARCHAR NOT NULL,
                mobile         VARCHAR NOT NULL UNIQUE,
                email          VARCHAR UNIQUE,
                join_date      DATE    NOT NULL,
                points_balance INTEGER NOT NULL DEFAULT 0 CHECK (points_balance >= 0)
            )
        """)
        _con.sql("""
            CREATE TABLE products (
                product_id   INTEGER PRIMARY KEY,
                name         VARCHAR NOT NULL UNIQUE,
                category     VARCHAR NOT NULL CHECK (category IN ('coffee', 'tea', 'food', 'other')),
                price        DECIMAL(8, 2) NOT NULL CHECK (price > 0),
                cost         DECIMAL(8, 2) NOT NULL CHECK (cost >= 0),
                is_available BOOLEAN NOT NULL DEFAULT true,
                CHECK (price >= cost)
            )
        """)
        _con.sql("""
            CREATE TABLE options (
                option_id INTEGER PRIMARY KEY,
                name      VARCHAR NOT NULL UNIQUE,
                price     DECIMAL(8, 2) NOT NULL CHECK (price >= 0),
                cost      DECIMAL(8, 2) NOT NULL CHECK (cost >= 0)
            )
        """)
        _con.sql("""
            CREATE TABLE orders (
                order_id   INTEGER PRIMARY KEY,
                ordered_at TIMESTAMP NOT NULL,
                member_id  INTEGER REFERENCES members (member_id),
                channel    VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
            )
        """)
        _con.sql("""
            CREATE TABLE order_lines (
                line_id       INTEGER PRIMARY KEY,
                order_id      INTEGER NOT NULL REFERENCES orders (order_id),
                product_id    INTEGER NOT NULL REFERENCES products (product_id),
                quantity      INTEGER NOT NULL CHECK (quantity > 0),
                price_charged DECIMAL(8, 2) NOT NULL CHECK (price_charged > 0)
            )
        """)
        _con.sql("""
            CREATE TABLE line_options (
                line_id       INTEGER NOT NULL REFERENCES order_lines (line_id),
                option_id     INTEGER NOT NULL REFERENCES options (option_id),
                price_charged DECIMAL(8, 2) NOT NULL CHECK (price_charged >= 0),
                PRIMARY KEY (line_id, option_id)
            )
        """)
        _con.sql("""
            CREATE TABLE payments (
                payment_id INTEGER PRIMARY KEY,
                order_id   INTEGER NOT NULL REFERENCES orders (order_id),
                method     VARCHAR NOT NULL CHECK (method IN ('cash', 'card', 'app', 'points')),
                amount     DECIMAL(8, 2) NOT NULL CHECK (amount > 0)
            )
        """)

        for _table in ["members", "products", "options", "orders",
                       "order_lines", "line_options", "payments"]:
            _con.sql(f"COPY {_table} FROM '{data_dir / (_table + '.csv')}' (HEADER)")

        # The View: revenue by week, the question the café asks every Monday.
        # Lines and options are totaled separately first, so no row is counted twice.
        _con.sql("""
            CREATE VIEW weekly_revenue AS
            WITH line_value AS (
                SELECT ol.order_id,
                       ol.quantity * (ol.price_charged + COALESCE(opt.option_total, 0)) AS value
                FROM order_lines ol
                LEFT JOIN (SELECT line_id, SUM(price_charged) AS option_total
                           FROM line_options GROUP BY line_id) opt USING (line_id)
            ),
            order_value AS (
                SELECT order_id, SUM(value) AS total FROM line_value GROUP BY order_id
            )
            SELECT date_trunc('week', o.ordered_at)::DATE AS week_start,
                   count(*)                               AS orders,
                   SUM(ov.total)                          AS revenue,
                   ROUND(AVG(ov.total), 2)                AS average_order
            FROM orders o
            JOIN order_value ov USING (order_id)
            GROUP BY 1
        """)

    built = True
    mo.md("Database built from `data/*.csv`.")
    return (built,)


@app.cell
def _(mo):
    mo.md("""
    ## The Data

    `make_data.py` writes one CSV file per table into `data/`, with a fixed random seed, so it writes the same files every time. It covers the 12 months from 2025-11-08 to the as_of date, 2026-11-07, and makes 60 members, 25 products, 9 options and 1,250 orders.

    The data follows every rule of the scenario except one, on purpose. The question that checks a rule is the one about an order's payments adding up to its total, and exactly two orders break it:

    - **Order 419** has a total of 13.10 and its payment is 12.35, which is 0.75 short.
    - **Order 847** has a total of 5.35 and its payment is 7.35, which is 2.00 too much.

    No constraint can hold this rule, because it adds up rows of two other tables, so the database accepts both orders. The query below finds them.
    """)
    return


@app.cell
def _(ask, built):
    ask("""
        WITH line_value AS (
            SELECT ol.order_id,
                   ol.quantity * (ol.price_charged + COALESCE(opt.option_total, 0)) AS value
            FROM order_lines ol
            LEFT JOIN (SELECT line_id, SUM(price_charged) AS option_total
                       FROM line_options GROUP BY line_id) opt USING (line_id)
        ),
        order_value AS (SELECT order_id, SUM(value) AS total FROM line_value GROUP BY order_id),
        paid AS (SELECT order_id, SUM(amount) AS paid FROM payments GROUP BY order_id)
        SELECT ov.order_id, ov.total, p.paid, p.paid - ov.total AS difference
        FROM order_value ov
        JOIN paid p USING (order_id)
        WHERE p.paid <> ov.total
        ORDER BY ov.order_id
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## A Look at the Data
    """)
    return


@app.cell
def _(data_dir, mo, pl):
    import altair as alt

    _orders = pl.read_csv(data_dir / "orders.csv", try_parse_dates=True)
    _by_hour = (
        _orders.group_by(pl.col("ordered_at").dt.hour().alias("hour"))
        .len()
        .rename({"len": "orders"})
        .sort("hour")
    )
    _chart = (
        alt.Chart(_by_hour)
        .mark_bar()
        .encode(
            x=alt.X("hour:O", title="Hour of the day (24 hour clock)"),
            y=alt.Y("orders:Q", title="Number of orders"),
        )
        .properties(title="Orders by hour of the day", width=520, height=260)
    )
    mo.vstack([
        _chart,
        mo.md(
            "A real campus café would look like this: a rush at 8 am (the tallest bar), a smaller bump "
            "around lunch, and a taper to a handful of orders by 5 pm, so I did not change the hour "
            "weights in `make_data.py`."
        ),
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    ## Row Counts
    """)
    return


@app.cell
def _(ask, built):
    ask("""
        SELECT 'members' AS table_name, count(*) AS row_count FROM members
        UNION ALL SELECT 'products', count(*) FROM products
        UNION ALL SELECT 'options', count(*) FROM options
        UNION ALL SELECT 'orders', count(*) FROM orders
        UNION ALL SELECT 'order_lines', count(*) FROM order_lines
        UNION ALL SELECT 'line_options', count(*) FROM line_options
        UNION ALL SELECT 'payments', count(*) FROM payments
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## A Row It Refuses

    A payment of minus 5.00 breaks the rule that a payment is more than zero. `ask()` only reads, so this cell opens a short write connection of its own, inside `try` and `except`.
    """)
    return


@app.cell
def _(built, database, duckdb, mo):
    try:
        with duckdb.connect(database) as _con:
            _con.sql("INSERT INTO payments VALUES (99999, 1, 'cash', -5.00)")
        _message = "The database accepted the row, which it should not have."
    except duckdb.Error as _error:
        _message = str(_error)
    mo.md(f"The database refused the row and said:\n\n```\n{_message}\n```")
    return


@app.cell
def _(mo):
    mo.md("""
    ## Answers You Already Knew

    Three queries whose answers I knew before running them, because of what I asked the data script to make. The expected answer is written next to each result.
    """)
    return


@app.cell
def _(ask, built, pl):
    _checks = [
        ("How many orders are there?",
         "SELECT count(*) AS n FROM orders",
         1250, "I asked make_data.py for 1,250 orders."),
        ("How many members have never ordered?",
         "SELECT count(*) AS n FROM members m WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.member_id)",
         7, "I made 5 recent joiners and 2 older members who never order."),
        ("How many lines sold Pumpkin Spice Latte after 2025-11-30?",
         """SELECT count(*) AS n FROM order_lines ol
            JOIN orders o USING (order_id) JOIN products p USING (product_id)
            WHERE p.name = 'Pumpkin Spice Latte' AND o.ordered_at >= DATE '2025-12-01'""",
         0, "It was a November 2025 seasonal drink and is off the menu today."),
    ]
    pl.DataFrame({
        "question": [c[0] for c in _checks],
        "query": [" ".join(c[1].split()) for c in _checks],
        "I expected": [c[2] for c in _checks],
        "why": [c[3] for c in _checks],
        "the database says": [int(ask(c[1])["n"][0]) for c in _checks],
    })
    return


@app.cell
def _(mo):
    mo.md("""
    ## A View

    `weekly_revenue` answers the question the café asks every Monday: how many orders and how much revenue did each week bring in? Revenue is what the lines and their options were charged, however the order was paid. It is saved with `CREATE VIEW` in the build cell above, so asking for it by name always gives the current rows.
    """)
    return


@app.cell
def _(ask, built):
    ask("SELECT * FROM weekly_revenue ORDER BY week_start DESC LIMIT 8")
    return


if __name__ == "__main__":
    app.run()
