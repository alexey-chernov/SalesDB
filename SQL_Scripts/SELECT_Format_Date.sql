SELECT
	to_char("invoice".dateinvoice, 'dd Mon yyyy'),
	"invoice".dateinvoice
FROM
	public.invoice;