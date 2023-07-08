SELECT
	"types".nametype AS "Тип накладної",
	"invoice".numdoc AS "Номер накладної",
	"products".nameproduct AS "Товар",
	"invoice".quantity AS "Кількість",
	"units".nameunitshort AS "Одиниці",
	"invoice".leftovers AS "Залишок", 
	"units".nameunitshort AS "Одиниці"
FROM 
	public."invoice", 
	public."products",
	public."types",
	public."units"
WHERE
	"invoice"."idTov" = "products".id AND
	"invoice"."unit" = "units".id AND
	"invoice"."idType" = "types".id AND
	"invoice"."dateinvoice" = '2023-06-13'
ORDER BY
	"invoice".numdoc, "products".nameproduct;