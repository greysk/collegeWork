--List the names of all people who stared in a movie
-- in which Kevin Bacon (born in 1958) also starred.
-- Does not include Kevin Bacon in list.
SELECT
    DISTINCT people.name
FROM
    stars
INNER JOIN
    people
ON
    stars.person_id=people.id
WHERE
    stars.movie_id
    IN (SELECT movies.id FROM movies
        INNER JOIN stars ON stars.movie_id=movies.id
        INNER JOIN people ON stars.person_id=people.id
        WHERE people.name="Kevin Bacon" AND people.birth=1958)
AND
    people.name IS NOT "Kevin Bacon"
ORDER BY
    people.name;
