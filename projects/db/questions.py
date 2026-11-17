import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    import altair as alt
    from datetime import date, timedelta

    return alt, date, duckdb, mo, pl, timedelta


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Babson Bean Café: The Questions

    Ten questions a manager of the café would ask, answered with SQL against `database.duckdb`, which `build.py` builds from the CSV files in `data/`.
    """)
    return


@app.cell
def _(date, mo, timedelta):
    # One date for every question. Change it here and every question follows.
    as_of = date(2026, 11, 7)

    last_month_end = as_of.replace(day=1) - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    days_60_start = as_of - timedelta(days=59)
    days_90_start = as_of - timedelta(days=89)

    mo.md(
        f"""
        **The as_of date is {as_of}.** "Last month" means the last full calendar month before it, {last_month_start} to {last_month_end}.
        "Last 60 days" means the 60 days ending on the as_of date, {days_60_start} to {as_of}.
        """
    )
    return as_of, days_60_start, days_90_start, last_month_end, last_month_start


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"
    data_dir = mo.notebook_dir() / "data"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    def money(x):
        return f"{float(x):,.2f}"

    return ask, data_dir, money


# ---------------------------------------------------------------- Question 1


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 1. What were the three best selling products last month?
    """)
    return


@app.cell
def _(ask, last_month_end, last_month_start):
    q1 = ask(f"""
        SELECT p.name AS product,
               CAST(SUM(ol.quantity) AS INTEGER) AS units
        FROM order_lines ol
        JOIN orders o   ON o.order_id = ol.order_id
        JOIN products p ON p.product_id = ol.product_id
        WHERE o.ordered_at::DATE BETWEEN DATE '{last_month_start}' AND DATE '{last_month_end}'
        GROUP BY p.name
        ORDER BY units DESC, product
        LIMIT 3
    """)
    q1
    return (q1,)


@app.cell(hide_code=True)
def _(last_month_start, mo, q1):
    mo.md(
        f"""
        **Answer.** In {last_month_start:%B %Y} the three best selling products were {q1['product'][0]} ({q1['units'][0]} units), {q1['product'][1]} ({q1['units'][1]} units) and {q1['product'][2]} ({q1['units'][2]} units). I counted units, the total of the quantity on order lines, and not the number of lines.
        """
    )
    return


# ---------------------------------------------------------------- Question 2


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 2. How much did each menu category earn, cost and keep as margin, with add ons counted in?

    *Uses three tables or more.*
    """)
    return


@app.cell
def _(ask):
    q2 = ask("""
        WITH option_totals AS (
            SELECT lo.line_id,
                   SUM(lo.price_charged) AS option_price,
                   SUM(opt.cost)         AS option_cost
            FROM line_options lo
            JOIN options opt ON opt.option_id = lo.option_id
            GROUP BY lo.line_id
        ),
        category_totals AS (
            SELECT p.category,
                   SUM(ol.quantity * (ol.price_charged + COALESCE(ot.option_price, 0))) AS revenue,
                   SUM(ol.quantity * (p.cost + COALESCE(ot.option_cost, 0)))            AS cost
            FROM order_lines ol
            JOIN products p ON p.product_id = ol.product_id
            LEFT JOIN option_totals ot ON ot.line_id = ol.line_id
            GROUP BY p.category
        )
        SELECT category,
               revenue,
               cost,
               revenue - cost AS margin,
               ROUND(100.0 * (revenue - cost) / revenue, 1) AS margin_percent
        FROM category_totals
        ORDER BY revenue DESC
    """)
    q2
    return (q2,)


@app.cell(hide_code=True)
def _(mo, money, q2):
    _best = q2.sort("margin", descending=True).row(0, named=True)
    _thin = q2.sort("margin_percent").row(0, named=True)
    mo.md(
        f"""
        **Answer.** {_best['category'].capitalize()} keeps the most margin, {money(_best['margin'])} dollars on {money(_best['revenue'])} dollars of revenue, and {_thin['category']} keeps the smallest share of its revenue, {float(_thin['margin_percent']):.1f} percent. Each add on is counted under the category of the product on its line, and cost uses the one current cost stored for each product and add on.
        """
    )
    return


# ---------------------------------------------------------------- Question 3


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 3. Which loyalty members spent more than the average member, and how often do they order?

    *Uses three tables or more.*
    """)
    return


