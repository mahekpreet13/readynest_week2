import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64_image("image-vi-s_202602.webp")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Insights Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/webp;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(255, 255, 255, 0.80);
    z-index: 0;
}}
.block-container {{
    position: relative;
    z-index: 1;
}}
</style>
""", unsafe_allow_html=True)

TEAL      = "#1a7f74"
TEAL_LIGHT= "#a8d5d1"
ORANGE    = "#e07b54"
PALETTE   = [TEAL, TEAL_LIGHT, ORANGE, "#f4a261", "#264653", "#2a9d8f"]

# ── Load & prepare data ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_customer_insights.csv", parse_dates=["order_date", "join_date"])
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("Filters")

regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
sel_region = st.sidebar.selectbox("Region", regions)

segments = ["All"] + sorted(df["segment"].dropna().unique().tolist())
sel_segment = st.sidebar.selectbox("Customer Segment", segments)

cust_types = ["All"] + sorted(df["customer_type"].dropna().unique().tolist())
sel_type = st.sidebar.selectbox("Customer Type", cust_types)

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()
date_range = st.sidebar.date_input("Order Date Range", value=(min_date, max_date),
                                    min_value=min_date, max_value=max_date)

# Apply filters
filtered = df.copy()
if sel_region != "All":
    filtered = filtered[filtered["region"] == sel_region]
if sel_segment != "All":
    filtered = filtered[filtered["segment"] == sel_segment]
if sel_type != "All":
    filtered = filtered[filtered["customer_type"] == sel_type]
if len(date_range) == 2:
    filtered = filtered[
        (filtered["order_date"].dt.date >= date_range[0]) &
        (filtered["order_date"].dt.date <= date_range[1])
    ]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<h1 style='
    color:black;
    font-family: "Times New Roman", serif;
    margin-bottom:0;
'>
Customer Insights Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("---")



# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_customers = filtered["customer_id"].nunique()
total_sales     = filtered["total_amount"].sum()
total_orders    = filtered["order_id"].nunique()
avg_order_val   = filtered.groupby("order_id")["total_amount"].sum().mean() if total_orders > 0 else 0

st.markdown(f"""
<style>
.kpi-btn {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    background: rgba(255,255,255,0.85);
    border: 1.5px solid rgba(26,127,116,0.2);
    border-radius: 14px;
    padding: 22px 28px;
    cursor: pointer;
    transition: all 0.22s ease;
    box-shadow: 0 2px 8px rgba(26,127,116,0.07);
    width: 100%;
    text-align: left;
}}
.kpi-btn:hover {{
    background: rgba(26,127,116,0.08);
    border-color: #1a7f74;
    box-shadow: 0 6px 24px rgba(26,127,116,0.18);
    transform: translateY(-3px) scale(1.03);
}}
.kpi-btn:hover .kpi-value {{
    font-size: 2.2rem;
    color: #1a7f74;
}}
.kpi-label {{
    font-size: 0.85rem;
    color: #666;
    font-weight: 500;
    margin-bottom: 6px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}}
.kpi-value {{
    font-size: 1.9rem;
    font-weight: 700;
    color: #1a1a2e;
    transition: font-size 0.22s ease, color 0.22s ease;
    line-height: 1.1;
}}
</style>

<div style="display:grid; grid-template-columns: repeat(4,1fr); gap:16px; margin-bottom:8px;">
    <button class="kpi-btn" onclick="">
        <span class="kpi-label">Total Customers</span>
        <span class="kpi-value">{total_customers:,}</span>
    </button>
    <button class="kpi-btn" onclick="">
        <span class="kpi-label">Total Sales</span>
        <span class="kpi-value">${total_sales:,.2f}</span>
    </button>
    <button class="kpi-btn" onclick="">
        <span class="kpi-label">Total Orders</span>
        <span class="kpi-value">{total_orders:,}</span>
    </button>
    <button class="kpi-btn" onclick="">
        <span class="kpi-label">Avg Order Value</span>
        <span class="kpi-value">${avg_order_val:,.2f}</span>
    </button>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Illustration banner ───────────────────────────────────────────────────────
