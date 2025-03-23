--List the names of all people who stared in a movie
-- released in 2004, ordered by birth year.
SELECT
    name
FROM
    people
WHERE
    id IN (
    SELECT stars.person_id
    FROM movies INNER JOIN stars ON movies.id=stars.movie_id
    WHERE movies.year=2004)
ORDER BY people.birth;