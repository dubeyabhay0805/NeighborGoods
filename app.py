from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Order, OrderItem
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abhayutkarsh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neighbourgoods.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'neighbourgoodshop@gmail.com'
app.config['MAIL_PASSWORD'] = 'lrwzolifbsakurxl'  
app.config['MAIL_DEFAULT_SENDER'] = 'neighbourgoodshop@gmail.com' 
# Initialize the database with the app
db.init_app(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

# Call this function to create tables
create_tables()

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Updated function to send order email with customer details
def send_order_email(order):
    if getattr(order, 'email_sent', False):
        return  # Skip if email has already been sent

    # Get the user associated with the order
    user = User.query.get(order.user_id)
    
    msg = Message('New Order Placed',
                  recipients=['neighbourgoodshop@gmail.com'])  
    msg.body = f"""
    A new order has been placed:
    
    Customer Details:
    Name: {user.first_name} {user.last_name}
    Phone: {user.phone}
    
    Order Details:
    Order ID: {order.id}
    Total Amount: ₹{order.total_amount :.2f}
    Shipping Address: {order.shipping_address}
    
    Items:
    {', '.join([f"{item.product_name} (x{item.quantity})" for item in order.items])}
    
    Thank you for using our service!
    """
    mail.send(msg)
    
    # Mark the order as having been emailed
    order.email_sent = True
    db.session.commit()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

items = [
    {"name": "Yellow Daal 1kg", "price":79 , "image_url": "/static/images/yellow_dall.jpg"},
    {"name": "Fortune Mogra Basmati Rice 5kg", "price": 525, "image_url": "/static/images/fortune_mogra_basmati_rice.jpg"},
    {"name": "Maggi", "price": 15, "image_url": "/static/images/maggi.jpg"},
    {"name": "Amul Cheese 250gm", "price": 249, "image_url": "/static/images/amul_cheese.jpg"},
    {"name": "Dawat Basmati Rice 5kg", "price": 449, "image_url": "/static/images/Daawat_basmiti_rice.jpg"},
    {"name": "Fortune Basmati Rice 5kg", "price": 429, "image_url": "/static/images/Fortune_basmati_rice.jpg"},
    {"name": "Aashirvaad Seleted Aata 5kg", "price": 399, "image_url": "/static/images/Aashirwad_seleted_aata.jpg"},
    {"name": "Everest Kasuri Methi", "price": 30, "image_url": "/static/images/Everest_kasuri_methi.jpg"},
    {"name": "Amul Malai Paneer 150gm", "price": 249, "image_url": "/static/images/amul_malai_paneer.jpg"},
    {"name": "Amul Masti", "price": 10, "image_url": "/static/images/amul_Masti.jpg"},
    {"name": "Amul Milk 500ml", "price": 27, "image_url": "/static/images/amul_taza_milk.jpg"},
    {"name": "Fortune Indori Poha 1kg", "price": 49, "image_url": "/static/images/Fortune_indori_poha.jpg"},
    {"name": "Fortune Sunlite Oil 5kg", "price": 649, "image_url": "/static/images/Fortune_sun_light_5L.jpg"},
    {"name": "Silver Coin Aata 5kg", "price":379 , "image_url": "/static/images/seliver_coin_aata_5kg.jpg"},
    {"name": "Sunday Sunflower Oil 1kg", "price": 119, "image_url": "/static/images/Sunday_sunflower_oil.jpg"},
    {"name": "Tata Salt 1kg", "price": 60, "image_url": "/static/images/Tata_salt.jpg"},
    {"name": "Tata Sampann Poha 850gm", "price": 35, "image_url": "/static/images/Tata_Sampan_poha.jpg"},
    {"name": "Lizol 2L", "price": 70, "image_url": "/static/images/Lizol.jpg"}, 
    {"name": "Surf Excel 100gm", "price": 12, "image_url": "/static/images/Surf_Excel.jpg"},
    {"name": "Sunfeast Bounce buiscuit ", "price": 50, "image_url": "/static/images/1.jpg"},
    {"name": "Vita marie gold ", "price": 155, "image_url": "/static/images/2.jpg"},
    {"name": "Britiania 5050 Maska Chaska ", "price": 10, "image_url": "/static/images/3.jpg"},
    {"name": "Britiania Little Hearts Buiscuit", "price": 10, "image_url": "/static/images/4.jpg"},
    {"name": "Britiania Bourboun Buiscuit", "price": 40, "image_url": "/static/images/5.jpg"},
    {"name": "Maggie Tomato Ketchup", "price": 149, "image_url": "/static/images/6.jpg"},
    {"name": "Kissan Mixed Fruit Jam", "price": 220, "image_url": "/static/images/7.jpg"},
    {"name": "Everest Kitchen king Masala 500 gm", "price": 445, "image_url": "/static/images/8.jpg"},
    {"name": "Everest Chat Masala ", "price": 105, "image_url": "/static/images/9.jpg"},
    {"name": "Everest White Pepper 100 gm ", "price": 125, "image_url": "/static/images/10.jpg"},
    {"name": "Everest Hingraj Powder 100 gm ", "price":109 , "image_url": "/static/images/11.jpg"},
       {"name": " Everest Dry Mango Powder 100gm", "price": 89, "image_url": "/static/images/12.jpg"},
{"name": "Everest Cummin Powder 100gm", "price":167 , "image_url": "/static/images/13.jpg"},
{"name": " Catch Turmeric Powder 1kg", "price":400 , "image_url": "/static/images/14.jpg"},
{"name": " Everest Corrainder 500gm ", "price": 380, "image_url": "/static/images/15.jpg"},
{"name": " Everest Kashmirilal Mirchi powder 100gm", "price":60 , "image_url": "/static/images/16.jpg"},
{"name": "Amul Garlic Butter  100gm ", "price":70 , "image_url": "/static/images/17.jpg"},
{"name": " Amul Butter 2x100gm", "price":100 , "image_url": "/static/images/18.jpg"},
{"name": "Mother Dairy Classic Dahi  4x200gm ", "price":100 , "image_url": "/static/images/19.jpg"},
{"name": " Mother Dairyu Mioshti Doi 2x400gm", "price":140 , "image_url": "/static/images/20.jpg"},
{"name": " Nandani Curd ", "price":55 , "image_url": "/static/images/21.jpg"},
{"name": " Amul Malai Paneer 200gm", "price":82 , "image_url": "/static/images/22.jpg"},
{"name": " Amul Malai Paneer frozen 3x200gm", "price": 267, "image_url": "/static/images/23.jpg"},
{"name": " Amul Fresh Cream 1l ", "price": 220, "image_url": "/static/images/24.jpg"},
{"name": " Nandani Milk 500ml", "price":35 , "image_url": "/static/images/25.jpg"},
{"name": " Amul Taaza Milk 12x200ml", "price":180 , "image_url": "/static/images/26.jpg"},
{"name": "Cavins Lassi 4x180ml ", "price": 95, "image_url": "/static/images/27.jpg"},
{"name": " Amul Masti Mutter milk 6x200ml", "price": 85, "image_url": "/static/images/28.jpg"},
]

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    results = [item for item in items if query in item['name'].lower()]
    return render_template('search_results.html', query=query, results=results)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        form_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'confirm_password': request.form.get('confirm_password'),
            'phone': request.form.get('phone')
        }
        if form_data['password'] != form_data['confirm_password']:
            flash('Passwords do not match')
            return render_template('create_account.html')
        existing_user = User.query.filter_by(email=form_data['email']).first()
        if existing_user:
            flash('Email already exists')
            return render_template('create_account.html')
        try:
            new_user = User.create_user(
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data['email'],
                password=form_data['password'],
                phone=form_data['phone']
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account created successfully!')
            return redirect(url_for('home'))
        except ValueError as ve:
            flash(str(ve))
        except Exception as e:
            db.session.rollback()
            flash(f'An unexpected error occurred. Please try again.')
            app.logger.error(f"Error creating user: {str(e)}")
    return render_template('create_account.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    if 'cart' not in session:
        session['cart'] = {}
    elif isinstance(session['cart'], list):
        # Convert existing list to dictionary
        cart_dict = {}
        for item in session['cart']:
            if item['name'] in cart_dict:
                cart_dict[item['name']]['quantity'] += 1
            else:
                cart_dict[item['name']] = item.copy()
                cart_dict[item['name']]['quantity'] = 1
        session['cart'] = cart_dict

    quantity = int(request.form.get('quantity', 1))
    item = items[item_id]
    
    if item['name'] in session['cart']:
        session['cart'][item['name']]['quantity'] += quantity
    else:
        session['cart'][item['name']] = {
            'id': item_id,
            'name': item['name'],
            'price': item['price'],
            'image_url': item['image_url'],
            'quantity': quantity
        }
    
    session.modified = True
    flash(f'{quantity} {item["name"]}(s) added to cart successfully!')
    return redirect(url_for('search'))

@app.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', {})
    cart_total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)

@app.route('/update_cart_quantity/<item_name>', methods=['POST'])
@login_required
def update_cart_quantity(item_name):
    quantity = int(request.form.get('quantity', 1))
    if 'cart' in session and item_name in session['cart']:
        session['cart'][item_name]['quantity'] = quantity
        session.modified = True
        flash(f'Quantity updated for {item_name}')
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<item_name>', methods=['POST'])
@login_required
def remove_from_cart(item_name):
    if 'cart' in session and item_name in session['cart']:
        del session['cart'][item_name]
        session.modified = True
        flash(f'{item_name} removed from cart.')
    return redirect(url_for('cart'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='email-confirm')
            msg = Message('Password Reset Request', 
                          recipients=[email])
            link = url_for('reset_password', token=token, _external=True)
            msg.body = f'Your password reset link is {link}'
            try:
                mail.send(msg)
                flash('Password reset instructions sent to your email')
            except Exception as e:
                app.logger.error(f"Error sending email: {str(e)}")
                flash('An error occurred while sending the email. Please try again later.')
        else:
            flash('Email not found')
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)  # Token expires after 1 hour
    except SignatureExpired:
        flash('The password reset link has expired.')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        new_password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password successfully reset')
            return redirect(url_for('login'))
    return render_template('reset_password.html')

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = session.get('cart', {})
    cart_total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    cart_total_paise = int(cart_total)  # Convert to paise

    if not cart_items:
        flash('Your cart is empty. Please add items before checking out.', 'warning')
        return redirect(url_for('cart'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        payment_method = 'cash_on_delivery'

        if not all([name, email, address, city, state, zipcode]):
            flash('Please fill in all required fields', 'error')
            return render_template('checkout.html', cart_items=cart_items, cart_total=cart_total)

        # Create a new order
        new_order = Order(
            user_id=current_user.id,
            total_amount=cart_total_paise,
            shipping_address=f"{address}, {city}, {state} {zipcode}",
            payment_method=payment_method,
            status='Pending'
        )

        # Add order items
        for item in cart_items.values():
            order_item = OrderItem(
                product_name=item['name'],
                quantity=item['quantity'],
                price=int(item['price'])  # Convert to paise
            )
            new_order.items.append(order_item)

        try:
            db.session.add(new_order)
            db.session.commit()
            
            # Send email notification
            send_order_email(new_order)
            
            # Clear the cart after successful checkout
            session.pop('cart', None)

            flash('Order placed successfully! You will pay cash on delivery.', 'success')
            return redirect(url_for('order_confirmation', order_id=new_order.id))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while processing your order: {str(e)}', 'error')
            return render_template('checkout.html', cart_items=cart_items, cart_total=cart_total)

    return render_template('checkout.html', cart_items=cart_items, cart_total=cart_total)

@app.route('/order_confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You do not have permission to view this order.', 'error')
        return redirect(url_for('home'))
    return render_template('order_confirmation.html', order=order)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)