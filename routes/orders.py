from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from models import db, Order, OrderItem, Product

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    order = Order.query.filter_by(user_id = current_user.id, is_paid = False).first()
    if not order:
        order = Order(user_id = current_user.id, total_amount = 0, is_paid = False)
        db.session.add(order)
        db.session.commit()
    order_item = OrderItem.query.filter_by(order_id = order.id, product_id = product_id).first()
    if order_item:
        order_item.quantity += 1
    else:
        order_item = OrderItem(order_id = order.id, product_id = product.id, quantity= 1, price = product.price)
        db.session.add(order_item)
    order.total_amount += product.price
    db.session.commit()
    return redirect(url_for('orders.cart'))

@orders_bp.route('/cart')
@login_required
def cart():
    order = Order.query.filter_by(user_id = current_user.id, is_paid = False).first()
    return render_template('cart.html', order = order)

@orders_bp.route('/checkout', methods = ['GET','POST'])
@login_required
def checkout():
    order = Order.query.filter_by(user_id = current_user.id, is_paid = False).first()
    if request.method == 'POST':
        order.is_paid = True
        db.session.commit()
        return redirect(url_for('orders.order_confirmation', order_id=order.id))
    return render_template('checkout.html', order=order)

@orders_bp.route('/order_confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)
