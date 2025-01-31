SELECT row_num, col_num
FROM supermarket
WHERE productid = (
    SELECT id
    FROM product 
    WHERE name = ?
)