from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
import re
import json
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bca-project-key-2026'
DATABASE = 'database.db'


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# AUTH DECORATORS
# -----------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access only', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# -----------------------------
# PRODUCT HELPER WITH PRICE TRACKING
# -----------------------------
def get_product_with_prices(pid):
    db = get_db()
    p_row = db.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
    ''', (pid,)).fetchone()
    if not p_row:
        db.close()
        return None

    product = dict(p_row)
    prices_rows = db.execute(
        'SELECT * FROM store_prices WHERE product_id = ?',
        (pid,)
    ).fetchall()
    db.close()

    prices = [dict(row) for row in prices_rows]
    product['prices'] = prices

    if prices:
        product['min_price'] = min(p['current_price'] for p in prices if p['current_price'])
        product['max_price'] = max(p['current_price'] for p in prices if p['current_price'])
        
        # Find best deal
        for p in prices:
            if p['current_price'] == product['min_price']:
                product['best_store'] = p['store_name']
                product['best_link'] = p['store_link']
                product['best_price'] = p['current_price']
                break
    else:
        product['min_price'] = 0
        product['max_price'] = 0
        product['best_link'] = "#"

    return product


def get_related_products(category_id, current_product_id, limit=4):
    db = get_db()
    rows = db.execute('''
        SELECT id FROM products
        WHERE category_id = ? AND id != ?
        ORDER BY id DESC
        LIMIT ?
    ''', (category_id, current_product_id, limit)).fetchall()
    db.close()
    return [get_product_with_prices(r['id']) for r in rows]


# Helper: Calculate price drop
def calculate_price_drop(current, previous):
    if previous == 0 or previous is None:
        return 0, "same"
    diff = previous - current
    if diff > 0:
        return round(diff, 2), "drop"
    elif diff < 0:
        return round(abs(diff), 2), "increase"
    return 0, "same"


# -----------------------------
# HOME
# -----------------------------
@app.route('/')
def home():
    db = get_db()
    trending_rows = db.execute('SELECT id FROM products WHERE is_trending = 1 LIMIT 4').fetchall()
    categories = db.execute('SELECT * FROM categories').fetchall()
    db.close()
    trending = [get_product_with_prices(r['id']) for r in trending_rows]
    return render_template('index.html', trending=trending, categories=categories)


# -----------------------------
# LOGIN
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        db.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            if user['is_admin'] == 1:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')


# -----------------------------
# REGISTER (STRONG PASSWORD)
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        db = get_db()

        if db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            db.close()
            flash('Email already exists', 'warning')
            return redirect(url_for('register'))

        # Username validation
        if not re.match(r'^[A-Za-z\s]+$', username):
            db.close()
            flash('Name should contain alphabetic characters only', 'danger')
            return redirect(url_for('register'))

        # Email validation
        if not re.match(r'(?i)^[a-z0-9._%+-]+@(gmail\.com|yahoo\.com|outlook\.com|hotmail\.com|icloud\.com)$', email):
            db.close()
            flash('Invalid email format. Must use allowed domains (gmail.com, yahoo.com, outlook.com, hotmail.com, icloud.com).', 'danger')
            return redirect(url_for('register'))

        # Strong password validation
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$', password):
            db.close()
            flash('Password must be at least 8 characters and include letters & numbers', 'danger')
            return redirect(url_for('register'))

        if password != confirm:
            db.close()
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        hashed = generate_password_hash(password)
        db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed))
        db.commit()
        db.close()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# -----------------------------
# LOGOUT
# -----------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


# -----------------------------
# DASHBOARD (Value Score References Removed)
# -----------------------------
@app.route('/dashboard')
def dashboard():
    search = request.args.get('search', '')
    category_id = request.args.get('category_id', type=int)
    budget = request.args.get('budget', type=float)
    sort = request.args.get('sort', 'relevance')


    # Block empty/whitespace search form (allow All Products & filters)
    if not search.strip() and request.args.get('view') != 'all' and category_id is None and budget is None:
        return redirect(url_for('home'))


    db = get_db()

    query = 'SELECT id FROM products WHERE 1=1'
    params = []
    if search:
        query += ' AND name LIKE ?'
        params.append('%' + search + '%')
    if category_id:
        query += ' AND category_id = ?'
        params.append(category_id)
    rows = db.execute(query, params).fetchall()
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    db.close()

    products = [get_product_with_prices(r['id']) for r in rows]
    if budget:
        products = [p for p in products if p['min_price'] <= budget]

    if sort == 'low_price':
        products.sort(key=lambda x: x['min_price'])
    elif sort == 'high_rating':
        products.sort(key=lambda x: x['rating'], reverse=True)
    elif sort == 'value':
        products.sort(key=lambda x: x['min_price'])

    recommended = min(products, key=lambda x: x['min_price']) if products else None

    return render_template('dashboard.html', products=products, recommended=recommended, search=search, category_id=category_id, categories=categories)


# -----------------------------
# PRODUCT DETAIL
# -----------------------------
@app.route('/product/<int:id>')
def product_detail(id):
    product = get_product_with_prices(id)
    if not product:
        return redirect(url_for('dashboard'))
    
    # Add price drop info for each store
    for price in product['prices']:
        drop_amt, drop_type = calculate_price_drop(price['current_price'], price['previous_price'])
        price['price_drop_amount'] = drop_amt
        price['price_drop_type'] = drop_type

    related_products = get_related_products(product['category_id'], id, limit=4)
    return render_template('product_detail.html', product=product, related_products=related_products)


# -----------------------------
# PRICE COMPARISON PAGE
# -----------------------------
@app.route('/compare/<int:id>')
def compare_prices(id):
    product = get_product_with_prices(id)
    if not product:
        return redirect(url_for('dashboard'))
    
    # Add price drop info for each store
    for price in product['prices']:
        drop_amt, drop_type = calculate_price_drop(price['current_price'], price['previous_price'])
        price['price_drop_amount'] = drop_amt
        price['price_drop_type'] = drop_type
    
    return render_template('price_comparison.html', product=product)


# -----------------------------
# API: GET PRICE HISTORY (For Chart.js)
# -----------------------------
@app.route('/api/price-history/<int:product_id>/<store_name>')
def get_price_history(product_id, store_name):
    db = get_db()
    history = db.execute('''
        SELECT price, recorded_date FROM price_history 
        WHERE product_id = ? AND store_name = ?
        ORDER BY recorded_date ASC
    ''', (product_id, store_name)).fetchall()
    db.close()
    
    if not history:
        return jsonify([])
    
    data = [{
        'date': row['recorded_date'].split()[0],
        'price': row['price']
    } for row in history]
    
    return jsonify(data)


# -----------------------------
# CART
# -----------------------------
@app.route('/add_to_cart/<int:id>')
@login_required
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    cart = session['cart']
    if id not in cart:
        cart.append(id)
        session['cart'] = cart
        flash('Added to cart!', 'success')
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/cart')
@login_required
def cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', products=[], total=0)
    products = [get_product_with_prices(pid) for pid in session['cart']]
    total = sum(p['min_price'] for p in products)
    return render_template('cart.html', products=products, total=total)


@app.route('/remove_from_cart/<int:id>')
@login_required
def remove_from_cart(id):
    if 'cart' in session:
        cart = session['cart']
        if id in cart:
            cart.remove(id)
            session['cart'] = cart
    return redirect(url_for('cart'))


# -----------------------------
# ADMIN LOGIN
# -----------------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        admin = db.execute('SELECT * FROM users WHERE username = ? AND is_admin = 1', (username,)).fetchone()
        db.close()
        if admin and check_password_hash(admin['password'], password):
            session['admin_id'] = admin['id']
            session['admin_name'] = admin['username']
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin login', 'danger')
    return render_template('admin_login.html')


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()
    rows = db.execute('SELECT id FROM products').fetchall()
    db.close()
    products = [get_product_with_prices(r['id']) for r in rows]
    return render_template('admin_dashboard.html', products=products)


# -----------------------------
# ADD PRODUCT
# -----------------------------
@app.route('/admin/add_product', methods=['GET', 'POST'])
@admin_required
def add_product():
    db = get_db()
    if request.method == 'POST':
        name = request.form.get('name')
        brand = request.form.get('brand', 'Generic')
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        category_id = request.form.get('category_id')
        rating = request.form.get('rating', 4.0)
        is_trending = 1 if request.form.get('is_trending') else 0

        cursor = db.execute('''
            INSERT INTO products (name, brand, description, image_url, category_id, rating, is_trending)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, brand, description, image_url, category_id, rating, is_trending))
        product_id = cursor.lastrowid

        stores = ['flipkart', 'amazon', 'meesho']
        for store in stores:
            price = request.form.get(f'{store}_price')
            link = request.form.get(f'{store}_link', '#')
            if price:
                db.execute('''
                    INSERT INTO store_prices (product_id, store_name, current_price, previous_price, store_link)
                    VALUES (?, ?, ?, ?, ?)
                ''', (product_id, store.capitalize(), float(price), float(price), link))
                
                # Add to price history
                db.execute('''
                    INSERT INTO price_history (product_id, store_name, price)
                    VALUES (?, ?, ?)
                ''', (product_id, store.capitalize(), float(price)))
        
        db.commit()
        db.close()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    categories = db.execute('SELECT * FROM categories').fetchall()
    db.close()
    return render_template('add_product.html', categories=categories)


