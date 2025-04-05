import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# App Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tradenest.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder for storing images

# Create Uploads Folder if not exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    seller = db.Column(db.String(100), nullable=False)

# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

# Homepage (Redirects to Login First)
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('buy_or_sell'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please login.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for('buy_or_sell'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

# Buy or Sell Page
@app.route('/buy_or_sell')
def buy_or_sell():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('buy_or_sell.html')

# Marketplace (Product Listing)
@app.route('/marketplace')
def marketplace():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('marketplace.html', products=products)

# Sell Product (With Image Upload)
@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        seller = User.query.get(session['user_id']).username

        # Handle File Upload
        if 'image' not in request.files:
            flash("No image uploaded!", "danger")
            return redirect(url_for('sell'))
        
        image = request.files['image']
        if image.filename == '':
            flash("No image selected!", "danger")
            return redirect(url_for('sell'))

        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        product = Product(name=name, description=description, price=price, image_url=f"static/uploads/{filename}", seller=seller)
        db.session.add(product)
        db.session.commit()

        flash("Product listed successfully!", "success")
        return redirect(url_for('marketplace'))
    
    return render_template('sell.html')

# Cart (Display User's Cart)
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    products = [Product.query.get(item.product_id) for item in cart_items]

    return render_template('cart.html', cart_items=products)

# Add to Cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    existing_item = Cart.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    
    if existing_item:
        flash("Item already in cart!", "info")
    else:
        cart_item = Cart(user_id=session['user_id'], product_id=product_id)
        db.session.add(cart_item)
        db.session.commit()
        flash("Item added to cart!", "success")
    
    return redirect(url_for('marketplace'))

# Remove from Cart
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cart_item = Cart.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Item removed from cart!", "success")
    
    return redirect(url_for('cart'))

# Checkout (Clears Cart)
@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    Cart.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash("Checkout successful!", "success")
    
    return redirect(url_for('marketplace'))

if __name__ == '__main__':
    app.run(debug=True)







