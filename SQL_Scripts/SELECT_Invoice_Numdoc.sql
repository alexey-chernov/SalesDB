SELECT 
	products.nameproduct, 
	invoice.quantity, 
	units.nameunitshort, 
	price, 
	sum
FROM 
	public.invoice, 
	public.products, 
	public.units
WHERE
	invoice."idTov" = products.id AND
	invoice.unit = units.id AND
	invoice.numdoc = '443'
ORDER BY
	products.nameproduct;