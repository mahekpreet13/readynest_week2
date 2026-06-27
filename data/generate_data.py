import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = os.path.dirname(__file__)

# ── Customers ─────────────────────────────────────────────────────────────────
first_names = ["Aisha","Rahul","Priya","James","Fatima","Chen","Sofia","Liam",
                "Amara","Noah","Zara","Arjun","Emma","Omar","Mei","Carlos",
                "Nadia","Ethan","Layla","Vikram"]
last_names  = ["Sharma","Johnson","Patel","Williams","Khan","Wang","Garcia",
               "Brown","Nkosi","Davis","Ali","Gupta","Martinez","Hassan",
               "Zhang","Lopez","Cohen","Lee","Okonkwo","Singh"]
regions = ["North","South","East","West","Central"]
email_domains = ["gmail.com","yahoo.com","outlook.com","hotmail.com"]

start_date = datetime(2023, 1, 1)
end_date   = datetime(2025, 6, 30)

def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

n_customers = 500
customer_ids = [f"C{str(i).zfill(4)}" for i in range(1, n_customers + 1)]

# Pareto-like weights: top 20% customers get higher order probability
pareto_weights = np.concatenate([
    np.ones(400) * 1,
    np.ones(100) * 4
])
np.random.shuffle(pareto_weights)

customers = pd.DataFrame({
    "customer_id":   customer_ids,
    "name":          [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(n_customers)],
    "email":         [None] * n_customers,  # filled below
    "region":        [random.choice(regions) for _ in range(n_customers)],
    "join_date":     [rand_date(start_date, end_date).strftime("%Y-%m-%d") for _ in range(n_customers)],
    "customer_type": [random.choice(["New", "Returning"]) for _ in range(n_customers)],
})
# Fix email column (list comprehension above is awkward, redo cleanly)
emails = []
for i in range(n_customers):
    fn = first_names[i % len(first_names)]
    ln = last_names[i % len(last_names)]
    if random.random() > 0.05:
        emails.append(f"{fn.lower()}.{ln.lower()}{random.randint(1,99)}@{random.choice(email_domains)}")
    else:
        emails.append(None)
customers["email"] = emails

customers.to_csv(os.path.join(OUTPUT_DIR, "raw_customers.csv"), index=False)
print(f"Customers: {len(customers)} rows")

# ── Products ──────────────────────────────────────────────────────────────────
products_data = [
    ("P001","Wireless Earbuds","Electronics",49.99),
    ("P002","Smart Watch","Electronics",199.99),
    ("P003","Laptop Stand","Electronics",34.99),
    ("P004","USB-C Hub","Electronics",29.99),
    ("P005","Mechanical Keyboard","Electronics",89.99),
    ("P006","Running Shoes","Footwear",79.99),
    ("P007","Yoga Mat","Sports",25.99),
    ("P008","Resistance Bands","Sports",19.99),
    ("P009","Water Bottle","Sports",14.99),
    ("P010","Dumbbell Set","Sports",59.99),
    ("P011","Face Moisturizer","Beauty",22.99),
    ("P012","Vitamin C Serum","Beauty",35.99),
    ("P013","Sunscreen SPF50","Beauty",18.99),
    ("P014","Hair Dryer","Beauty",44.99),
    ("P015","Novel: The Journey","Books",12.99),
    ("P016","Python Programming","Books",39.99),
    ("P017","Self-Help Guide","Books",14.99),
    ("P018","Coffee Maker","Home",69.99),
    ("P019","Air Purifier","Home",129.99),
    ("P020","Desk Lamp","Home",39.99),
]
products = pd.DataFrame(products_data, columns=["product_id","product_name","category","unit_price"])
products.to_csv(os.path.join(OUTPUT_DIR, "raw_products.csv"), index=False)
print(f"Products: {len(products)} rows")

# ── Orders ────────────────────────────────────────────────────────────────────
n_orders = 1000
# Weight customers by pareto_weights so top 20% get more orders
order_customer_ids = np.random.choice(customer_ids, size=n_orders, p=pareto_weights/pareto_weights.sum())

region_map = customers.set_index("customer_id")["region"].to_dict()

order_ids = [f"O{str(i).zfill(5)}" for i in range(1, n_orders + 1)]
order_dates = [rand_date(start_date, end_date).strftime("%Y-%m-%d") for _ in range(n_orders)]

orders = pd.DataFrame({
    "order_id":    order_ids,
    "customer_id": order_customer_ids,
    "order_date":  order_dates,
    "region":      [region_map[cid] for cid in order_customer_ids],
})

# Add ~30 duplicate rows to simulate dirty data
dupes = orders.sample(30, random_state=1)
orders = pd.concat([orders, dupes], ignore_index=True)
orders.to_csv(os.path.join(OUTPUT_DIR, "raw_orders.csv"), index=False)
print(f"Orders (with dupes): {len(orders)} rows")

# ── Sales ─────────────────────────────────────────────────────────────────────
# Product popularity weights (top sellers get more)
product_ids = products["product_id"].tolist()
pop_weights = np.array([5,4,3,3,2,4,3,2,3,2,3,2,2,2,1,3,1,3,2,2], dtype=float)
pop_weights /= pop_weights.sum()

n_sales = 3000
sale_order_ids = np.random.choice(order_ids, size=n_sales)  # from original 1000 orders only
sale_product_ids = np.random.choice(product_ids, size=n_sales, p=pop_weights)
quantities = np.random.randint(1, 5, size=n_sales)
discounts = np.random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20], size=n_sales)

price_map = products.set_index("product_id")["unit_price"].to_dict()
totals = [
    round(price_map[pid] * qty * (1 - disc), 2)
    for pid, qty, disc in zip(sale_product_ids, quantities, discounts)
]

# Inject ~20 outlier values
outlier_idx = np.random.choice(n_sales, 20, replace=False)
for i in outlier_idx:
    totals[i] = round(totals[i] * random.uniform(8, 15), 2)

sales = pd.DataFrame({
    "sale_id":    [f"S{str(i).zfill(6)}" for i in range(1, n_sales + 1)],
    "order_id":   sale_order_ids,
    "product_id": sale_product_ids,
    "quantity":   quantities,
    "discount":   discounts,
    "total_amount": totals,
})
sales.to_csv(os.path.join(OUTPUT_DIR, "raw_sales.csv"), index=False)
print(f"Sales: {len(sales)} rows")
print("Data generation complete.")
