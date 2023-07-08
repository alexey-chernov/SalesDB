CREATE OR REPLACE FUNCTION public.report_leftovers_specified_date(
	date date
	)
    RETURNS TABLE(nametype character varying, numdoc character varying, nameproduct character varying, quantity numeric, unitq character varying, leftovers numeric, unitl character varying) 
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
SELECT
	"types".nametype,
	"invoice".numdoc,
	"products".nameproduct, 
	"invoice".quantity,
	"units".nameunitshort,
	"invoice".leftovers, 
	"units".nameunitshort
FROM 
	public."invoice", 
	public."products",
	public."types",
	public."units"
WHERE
	"invoice"."idTov" = "products".id AND
	"invoice"."unit" = "units".id AND
	"invoice"."idType" = "types".id AND
	"invoice"."dateinvoice" = $1
ORDER BY
	"invoice".numdoc, "products".nameproduct;
$BODY$;

ALTER FUNCTION public.report_leftovers_specified_date(date)
    OWNER TO salesadmin;