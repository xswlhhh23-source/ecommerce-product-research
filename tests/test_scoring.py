import unittest
import pandas as pd

from src.scoring import load_products, analyze_products


class ProductScoringTests(unittest.TestCase):
    def sample(self):
        return pd.DataFrame([{
            "product": "Demo", "category": "Home",
            "selling_price": 100, "unit_cost": 40, "shipping_cost": 10,
            "platform_fee_rate": 0.05, "estimated_monthly_sales": 500,
            "competition_level": 3, "return_risk": 2, "shipping_complexity": 1,
        }])

    def test_unit_economics(self):
        data, errors = load_products(self.sample())
        self.assertFalse(errors)
        result = analyze_products(data).iloc[0]
        self.assertAlmostEqual(result["platform_fee_per_unit"], 5)
        self.assertAlmostEqual(result["contribution_profit"], 45)
        self.assertAlmostEqual(result["contribution_margin_pct"], 45)

    def test_invalid_fee_rate_is_rejected(self):
        frame = self.sample()
        frame.loc[0, "platform_fee_rate"] = 1.2
        data, errors = load_products(frame)
        self.assertTrue(errors)
        self.assertTrue(data.empty)

    def test_score_is_bounded(self):
        data, errors = load_products(self.sample())
        result = analyze_products(data)
        self.assertTrue(result["opportunity_score"].between(0, 100).all())


if __name__ == "__main__":
    unittest.main()
