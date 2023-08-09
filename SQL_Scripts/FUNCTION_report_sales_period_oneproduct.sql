-- FUNCTION: public.report_report_sales_period_oneproduct(date, date, integer);

-- DROP FUNCTION IF EXISTS public.report_report_sales_period_oneproduct(date, date, integer);

CREATE OR REPLACE FUNCTION public.report_sales_period_oneproduct(
	date1 date,
	date2 date,
	ProductCode integer)
    RETURNS TABLE(dateinvoice character, nameproduct character varying, quantity numeric, unitq character varying, price numeric, sum numeric) 
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
SELECT
	to_char("invoice".dateinvoice, 'dd/mm/yyyy') AS "Дата продажу",
	"products".nameproduct AS "Найменування товару", 
	"invoice".quantity AS "Кількість",
	"units".nameunitshort AS "Одиниці",
	"invoice".price AS "Ціна",
	"invoice".sum AS "Сума"
FROM 
	public."invoice", 
	public."products",
	public."units"
WHERE
	"invoice"."idTov" = "products".id AND
	"invoice"."unit" = "units".id AND
	"invoice"."idType" = 2 AND
	"invoice"."idTov" = $3 AND
	"invoice"."dateinvoice" BETWEEN $1 AND $2
UNION ALL
SELECT
	NULL,NULL, NULL,NULL, NULL,
	sum(sum) As "Загальна суиа"
FROM 
	public."invoice"
WHERE
	"invoice"."idType" = 2 AND
	"invoice"."idTov" = $3 AND
	"invoice"."dateinvoice" BETWEEN $1 AND $2
ORDER BY
	"Дата продажу", 
	"Найменування товару";
$BODY$;

ALTER FUNCTION public.report_sales_period_oneproduct(date, date, integer)
    OWNER TO salesadmin;