from flask import redirect, render_template, url_for, flash, request, session, current_app
import secrets, os 
from flask_login import login_required, current_user, logout_user, login_user

from shop import db, app, photos, produtos, search, bcrypt, login_manager
from shop.admin.routes import category
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder


#cadastro de clientes
@app.route('/register', methods=['GET', 'POST'])
def customer_register():
    form= CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password= bcrypt.generate_password_hash(form.password.data)
        register= Register(
        name=form.name.data, username=form.username.data,
        email=form.email.data, password=hash_password, 
        city=form.city.data, address=form.address.data
        )
        db.session.add(register)
        flash(f'Bem-vindo {form.name.data}. Obrigado por cadastrar-se!','success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)

#login cliente
@app.route('/login', methods=['GET', 'POST'])
def customerLogin():
    form= CustomerLoginForm()
    if form.validate_on_submit():
        user= Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next= request.args.get('next')
            return redirect(next or url_for('home'))
        else:    
            flash('E-mail e senha incorretos. Tente novamente','danger')  
            return redirect(url_for('customerLogin'))  
    return render_template('customer/login.html', form=form)

#logout cliente
@app.route('/logout')
def customerLogout():
    logout_user()
    flash('Você foi desconectado.','success')
    return redirect(url_for('home'))

#orçamento
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id= current_user.id
        invoice= secrets.token_hex(5)
        try:
            order= CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Seu pedido foi enviado com sucesso.','success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Alguma coisa deu errado.','danger')
            return redirect(url_for('getCart'))

#orçamento
@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal= 0
        subTotal=0
        customer_id= current_user.id
        customer= Register.query.filter_by(id=customer_id).first()
        orders= CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
           discount= (product['discount'] / 100) * float(product['price']) 
           subTotal += float(product['price']) * int(product['quantity'])
           subTotal -= discount
           tax=("%.2f" % (.06 * float(subTotal)))
           grandTotal= float("%.2f" % (1.06 * subTotal))

    else:
        return redirect(url_for('customerLogin'))    
    return render_template('cliente/order.html', invoice=invoice, 
    tax=tax, subTotal=subTotal, grandTotal=grandTotal, customer=customer, orders=orders)  