-- F3: the same questions you'd answer with a spreadsheet filter, asked in SQL.
-- Load the CSV first:  sqlite3 shop.db ".import --csv orders.csv orders"

-- 1. Show me everything (like opening the sheet)
SELECT * FROM orders;

-- 2. Only the orders from Boston (like a filter)
SELECT order_id, customer, item FROM orders WHERE city = 'Boston';

-- 3. How much did each city spend? (like a pivot table)
SELECT city, SUM(quantity * price_each) AS total_spent
FROM orders
GROUP BY city
ORDER BY total_spent DESC;
