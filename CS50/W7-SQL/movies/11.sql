--List the titles of the 5 highest rated movies (in order) that
-- Chadwick Boseman stared in, starting with highest rated.
SELECT
    title
FROM
    movies
INNER JOIN
    ratings
ON
    ratings.movie_id=movies.id
INNER JOIN
    stars
ON
    stars.movie_id=movies.id
INNER JOIN
    people
ON
    people.id=stars.person_id
WHERE
    people.name="Chadwick Boseman"
ORDER BY
    ratings.rating DESC
LIMIT 5;