@app.cell
def _(ask):
    q3 = ask("""
        WITH line_value AS (
            SELECT ol.order_id,
                   ol.quantity * (ol.price_charged + COALESCE(opt.option_price, 0)) AS value
            FROM order_lines ol
            LEFT JOIN (SELECT line_id, SUM(price_charged) AS option_price
                       FROM line_options
                       GROUP BY line_id) opt ON opt.line_id = ol.line_id
        ),
        order_total AS (
            SELECT order_id, SUM(value) AS total
            FROM line_value
            GROUP BY order_id
        ),
        member_total AS (
            SELECT m.member_id,
                   m.first_name,
                   COUNT(*)                  AS orders,
                   SUM(ot.total)             AS spent,
                   ROUND(AVG(ot.total), 2)   AS average_order
            FROM members m
            JOIN orders o       ON o.member_id = m.member_id
            JOIN order_total ot ON ot.order_id = o.order_id
            GROUP BY m.member_id, m.first_name
        )
        SELECT member_id,
               first_name,
               orders,
               spent,
               average_order,
               (SELECT ROUND(AVG(spent), 2) FROM member_total) AS average_member_spend,
               (SELECT COUNT(*) FROM member_total)             AS members_who_ordered
        FROM member_total
        WHERE spent > (SELECT AVG(spent) FROM member_total)
        ORDER BY spent DESC
    """)
    q3
    return (q3,)


@app.cell(hide_code=True)
def _(mo, money, q3):
    _top = q3.row(0, named=True)
    mo.md(
        f"""
        **Answer.** {q3.height} of the {_top['members_who_ordered']} members who have ordered spent more than the average member total of {money(_top['average_member_spend'])} dollars, and {_top['first_name']} spent the most, {money(_top['spent'])} dollars over {_top['orders']} orders. I took the average across members who have ordered at least once, and "spent" is what the lines and add ons were charged, however the order was paid.
        """
    )
    return


# ---------------------------------------------------------------- Question 4


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 4. Which orders were paid a different amount from what they cost?

    *Uses three tables or more. Checks a rule: an order's payments add up to the order's total.*
    """)
    return


@app.cell
def _(ask):
    q4 = ask("""
        WITH line_value AS (
            SELECT ol.order_id,
                   ol.quantity * (ol.price_charged + COALESCE(opt.option_price, 0)) AS value
            FROM order_lines ol
            LEFT JOIN (SELECT line_id, SUM(price_charged) AS option_price
                       FROM line_options
                       GROUP BY line_id) opt ON opt.line_id = ol.line_id
        ),
        order_total AS (
            SELECT order_id, SUM(value) AS total
            FROM line_value
            GROUP BY order_id
        ),
        order_paid AS (
            SELECT order_id, SUM(amount) AS paid
            FROM payments
            GROUP BY order_id
        )
        SELECT ot.order_id,
               o.ordered_at,
               ot.total,
               COALESCE(op.paid, 0)            AS paid,
               COALESCE(op.paid, 0) - ot.total AS difference
        FROM order_total ot
        JOIN orders o           ON o.order_id = ot.order_id
        LEFT JOIN order_paid op ON op.order_id = ot.order_id
        WHERE COALESCE(op.paid, 0) <> ot.total
        ORDER BY ot.order_id
    """)
    q4
    return (q4,)


@app.cell(hide_code=True)
def _(ask, mo, money, q4):
    _orders = ask("SELECT COUNT(*) AS n FROM orders")["n"][0]
    _parts = " and ".join(
        f"order {_r['order_id']} was paid {money(abs(_r['difference']))} dollars {'short' if _r['difference'] < 0 else 'too much'}"
        for _r in q4.iter_rows(named=True)
    )
    mo.md(
        f"""
        **Answer.** {q4.height} of {_orders} orders have payments that do not add up to the order's total: {_parts}. These are the two orders I broke on purpose in Part A. Orders with no payment at all would also be listed, because a missing payment counts as zero.
        """
    )
    return


# ---------------------------------------------------------------- Question 5


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 5. Which loyalty members joined but have never ordered?
    """)
    return