# -----------------------------
# DELETE PRODUCT
# -----------------------------
@app.route('/admin/delete_product/<int:id>')
@admin_required
def delete_product(id):
    db = get_db()
    db.execute('DELETE FROM price_history WHERE product_id = ?', (id,))
    db.execute('DELETE FROM store_prices WHERE product_id = ?', (id,))
    db.execute('DELETE FROM products WHERE id = ?', (id,))
    db.commit()
    db.close()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# ========================================
# ADMIN: MANAGE PRICES
# ========================================

# --------- VIEW ALL PRICES FOR A PRODUCT ---------
@app.route('/admin/edit_prices/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_prices(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if not product:
        db.close()
        flash('Product not found', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        store_prices = db.execute(
            'SELECT id, store_name, current_price FROM store_prices WHERE product_id = ?',
            (product_id,)
        ).fetchall()
        
        for sp in store_prices:
            price_input = request.form.get(f'price_{sp["id"]}')
            if price_input:
                try:
                    new_price = float(price_input)
                    
                    # Get current price before updating
                    current = db.execute(
                        'SELECT current_price FROM store_prices WHERE id = ?',
                        (sp['id'],)
                    ).fetchone()
                    
                    # Move current_price to previous_price, then update current_price
                    db.execute('''
                        UPDATE store_prices 
                        SET previous_price = current_price, current_price = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (new_price, sp['id']))
                    
                    # Add to price history
                    db.execute('''
                        INSERT INTO price_history (product_id, store_name, price)
                        VALUES (?, ?, ?)
                    ''', (product_id, sp['store_name'], new_price))
                    
                except ValueError:
                    flash(f'Invalid price for {sp["store_name"]}', 'warning')
        
        db.commit()
        db.close()
        flash('Prices updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    prices = db.execute(
        'SELECT * FROM store_prices WHERE product_id = ?',
        (product_id,)
    ).fetchall()
    
    db.close()
    return render_template('edit_prices.html', product=dict(product), prices=[dict(p) for p in prices])


# --------- VIEW PRICE HISTORY FOR A STORE ---------
@app.route('/admin/price_history/<int:product_id>/<store_name>')
@admin_required
def view_price_history(product_id, store_name):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    history = db.execute('''
        SELECT * FROM price_history 
        WHERE product_id = ? AND store_name = ?
        ORDER BY recorded_date DESC
    ''', (product_id, store_name)).fetchall()
    db.close()
    
    return render_template('price_history.html', 
                          product=dict(product) if product else {},
                          store_name=store_name,
                          history=[dict(h) for h in history])


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        import models
        models.init_db()
    app.run(debug=True)
