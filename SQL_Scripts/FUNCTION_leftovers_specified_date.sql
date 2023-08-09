CREATE OR REPLACE FUNCTION public.report_leftovers_specified_date(
	date date
	)
    RETURNS TABLE(nameproduct character varying, leftovers numeric, unitl character varying) 
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
SELECT
	"products".nameproduct AS "Найменування товару", 
	"invoice".leftovers AS "Залишок", 
	"units".nameunitshort AS "Одиниці"
FROM 
	public."invoice", 
	public."products",
	public."units"
WHERE
	"invoice"."idTov" = "products".id AND
	"invoice"."unit" = "units".id AND
	"invoice"."dateinvoice" = $1
ORDER BY
	"invoice".numdoc, "products".nameproduct;
$BODY$;

ALTER FUNCTION public.report_leftovers_specified_date(date)
    OWNER TO salesadmin;