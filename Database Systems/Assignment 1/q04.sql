SELECT
	c.name AS category,
    AVG(DATEDIFF(r.return_date,r.rental_date)) AS avg_rental_duration,
    COUNT(DISTINCT fc.film_id) AS film_count,
    COUNT(DISTINCT r.customer_id) AS num_customers
FROM category c
	JOIN film_category fc ON c.category_id=fc.category_id
    LEFT JOIN inventory i ON fc.film_id=i.film_id
    LEFT JOIN rental r ON i.inventory_id=r.inventory_id
GROUP BY c.name, fc.category_id
HAVING film_count>=65 AND num_customers>=400 AND avg_rental_duration>3
ORDER BY film_count DESC;