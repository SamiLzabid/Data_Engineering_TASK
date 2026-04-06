CREATE TABLE data_engineering.books_summary AS
SELECT 
    year AS publication_year, 
    COUNT(id) AS book_count,
    ROUND(
        AVG(
            CASE 
                WHEN price LIKE '€%' THEN CAST(REPLACE(price, '€', '') AS DECIMAL(10, 4)) * 1.2
                WHEN price LIKE '$%' THEN CAST(REPLACE(price, '$', '') AS DECIMAL(10, 4))
                ELSE NULL 
            END
        ), 2
    ) AS average_price_USD
FROM data_engineering.books
GROUP BY year
ORDER BY year DESC;
SELECT * FROM data_engineering.books_summary;