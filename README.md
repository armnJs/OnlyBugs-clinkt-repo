# Team OnlyBugs — Clinkt Investigation

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

### Report / Dashboard & Solution Engine
- **Findings Report (PDF)**: [`findings_report.pdf`](findings_report.pdf) — Complete 7-page executive report with linked evidence chains, ruled-out hypotheses, and financial recovery models.
- **Interactive Investigation Dashboard & Solution Simulator**: [`dashboard.html`](dashboard.html) — Live interactive Chart.js analytics dashboard with real-time **Revenue Recovery Simulator**, Dynamic Replenishment Table, and Recommendation Re-Weighting Matrix.
- **Storefront Prototype UI**: [`clinkt-ui.html`](clinkt-ui.html) — Customer-facing e-commerce storefront prototype.

### Code & Solution Engine
- **Solution Engine & Optimization Model**: [`cleaned data/solution_engine.py`](cleaned%20data/solution_engine.py) — calculates dynamic reorder points (ROP), safety stocks, and category recommendation weights.
- **Full Investigation Script**: [`cleaned data/full_investigation.py`](cleaned%20data/full_investigation.py) — executes all 5 root-cause investigations.
- **Data Export Script**: [`cleaned data/export_data.py`](cleaned%20data/export_data.py) — generates cleaned analytical datasets.
- **Analysis Scripts**: [`cleaned data/`](cleaned%20data/) — individual analysis notebooks.

### Data Outputs & Solution Plans
- **Cleaned Datasets & Solution Schedules**: [`cleaned data/exports/`](cleaned%20data/exports/) — 14 Excel files including:
  - `13_optimized_replenishment_plan.xlsx` (Dynamic safety stocks & reorder points for all 36 SKUs)
  - `14_recommendation_reweighting_model.xlsx` (Corrected category visibility weights)
  - Full funnel, segment, inventory, and city analytical exports.
- **Chart & Simulation Data**: [`cleaned data/charts/`](cleaned%20data/charts/) — JSON data powering the live dashboard and simulator.

### How to Run
```bash
# Requires Python 3.6+ with pandas, numpy, openpyxl
pip install pandas numpy openpyxl

# Run the full investigation pipeline
python "cleaned data/full_investigation.py"

# Run the solution engine & generate optimization models
python "cleaned data/solution_engine.py"

# Generate analytical Excel exports
python "cleaned data/export_data.py"
```

## Team
Team OnlyBugs
