-- F3 your turn, solved: which customer spent the most, and on how many orders?
-- Run from foundations/f03-spreadsheets-to-sql after loading orders.csv into shop.db.
SELECT customer, COUNT(*) AS orders, SUM(quantity * price_each) AS total_spent
FROM orders
GROUP BY customer
ORDER BY total_spent DESC
LIMIT 1;
