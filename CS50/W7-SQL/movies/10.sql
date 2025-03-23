--List names of all people who have directed a movie
-- that received a rating of at least 9.0
SELECT
    name
FROM
    people
WHERE
    id IN (
SELECT
    DISTINCT directors.person_id
FROM
    directors
INNER JOIN
    ratings
ON directors.movie_id=ratings.movie_id
WHERE ratings.rating>=9.0
ORDER BY person_id);