SELECT region.name, row_num, col_num 
FROM region, supermarket 
WHERE region.id = regionid