@app.cell
def _(ask):
    q5 = ask("""
        SELECT m.member_id, m.first_name, m.join_date
        FROM members m
        LEFT JOIN orders o ON o.member_id = m.member_id
        WHERE o.order_id IS NULL
        ORDER BY m.join_date
    """)
    q5
    return (q5,)


@app.cell(hide_code=True)
def _(mo, q5):
    mo.md(
        f"""
        **Answer.** {q5.height} members joined and have never ordered: {', '.join(q5['first_name'])}, with join dates from {q5['join_date'].min()} to {q5['join_date'].max()}.
        """
    )
    return


# ---------------------------------------------------------------- Question 6


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 6. What share of orders each month were paid at least partly with points?
    """)
    return


@app.cell
def _(ask):
    q6 = ask("""
        WITH orders_with_points AS (
            SELECT DISTINCT order_id
            FROM payments
            WHERE method = 'points'
        )
        SELECT date_trunc('month', o.ordered_at)::DATE AS order_month,
               COUNT(*)                                AS orders,
               COUNT(owp.order_id)                     AS orders_with_points,
               ROUND(100.0 * COUNT(owp.order_id) / COUNT(*), 1) AS share_percent
        FROM orders o
        LEFT JOIN orders_with_points owp ON owp.order_id = o.order_id
        GROUP BY order_month
        ORDER BY order_month
    """)
    q6
    return (q6,)


@app.cell(hide_code=True)
def _(mo, q6):
    _all = 100 * q6["orders_with_points"].sum() / q6["orders"].sum()
    _hi = q6.sort("share_percent", descending=True).row(0, named=True)
    _lo = q6.sort("share_percent").row(0, named=True)
    mo.md(
        f"""
        **Answer.** Over the whole year {_all:.1f} percent of orders were paid at least partly with points, from {float(_lo['share_percent']):.1f} percent in {_lo['order_month']:%B %Y} to {float(_hi['share_percent']):.1f} percent in {_hi['order_month']:%B %Y}. The share counts every order in the month, including orders from customers who are not members, and the first and last months are partial because the data runs from 2025-11-08 to the as_of date.
        """
    )
    return


# ---------------------------------------------------------------- Question 7


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 7. Which menu products have not sold in the last 60 days?
    """)
    return


@app.cell
def _(as_of, ask, days_60_start):
    q7 = ask(f"""
        WITH sold_recently AS (
            SELECT DISTINCT ol.product_id
            FROM order_lines ol
            JOIN orders o ON o.order_id = ol.order_id
            WHERE o.ordered_at::DATE BETWEEN DATE '{days_60_start}' AND DATE '{as_of}'
        ),
        last_sale AS (
            SELECT ol.product_id, MAX(o.ordered_at)::DATE AS last_sold
            FROM order_lines ol
            JOIN orders o ON o.order_id = ol.order_id
            GROUP BY ol.product_id
        )
        SELECT p.name AS product,
               p.category,
               p.is_available,
               ls.last_sold
        FROM products p
        LEFT JOIN sold_recently sr ON sr.product_id = p.product_id
        LEFT JOIN last_sale ls     ON ls.product_id = p.product_id
        WHERE sr.product_id IS NULL
        ORDER BY ls.last_sold NULLS FIRST
    """)
    q7
    return (q7,)


@app.cell(hide_code=True)
def _(as_of, days_60_start, mo, q7):
    _never = q7.filter(q7["last_sold"].is_null())["product"].to_list()
    _available = q7.filter(q7["is_available"])["product"].to_list()
    mo.md(
        f"""
        **Answer.** {q7.height} products did not sell in the 60 days from {days_60_start} to {as_of}: {', '.join(q7['product'])}. {len(_available)} of them are still available today ({', '.join(_available)}), and {', '.join(_never)} has never sold at all.
        """
    )
    return


