from flask import render_template, request, redirect, url_for
from app import app, db
from models import Product
from flask_login import login_required, current_user

# Route to display all products
@app.route('/marketplace')
def marketplace():
    products = Product.query.all()
    return render_template('marketplace.html', products=products)

# Route to add a product
@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']

        new_product = Product(name=name, description=description, price=price, image_url=image_url, seller_id=current_user.id)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('marketplace'))

    return render_template('add_product.html')
