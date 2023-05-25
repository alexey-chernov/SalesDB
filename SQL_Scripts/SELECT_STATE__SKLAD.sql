SELECT 
        "sklad".id AS idProd, 
        "products".nameproduct AS NameProd, 
        "sklad".quantity AS Quantity, 
        "units".nameunitshort AS UnitName, 
        "sklad".price AS Price, 
        ("sklad".quantity * "sklad".price) AS Vartist
FROM 
        public."sklad",
        public."products",
        public."units"
WHERE
        "sklad"."idTov" = "products".id AND
        "sklad".unit = "units".id
ORDER BY nameproduct;