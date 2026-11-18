"""Transparent unit economics and product opportunity scoring."""

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "product", "category", "selling_price", "unit_cost", "shipping_cost",
    "platform_fee_rate", "estimated_monthly_sales", "competition_level",
    "return_risk", "shipping_complexity",
]


def load_products(frame: pd.DataFrame):
    missing = [col for col in REQUIRED_COLUMNS if col not in frame.columns]
    if missing:
        return pd.DataFrame(), [f"Missing required columns: {', '.join(missing)}"]

    data = frame[REQUIRED_COLUMNS].copy()
    for col in REQUIRED_COLUMNS[2:]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    errors = []
    if data[REQUIRED_COLUMNS[2:]].isna().any().any():
        errors.append("Numeric fields contain blank or non-numeric values.")
    if (data[["selling_price", "unit_cost", "shipping_cost", "estimated_monthly_sales"]] < 0).any().any():
        errors.append("Prices, costs, and estimated sales cannot be negative.")
    if not data["platform_fee_rate"].between(0, 1).all():
        errors.append("platform_fee_rate must be between 0 and 1 (e.g. 0.05 for 5%).")
    for col in ["competition_level", "return_risk", "shipping_complexity"]:
        if not data[col].between(1, 5).all():
            errors.append(f"{col} must be between 1 and 5.")
    if data["product"].fillna("").astype(str).str.strip().eq("").any():
        errors.append("Product names cannot be blank.")
    if errors:
        return pd.DataFrame(), errors
    data["product"] = data["product"].astype(str)
    data["category"] = data["category"].fillna("Uncategorized").astype(str)
    return data, []


def _percentile(series: pd.Series) -> pd.Series:
    if len(series) <= 1:
        return pd.Series([100.0] * len(series), index=series.index)
    return series.rank(pct=True, method="average") * 100


def analyze_products(data: pd.DataFrame) -> pd.DataFrame:
    result = data.copy()
    result["platform_fee_per_unit"] = result["selling_price"] * result["platform_fee_rate"]
    result["contribution_profit"] = (
        result["selling_price"] - result["unit_cost"]
        - result["shipping_cost"] - result["platform_fee_per_unit"]
    )
    result["contribution_margin_pct"] = np.where(
        result["selling_price"] > 0,
        result["contribution_profit"] / result["selling_price"] * 100,
        0,
    )
    invested = result["unit_cost"] + result["shipping_cost"]
    result["unit_roi_pct"] = np.where(
        invested > 0, result["contribution_profit"] / invested * 100, 0
    )

    margin_component = result["contribution_margin_pct"].clip(lower=0, upper=60) / 60 * 100
    demand_component = np.log1p(result["estimated_monthly_sales"])
    demand_component = _percentile(demand_component)
    competition_component = (6 - result["competition_level"]) / 5 * 100
    return_component = (6 - result["return_risk"]) / 5 * 100
    shipping_component = (6 - result["shipping_complexity"]) / 5 * 100

    result["opportunity_score"] = (
        margin_component * 0.30
        + demand_component * 0.25
        + competition_component * 0.20
        + return_component * 0.15
        + shipping_component * 0.10
    ).round(1)
    return result


def build_research_brief(row: dict) -> str:
    return f"""# Product Validation Brief: {row.get('product', '')}

## Current model assumptions
- Category: {row.get('category', '')}
- Selling price: {row.get('selling_price', 0)}
- Unit cost: {row.get('unit_cost', 0)}
- Shipping cost: {row.get('shipping_cost', 0)}
- Platform fee rate: {row.get('platform_fee_rate', 0):.1%}
- Estimated monthly sales: {row.get('estimated_monthly_sales', 0)}
- Contribution profit per unit: {row.get('contribution_profit', 0):.2f}
- Contribution margin: {row.get('contribution_margin_pct', 0):.1f}%
- Opportunity score: {row.get('opportunity_score', 0):.1f}/100

## Before committing capital, validate
1. Demand: collect current keyword/search evidence and review seasonality.
2. Competition: compare at least 5 relevant listings, pricing, reviews, and differentiation.
3. Supplier: verify quotation, MOQ, lead time, quality, and payment terms.
4. Fulfillment: confirm packaging, shipping dimensions, damage risk, and delivery time.
5. Returns: review likely defects, sizing/fit issues, compatibility, and customer expectations.
6. Compliance: check category restrictions, labeling, intellectual property, and platform policies.
7. Economics: add advertising, discounts, taxes, storage, returns, labor, and overhead to the model.
8. Test: define a small, controlled validation plan before scaling.

## Decision
Do not treat the score as a buy recommendation. Record the source, date, and confidence level for every important assumption.
"""
