SELECT row_num, col_num
FROM supermarket
WHERE regionid = (
    SELECT id
    FROM region
    WHERE name = ?
)