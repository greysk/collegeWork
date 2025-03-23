--List titles of all movies in which both Johnny Depp
-- and Helena Bonham Carter starred.
SELECT
    title
FROM
    movies
LEFT JOIN
    stars
ON
    stars.movie_id=movies.id
LEFT JOIN
    people
ON
    people.id=stars.person_id
WHERE
    stars.person_id=(SELECT id FROM people WHERE name="Johnny Depp")
INTERSECT
SELECT
    title
FROM
    movies
LEFT JOIN
    stars
ON
    stars.movie_id=movies.id
LEFT JOIN
    people
ON
    people.id=stars.person_id
WHERE
    stars.person_id=(SELECT id FROM people WHERE name="Helena Bonham Carter");