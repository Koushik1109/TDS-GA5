WITH parsed_sales AS (
    -- Safely parse all three date formats without errors using CASE and LIKE
    SELECT 
        amount,
        CASE 
            WHEN sale_date LIKE '%-%-%' THEN strptime(sale_date, '%Y-%m-%d')
            WHEN sale_date LIKE '%/%/%' THEN strptime(sale_date, '%d/%m/%Y')
            ELSE strptime(sale_date, '%B %d, %Y')
        END AS valid_date
    FROM sales
),
monthly_revenue AS (
    -- Aggregate total revenue per calendar month
    SELECT 
        strftime(valid_date, '%Y-%m') AS month,
        SUM(amount) AS total_revenue
    FROM parsed_sales
    WHERE valid_date IS NOT NULL
    GROUP BY strftime(valid_date, '%Y-%m')
),
mom_growth AS (
    -- Calculate previous month's revenue using LAG()
    SELECT 
        month,
        total_revenue,
        LAG(total_revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly_revenue
)
-- Compute MoM growth rate, filter for 2024, order, and limit
SELECT 
    month,
    ROUND(((total_revenue - prev_revenue) / prev_revenue) * 100, 2) AS mom_growth_pct
FROM mom_growth
WHERE month LIKE '2024-%'
ORDER BY mom_growth_pct DESC NULLS LAST
LIMIT 1;
