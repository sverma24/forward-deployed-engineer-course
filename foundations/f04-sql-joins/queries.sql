-- F4: everyday SQL for messy client data.
-- Load:  sqlite3 shop.db ".import --csv customers.csv customers" ".import --csv orders.csv orders"

-- 1. JOIN: put each order next to the customer who placed it
SELECT o.order_id, c.name, c.city, o.item
FROM orders o JOIN customers c ON c.customer_id = o.customer_id;

-- 2. LEFT JOIN: find orders whose customer doesn't exist (an "orphan")
SELECT o.order_id, o.customer_id
FROM orders o LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;

-- 3. Find the same order entered twice
SELECT order_id, COUNT(*) AS times
FROM orders GROUP BY order_id HAVING COUNT(*) > 1;

-- 4. Find customers with no city
SELECT customer_id, name FROM customers WHERE city IS NULL OR city = '';