illustration = get_base64_image("images.webp")
st.markdown(f"""
<div style="
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(135deg, rgba(26,127,116,0.10) 0%, rgba(168,213,209,0.15) 100%);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    border: 1px solid rgba(26,127,116,0.15);
">
    <div style="flex: 1;">
        <h2 style="color:#1a7f74; margin:0 0 8px 0; font-size:1.4rem;">Analyze. Understand. Suggest. Grow.</h2>
        <p style="color:#444; margin:0; font-size:0.95rem; max-width:480px;">
            Explore sales trends, customer segments, and product performance across all regions.
            Use the sidebar filters to drill down into specific segments or time periods.
        </p>
    </div>
    <div style="flex-shrink: 0; margin-left: 32px;">
        <img src="data:image/webp;base64,{illustration}"
             style="height: 160px; object-fit: contain; border-radius: 8px; opacity: 0.92;" />
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pre-compute all chart data ────────────────────────────────────────────────
monthly = (
    filtered.groupby("year_month")["total_amount"]
    .sum().reset_index().sort_values("year_month")
)
top_region = filtered.groupby("region")["total_amount"].sum().idxmax()
top_month  = monthly.loc[monthly["total_amount"].idxmax(), "year_month"] if len(monthly) else "—"

prod_perf = (
    filtered.groupby(["product_name", "category"])["total_amount"]
    .sum().reset_index().sort_values("total_amount", ascending=False)
)
top_product = prod_perf.iloc[0]["product_name"] if len(prod_perf) else "—"

seg_counts = filtered.groupby("segment")["customer_id"].nunique().reset_index()
seg_counts.columns = ["segment", "customers"]
top_seg = seg_counts.sort_values("customers", ascending=False).iloc[0]["segment"] if len(seg_counts) else "—"

cat_perf = filtered.groupby("category")["total_amount"].sum().reset_index().sort_values("total_amount", ascending=False)
top_cat  = cat_perf.iloc[0]["category"] if len(cat_perf) else "—"

rfm = filtered.groupby("customer_id").agg(
    frequency=("order_id", pd.Series.nunique),
    monetary=("total_amount", "sum"),
    segment=("segment", "first"),
    recency=("recency", "first"),
).reset_index()

# ── Summary cards ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
.card-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-bottom: 28px; }
.sum-card {
    background: rgba(255,255,255,0.88);
    border: 1.5px solid rgba(26,127,116,0.18);
    border-radius: 16px;
    padding: 22px 24px;
    cursor: pointer;
    transition: all 0.22s ease;
    box-shadow: 0 2px 10px rgba(26,127,116,0.07);
}
.sum-card:hover {
    background: rgba(26,127,116,0.07);
    border-color: #1a7f74;
    box-shadow: 0 8px 28px rgba(26,127,116,0.16);
    transform: translateY(-4px);
}
.card-tag  { font-size:0.72rem; font-weight:700; letter-spacing:0.08em;
             text-transform:uppercase; color:#1a7f74; margin-bottom:6px; }
.card-title{ font-size:1.05rem; font-weight:700; color:#1a1a2e; margin-bottom:4px; }
.card-hint { font-size:0.82rem; color:#777; }
.card-stat { font-size:0.88rem; color:#1a7f74; font-weight:600; margin-top:10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("### Explore the data — click a card to expand")

# Row 1 of cards
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="sum-card">
        <div class="card-tag">Sales Performance</div>
        <div class="card-title">Monthly Sales Trend</div>
        <div class="card-hint">Revenue over time across all months</div>
        <div class="card-stat">Peak month: {top_month}</div>
    </div>""", unsafe_allow_html=True)
    if st.button("View Monthly Sales Trend", key="btn_sales"):
        st.session_state["open_card"] = "sales"

with c2:
    st.markdown(f"""<div class="sum-card">
        <div class="card-tag">Regional Analysis</div>
        <div class="card-title">Sales by Region</div>
        <div class="card-hint">Which regions drive the most revenue</div>
        <div class="card-stat">Top region: {top_region}</div>
    </div>""", unsafe_allow_html=True)
    if st.button("View Sales by Region", key="btn_region"):
        st.session_state["open_card"] = "region"

with c3:
    st.markdown(f"""<div class="sum-card">
        <div class="card-tag">Product Performance</div>
        <div class="card-title">Top & Bottom Products</div>
        <div class="card-hint">Best and worst performing products</div>
        <div class="card-stat">Top product: {top_product}</div>
    </div>""", unsafe_allow_html=True)
    if st.button("View Product Performance", key="btn_products"):
        st.session_state["open_card"] = "products"

