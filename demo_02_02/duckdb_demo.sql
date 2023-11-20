-- Crea una tabella dai CSV files delle compagnie Nasdaq
CREATE TABLE nasdaq_csv (Date DATE, Low DOUBLE, Open DOUBLE, Volume BIGINT, High DOUBLE, Close DOUBLE, AdjustedClose DOUBLE, filename VARCHAR);
-- Cambia 'path_to_csv' con l'ubicazione dela CSV file in locale
COPY nasdaq_csv FROM 'path_to_csv' (HEADER True, DATEFORMAT '%d-%m-%Y') ;

-- Recupera le prime 500 righe dalla tabella
SELECT * FROM main.nasdaq_csv limit 500 ;

-- Somma tutti i Low
SELECT SUM(Low) FROM main.nasdaq_csv ;

-- Recupera il numero di valori unici per 'filename'
SELECT COUNT(DISTINCT(filename)) FROM main.nasdaq_csv ;

-- Mostra i primi 200 risultti dove i valori medi di Low/High provengono da compagnie il cui 'Volume' è maggiore di 100000
SELECT filename, AVG(Low), AVG(High) FROM main.nasdaq_csv WHERE Volume > 100000 GROUP BY filename LIMIT 200;

--Cancella la tabella
DROP TABLE main.nasdaq_csv ;
