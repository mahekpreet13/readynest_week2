# Power BI Dashboard — Step-by-Step Setup Guide
**ReadyNest Week 2 | Customer Insights Dashboard**

---

## Step 1 — Load the Data

1. Open **Power BI Desktop**
2. Click **Home → Get Data → Text/CSV**
3. Select `data/cleaned_customer_insights.csv`
4. Click **Load** (do NOT use Transform for now)

---

## Step 2 — Verify the Data Model

In the **Data** pane (right side), confirm these columns are present:

| Column | Type |
|---|---|
| customer_id | Text |
| order_id | Text |
| order_date | Date |
| region | Text |
| product_name | Text |
| category | Text |
| quantity | Whole Number |
| total_amount | Decimal Number |
| customer_type | Text |
| segment | Text |
| recency | Whole Number |
| frequency | Whole Number |
| monetary | Decimal Number |

> If `order_date` shows as Text, click the column header → **Change Type → Date**.

---

## Step 3 — Create DAX Measures

Click **Home → New Measure** and create each of the following:

```dax
Total Sales = SUM(cleaned_customer_insights[total_amount])

Total Orders = DISTINCTCOUNT(cleaned_customer_insights[order_id])

Total Customers = DISTINCTCOUNT(cleaned_customer_insights[customer_id])

Avg Order Value = DIVIDE([Total Sales], [Total Orders], 0)

High Value Customers =
CALCULATE(
    DISTINCTCOUNT(cleaned_customer_insights[customer_id]),
    cleaned_customer_insights[segment] = "High Value"
)
```

---

## Step 4 — Build the Dashboard Page

### Page Layout (suggested)
```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Customer Insights Dashboard — ReadyNest            │
├───────────┬───────────┬──────────────┬─────────────────────┤
│  KPI Card │  KPI Card │   KPI Card   │      KPI Card       │
│  Total    │  Total    │   Total      │    Avg Order        │
│ Customers │  Sales    │   Orders     │      Value          │
├───────────┴───────────┼──────────────┴─────────────────────┤
│  Sales by Month       │  Sales by Region (Bar)             │
│  (Line Chart)         │                                    │
├───────────────────────┼────────────────────────────────────┤
│  Top 5 Products       │  Customer Segment (Donut Chart)    │
│  (Horizontal Bar)     │                                    │
└───────────────────────┴────────────────────────────────────┘
│  SLICERS: Region | Date Range | Customer Type | Segment    │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 5 — Add Each Visual

### KPI Cards (×4)
- Insert → **Card** visual
- Card 1: Drag **[Total Customers]** measure to the Value field
- Card 2: Drag **[Total Sales]** → Format as Currency ($)
- Card 3: Drag **[Total Orders]**
- Card 4: Drag **[Avg Order Value]** → Format as Currency ($)

---

### Sales by Month — Line Chart
- Insert → **Line Chart**
- **X-axis:** `order_date` (set to **Month** hierarchy level)
- **Y-axis:** `[Total Sales]`
- **Title:** "Monthly Sales Trend"
- Format: Enable data labels, set line color to `#1a7f74`

---

### Sales by Region — Clustered Bar Chart
- Insert → **Clustered Bar Chart**
- **Y-axis:** `region`
- **X-axis:** `[Total Sales]`
- **Title:** "Revenue by Region"
- Sort bars by value descending (click "..." on visual → Sort)

---

### Top 5 Products — Horizontal Bar Chart
- Insert → **Clustered Bar Chart**
- **Y-axis:** `product_name`
- **X-axis:** `[Total Sales]`
- **Title:** "Top Products by Revenue"
- Apply a **Top N filter:** Visual Filters → `product_name` → Filter type: Top N → Top 5 → By value: [Total Sales]

---

### Customer Segment — Donut Chart
- Insert → **Donut Chart**
- **Legend:** `segment`
- **Values:** `[Total Customers]`
- **Title:** "Customer Segmentation"
- Set slice colors:
  - High Value → `#1a7f74` (teal)
  - Medium Value → `#a8d5d1` (light teal)
  - Low Value → `#e07b54` (orange)

---

## Step 6 — Add Slicers

Insert → **Slicer** for each of the following:

| Slicer | Field | Style |
|---|---|---|
| Region | `region` | Dropdown |
| Date Range | `order_date` | Between (date range picker) |
| Customer Type | `customer_type` | List |
| Segment | `segment` | List |

Arrange slicers in a horizontal row at the bottom of the canvas.

---

## Step 7 — Style the Dashboard

1. **Canvas background:** Format pane → Page background → Color `#f5f9f9`
2. **Header:** Insert → Text Box → "Customer Insights Dashboard" (Font: 20pt, Bold, Color: `#1a7f74`)
3. **All visuals:** Set border radius to 8px, shadow: on, background white
4. **Consistent font:** Segoe UI across all titles and labels

---

## Step 8 — Add a Second Page — Segment Deep Dive (Optional)

1. Right-click page tab → **Duplicate page**
2. Rename: "Segment Analysis"
3. Replace the donut chart with:
   - **Table visual**: customer_id, name, region, frequency, monetary, segment (filtered to High Value)
   - **Bar chart**: Avg Spend by Segment
   - **Scatter chart**: Frequency (X) vs Monetary (Y), colored by Segment

---

## Step 9 — Export to PDF/PPT

- **PDF:** File → Export → Export to PDF
- **PPT:** File → Export → Export to PowerPoint
- Ensure "Include current values of slicers" is checked

---

## DAX Reference — All Measures

```dax
Total Sales         = SUM(cleaned_customer_insights[total_amount])
Total Orders        = DISTINCTCOUNT(cleaned_customer_insights[order_id])
Total Customers     = DISTINCTCOUNT(cleaned_customer_insights[customer_id])
Avg Order Value     = DIVIDE([Total Sales], [Total Orders], 0)
High Value Cust     = CALCULATE(DISTINCTCOUNT(cleaned_customer_insights[customer_id]), cleaned_customer_insights[segment] = "High Value")
Medium Value Cust   = CALCULATE(DISTINCTCOUNT(cleaned_customer_insights[customer_id]), cleaned_customer_insights[segment] = "Medium Value")
Low Value Cust      = CALCULATE(DISTINCTCOUNT(cleaned_customer_insights[customer_id]), cleaned_customer_insights[segment] = "Low Value")
Avg Recency         = AVERAGE(cleaned_customer_insights[recency])
Total Units Sold    = SUM(cleaned_customer_insights[quantity])
```

---

*Data source: `cleaned_customer_insights.csv` (3,000 rows)*
*Generated by: Python (pandas) EDA notebook*
