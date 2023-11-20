-- Parte 1

SELECT
	*
FROM
	media_types mt ;

SELECT
	Name
FROM
	media_types mt ;

SELECT
	Upper(Name) as Name_Upper
FROM
	media_types mt ;
-- Parte 2

SELECT
	TrackId ,
	Name ,
	Composer,
	Milliseconds ,
	Bytes ,
	UnitPrice
FROM
	tracks t
ORDER BY
	Name ASC;

SELECT
	TrackId ,
	Name ,
	Composer,
	Milliseconds ,
	Bytes ,
	UnitPrice
FROM
	tracks t
ORDER BY
	Name DESC;

SELECT
	TrackId ,
	Name ,
	Composer,
	Milliseconds ,
	Bytes ,
	UnitPrice
FROM
	tracks t
ORDER BY
	Name ASC,
	Composer DESC;

SELECT
	TrackId ,
	Name ,
	Composer,
	Milliseconds ,
	Bytes ,
	UnitPrice
FROM
	tracks t
ORDER BY
	Name,
	Composer ASC;

SELECT
	TrackId ,
	Name ,
	Composer,
	Milliseconds ,
	Bytes ,
	UnitPrice
FROM
	tracks t
ORDER BY
	1 ASC;
-- Parte 3

SELECT
	CustomerId ,
	FirstName ,
	LastName ,
	Company ,
	City ,
	Country ,
	Email
from
	customers c ;

SELECT
	DISTINCT (FirstName) as Unique_Names
from
	customers c ;

SELECT
	CustomerId ,
	FirstName ,
	LastName ,
	Company ,
	City ,
	Country ,
	Email
from
	customers c
LIMIT 20;

SELECT
	CustomerId ,
	FirstName ,
	LastName ,
	Company ,
	City ,
	Country ,
	Email
from
	customers c
WHERE
	Country = 'Germany';

SELECT
	CustomerId ,
	FirstName ,
	LastName ,
	Company ,
	City ,
	Country ,
	Email
from
	customers c
WHERE
	LENGTH (Country) > 8;

SELECT
	FirstName ,
	LastName,
	City ,
	Country ,
	Email
from
	customers c
WHERE
	City IN ('Berlin', 'Rome');

SELECT
	FirstName ,
	LastName,
	City ,
	Country ,
	Email
from
	customers c
WHERE
	City NOT IN ('Berlin', 'Rome');

SELECT
	FirstName ,
	LastName,
	City ,
	Country ,
	Email
from
	customers c
WHERE
	City LIKE 'San%';

SELECT
	FirstName ,
	LastName,
	City ,
	Country ,
	Email
from
	customers c
WHERE
	LENGTH (FirstName) > 5
	AND City IN ('Berlin', 'Rome');

SELECT
	FirstName ,
	LastName,
	City ,
	Country ,
	Email
from
	customers c
WHERE
	LENGTH (FirstName) > 5
	OR City IN ('Berlin', 'Rome');

SELECT
	FirstName,
	LastName
FROM
	customers c
WHERE
	LENGTH (LastName) BETWEEN 6 AND 8;

SELECT
	FirstName,
	LastName
FROM
	customers c
WHERE
	City IS NULL;
-- Parte 4

SELECT
	TrackId,
	Name ,
	CASE
		GenreId WHEN 1 THEN 'HipHop'
		WHEN 2 THEN 'Metal'
		WHEN 3 THEN 'Classic'
	END AS Genre
FROM
	tracks t
where
	GenreId IN (1, 2, 3) ;
-- Parte 5

SELECT
	t.Name as Track_Name,
	g.Name as Genre_Name,
	t.Milliseconds as Track_Length
FROM
	tracks t
INNER JOIN genres g ON
	t.GenreId = g.GenreId;

CREATE TABLE alternative_genres AS
SELECT
	*
FROM
	genres g;

INSERT
	INTO
	alternative_genres
VALUES (26,
'Post Norwegian Black Ambient Metal');

SELECT
	*
FROM
	tracks t
RIGHT OUTER JOIN alternative_genres ag ON
	t.GenreId = ag.GenreId
WHERE
	t.TrackId IS NULL;

DROP TABLE alternative_genres ;

SELECT
	t.Composer as Composer_Name,
	g.Name as Genre_Name
FROM
	tracks t
CROSS JOIN genres g
WHERE
	g.GenreId IN (1, 2)
	AND t.Composer IS NOT NULL
ORDER BY
	1;

SELECT
	e1.FirstName || ' ' || e1.LastName as employee,
	e2.FirstName || ' ' || e2.LastName as manager
FROM
	employees e1
INNER JOIN employees e2 ON
	e1.EmployeeId = e2.ReportsTo ;
-- Parte 6

SELECT
	AVG(t.Milliseconds) as avg_len,
	MAX(t.Milliseconds) as max_len,
	MIN(t.Milliseconds) as min_len
from
	tracks t;

SELECT
	COUNT(DISTINCT(FirstName || LastName)) as Unique_Names_Count
FROM
	employees e ;
-- Parte 7

SELECT
	GenreId ,
	ROUND(AVG((Milliseconds / 1000)/ 60), 2) as avg_len_in_minutes
from
	tracks
GROUP BY
	GenreId ;

SELECT
	GenreId ,
	ROUND(AVG((Milliseconds / 1000)/ 60), 2) as avg_len_in_minutes
from
	tracks
GROUP BY
	GenreId
HAVING
	GenreId in (2, 3);
-- Parte 8

SELECT
	*
FROM
	media_types mt
UNION ALL
select
	*
FROM
	media_types mt2 ;

SELECT
	*
FROM
	media_types mt
UNION
select
	*
FROM
	media_types mt2 ;

CREATE TABLE alternative_media_types AS
SELECT
	*
FROM
	media_types mt
WHERE
	mt.MediaTypeId in (1, 2, 3);

SELECT
	*
from
	media_types mt
INTERSECT
SELECT
	*
FROM
	alternative_media_types;

DROP TABLE alternative_media_types ;
-- Parte 9

CREATE TABLE alternative_genres AS
SELECT
	*
FROM
	genres g;

UPDATE
	alternative_genres
SET
	Name = 'Classic Rock'
where
	GenreId = 1;

SELECT
	*
FROM
	alternative_genres g
WHERE
	GenreId = 1 ;

DELETE
FROM
	alternative_genres
WHERE
	GenreId = 1;

SELECT
	*
FROM
	alternative_genres g
WHERE
	GenreId = 1 ;

INSERT
	INTO
	alternative_genres
VALUES (1,
'Rock');

SELECT
	*
FROM
	alternative_genres g
WHERE
	GenreId = 1 ;

DROP TABLE alternative_genres ;
-- Parte 10

CREATE TABLE alternative_genres AS
SELECT
	*
FROM
	genres g;

ALTER TABLE alternative_genres ADD FakeColumn INT DEFAULT 1;

SELECT
	*
FROM
	alternative_genres g;

ALTER TABLE alternative_genres DROP FakeColumn;

SELECT
	*
FROM
	alternative_genres g;

DROP TABLE alternative_genres ;

ALTER TABLE alternative_genres DROP FakeColumn;

SELECT
	*
FROM
	alternative_genres g;
