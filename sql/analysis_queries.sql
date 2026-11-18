-- 1. Unit economics by product.
SELECT
    product,
    selling_price,
    unit_cost,
    shipping_cost,
    selling_price * platform_fee_rate AS platform_fee_per_unit,
    selling_price - unit_cost - shipping_cost
        - selling_price * platform_fee_rate AS contribution_profit,
    CASE WHEN selling_price > 0 THEN
        100.0 * (selling_price - unit_cost - shipping_cost
        - selling_price * platform_fee_rate) / selling_price
    ELSE 0 END AS contribution_margin_pct
FROM product_candidates
ORDER BY contribution_profit DESC;

-- 2. Identify products with positive contribution profit and manageable risk.
SELECT product, category, estimated_monthly_sales,
       competition_level, return_risk
FROM product_candidates
WHERE selling_price - unit_cost - shipping_cost
      - selling_price * platform_fee_rate > 0
  AND competition_level <= 3
  AND return_risk <= 3
ORDER BY estimated_monthly_sales DESC;

-- 3. Average price and estimated demand by category.
SELECT category,
       COUNT(*) AS product_count,
       AVG(selling_price) AS average_selling_price,
       AVG(estimated_monthly_sales) AS average_estimated_monthly_sales
FROM product_candidates
GROUP BY category
ORDER BY average_estimated_monthly_sales DESC;