# ---------------------------------------------------------------- Question 8


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 8. On average, how many add ons does an order line carry, for each coffee and tea product?

    *Uses three tables or more.*
    """)
    return


@app.cell
def _(ask):
    q8 = ask("""
        SELECT p.name     AS product,
               p.category,
               COUNT(DISTINCT ol.line_id) AS lines,
               COUNT(lo.option_id)        AS add_ons_on_those_lines,
               ROUND(COUNT(lo.option_id) * 1.0 / COUNT(DISTINCT ol.line_id), 3) AS average_add_ons_per_line
        FROM products p
        JOIN order_lines ol        ON ol.product_id = p.product_id
        LEFT JOIN line_options lo  ON lo.line_id = ol.line_id
        WHERE p.category IN ('coffee', 'tea')
        GROUP BY p.name, p.category
        ORDER BY average_add_ons_per_line DESC
    """)
    q8
    return (q8,)


@app.cell(hide_code=True)
def _(mo, q8):
    _top = q8.row(0, named=True)
    _bottom = q8.row(q8.height - 1, named=True)
    mo.md(
        f"""
        **Answer.** {_top['product']} lines carry the most add ons, {float(_top['average_add_ons_per_line']):.3f} per line on average, and {_bottom['product']} lines the fewest, {float(_bottom['average_add_ons_per_line']):.3f}, across the {q8.height} coffee and tea products that have sold. A line with no add ons counts as zero, and the average is per order line, not per unit, so a line of two lattes counts once. A product that has never sold has no lines to average, so it is not listed.
        """
    )
    return


# ---------------------------------------------------------------- Question 9


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 9. Which add ons earn their keep?

    *My own question. The scenario says the café wants to know which add ons earn their keep, so for each add on this shows how often it is taken and what it brings in after its cost.*
    """)
    return


@app.cell
def _(ask):
    q9 = ask("""
        SELECT opt.name                                         AS add_on,
               COUNT(*)                                         AS lines,
               CAST(SUM(ol.quantity) AS INTEGER)                AS units,
               SUM(ol.quantity * lo.price_charged)              AS revenue,
               SUM(ol.quantity * opt.cost)                      AS cost,
               SUM(ol.quantity * (lo.price_charged - opt.cost)) AS margin,
               ROUND(100.0 * COUNT(*) / (
                   SELECT COUNT(*)
                   FROM order_lines ol2
                   JOIN products p2 ON p2.product_id = ol2.product_id
                   WHERE p2.category IN ('coffee', 'tea')
               ), 1) AS percent_of_drink_lines
        FROM line_options lo
        JOIN order_lines ol ON ol.line_id = lo.line_id
        JOIN options opt    ON opt.option_id = lo.option_id
        GROUP BY opt.name
        ORDER BY margin DESC
    """)
    q9
    return (q9,)


@app.cell(hide_code=True)
def _(mo, money, q9):
    _best = q9.row(0, named=True)
    _most = q9.sort("revenue", descending=True).row(0, named=True)
    _free = q9.filter(q9["revenue"] == 0)["add_on"].to_list()
    mo.md(
        f"""
        **Answer.** {_best['add_on']} earns the most margin, {money(_best['margin'])} dollars on {_best['units']} units, while {_most['add_on']} brings in the most revenue, {money(_most['revenue'])} dollars. {' and '.join(_free)} are free, so they bring in nothing and cost nothing. Margin uses each add on's current cost, since the database stores one cost for each.
        """
    )
    return


# --------------------------------------------------------------- Question 10


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Question 10. How much did the café take in each of the last eight weeks?

    *My own question. A manager would look at this every Monday, so it asks the `weekly_revenue` view that `build.py` saved, by name.*
    """)
    return


@app.cell
def _(as_of, ask):
    q10 = ask(f"""
        SELECT week_start, orders, revenue, average_order
        FROM weekly_revenue
        WHERE week_start >= date_trunc('week', DATE '{as_of}') - INTERVAL 7 WEEK
        ORDER BY week_start
    """)
    q10
    return (q10,)


@app.cell(hide_code=True)
def _(as_of, mo, money, q10):
    _best = q10.sort("revenue", descending=True).row(0, named=True)
    _weak = q10.sort("revenue").row(0, named=True)
    mo.md(
        f"""
        **Answer.** The best of the last eight weeks started on {_best['week_start']} with {money(_best['revenue'])} dollars from {_best['orders']} orders, and the weakest started on {_weak['week_start']} with {money(_weak['revenue'])} dollars from {_weak['orders']} orders. Weeks start on Monday, and the latest week only counts orders up to the as_of date, {as_of}.
        """
    )
    return


# ------------------------------------------------------------------ Sections


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1. How I Know These Numbers Are Right

    Each check below reaches an answer a second way and shows both numbers. Each one stops with an error if the two do not agree, so a wrong query above would turn the cell red.
    """)
    return


