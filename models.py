from sqlalchemy import Table, Column, Integer, String, Float, MetaData, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy import select, func
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField
from werkzeug.routing import ValidationError
import psycopg2
import datetime

engine = create_engine(
    'postgresql+psycopg2://salesadmin:qwerty123456@localhost/salesdb')
conn = engine.connect()
meta = MetaData()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "change-me"

sklad = Table(
    'sklad', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('idTov', Integer),
    Column('quantity', Integer),
    Column('unit', Integer),
    Column('price', Float)
)

invoice = Table(
    'invoice', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('idType', Integer),
    Column('idTov', Integer),
    Column('quantity', Integer),
    Column('unit', Integer),
    Column('leftovers', Integer),
    Column('numdoc', String(50)),
    Column('datedoc', DateTime, nullable=False),
    Column('dateinvoice', DateTime, nullable=False,
           default=datetime.datetime.utcnow),
    Column('price', Float),
    Column('sum', Float),
    Column('status', Integer, default=1)
)

products = Table(
    'products', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('nameproduct', String(250))
)

types = Table(
    'types', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('nametype', String(50))
)

status = Table(
    'status', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('namestatus', String(50))
)

units = Table(
    'units', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('nameunit', String(50)),
    Column('nameunitshort', String(5))
)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, field):
        if field.data != ADMIN_USERNAME:
            raise ValidationError("Invalid username")
        return field.data

    def validate_password(self, field):
        if field.data != ADMIN_PASSWORD:
            raise ValidationError("Invalid password")
        return field.data


class OptTrade:
    # SELECT
    def getWarehouse(self):
        sql = select(sklad, products, units, (sklad.c.quantity * sklad.c.price)).where(
            sklad.c.idTov == products.c.id, sklad.c.unit == units.c.id).order_by(products.c.nameproduct)
        result = conn.execute(sql)
        return result

    def getProductInfo(self, product_id):
        sql = select(sklad, products, units, (sklad.c.quantity * sklad.c.price)).where(
            sklad.c.idTov == products.c.id, sklad.c.unit == units.c.id, sklad.c.idTov == product_id)
        result = conn.execute(sql)
        row = result.fetchone()
        return row

    def getListProducts(self):
        sql = select(products).join(sklad, products.c.id == sklad.c.idTov, isouter=True).where(
            sklad.c.idTov == None).order_by(products.c.nameproduct)

        # SELECT products.nameproduct
        # FROM products LEFT OUTER JOIN sklad ON products.id = sklad."idTov"
        # WHERE sklad."idTov" IS NULL ORDER BY products.nameproduct

        result = conn.execute(sql)
        return result

    def getUnits(self):
        sql = units.select().order_by(units.c.nameunit)
        result = conn.execute(sql)
        return result

    def getIdUnit(self, nameunits):
        sql = units.select().where(units.c.nameunit == nameunits)
        result = conn.execute(sql)
        row = result.fetchone()
        return row

    def getProductName(self, product_id):
        sql = products.select().where(products.c.id == product_id)
        result = conn.execute(sql)
        row = result.fetchone()
        return row

    def getInvoices(self):
        sql = select(invoice, products, units, types, status).where(
            invoice.c.idTov == products.c.id, invoice.c.unit == units.c.id, invoice.c.idType == types.c.id,
            invoice.c.status == status.c.id).order_by(invoice.c.dateinvoice.desc())
        result = conn.execute(sql)
        return result

    def getInvoiceInfo(self, invoice_id):
        sql = select(invoice, products, units, types, status).where(
            invoice.c.idTov == products.c.id, invoice.c.unit == units.c.id, invoice.c.idType == types.c.id,
            invoice.c.status == status.c.id, invoice.c.id == invoice_id)
        result = conn.execute(sql)
        row = result.fetchone()
        return row

    # INSERT INTO
    def createinvoice(self, typeid, productid, quantity, unit, leftovers, price, sum, numberdocument, datedocument, is_saled):
        if (is_saled == 'on'):
            is_saled = 2
        else:
            is_saled = 1
        sql = invoice.insert().values(idType=typeid,
                                      idTov=productid,
                                      quantity=quantity,
                                      unit=unit,
                                      leftovers=leftovers,
                                      numdoc=numberdocument,
                                      datedoc=datedocument,
                                      price=price,
                                      sum=sum,
                                      status=is_saled)
        result = conn.execute(sql, [{'idType': typeid, 'idTov': productid, 'quantity': quantity,
                                     'unit': unit, 'leftovers':leftovers, 'numdoc': numberdocument, 
                                     'datedoc': datedocument, 'price': price, 'sum': sum, 'status': is_saled}])
        conn.commit()

    def createproductinwarehouse(self, idTov, quantity, unit, price):
        sql = sklad.insert().values(idTov=idTov,
                                    quantity=quantity,
                                    unit=unit,
                                    price=price)
        result = conn.execute(sql, [{'idTov': idTov, 'quantity': quantity,
                                     'unit': unit, 'price': price}])
        conn.commit()

    # UPDATE
    def updateSkladQuantity(self, id, newquantity):
        sql = sklad.update().where(sklad.c.idTov == id).values(quantity=newquantity)
        result = conn.execute(sql)
        conn.commit()

    def updateStatusInvoice(self, id, idstatus):
        sql = invoice.update().where(invoice.c.id == id).values(status=idstatus)
        result = conn.execute(sql)
        conn.commit()

    # При завершенні роботи - закрити з'єднання з БД
    def __del__(self):
        conn.close()


opttrade = OptTrade()
