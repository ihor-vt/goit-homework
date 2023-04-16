from flask import render_template, request, redirect, url_for, flash
from src.models import Contact
from src import db
from sqlalchemy.orm import joinedload
from . import app


@app.route("/healthcheck")
def healthcheck():
    return 'I am alive!'


@app.route('/', strict_slashes=False)
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/detail/<int:pk>', strict_slashes=False)
def detail(pk):
    contact = Contact.query.get(pk)
    return render_template('detail.html', contact=contact)


@app.route('/contact', methods=['GET', 'POST'], strict_slashes=False)
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        user = Contact(name=name, phone=phone, email=email, address=address)
        db.session.add(user)
        db.session.commit()
        flash('Contact added successfully!')
        return redirect(url_for('index'))
    return render_template('contact.html')


@app.route('/update', defaults={'pk': None}, methods=['POST'])
@app.route('/update/<int:pk>', methods=['GET', 'POST'], strict_slashes=False)
def update(pk):
    if request.method == 'POST':
        user = Contact.query.get(request.form['id'])
        user.name = request.form['name']
        user.phone = request.form['phone']
        user.email = request.form['email']
        user.address = request.form['address']
        db.session.commit()
        flash('Contact updated successfully!')
        return redirect(url_for('index'))
    user = Contact.query.get(pk)
    return render_template('update.html', user=user)


@app.route('/delete/<int:pk>', strict_slashes=False)
def delete(pk):
    user = Contact.query.get(pk)
    db.session.delete(user)
    db.session.commit()
    flash('Contact deleted successfully!')
    return redirect(url_for('index'))
