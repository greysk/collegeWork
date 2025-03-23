--List all movies released in 2010 and their ratings in
-- decending order by rating and then alphabetically
-- by movie title.
SELECT
    title,
    rating
FROM
    ratings
INNER JOIN
    movies
ON
    movies.id=ratings.movie_id
WHERE
    movies.year=2010
ORDER BY
    rating DESC,
    title ASC;