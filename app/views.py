from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import db, User, Product
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products, title='Products')


@app.route('/favourites')
def favourites():
    if current_user.is_authenticated:
        favourites = current_user.favourites
    else:
        favourites = []
    return render_template('favourites.html', favourites=favourites)


@app.route('/add_to_favourites/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_to_favourites(product_id):
    product = Product.query.get_or_404(product_id)
    if product not in current_user.favourites:
        current_user.favourites.append(product)
        db.session.commit()
        flash('Product added to favourites!', 'success')
    else:
        flash('Product already in favourites!', 'info')
    return redirect(url_for('favourites'))


@app.route('/remove_from_favourites/<int:product_id>', methods=['GET', 'POST'])
@login_required
def remove_from_favourites(product_id):
    product = Product.query.get_or_404(product_id)
    if product in current_user.favourites:
        current_user.favourites.remove(product)
        db.session.commit()
        flash('Product removed from favourites!', 'success')
    else:
        flash('Product not in favourites!', 'info')
    return redirect(url_for('favourites'))


@app.route('/basket')
def basket():
    if current_user.is_authenticated:
        basket_items = current_user.basket_items
    else:
        basket_items = []
    return render_template('basket.html', basket_items=basket_items)


@app.route('/add_to_basket/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_to_basket(product_id):
    product = Product.query.get_or_404(product_id)
    if product.stock_level > 0:
        if product not in current_user.basket_items:
            current_user.basket_items.append(product)
            product.stock_level -= 1  # Decrease stock level
            db.session.commit()
            flash('Product added to basket!', 'success')
    else:
        flash('This product is out of stock.', 'error')
    return redirect(url_for('basket'))


@app.route('/remove_from_basket/<int:product_id>', methods=['POST'])
@login_required
def remove_from_basket(product_id):
    product = Product.query.get_or_404(product_id)
    if product in current_user.basket_items:
        current_user.basket_items.remove(product)
        product.stock_level += 1  # Increase stock level
        db.session.commit()
        flash('Product removed from basket!', 'success')
    else:
        flash('Product not in basket!', 'info')
    return redirect(url_for('basket'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            next_page = request.args.get('next') or url_for('home')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created! You are now logged in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/like_product', methods=['POST'])
@login_required
def like_product():
    data = request.get_json()
    product_id = data.get('product_id')
    product = Product.query.get_or_404(product_id)
    product.likes += 1
    db.session.commit()
    return jsonify({'message': 'Product liked!', 'likes': product.likes})
