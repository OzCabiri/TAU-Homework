SELECT c.name AS category, MAX(counts.film_count) AS max_films
FROM (SELECT  i.store_id, fc.category_id, COUNT(DISTINCT fc.film_id) AS film_count
	FROM film_category fc
	JOIN inventory i ON i.film_id = fc.film_id
	GROUP BY i.store_id, fc.category_id
	) AS counts
JOIN category c ON counts.category_id=c.category_id
GROUP BY c.name, c.category_id
HAVING MIN(counts.film_count)>50
ORDER BY max_films DESC;