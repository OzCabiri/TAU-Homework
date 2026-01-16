WITH actor_category_count AS (
	SELECT a.actor_id, a.first_name AS fname, a.last_name AS lname, COUNT(DISTINCT fc.category_id) AS num_categories
	FROM actor a
	JOIN film_actor fa   ON a.actor_id = fa.actor_id
	JOIN film_category fc ON fa.film_id = fc.film_id
	GROUP BY a.actor_id, a.first_name, a.last_name
)
SELECT acc.fname, acc.lname, acc.num_categories
FROM actor_category_count acc
JOIN (
	SELECT MIN(num_categories) AS min_cat, MAX(num_categories) AS max_cat
    FROM actor_category_count
) AS minmax
ON acc.num_categories = minmax.min_cat OR acc.num_categories = minmax.max_cat
ORDER BY acc.fname, acc.lname;