@app.cell
def _(ask, pl, q2):
    # Check 1. Question 2's category revenues against the revenue of the lines and the add ons added up separately.
    _from_q2 = float(q2["revenue"].sum())
    _lines = float(ask("SELECT SUM(quantity * price_charged) AS v FROM order_lines")["v"][0])
    _add_ons = float(
        ask("""
            SELECT SUM(ol.quantity * lo.price_charged) AS v
            FROM line_options lo
            JOIN order_lines ol ON ol.line_id = lo.line_id
        """)["v"][0]
    )
    _view = float(ask("SELECT SUM(revenue) AS v FROM weekly_revenue")["v"][0])

    _check_1 = pl.DataFrame(
        {
            "how I got total revenue": [
                "Question 2, the four categories added up",
                "Lines alone plus add ons alone",
                "The weekly_revenue view, all weeks added up",
            ],
            "revenue": [round(_from_q2, 2), round(_lines + _add_ons, 2), round(_view, 2)],
        }
    )
    assert _check_1["revenue"].n_unique() == 1, "the three totals do not agree"
    _check_1
    return


@app.cell
def _(ask, pl, q8):
    # Check 2. Question 8's average computed a second way: count the add ons on each line first, then average the lines.
    _second = ask("""
        WITH per_line AS (
            SELECT ol.line_id, ol.product_id, COUNT(lo.option_id) AS add_ons
            FROM order_lines ol
            LEFT JOIN line_options lo ON lo.line_id = ol.line_id
            GROUP BY ol.line_id, ol.product_id
        )
        SELECT p.name AS product, ROUND(AVG(pl.add_ons), 3) AS second_way
        FROM per_line pl
        JOIN products p ON p.product_id = pl.product_id
        WHERE p.category IN ('coffee', 'tea')
        GROUP BY p.name
    """)
    _check_2 = (
        q8.select(["product", "average_add_ons_per_line"])
        .join(_second, on="product")
        .with_columns(
            (pl.col("average_add_ons_per_line").cast(pl.Float64) - pl.col("second_way").cast(pl.Float64))
            .abs()
            .alias("gap")
        )
    )
    assert _check_2.height == q8.height and _check_2["gap"].max() <= 0.001, "the two ways of averaging disagree"
    _check_2
    return


@app.cell
def _(ask, pl, q4):
    # Check 3. Question 4 against the row count of orders and the two orders written down in Part A.
    _orders = int(ask("SELECT COUNT(*) AS n FROM orders")["n"][0])
    _matching = int(
        ask("""
            WITH line_value AS (
                SELECT ol.order_id,
                       ol.quantity * (ol.price_charged + COALESCE(opt.option_price, 0)) AS value
                FROM order_lines ol
                LEFT JOIN (SELECT line_id, SUM(price_charged) AS option_price
                           FROM line_options
                           GROUP BY line_id) opt ON opt.line_id = ol.line_id
            ),
            order_total AS (SELECT order_id, SUM(value) AS total FROM line_value GROUP BY order_id),
            order_paid  AS (SELECT order_id, SUM(amount) AS paid FROM payments GROUP BY order_id)
            SELECT COUNT(*) AS n
            FROM order_total ot
            JOIN order_paid op ON op.order_id = ot.order_id
            WHERE op.paid = ot.total
        """)["n"][0]
    )
    _part_a = [419, 847]
    _check_3 = pl.DataFrame(
        {
            "what": ["Orders that match", "Orders listed by Question 4", "Together", "Rows in orders"],
            "number": [_matching, q4.height, _matching + q4.height, _orders],
        }
    )
    assert _matching + q4.height == _orders, "matching plus listed orders is not every order"
    assert sorted(q4["order_id"].to_list()) == _part_a, "Question 4 did not find the two orders written down in Part A"
    _check_3
    return