# Row 2 of cards
c4, c5, c6 = st.columns(3)
with c4:
    st.markdown(f"""<div class="sum-card">
        <div class="card-tag">Segmentation</div>
        <div class="card-title">Customer Segments</div>
        <div class="card-hint">High / Medium / Low Value breakdown</div>
        <div class="card-stat">Largest segment: {top_seg}</div>
    </div>""", unsafe_allow_html=True)
    if st.button("View Customer Segmentation", key="btn_seg"):
        st.session_state["open_card"] = "segmentation"

with c5:
    st.markdown(f"""<div class="sum-card">
        <div class="card-tag">Category Breakdown</div>
        <div class="card-title">Revenue by Category</div>
        <div class="card-hint">Which product categories earn the most</div>
        <div class="card-stat">Top category: {top_cat}</div>
    </div>""", unsafe_allow_html=True)
    if st.button("View Category Revenue", key="btn_cat"):
        st.session_state["open_card"] = "category"

with c6:
    st.markdown("""<div class="sum-card">
        <div class="card-tag">RFM & Customers</div>
        <div class="card-title">RFM Analysis & Top Customers</div>
        <div class="card-hint">Frequency vs spend scatter + top 10 table</div>
        <div class="card-stat">View full customer breakdown</div>
    </div>""", unsafe_allow_html=True)
    if st.button("View RFM Analysis", key="btn_rfm"):
        st.session_state["open_card"] = "rfm"

# ── Expanded chart area ───────────────────────────────────────────────────────
open_card = st.session_state.get("open_card", None)

if open_card:
    st.markdown("---")
    close_col, _ = st.columns([1, 5])
    with close_col:
        if st.button("Close", key="close_btn"):
            st.session_state["open_card"] = None
            st.rerun()

