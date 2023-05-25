from flask import Flask, jsonify, abort, make_response, request, render_template, session, flash, redirect, url_for
from models import opttrade
from models import LoginForm
import functools

app = Flask(__name__)
app.config["SECRET_KEY"] = "saleprog"


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('index'))


@app.route("/")
def index():
    return render_template("base.html")


@app.route('/warehouse', methods=["GET"])
@login_required
def warehouse():
    items = opttrade.getWarehouse()
    return render_template("warehouse.html", items=items)


@app.route('/productinfo/<product_id>', methods=["GET"])
@login_required
def productinfo(product_id):
    itemone = opttrade.getProductInfo(product_id)
    return render_template("productinfo.html", itemone=itemone)


@app.route('/income/<product_id>', methods=["POST"])
@login_required
def income(product_id):
    item = opttrade.getProductInfo(product_id)
    return render_template("income.html", item=item)


@app.route('/saveincome/<product_id>', methods=["POST"])
@login_required
def saveincome(product_id):
    data = request.form
    quantity_to_income = data.get('quantity_to_income')
    oldquantity = data.get('oldquantity')
    leftovers = int(quantity_to_income) + int(oldquantity)
    idunit = data.get('idunit')
    price_to_income = data.get('price_to_income')
    sum_to_income = float(price_to_income) * int(quantity_to_income)
    numberdocument = data.get('numberdocument')
    datedocument = data.get('datedocument')
    is_saled = data.get('is_saled')
    opttrade.createinvoice(1, product_id, quantity_to_income, idunit, leftovers,
                           price_to_income, sum_to_income, numberdocument, datedocument, is_saled)
    opttrade.updateSkladQuantity(product_id, int(
        quantity_to_income) + int(oldquantity))
    items = opttrade.getWarehouse()
    return render_template("warehouse.html", items=items)


@app.route('/selling/<product_id>', methods=["POST"])
@login_required
def sale(product_id):
    item = opttrade.getProductInfo(product_id)
    return render_template("sales.html", item=item)


@app.route('/savesale/<product_id>', methods=["POST"])
@login_required
def savesales(product_id):
    data = request.form
    quantity_to_sale = data.get('quantity_to_sale')
    oldquantity = data.get('oldquantity')
    idunit = data.get('idunit')
    leftovers = int(oldquantity) - int(quantity_to_sale)
    price_to_sale = data.get('price_to_sale')
    sum_to_sale = float(price_to_sale) * int(quantity_to_sale)
    numberdocument = data.get('numberdocument')
    datedocument = data.get('datedocument')
    is_saled = data.get('is_saled')
    opttrade.createinvoice(2, product_id, quantity_to_sale, idunit, leftovers,
                           price_to_sale, sum_to_sale, numberdocument, datedocument, is_saled)
    opttrade.updateSkladQuantity(product_id, int(
        oldquantity) - int(quantity_to_sale))
    items = opttrade.getWarehouse()
    return render_template("warehouse.html", items=items)


@app.route('/productadd', methods=["POST"])
@login_required
def productadd():
    items = opttrade.getListProducts()
    return render_template("productadd.html", items=items)


@app.route('/newproduct/<product_id>', methods=["GET"])
@login_required
def newproduct(product_id):
    units = []
    for unit in opttrade.getUnits():
        units.append(unit[1])
    product = opttrade.getProductName(product_id)
    return render_template("newproduct.html", units=units, product_id=product_id, product=product)


@app.route('/saveproduct/<product_id>', methods=["POST"])
@login_required
def saveproduct(product_id):
    data = request.form
    quantity = data.get('quantity')
    idunit = opttrade.getIdUnit(data.get('unitcode'))
    price = data.get('price')
    opttrade.createproductinwarehouse(product_id, quantity, idunit.id, price)
    items = opttrade.getListProducts()
    return render_template("productadd.html", items=items)


@app.route('/invoices', methods=["GET"])
@login_required
def invoices():
    items = opttrade.getInvoices()
    return render_template("invoices.html", items=items)


@app.route('/invoiceinfo/<numberdoc>', methods=["GET"])
@login_required
def invoiceinfo(numberdoc):
    itemone = opttrade.getInvoiceInfo(numberdoc)
    items = opttrade.getInvoiceProducts(numberdoc)
    return render_template("invoiceinfo.html", itemone=itemone, items=items)


@app.route('/changestatus/<invoice_id>', methods=["POST"])
@login_required
def changestatus(invoice_id):
    data = request.form
    idstatus = int(data.get('id_status'))
    if idstatus == 1:
        opttrade.updateStatusInvoice(invoice_id, 2)
    elif idstatus == 2:
        opttrade.updateStatusInvoice(invoice_id, 1)
    items = opttrade.getInvoices()
    return render_template("invoices.html", items=items)


@app.route('/setprice/<product_id>', methods=["POST"])
@login_required
def setprice(product_id):
    data = request.form
    newprice = data.get('newprice')
    opttrade.updateSkladPrice(product_id, newprice)
    itemone = opttrade.getProductInfo(product_id)
    return render_template("productinfo.html", itemone=itemone)
