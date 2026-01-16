WITH customer_actor_counts AS (
    SELECT r.customer_id, fa.actor_id, COUNT(DISTINCT fa.film_id) AS numrented
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film_actor fa ON i.film_id = fa.film_id
    GROUP BY r.customer_id, fa.actor_id
),
top_actor_per_customer AS (
    SELECT ca.customer_id, MAX(ca.actor_id) AS actor_id, ca.numrented AS numrented
    FROM customer_actor_counts ca
    JOIN (
        SELECT customer_id, MAX(numrented) AS max_rented
        FROM customer_actor_counts
        GROUP BY customer_id
    ) AS m ON ca.customer_id=m.customer_id AND ca.numrented=m.max_rented
    GROUP BY ca.customer_id
)
SELECT
    c.first_name AS customer_fname,
    c.last_name AS customer_lname,
    a.first_name AS actor_fname,
    a.last_name AS actor_lname,
    tapc.numrented
FROM top_actor_per_customer tapc
JOIN customer c ON tapc.customer_id = c.customer_id
JOIN actor a ON tapc.actor_id = a.actor_id
JOIN address adrs ON c.address_id = adrs.address_id
JOIN city ct ON adrs.city_id = ct.city_id
JOIN country ON ct.country_id = country.country_id
WHERE country.country='Argentina'
ORDER BY c.first_name, c.last_name;
