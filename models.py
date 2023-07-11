from sqlalchemy import Table, Column, Integer, String, Float, MetaData, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy import select, func, desc
from sqlalchemy.sql import text
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField
from werkzeug.routing import ValidationError
#import psycopg2
import datetime

engine = create_engine(
    'postgresql+psycopg2://salesadmin:qwerty123456@10.66.66.1/salesdb')
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

reports = Table(
    'reports', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('reportname', String(250)),
    Column('functionname', String(100)),
    Column('functionparameters', String(10))
)

reference_books = Table(
    'reference_books', meta,
    Column('id', Integer, nullable=False, primary_key=True),
    Column('referencename', String(100)),
    Column('referencetablename', String(100))
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
        #sql = select(sklad, products, units, (sklad.c.quantity * sklad.c.price).label("sum")).where(
        #    sklad.c.idTov == products.c.id, sklad.c.unit == units.c.id).order_by(products.c.nameproduct)

        sql = select('*').select_from(func.select_warehouse()) #Викликається функція select_warehouse
        result = conn.execute(sql)
        return result

    def getProductInfo(self, product_id):
        sql = select(sklad, products, units, (sklad.c.quantity * sklad.c.price).label("sum")).where(
            sklad.c.idTov == products.c.id, sklad.c.unit == units.c.id, sklad.c.idTov == product_id)
        result = conn.execute(sql).fetchone()
        return result

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
        result = conn.execute(sql).fetchone()
        return result

    def getProductName(self, product_id):
        sql = products.select().where(products.c.id == product_id)
        result = conn.execute(sql).fetchone()
        return result

    def getInvoices(self):
        #sql = select(invoice.c.dateinvoice, types.c.nametype, invoice.c.numdoc, func.sum(invoice.c.sum).label("totalsum"),
        #             func.count(invoice.c.id).label("counttov"), status.c.namestatus).where(
        #    invoice.c.idType == types.c.id, invoice.c.status == status.c.id).group_by(
        #    types.c.nametype, invoice.c.numdoc, status.c.namestatus, invoice.c.dateinvoice).order_by(
        #    invoice.c.dateinvoice.desc())

        sql = select('*').select_from(func.select_invoices()) #Викликається функція select_invoices
        result = conn.execute(sql)
        return result

    def getInvoiceProducts(self, numberdoc):
        sql = select(invoice, products, units).where(
            invoice.c.idTov == products.c.id, invoice.c.unit == units.c.id, invoice.c.numdoc == numberdoc
            ).order_by(products.c.nameproduct)
        result = conn.execute(sql)
        return result
    
    def getInvoiceInfo(self, numberdoc):
        sql = select(types.c.nametype, invoice.c.numdoc, invoice.c.datedoc, invoice.c.dateinvoice, 
                     func.sum(invoice.c.sum).label("totalsum"), func.count(invoice.c.id).label("countTov"), 
                     status.c.namestatus, invoice.c.status).where(
            invoice.c.idType == types.c.id, invoice.c.status == status.c.id, invoice.c.numdoc == numberdoc
            ).group_by(types.c.nametype, invoice.c.numdoc, invoice.c.datedoc, invoice.c.dateinvoice, 
                       status.c.namestatus, invoice.c.status)
        result = conn.execute(sql).fetchone()
        return result
    
    def getReportsList(self):
        sql = select(reports).order_by(reports.c.reportname)
        result = conn.execute(sql)
        return result
    
    def getReportParameters(self, functionname):
        sql = select(reports).where(reports.c.functionname == functionname)
        result = conn.execute(sql).fetchone()
        return result

    def buildReport(self, functionname, functionparameters):
        sql = text(f"SELECT * FROM {functionname}({functionparameters});")
        #Викликається функція для вибраного звіту 
        result = conn.execute(sql).fetchall()
        return result
    
    def getReferencebooksList(self):
        sql = select(reference_books).order_by(reference_books.c.id)
        result = conn.execute(sql)
        return result
    
    def buildreferencesform(self, referencetablename):
        sql = text(f"SELECT * FROM {referencetablename} ORDER BY id;")
        result = conn.execute(sql).fetchall()
        return result

    def getreferencesname(self, referencetablename):
        sql = select(reference_books).where(reference_books.c.referencetablename == referencetablename)
        result = conn.execute(sql).fetchone()
        return result

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
                                     'unit': unit, 'leftovers': leftovers, 'numdoc': numberdocument,
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

    def updateSkladPrice(self, id, newprice):
        sql = sklad.update().where(sklad.c.idTov == id).values(price=newprice)
        result = conn.execute(sql)
        conn.commit()

    def updateStatusInvoice(self, numdoc, idstatus):
        sql = invoice.update().where(invoice.c.numdoc == numdoc).values(status=idstatus)
        result = conn.execute(sql)
        conn.commit()

    # При завершенні роботи - закрити з'єднання з БД
    def __del__(self):
        conn.close()


opttrade = OptTrade()
