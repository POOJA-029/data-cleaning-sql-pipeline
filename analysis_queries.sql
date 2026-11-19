-- Business Analysis Queries
-- Run against orders.db after executing clean_pipeline.py.

-- (a) Monthly revenue totals
SELECT
    order_month,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM orders
WHERE order_month IS NOT NULL
GROUP BY order_month
ORDER BY order_month;

-- (b) Top-performing service categories
-- Ranked by total revenue; records without a category are excluded.
SELECT
    service_category,
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM orders
WHERE service_category IS NOT NULL
GROUP BY service_category
ORDER BY total_revenue DESC;

-- (c) Incomplete / flagged records
-- Includes records with missing key fields or an invalid/missing date/price.
SELECT
    order_id,
    customer_id,
    order_date,
    service_category,
    quantity,
    unit_price,
    is_flagged,
    quality_issue
FROM orders
WHERE is_flagged = 1
ORDER BY order_id;
