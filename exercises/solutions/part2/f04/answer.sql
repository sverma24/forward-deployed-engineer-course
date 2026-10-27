-- F4 your turn, solved.
-- 1. Orders worth more than $20, with the customer's name (the orphan order 1006 can't have a name)
SELECT o.order_id, c.name, o.item, o.quantity * o.price_each AS order_value
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
WHERE o.quantity * o.price_each > 20;

-- 2. Orders per customer, counting the duplicated order only once
SELECT c.name, COUNT(DISTINCT o.order_id) AS orders
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.name
ORDER BY orders DESC;
