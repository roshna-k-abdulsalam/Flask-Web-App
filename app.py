import datetime
import random

import faker

from flask import Flask, render_template, request, redirect, url_for

import models

app = Flask("lycaeum")


@app.route("/", methods=['GET'])
def hello():
    added = request.args.get('info')
    session = models.get_session()
    customers = session.query(models.Customer).all()
    return render_template("customers.html", customers=customers, added=added)


@app.route("/invoices", methods=['GET'])
def invoices():
    cid = request.args.get('cid')
    added = request.args.get('info')
    session = models.get_session()
    customer = session.query(models.Customer).filter(
        models.Customer.id == cid).first()
    invoices = session.query(models.Invoice).filter(
        models.Invoice.customer_id == cid).all()
    if request.headers.get('Accept') == 'application/json':
        ret = []
        for i in invoices:
            ret.append(
                dict(date=i.date, particulars=i.particulars, amount=i.amount))
        return dict(invoices=ret)
    else:
        return render_template("invoice_new.html", customer=customer, invoices=invoices, added=added)


@app.route("/invoices", methods=['POST'])
def create_invoice():
    session = models.get_session()
    particulars = request.form['particulars']
    amount = request.form['amount']
    cid = request.form['cid']

    invoice = models.Invoice(date=datetime.date.today(),
                             particulars=particulars,
                             customer_id=int(cid),
                             amount=amount)

    session.add(invoice)
    session.commit()
    return redirect(url_for('invoices', cid=cid, info="added"))


@app.route("/", methods=['POST'])
def create_customer():
    session = models.get_session()

    name = request.form['name']
    address = request.form['address']
    email = request.form['email']

    new_customer = models.Customer(name=name,
                                   jdate=datetime.date.today(),
                                   address=address,
                                   email=email)
    session.add(new_customer)
    f = faker.Faker()
    for i in range(5):
        invoice = models.Invoice(particulars=f.sentence(),
                                 date=f.date(),
                                 amount=random.randint(10, 99),
                                 customer=new_customer)
        session.add(invoice)

    session.commit()
    return redirect(url_for('hello', info="added"))


@app.route("/about")
def about():
    return render_template("about_us.html")


@app.route("/info")
def info():
    session = models.get_session()
    customer_count = session.query(models.Customer).count()
    print(customer_count)
    last_id = session.query(models.Invoice).count()
    print(last_id)
    details_of_last_invoice = session.query(
        models.Invoice).filter(models.Invoice.id == '6').all()
    print(details_of_last_invoice)
    return render_template("info.html", customer_count=customer_count, details_of_last_invoice=details_of_last_invoice)
