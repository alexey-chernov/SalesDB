CREATE OR REPLACE FUNCTION public.select_invoices()
    RETURNS TABLE(dateinvoice date, nametype character varying, numdoc character varying, counttov numeric, totalsum numeric, namestatus character varying) 
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
SELECT
	invoice.dateinvoice AS dateinvoice,
	types.nametype AS nametype,
	invoice.numdoc AS numdoc,
	count(invoice.id) AS counttov,
	sum(invoice.sum) AS totalsum,
	status.namestatus AS namestatus
FROM
	public.invoice,
	public.types,
	public.status
WHERE
	invoice."idType" = types.id AND
	invoice.status = status.id
GROUP BY
	types.nametype,
	invoice.numdoc,
	status.namestatus,
	invoice.dateinvoice
ORDER BY
	invoice.dateinvoice DESC;
$BODY$;

ALTER FUNCTION public.select_invoices()
    OWNER TO salesadmin;