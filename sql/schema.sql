-- SQLite-compatible schema for a product research tracker.
CREATE TABLE IF NOT EXISTS product_candidates (
    product_id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    category TEXT,
    selling_price REAL NOT NULL CHECK (selling_price >= 0),
    unit_cost REAL NOT NULL CHECK (unit_cost >= 0),
    shipping_cost REAL NOT NULL CHECK (shipping_cost >= 0),
    platform_fee_rate REAL NOT NULL CHECK (platform_fee_rate BETWEEN 0 AND 1),
    estimated_monthly_sales INTEGER NOT NULL DEFAULT 0 CHECK (estimated_monthly_sales >= 0),
    competition_level INTEGER NOT NULL CHECK (competition_level BETWEEN 1 AND 5),
    return_risk INTEGER NOT NULL CHECK (return_risk BETWEEN 1 AND 5),
    shipping_complexity INTEGER NOT NULL CHECK (shipping_complexity BETWEEN 1 AND 5),
    source_url TEXT,
    research_date TEXT
);
