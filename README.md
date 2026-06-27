# Customer Insights Dashboard

This project is a Streamlit-based dashboard for exploring customer, sales, and product insights from a synthetic retail dataset.

## What this app does

The dashboard helps users:
- view overall customer and sales performance
- filter data by region, segment, customer type, and date range
- explore sales trends and product performance
- understand customer segmentation through RFM-style insights
- review business recommendations from the included report

## Project structure

- app.py - main Streamlit dashboard
- data/ - cleaned and generated datasets
- notebooks/ - EDA notebooks
- powerbi/ - Power BI dashboard guide
- reports/ - business insights report
- images.webp, image-vi-s_202602.webp - dashboard visuals

## Requirements

Install the Python dependencies before running the app:

```bash
pip install streamlit pandas numpy plotly
```

## Run the dashboard

From the project folder, run:

```bash
python3 -m streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Data

The dashboard uses the cleaned dataset in:

- data/cleaned_customer_insights.csv

## Notes

- The app is designed for interactive exploration with sidebar filters.
- A written business insights report is available in the reports folder.
- The project also includes notebook-based exploratory analysis and a Power BI guide.
