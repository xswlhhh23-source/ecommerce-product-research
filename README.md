# E-commerce Product Research & Unit Economics Analyzer

A practical product-research workspace for comparing candidate products, estimating unit economics, reviewing competition and return risk, and documenting a transparent shortlist.

> **MVP 1.0** — manual/CSV analysis using user-supplied research assumptions. The sample dataset is synthetic. This tool does not scrape marketplaces or claim to provide live sales, keyword, or competitor data.

## Features

- Import product research from CSV or use the fictional sample dataset.
- Calculate platform fee, estimated contribution profit per unit, contribution margin, and unit-level ROI.
- Score products using a documented weighted framework.
- Compare estimated demand, competition intensity, shipping complexity, and return risk.
- Rank candidate products and export the analysis as CSV.
- Generate a research checklist and product validation brief.

## Run locally

```bash
git clone https://github.com/xswlhhh23-source/ecommerce-product-research.git
cd ecommerce-product-research
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## CSV fields

Required: `product, category, selling_price, unit_cost, shipping_cost, platform_fee_rate, estimated_monthly_sales, competition_level, return_risk, shipping_complexity`.

- `platform_fee_rate`: decimal rate, e.g. 0.05 for 5%.
- `competition_level`: 1 (low) to 5 (very high).
- `return_risk`: 1 (low) to 5 (very high).
- `shipping_complexity`: 1 (simple) to 5 (complex).

A synthetic example dataset is in `data/sample_products.csv`. It is for demonstration only, not market evidence.

## Unit economics

- Platform fee per unit = selling price × platform fee rate.
- Contribution profit per unit = selling price − unit cost − shipping cost − platform fee.
- Contribution margin = contribution profit / selling price × 100.
- Unit ROI = contribution profit / (unit cost + shipping cost) × 100.

These estimates exclude taxes, advertising, discounts, refunds, storage, labor, overhead, and other costs unless you add them to the model. They are not a forecast or a guarantee of profitability.

## Product opportunity score

The MVP uses a 0–100 weighted score:
- Contribution margin: 30%
- Estimated monthly demand (log-scaled): 25%
- Lower competition: 20%
- Lower return risk: 15%
- Simpler shipping: 10%

The score is a prioritization framework, not a recommendation to purchase inventory. Validate demand and costs with current primary research.

## Project structure

```text
├── app.py
├── src/scoring.py
├── data/sample_products.csv
├── sql/schema.sql
├── sql/analysis_queries.sql
├── docs/methodology.md
├── tests/test_scoring.py
└── requirements.txt
```

## Responsible use

- Verify supplier quotes, shipping costs, platform fees, and competitor prices before making a decision.
- Treat estimated sales as assumptions unless supported by reliable source data.
- Do not use the score as a substitute for customer research, compliance checks, or financial due diligence.
- Sample products and metrics are synthetic.

## Author

Personal portfolio project by **Xudong Sun**. Demonstrates e-commerce operations thinking, product research, Excel/SQL-style analysis, unit economics, and data-informed decision support.
