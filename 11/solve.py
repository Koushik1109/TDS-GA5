import sqlite3

def solve():
    with open('q-datasette-sales-summary.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    conn = sqlite3.connect(':memory:')
    conn.executescript(sql)
    
    query = """
    SELECT city, SUM(quantity * unit_price) AS total_revenue
    FROM orders
    WHERE status = 'delivered'
    GROUP BY city
    ORDER BY total_revenue DESC
    LIMIT 1;
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    print(f"Top city: {result[0]}, Revenue: {result[1]}")

if __name__ == '__main__':
    solve()
