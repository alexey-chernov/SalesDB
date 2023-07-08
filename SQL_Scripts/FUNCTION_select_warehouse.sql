CREATE OR REPLACE FUNCTION public.select_warehouse()
    RETURNS TABLE(idProd numeric, NameProd character varying, Quantity numeric, UnitName character varying, Price numeric, Sum numeric) 
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
SELECT 
        "sklad".id AS idProd, 
        "products".nameproduct AS NameProd, 
        "sklad".quantity AS Quantity, 
        "units".nameunitshort AS UnitName, 
        "sklad".price AS Price, 
        ("sklad".quantity * "sklad".price) AS Sum
FROM 
        public."sklad",
        public."products",
        public."units"
WHERE
        "sklad"."idTov" = "products".id AND
        "sklad".unit = "units".id
ORDER BY nameproduct;
$BODY$;

ALTER FUNCTION public.select_warehouse()
    OWNER TO salesadmin;