from flask import Blueprint, render_template,flash, redirect, request
from .models import Product, Cart
from flask_login import login_required, current_user
from . import db
views = Blueprint('views', __name__)

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