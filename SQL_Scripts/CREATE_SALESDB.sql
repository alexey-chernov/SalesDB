--Створення користувача бази даних salesadmin з паролем qwerty123456
CREATE ROLE salesadmin WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'SCRAM-SHA-256$4096:2GUfnwMFfHutti4Id+To3w==$XPLbFxQ/GDVj6A5GYKK15anzaMkReUO338zAnwNrAeU=:sSSdg0REZG5SUhgKw0ur6R6wTbbf6nJ551CdtgMd6hs=';


--Сворення бази даних salesdb
CREATE DATABASE salesdb
    WITH
    OWNER = salesadmin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


--Створення таблиці Sklad
CREATE TABLE IF NOT EXISTS public."sklad"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "idTov" numeric(5,0) NOT NULL DEFAULT 0,
    quantity numeric(10,0) NOT NULL DEFAULT 0,
    unit numeric(4,0) NOT NULL DEFAULT 0,
    price numeric(10,2),
    CONSTRAINT "Sklad_pkey" PRIMARY KEY (id)
)

ABLESPACE pg_default;

ALTER TABLE IF EXISTS public.sklad
    OWNER to salesadmin;


--Створення таблиці Invoice
CREATE TABLE IF NOT EXISTS public."invoice"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "idType" numeric(5,0) NOT NULL DEFAULT 0,
    "idTov" numeric(5,0) NOT NULL DEFAULT 0,
    quantity numeric(10,0) NOT NULL DEFAULT 0,
    unit numeric(4,0) NOT NULL DEFAULT 0,
    leftovers numeric(10,0) DEFAULT 0,
    NumDoc character(50),
    datedoc date NOT NULL,
    dateinvoice date NOT NULL DEFAULT now(),
    price numeric(10,2),
    sum numeric(10,2),
    status numeric(5,0) NOT NULL DEFAULT 0,
    CONSTRAINT "Invoice_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.invoice
    OWNER to salesadmin;


--Створення таблиці Products
CREATE TABLE IF NOT EXISTS public."products"
(
    id serial,
    nameproduct character(250),
    CONSTRAINT "Products_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.products
    OWNER to salesadmin;


--Створення таблиці Units
CREATE TABLE IF NOT EXISTS public."units"
(
    id serial,
    nameunit character(50),
    nameunitshort character(5),
    CONSTRAINT "Units_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.units
    OWNER to salesadmin;


--Створення таблиці Types
CREATE TABLE IF NOT EXISTS public."types"
(
    id serial,
    nametype character(50),
    CONSTRAINT "Types_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.types
    OWNER to salesadmin;


--Створення таблиці Status
CREATE TABLE IF NOT EXISTS public."status"
(
    id serial,
    namestatus character(50),
    CONSTRAINT "Status_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.status
    OWNER to salesadmin;


--Створення таблиці Reports
CREATE TABLE IF NOT EXISTS public."reports"
(
    id serial,
    reportname character(250),
    functionname character(100),
    functionparameters character(10),
    CONSTRAINT "Reports_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.reports
    OWNER to salesadmin;


--Створення таблиці Reference_books
CREATE TABLE IF NOT EXISTS public.reference_books
(
    id serial,
    referencename character(100),
    referencetablename character(100),
    CONSTRAINT reference_books_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.reference_books
    OWNER to salesadmin;