if open_card == "sales":
    st.subheader("Monthly Sales Trend")
    col1, col2 = st.columns([3, 2])
    with col1:
        fig = px.bar(monthly, x="year_month", y="total_amount",
                     color_discrete_sequence=[TEAL],
                     labels={"year_month": "Month", "total_amount": "Revenue ($)"})
        fig.update_layout(xaxis_tickangle=-45, plot_bgcolor="white",
                          yaxis_tickprefix="$", margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.metric("Peak Revenue Month", top_month)
        st.metric("Total Revenue", f"${filtered['total_amount'].sum():,.2f}")
        st.metric("Months of Data", str(monthly.shape[0]))

elif open_card == "region":
    st.subheader("Sales by Region")
    region_sales = filtered.groupby("region")["total_amount"].sum().reset_index().sort_values("total_amount")
    col1, col2 = st.columns([3, 2])
    with col1:
        fig = px.bar(region_sales, x="total_amount", y="region", orientation="h",
                     color_discrete_sequence=[TEAL],
                     labels={"total_amount": "Revenue ($)", "region": ""})
        fig.update_layout(plot_bgcolor="white", xaxis_tickprefix="$", margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        type_counts = filtered.groupby("customer_type")["customer_id"].nunique().reset_index()
        type_counts.columns = ["customer_type", "customers"]
        fig2 = px.pie(type_counts, values="customers", names="customer_type",
                      color_discrete_sequence=[TEAL, ORANGE],
                      title="New vs Returning")
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        fig2.update_layout(margin=dict(t=40))
        st.plotly_chart(fig2, use_container_width=True)

elif open_card == "products":
    st.subheader("Top & Bottom Products by Revenue")
    n_show = st.slider("Number of products to show", 5, 20, 10)
    top_n = pd.concat([prod_perf.head(n_show // 2), prod_perf.tail(n_show // 2)]).drop_duplicates()
    top_n = top_n.sort_values("total_amount", ascending=True)
    fig = px.bar(top_n, x="total_amount", y="product_name", color="category",
                 orientation="h", color_discrete_sequence=PALETTE,
                 labels={"total_amount": "Revenue ($)", "product_name": ""})
    fig.update_layout(plot_bgcolor="white", xaxis_tickprefix="$",
                      legend_title="Category", margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

elif open_card == "segmentation":
    st.subheader("Customer Segmentation")
    col1, col2 = st.columns([2, 3])
    with col1:
        color_map = {"High Value": TEAL, "Medium Value": TEAL_LIGHT, "Low Value": ORANGE}
        fig = px.pie(seg_counts, values="customers", names="segment",
                     hole=0.5, color="segment", color_discrete_map=color_map)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(showlegend=True, margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        seg_detail = rfm.groupby("segment").agg(
            Customers=("customer_id","count"),
            Avg_Spend=("monetary","mean"),
            Avg_Orders=("frequency","mean")
        ).round(2).reset_index()
        seg_detail.columns = ["Segment", "Customers", "Avg Spend ($)", "Avg Orders"]
        st.dataframe(seg_detail, use_container_width=True, hide_index=True)

elif open_card == "category":
    st.subheader("Revenue by Category")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(cat_perf, x="category", y="total_amount",
                     color="category", color_discrete_sequence=PALETTE,
                     labels={"total_amount": "Revenue ($)", "category": ""})
        fig.update_layout(plot_bgcolor="white", yaxis_tickprefix="$",
                          showlegend=False, margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.pie(cat_perf, values="total_amount", names="category",
                      color_discrete_sequence=PALETTE, hole=0.4)
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        fig2.update_layout(margin=dict(t=10))
        st.plotly_chart(fig2, use_container_width=True)

elif open_card == "rfm":
    st.subheader("RFM Analysis — Frequency vs Monetary Value")
    fig = px.scatter(rfm, x="frequency", y="monetary", color="segment",
                     size="monetary", hover_data=["customer_id", "recency"],
                     color_discrete_map={"High Value": TEAL, "Medium Value": TEAL_LIGHT, "Low Value": ORANGE},
                     labels={"frequency": "Order Frequency", "monetary": "Total Spend ($)", "segment": "Segment"})
    fig.update_layout(plot_bgcolor="white", yaxis_tickprefix="$", margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Customers by Spend")
    top_custs = (
        rfm.merge(filtered[["customer_id","name","region","customer_type"]].drop_duplicates("customer_id"),
                  on="customer_id")
        .sort_values("monetary", ascending=False)
        .head(10)[["name","region","customer_type","frequency","monetary","segment"]]
        .rename(columns={"name":"Name","region":"Region","customer_type":"Type",
                         "frequency":"Orders","monetary":"Total Spend ($)","segment":"Segment"})
        .reset_index(drop=True)
    )
    top_custs["Total Spend ($)"] = top_custs["Total Spend ($)"].round(2)
    st.dataframe(top_custs, use_container_width=True, hide_index=True)

# ── Business Suggestions ──────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Business Suggestions")

suggestions = [
    ("Launch a High Value Loyalty Program",
     "85 High Value customers drive the majority of revenue. Introduce Gold/Platinum tiers with exclusive perks to increase their purchase frequency by 15–20%."),
    ("Upsell Medium Value Customers",
     "218 Medium Value customers average only 1.91 orders. Personalized cross-sell emails + 'double points on 3rd order' can convert 10%+ to High Value."),
    ("Win-Back Low Value / At-Risk Customers",
     "64 Low Value customers have very low recency. A 20% discount win-back campaign with 30-day expiry could recover 25%+ of this group."),
    ("Boost South Region Performance",
     "South underperforms by ~15% vs other regions. Investigate product-market fit and run region-specific promotions."),
    ("Reduce Dependency on Smart Watch",
     "Smart Watch alone is 22.6% of revenue — a concentration risk. Invest in promoting Running Shoes, Air Purifier, and Coffee Maker."),
    ("Reposition or Retire Underperforming Books",
     "Books generate only 5.7% of revenue. Bundle with Sports products or retire the 2 lowest SKUs and replace with higher-margin items."),
]

for i in range(0, len(suggestions), 2):
    c1, c2 = st.columns(2)
    with c1:
        title, body = suggestions[i]
        st.info(f"**{title}**\n\n{body}")
    if i + 1 < len(suggestions):
        with c2:
            title, body = suggestions[i + 1]
            st.info(f"**{title}**\n\n{body}")

st.markdown(f"""
<hr>

""", unsafe_allow_html=True)
