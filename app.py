import pandas as pd
import streamlit as st

from src.scoring import REQUIRED_COLUMNS, analyze_products, load_products, build_research_brief

st.set_page_config(page_title="E-commerce Product Research", page_icon="🛒", layout="wide")
st.title("🛒 E-commerce Product Research & Unit Economics")
st.caption("Compare product ideas using transparent assumptions, unit economics, and a structured opportunity score.")
st.info("This MVP uses manually entered or imported research assumptions. It does not fetch live marketplace sales, prices, or competitor data.")

uploaded = st.file_uploader("Upload product research CSV", type=["csv"])
try:
    raw = pd.read_csv(uploaded) if uploaded is not None else pd.read_csv("data/sample_products.csv")
    data, errors = load_products(raw)
except Exception as exc:
    st.error(f"Could not read the CSV: {exc}")
    st.stop()

if errors:
    st.error("Data validation issues: " + "; ".join(errors))
    st.stop()

results = analyze_products(data)
if results.empty:
    st.warning("No products available.")
    st.stop()

st.sidebar.header("Shortlist filters")
min_margin = st.sidebar.slider("Minimum contribution margin (%)", 0, 80, 10)
max_competition = st.sidebar.slider("Maximum competition level", 1, 5, 5)
shortlist = results[
    (results["contribution_margin_pct"] >= min_margin)
    & (results["competition_level"] <= max_competition)
].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Products reviewed", len(results))
c2.metric("Shortlisted", len(shortlist))
c3.metric("Average contribution margin", f"{results['contribution_margin_pct'].mean():.1f}%")
c4.metric("Best opportunity score", f"{results['opportunity_score'].max():.1f}/100")

st.subheader("Product comparison")
cols = [
    "product", "category", "selling_price", "unit_cost", "shipping_cost",
    "platform_fee_per_unit", "contribution_profit", "contribution_margin_pct",
    "unit_roi_pct", "estimated_monthly_sales", "competition_level",
    "return_risk", "shipping_complexity", "opportunity_score",
]
st.dataframe(shortlist.sort_values("opportunity_score", ascending=False)[cols], use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Opportunity score")
    st.bar_chart(shortlist.set_index("product")["opportunity_score"])
with right:
    st.subheader("Contribution margin")
    st.bar_chart(shortlist.set_index("product")["contribution_margin_pct"])

st.subheader("Shortlist interpretation")
if shortlist.empty:
    st.warning("No products meet the current filters. Review the assumptions or adjust the filters.")
else:
    best = shortlist.sort_values("opportunity_score", ascending=False).iloc[0]
    st.write(
        f"**Top item under the current assumptions: {best['product']}** "
        f"with an opportunity score of {best['opportunity_score']:.1f}/100 and "
        f"estimated contribution margin of {best['contribution_margin_pct']:.1f}%."
    )
    st.caption("This is a model-based shortlist, not a buy recommendation. Verify supplier, demand, compliance, and fulfillment assumptions.")

selected_product = st.selectbox("Generate a validation brief", results["product"].tolist())
selected = results[results["product"] == selected_product].iloc[0].to_dict()
brief = build_research_brief(selected)
st.text_area("Product validation checklist", brief, height=260)
st.download_button("Download analysis (.csv)", results.to_csv(index=False), file_name="product-research-analysis.csv", mime="text/csv")
st.download_button("Download validation brief (.md)", brief, file_name="product-validation-brief.md", mime="text/markdown")
st.caption("MVP 1.0 · Synthetic sample data · Transparent assumptions · Not financial advice")
