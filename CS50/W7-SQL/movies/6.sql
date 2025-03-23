--Determine average rating of all movies
-- released in 2012.
SELECT
    avg(rating)
FROM
    ratings
INNER JOIN
    movies
ON
    movies.id=ratings.movie_id
WHERE
    movies.year=2012;