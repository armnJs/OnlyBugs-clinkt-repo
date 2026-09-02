# Team — Clinkt Investigation

## Summary

Clinkt is hemorrhaging revenue through a **triple failure**: a broken recommendation engine that shows customers irrelevant products, chronic inventory mismanagement that leaves high-demand items out of stock, and a customer journey so fractured that **70.5% of cart additions are abandoned**. The company is losing **₹84,857 in potential revenue** — **1.75× its actual earned revenue of ₹48,412** — because customers arrive, can't find what they need, add items that turn out to be unavailable, and leave. We recommend an immediate overhaul of inventory prioritization using demand-signal scoring, a category-aware recommendation engine, and segment-specific retention strategies starting with the high-value Family segment.

## Key Findings

| Finding | Evidence | Business Impact |
|---------|----------|-----------------|
| **70.5% cart abandonment rate** | 666 of 945 cart additions never ordered | ₹84,857 lost revenue |
| **60.7% stock days sub-optimal** | Only 439 of 1,116 product-days at healthy stock | Supply-demand mismatch |
| **Family segment worst affected** | 79.5% abandonment despite highest AOV (₹192) | Losing best customers |
| **Recommendation gap: 6.5% for Home Care** | 15.5% views but 9.0% orders | Wasted product discovery |
| **Orders declining (-0.212 trend)** | Negative correlation over 31 days | Growth stalling |
| **View-only sessions: 1.4 min avg** | 264 sessions bounce with zero engagement | Broken first impression |

## How to View Our Work

### Report / Dashboard
- **Findings Report (PDF)**: [`findings_report.pdf`](findings_report.pdf) — Complete 7-page presentation report with linked evidence chains, ruled-out hypotheses, and quantified business impact.
- **Findings Report (HTML)**: [`findings_report.html`](findings_report.html) — Interactive / Printable HTML report.
- **Interactive Investigation Dashboard**: [`dashboard.html`](dashboard.html) — Live interactive Chart.js analytics dashboard.
- **Storefront Prototype UI**: [`clinkt-ui.html`](clinkt-ui.html) — Customer-facing e-commerce storefront prototype.

### Code
- **Full Investigation Script**: [`cleaned data/full_investigation.py`](cleaned%20data/full_investigation.py) — runs all 5 investigations
- **Data Export Script**: [`cleaned data/export_data.py`](cleaned%20data/export_data.py) — generates 12 Excel files
- **Analysis Scripts**: [`cleaned data/`](cleaned%20data/) — individual analysis notebooks (10 scripts)

### Data Outputs
- **Cleaned Datasets**: [`cleaned data/exports/`](cleaned%20data/exports/) — 12 Excel files covering funnel, inventory, segments, cities, products
- **Chart Data**: [`cleaned data/charts/`](cleaned%20data/charts/) — JSON data powering the dashboard

### How to Run
```bash
# Requires Python 3.6+ with pandas, numpy
pip install pandas numpy openpyxl

# Run the full investigation
python "cleaned data/full_investigation.py"

# Generate Excel exports
python "cleaned data/export_data.py"
```

## Team
[Your Names Here]
