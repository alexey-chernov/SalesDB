SELECT
	types.nametype,
	invoice.numdoc,
	sum(invoice.sum) AS totalsum,
	count(invoice.id) AS countTov,
	status.namestatus
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
