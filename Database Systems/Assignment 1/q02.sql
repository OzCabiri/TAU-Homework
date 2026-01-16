WITH counts AS (
    SELECT a.actor_id, a.first_name, a.last_name, COUNT(DISTINCT fa.film_id) AS film_count
    FROM actor a
    JOIN film_actor fa ON a.actor_id = fa.actor_id
    GROUP BY a.actor_id, a.first_name, a.last_name
),
avg_count AS (
    SELECT AVG(film_count) AS avg_film_count
    FROM counts
)
SELECT counts.first_name AS fname, counts.last_name AS lname, counts.film_count
FROM counts
CROSS JOIN avg_count
WHERE counts.film_count < avg_count.avg_film_count
ORDER BY counts.film_count DESC
LIMIT 20;
