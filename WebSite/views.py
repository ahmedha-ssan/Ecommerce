from flask import Blueprint, render_template,flash, redirect, request, jsonify
from .models import Product, Cart, Order
from flask_login import login_required, current_user
from . import db
from intasend import APIService

views = Blueprint('views', __name__)
API_PUBLISHABLE_KEY = 'ISPubKey_test_36e68075-1329-49a4-85c0-4e3df1319d7a'
API_TOKEN= 'ISSecretKey_test_d3f9c963-6aa2-4640-a7c9-673fd004e97a'


@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True)
    return render_template('home.html', items =items, cart = Cart.query.filter_by(customer_link = current_user.id).all()
    if current_user.is_authenticated else [])

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.qyantity = item_exists.qyantity + 1
            db.session.commit()
            flash(f'Quantity of { item_exists.product.product_name } has been updated')
            return redirect(request.referrer)
        except Exception as e:
            flash(f'Quantity of { item_exists.product.product_name } not updated')
            return redirect(request.referrer)

    new_cart_items = Cart()
    new_cart_items.qyantity = 1
    new_cart_items.product_link = item_to_add.id
    new_cart_items.customer_link = current_user.id

    try:
        db.session.add(new_cart_items)
        db.session.commit()
        flash(f'{new_cart_items.product.product_name} added to cart')
    except Exception as e:
        flash(f'{new_cart_items.product.product_name} has not been added to cart')
    return redirect(request.referrer)

@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount+= item.product.current_price*item.qyantity
    return render_template('cart.html',cart=cart, amount=amount,total=amount+200)

@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        if cart_item.qyantity < cart_item.product.in_stock:
            cart_item.qyantity += 1 
            db.session.commit()
            cart = Cart.query.filter_by(customer_link=current_user.id).all()
            amount = 0
            for item in cart:
                amount += item.product.current_price * item.qyantity
            data = {
                'qyantity': cart_item.qyantity,
                'amount': amount,
                'total': amount + 200
            }
            return jsonify(data)
        else:
            return jsonify({'message': 'Cannot exceed available quantity'})


@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        if cart_item.qyantity > 0:
            cart_item.qyantity -= 1
            db.session.commit()
            cart = Cart.query.filter_by(customer_link=current_user.id).all()
            amount = 0
            for item in cart:
                amount += item.product.current_price * item.qyantity
            data = {
                'qyantity': cart_item.qyantity,
                'amount': amount,
                'total': amount + 200
            }
            return jsonify(data)
        else:
            return jsonify({'message': 'Quantity is already at 0'})

@views.route('/removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = 0
        for item in cart:
            amount += item.product.current_price * item.qyantity
        data = {
            'qyantity': cart_item.qyantity,
            'amount': amount,
            'total': amount + 200
        }
        return jsonify(data) 

@views.route('/place-order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id)
    if customer_cart:
        try:
            total = 0
            for item in customer_cart:
                total += item.product.current_price * item.qyantity

            service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
            create_order_response = service.collect.mpesa_stk_push(phone_number='25401128793', email=current_user.email,amount=total + 200, narrative='Purchase of goods')

            for item in customer_cart:
                new_order = Order()
                new_order.qyantity = item.qyantity
                new_order.price = item.product.current_price
                new_order.status = create_order_response['invoice']['state'].capitalize()
                new_order.payment_id = create_order_response['id']

                new_order.product_link = item.product_link
                new_order.customer_link = item.customer_link

                db.session.add(new_order)

                product = Product.query.get(item.product_link)

                product.in_stock -= item.qyantity
                db.session.delete(item)
                db.session.commit()
            flash('Order Placed Successfully')
            return redirect('/orders')     
        except Exception as e:
            print(e)
            flash('Order not placed')
            return redirect('/')
    else:
        flash('Your cart is Empty')
        return redirect('/')


@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    
    return render_template('orders.html', orders=orders)






@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                        if current_user.is_authenticated else [])

    return render_template('search.html')