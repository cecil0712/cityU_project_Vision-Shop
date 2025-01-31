SELECT product.name 
FROM supermarket, product 
WHERE supermarket.productid = product.id
AND product.discount IS NOT NULL
AND supermarket.regionid = (
    SELECT region.id 
    FROM region, supermarket 
    WHERE region.id = supermarket.regionid 
    AND supermarket.productid = (
        SELECT id 
        FROM product 
        WHERE name = ?
    )
)