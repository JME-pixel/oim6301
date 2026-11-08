"""Write the CSV files for the Babson Bean Cafe database into data/.

Run it from anywhere:  python projects/db/make_data.py
It uses a fixed random seed, so it writes the same files every time.

Money is handled as whole cents inside the script and written as dollars.
The as_of date is 2026-11-07, so "last month" in Part B is October 2026.
"""

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 2026
AS_OF = date(2026, 11, 7)
START = date(2025, 11, 8)  # twelve months up to the as_of date
N_ORDERS = 1250
PRICE_CHANGE = date(2026, 6, 1)  # some menu prices went up on this day

rng = random.Random(SEED)
DATA = Path(__file__).resolve().parent / "data"
DATA.mkdir(exist_ok=True)


def dollars(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def write_csv(name, header, rows):
    with open(DATA / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  {name}.csv: {len(rows)} rows")


# ---------------------------------------------------------------- the menu
# name, category, price, cost, available today, popularity weight,
# price before 2026-06-01 (or None), first day sold, last day sold
PRODUCTS = [
    ("Drip Coffee", "coffee", 275, 45, True, 14, 250, None, None),
    ("Americano", "coffee", 325, 55, True, 6, None, None, None),
    ("Espresso", "coffee", 250, 50, True, 3, None, None, None),
    ("Latte", "coffee", 450, 95, True, 14, 425, None, None),
    ("Cappuccino", "coffee", 425, 90, True, 6, None, None, None),
    ("Flat White", "coffee", 475, 100, True, 4, None, None, None),
    ("Mocha", "coffee", 500, 120, True, 4, None, None, None),
    ("Cold Brew", "coffee", 425, 70, True, 8, 400, None, None),
    ("Iced Latte", "coffee", 475, 100, True, 8, None, None, None),
    ("Pumpkin Spice Latte", "coffee", 525, 110, False, 6, None, date(2025, 11, 8), date(2025, 11, 30)),
    ("Cortado", "coffee", 375, 80, True, 0, None, None, None),  # never sold
    ("Black Tea", "tea", 250, 35, True, 3, None, None, None),
    ("Green Tea", "tea", 250, 35, True, 3, None, None, None),
    ("Herbal Tea", "tea", 250, 35, False, 2, None, None, date(2026, 7, 15)),
    ("Chai Latte", "tea", 475, 105, True, 5, None, None, None),
    ("Matcha Latte", "tea", 525, 140, True, 4, None, None, None),
    ("Butter Croissant", "food", 350, 110, True, 7, 325, None, None),
    ("Blueberry Muffin", "food", 325, 95, True, 5, None, None, None),
    ("Bagel with Cream Cheese", "food", 375, 105, True, 4, None, None, None),
    ("Breakfast Sandwich", "food", 625, 240, True, 5, 595, None, None),
    ("Turkey Sandwich", "food", 850, 330, True, 4, None, None, None),
    ("Avocado Toast", "food", 725, 260, True, 3, None, None, None),
    ("Bottled Water", "other", 175, 40, True, 4, None, None, None),
    ("Hot Cocoa", "other", 425, 100, True, 3, None, date(2025, 11, 8), date(2026, 3, 31)),
    ("Orange Juice", "other", 350, 130, False, 2, None, None, date(2026, 8, 20)),
]
P = [
    dict(id=i + 1, name=r[0], cat=r[1], price=r[2], cost=r[3], avail=r[4],
         w=r[5], old=r[6], first=r[7], last=r[8])
    for i, r in enumerate(PRODUCTS)
]

# name, price, cost, price before 2026-06-01 (or None)
OPTIONS = [
    ("Extra Shot", 75, 25, None),
    ("Oat Milk", 70, 30, 60),
    ("Almond Milk", 70, 28, None),
    ("Vanilla Syrup", 60, 12, None),
    ("Caramel Syrup", 60, 14, None),
    ("Hazelnut Syrup", 60, 13, None),
    ("Whipped Cream", 50, 10, None),
    ("Decaf", 0, 0, None),
    ("Extra Hot", 0, 0, None),
]
O = {r[0]: dict(id=i + 1, name=r[0], price=r[1], cost=r[2], old=r[3]) for i, r in enumerate(OPTIONS)}

MILK_DRINKS = {"Latte", "Cappuccino", "Flat White", "Mocha", "Iced Latte",
               "Pumpkin Spice Latte", "Cortado", "Chai Latte", "Matcha Latte"}
ICED = {"Cold Brew", "Iced Latte"}


def option_pool(p):
    """Which options a drink can carry, with how often each is picked."""
    if p["cat"] not in ("coffee", "tea"):
        return {}
    n = p["name"]
    if n in MILK_DRINKS:
        pool = {"Oat Milk": 30, "Extra Shot": 20, "Vanilla Syrup": 18, "Caramel Syrup": 10,
                "Almond Milk": 8, "Hazelnut Syrup": 6, "Decaf": 2}
        if n in ("Mocha", "Pumpkin Spice Latte"):
            pool["Whipped Cream"] = 14
        elif n not in ICED:
            pool["Whipped Cream"] = 2
        if n not in ICED:
            pool["Extra Hot"] = 3
        if n in ("Chai Latte", "Matcha Latte"):
            del pool["Extra Shot"], pool["Decaf"]
        return pool
    if p["cat"] == "coffee":
        pool = {"Extra Shot": 22, "Vanilla Syrup": 14, "Caramel Syrup": 8,
                "Hazelnut Syrup": 6, "Decaf": 10}
        if n == "Cold Brew":
            pool.update({"Oat Milk": 12, "Almond Milk": 4})
        else:
            pool["Extra Hot"] = 8
        return pool
    return {"Vanilla Syrup": 8, "Extra Hot": 10}  # plain tea


def weighted_sample(items, weights, k):
    items, weights, out = list(items), list(weights), []
    for _ in range(min(k, len(items))):
        i = rng.choices(range(len(items)), weights=weights)[0]
        out.append(items.pop(i))
        weights.pop(i)
    return out


def price_on(item, d):
    return item["old"] if item["old"] is not None and d < PRICE_CHANGE else item["price"]


def product_weight(p, d, hour):
    w = p["w"]
    if w == 0:
        return 0
    if p["first"] and d < p["first"]:
        return 0
    if p["last"] and d > p["last"]:
        return 0
    n, m = p["name"], d.month
    if n in ICED:
        w *= 2.5 if m in (6, 7, 8, 9) else 0.4 if m in (12, 1, 2) else 1
    elif p["cat"] in ("coffee", "tea") and n != "Espresso":
        w *= 1.4 if m in (12, 1, 2) else 0.7 if m in (6, 7, 8) else 1
    if n in ("Butter Croissant", "Blueberry Muffin", "Bagel with Cream Cheese"):
        w *= 1 if hour <= 11 else 0.2
    if n == "Breakfast Sandwich":
        w *= 1 if hour <= 11 else 0.1
    if n in ("Turkey Sandwich", "Avocado Toast"):
        w *= 0.2 if hour < 11 else 2.5 if hour <= 14 else 1
    return w


# -------------------------------------------------------------- the members
FIRST_NAMES = [
    "Ava", "Liam", "Noah", "Emma", "Olivia", "Mateo", "Sofia", "Amara", "Kwame", "Priya",
    "Arjun", "Mei", "Hiro", "Yuki", "Fatima", "Omar", "Layla", "Diego", "Camila", "Luca",
    "Isabella", "Jamal", "Aaliyah", "Malik", "Imani", "Chen", "Wei", "Ananya", "Rohan", "Zara",
    "Elena", "Nikolai", "Ingrid", "Sven", "Tariq", "Noor", "Kofi", "Abena", "Tomas", "Marta",
    "Paolo", "Giulia", "Andre", "Simone", "Jonah", "Hannah", "Ethan", "Maya", "Leila", "Samir",
    "Dev", "Aiko", "Jin", "Carlos", "Valeria", "Ruth", "Gabriel", "Naomi", "Felix", "Tessa",
]
N_MEMBERS = 60
assert len(set(FIRST_NAMES)) >= N_MEMBERS
names = rng.sample(FIRST_NAMES, N_MEMBERS)

# 5 members joined in the last three weeks and have not ordered yet,
# 2 older members joined and never ordered, 23 joined before the data starts.
join_dates = []
join_dates += [date(2025, 1, 6) + timedelta(days=rng.randrange(0, 305)) for _ in range(23)]
join_dates += [START + timedelta(days=rng.randrange(0, (date(2026, 10, 15) - START).days)) for _ in range(32)]
join_dates += [date(2026, 10, 20) + timedelta(days=rng.randrange(0, 17)) for _ in range(5)]
join_dates.sort()

mobiles = rng.sample(range(10000), N_MEMBERS)
areas = [617, 508, 781, 978]
members = []
for i in range(N_MEMBERS):
    jd = join_dates[i]
    members.append(dict(
        id=i + 1,
        first=names[i],
        mobile=f"{rng.choice(areas)}-555-{mobiles[i]:04d}",
        email=f"{names[i].lower()}{rng.randint(10, 99)}@example.com" if rng.random() < 0.7 else "",
        join=jd,
        bal=rng.randrange(0, 100, 5) if jd < START else 0,
        weight=rng.lognormvariate(0, 1.0) * (1.5 if jd < START else 1.0),
    ))
recent_five = [m["id"] for m in members if m["join"] >= date(2026, 10, 20)]
assert len(recent_five) == 5
older_two = rng.sample([m["id"] for m in members if m["join"] < date(2026, 10, 1)][3:30], 2)
never_ordered = set(recent_five) | set(older_two)
eligible = [m for m in members if m["id"] not in never_ordered]


# --------------------------------------------------------------- the orders
def day_weight(d):
    w = [1.0, 1.05, 1.05, 1.0, 0.8, 0.3, 0.25][d.weekday()]
    if d.month in (6, 7, 8):
        w *= 0.45
    if (d.month == 12 and d.day >= 20) or (d.month == 1 and d.day <= 10):
        w *= 0.3
    return w


all_days = [START + timedelta(days=i) for i in range((AS_OF - START).days + 1)]
HOURS = list(range(7, 18))
HOUR_W = [10, 18, 14, 10, 9, 12, 10, 7, 5, 3, 2]
stamps = []
for d in rng.choices(all_days, weights=[day_weight(d) for d in all_days], k=N_ORDERS):
    h = rng.choices(HOURS, weights=HOUR_W)[0]
    stamps.append(datetime(d.year, d.month, d.day, h, rng.randrange(60), 0))
stamps.sort()

is_member_order = [rng.random() < 0.62 for _ in stamps]
member_of = [None] * N_ORDERS
member_idx = [i for i in range(N_ORDERS) if is_member_order[i]]

# every member who is meant to have ordered gets at least one order, latest joiners first
free = set(member_idx)
for m in sorted(eligible, key=lambda x: x["join"], reverse=True):
    cands = [i for i in free if stamps[i].date() >= m["join"]]
    i = rng.choice(sorted(cands))
    member_of[i] = m["id"]
    free.discard(i)
for i in sorted(free):
    cands = [m for m in eligible if m["join"] <= stamps[i].date()]
    member_of[i] = rng.choices(cands, weights=[m["weight"] for m in cands])[0]["id"]

bal = {m["id"]: m["bal"] for m in members}  # running points balance
orders, lines, line_opts, payments = [], [], [], []
order_totals = {}

for n, ts in enumerate(stamps):
    oid = n + 1
    d, hour = ts.date(), ts.hour
    mid = member_of[n]
    channel = "app" if mid and rng.random() < 0.30 else "counter"
    orders.append([oid, ts.strftime("%Y-%m-%d %H:%M:%S"), mid if mid else "", channel])

    n_lines = rng.choices([1, 2, 3], weights=[55, 32, 13])[0]
    total = 0
    for _ in range(n_lines):
        p = rng.choices(P, weights=[product_weight(x, d, hour) for x in P])[0]
        qty = rng.choices([1, 2, 3], weights=[88, 10, 2])[0]
        lid = len(lines) + 1
        price = price_on(p, d)
        lines.append([lid, oid, p["id"], qty, dollars(price)])
        per_unit = price
        pool = option_pool(p)
        if pool:
            weights_k = [46, 34, 15, 5] if p["name"] in MILK_DRINKS else [72, 22, 5, 1]
            k = rng.choices([0, 1, 2, 3], weights=weights_k)[0]
            for oname in weighted_sample(list(pool), list(pool.values()), k):
                op = price_on(O[oname], d)
                line_opts.append([lid, O[oname]["id"], dollars(op)])
                per_unit += op
        total += qty * per_unit
    order_totals[oid] = total

    # payments
    parts = []
    if mid and bal[mid] >= 100 and rng.random() < 0.40:  # members save up at least 100 points
        dollars_wanted = min(rng.choice([2, 3, 4, 5]), bal[mid] // 20, total // 100)
        if dollars_wanted >= 1:  # 20 points buy one dollar
            parts.append(("points", dollars_wanted * 100))
            bal[mid] -= dollars_wanted * 20
    rest = total - sum(a for _, a in parts)
    if rest > 0:
        if channel == "app":
            parts.append(("app" if rng.random() < 0.9 else "card", rest))
        else:
            cash_share = 0.20 if mid else 0.38
            if not parts and rest >= 400 and rng.random() < 0.04:
                cash_part = 100 * rng.randint(1, rest // 100 - 1)
                parts.append(("cash", cash_part))
                parts.append(("card", rest - cash_part))
            else:
                parts.append(("cash" if rng.random() < cash_share else "card", rest))
    for method, amount in parts:
        payments.append([len(payments) + 1, oid, method, amount])
    if mid:
        bal[mid] += (total // 100) * 2  # 2 points for every whole dollar, 20 points buy one dollar

# ------------------------------- break the payment rule on purpose, two orders
single = {}
for p_ in payments:
    single.setdefault(p_[1], []).append(p_)
under = next(v[0] for k, v in single.items()
             if len(v) == 1 and v[0][2] == "cash" and order_totals[k] >= 400 and stamps[k - 1].date() >= date(2026, 3, 1))
over = next(v[0] for k, v in single.items()
            if len(v) == 1 and v[0][2] == "card" and order_totals[k] >= 400 and stamps[k - 1].date() >= date(2026, 7, 1))
under_total, over_total = order_totals[under[1]], order_totals[over[1]]
under[3] -= 75   # this order is paid 75 cents short
over[3] += 200   # this order is paid 2 dollars too much
for p_ in payments:
    p_[3] = dollars(p_[3])

# ------------------------------------------------------------------- write
print("Writing CSV files to", DATA)
write_csv("members", ["member_id", "first_name", "mobile", "email", "join_date", "points_balance"],
          [[m["id"], m["first"], m["mobile"], m["email"], m["join"].isoformat(), bal[m["id"]]] for m in members])
write_csv("products", ["product_id", "name", "category", "price", "cost", "is_available"],
          [[p["id"], p["name"], p["cat"], dollars(p["price"]), dollars(p["cost"]),
            "true" if p["avail"] else "false"] for p in P])
write_csv("options", ["option_id", "name", "price", "cost"],
          [[o["id"], o["name"], dollars(o["price"]), dollars(o["cost"])] for o in O.values()])
write_csv("orders", ["order_id", "ordered_at", "member_id", "channel"], orders)
write_csv("order_lines", ["line_id", "order_id", "product_id", "quantity", "price_charged"], lines)
write_csv("line_options", ["line_id", "option_id", "price_charged"], line_opts)
write_csv("payments", ["payment_id", "order_id", "method", "amount"], payments)

print()
print("Rule broken on purpose: an order's payments add up to its total. Exactly two orders:")
print(f"  order {under[1]}: total {dollars(under_total)}, paid {dollars(under_total - 75)} (75 cents short)")
print(f"  order {over[1]}: total {dollars(over_total)}, paid {dollars(over_total + 200)} (2.00 too much)")
print(f"Members who have never ordered: {sorted(never_ordered)}")
print(f"as_of date: {AS_OF}")
