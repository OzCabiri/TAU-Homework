SELECT f.title AS title, a.first_name AS fname, a.last_name AS lname
FROM (
	SELECT f.film_id, f.title
	FROM film f
	WHERE
		EXISTS (
			SELECT i1.film_id
			FROM inventory i1
			JOIN inventory i2 ON i1.film_id = i2.film_id
			JOIN inventory i3 ON i2.film_id = i3.film_id 
			WHERE i1.film_id=f.film_id
				AND i1.inventory_id!=i2.inventory_id
				AND i1.inventory_id!=i3.inventory_id
				AND i2.inventory_id!=i3.inventory_id
		)
		AND
		NOT EXISTS (
			SELECT i1.film_id
			FROM inventory i1
				JOIN inventory i2 ON i1.film_id = i2.film_id
				JOIN inventory i3 ON i2.film_id = i3.film_id 
				JOIN inventory i4 ON i3.film_id = i4.film_id 
			WHERE i1.film_id=f.film_id
				AND i1.inventory_id!=i2.inventory_id
				AND i1.inventory_id!=i3.inventory_id
				AND i1.inventory_id!=i4.inventory_id
				AND i2.inventory_id!=i3.inventory_id
				AND i2.inventory_id!=i4.inventory_id
				AND i3.inventory_id!=i4.inventory_id
		)
) f
LEFT JOIN film_actor fa ON f.film_id=fa.film_id
LEFT JOIN actor a ON fa.actor_id=a.actor_id
WHERE a.actor_id >= ALL(
	SELECT fa2.actor_id
    FROM film_actor fa2
    WHERE f.film_id=fa2.film_id
) OR a.actor_id IS NULL
ORDER BY f.title
LIMIT 20;