# Importing the necassary packages to make program work
# Successfully and create, read, update and delete data

from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
mysql = MySQL(app)

#Articles=Articles()

# I utlized MySQL for my database, DB name is flaskdb
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1qaz2wsx!QAZ@WSX'
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_CURSOR'] = 'DictCursor'

# mainpage routing to show introduction to website
@app.route('/')
def index():
    return render_template('home.html')

# accessing the userstable database to populate columns
# on the interface
@app.route('/user')
def user():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM userstable")

    articles = cur.fetchall()

    if result > 0:
        return render_template('user.html', articles=articles)
    else:
        msg = 'No user data found'
        return render_template('user.html', msg=msg)

    cur.close()

    return render_template('user.html')


@app.route('/orders')
def orders():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM orders")

    orders = cur.fetchall()

    if result > 0:
        return render_template('orders.html', orders=orders)
    else:
        msg = 'No user data found'
        return render_template('orders.html', msg=msg)

    cur.close()

    return render_template('orders.html')

@app.route('/scene')
def scene():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM scenes")

    scene = cur.fetchall()

    if result > 0:
        return render_template('scene.html', scene=scene)
    else:
        msg = 'No user data found'
        return render_template('scene.html', msg=msg)

    cur.close()

    return render_template('scene.html')

# Classes and functions forms for user.
class UserForm(Form):
    fname = StringField('First Name', [validators.Length(min=3, max=50)])
    lname = StringField('Last Name', [validators.Length(min=3, max=50)])
    usemail = StringField('Email', [validators.Length(min=3, max=50)])
    dateusercreated = StringField('Date Created(mm/dd/yyyy)', [validators.Length(min=3, max=50)])
    usactive = StringField('Active/Not Active', [validators.Length(min=3, max=50)])

# acessing form for validation before submission
@app.route('/userregisterform', methods=['GET', 'POST'])
def userregisterform():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        fname = form.fname.data
        lname = form.lname.data
        usemail = form.usemail.data
        dateusercreated = form.dateusercreated.data
        usactive = form.usactive.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO userstable(firstname, lastname, useremail, datecreated, useractive) VALUES(%s, %s, %s, %s, %s)", (fname, lname, usemail, dateusercreated, usactive))

        mysql.connection.commit()

        cur.close()

        flash('User added to database', 'success')

        return redirect(url_for('user'))

    return render_template('userregisterform.html', form=form)

# Order form
class OrderForm(Form):
    orderident = StringField('Order ID', [validators.Length(min=3, max=50)])
    orderdte = StringField('Order Date (mm/dd/yyyy)', [validators.Length(min=3, max=50)])
    orderstatus = TextAreaField('Status of Order', [validators.Length(min=10, max=1200)])
    idorder = StringField('Active/Not Active', [validators.Length(min=3, max=50)])

# Validating Order form before submission
@app.route('/orderregform', methods=['GET', 'POST'])
def orderregform():
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        orderident = form.orderident.data
        orderdte = form.orderdte.data
        orderstatus = form.orderstatus.data
        idorder = form.idorder.data

        # Cursor for ordersform to access orders table
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO orders(orderid, orderdate, status, active) VALUES(%s, %s, %s, %s)", (orderident, orderdte, orderstatus, idorder))

        mysql.connection.commit()

        cur.close()

        # if the form is validated correctly and the data
        # has been transferred to the table within the
        # flaskdb, then a flash message will verify it
        # and return user to the user interface display
        flash('Order added to database', 'success')

        return redirect(url_for('orders'))

    return render_template('orderregform.html', form=form)

# Scene Form
class SceneForm(Form):
    imgname = StringField('Scene Name', [validators.Length(min=3, max=50)])
    statimg = TextAreaField('Status of Scene', [validators.Length(min=10, max=1200)])
    imgsensor = StringField('Sensor Used:', [validators.Length(min=3, max=50)])
    imgorderid = StringField('Scene OrderID', [validators.Length(min=3, max=50)])

# Validating Scene form before submission
@app.route('/sceneregistration', methods=['GET', 'POST'])
def sceneregistration():
    form = SceneForm(request.form)
    if request.method == 'POST' and form.validate():
        imgname = form.imgname.data
        statimg = form.statimg.data
        imgsensor = form.imgsensor.data
        imgorderid = form.imgorderid.data

        # cursor for sql
        cur = mysql.connection.cursor()

        # Executing data into the table of the flaskdb
        cur.execute("INSERT INTO scenes(scenename, scenestatus, sensor, sceneorderid) VALUES(%s, %s, %s, %s)", (imgname, statimg, imgsensor, imgorderid))

        # Commit
        mysql.connection.commit()

        # Execution complete, data transferred
        cur.close()

        # if the form is validated correctly and the data
        # has been transferred to the table within the
        # flaskdb, then a flash message will verify it
        # and return user to the user interface display
        flash('Scene added to database', 'success')

        return redirect(url_for('scene'))

    return render_template('sceneregistration.html', form=form)


if __name__ == '__main__':
    app.secret_key="usmc123"
    app.run(debug=True)