@app.cell
def _(data_dir, last_month_end, last_month_start, pl, q1):
    # Check 4. Question 1 recomputed with polars straight from the CSV files, without the database.
    _orders = pl.read_csv(data_dir / "orders.csv", try_parse_dates=True)
    _lines = pl.read_csv(data_dir / "order_lines.csv")
    _products = pl.read_csv(data_dir / "products.csv")
    _check_4 = (
        _lines.join(
            _orders.filter(pl.col("ordered_at").dt.date().is_between(last_month_start, last_month_end)),
            on="order_id",
        )
        .join(_products, on="product_id")
        .group_by("name")
        .agg(pl.col("quantity").sum().alias("units_from_csv"))
        .sort(["units_from_csv", "name"], descending=[True, False])
        .head(3)
    )
    _both = q1.with_columns(pl.col("units").cast(pl.Int64)).join(
        _check_4.rename({"name": "product"}), on="product", how="full", coalesce=True
    )
    assert _both.height == 3 and (_both["units"] == _both["units_from_csv"]).all(), "polars and SQL disagree on the top three"
    _both
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. Working With the Agent

    *Write this section yourself, in your own words. Pick one piece of AI output you did not accept as is. What did it give you, what did you change, and how did you know? Point to the commit or the cell. If the agent got it right the first time, say what you did to verify it, and point to the check cell above.*

    WRITE YOURS HERE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. Reading It Back

    **My question:** Question 8, the average number of add ons on an order line for each coffee and tea product. It reads three tables: products, order lines and line options.

    **My prediction, committed as `db: prediction` before I ran the joins:**
    How many rows I expect the joins to produce before any grouping, and why.

    

    I predict the joins will produce approximately 1,800 rows before grouping. There are 1,522 coffee and tea order lines. Since the query uses a LEFT JOIN, every order line will appear at least once, even if it has no add-ons. Some order lines have multiple add-ons, which will create additional rows.

   

   The data indicates that the joins produce 1,794 rows, so my prediction was very close. The difference happens because some order lines have multiple add-ons, causing them to appear more than once. Lines without add-ons still appear because of the LEFT JOIN.

    
    """)
    return


@app.cell(disabled=True)
def _(ask):
    # This cell is disabled on purpose. Commit your prediction first, then enable it from the cell menu.
    joined = ask("""
        SELECT p.name AS product, ol.line_id, lo.option_id
        FROM products p
        JOIN order_lines ol       ON ol.product_id = p.product_id
        LEFT JOIN line_options lo ON lo.line_id = ol.line_id
        WHERE p.category IN ('coffee', 'tea')
    """)
    joined_rows = joined.height
    joined_rows
    return joined, joined_rows


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 4. Going Further

    I took two steps past the ten questions. First, a chart of Question 10 with both axes titled. Second, a dropdown that changes what a query returns, so somebody can ask about a category without editing code.
    """)
    return


@app.cell
def _(alt, pl, q10):
    _data = q10.with_columns(
        pl.col("revenue").cast(pl.Float64),
        pl.col("week_start").dt.strftime("%b %d").alias("week_label"),
    )
    alt.Chart(_data).mark_bar().encode(
        x=alt.X("week_label:N", sort=_data["week_label"].to_list(), title="Week starting (Monday)"),
        y=alt.Y("revenue:Q", title="Revenue (dollars)"),
        tooltip=["week_start", "orders", "revenue"],
    ).properties(title="Café revenue by week, last eight weeks", width=560, height=280)
    return


@app.cell
def _(mo):
    category_picker = mo.ui.dropdown(
        options=["coffee", "tea", "food", "other"],
        value="coffee",
        label="Pick a category: the top five products in the last 90 days",
    )
    category_picker
    return (category_picker,)


@app.cell
def _(as_of, ask, category_picker, days_90_start):
    ask(f"""
        SELECT p.name AS product,
               CAST(SUM(ol.quantity) AS INTEGER) AS units
        FROM order_lines ol
        JOIN orders o   ON o.order_id = ol.order_id
        JOIN products p ON p.product_id = ol.product_id
        WHERE p.category = '{category_picker.value}'
          AND o.ordered_at::DATE BETWEEN DATE '{days_90_start}' AND DATE '{as_of}'
        GROUP BY p.name
        ORDER BY units DESC, product
        LIMIT 5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 5. Time Spent

    About WRITE A NUMBER hours outside class.
    """)
    return


if __name__ == "__main__":
    app.run()
