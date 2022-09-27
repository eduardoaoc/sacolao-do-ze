from flask import render_template, session, request, redirect, url_for, flash
from shop import app

from shop import db, bcrypt
from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User
from shop.produtos.models import AddProduct, Category


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Por favor, conecte-se primeiro.', 'danger')
        return redirect(url_for('login'))
    products = AddProduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/category')
def category():
    '''if 'email' not in session:
        flash(f'Por favor, conecte-se primeiro.', 'danger')
        return redirect(url_for('login'))'''
    categories=  Category.query.order_by(Category.id.desc()).all()  
    return render_template('admin/cat.html', title='Category page', categories=categories)

@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Bem-vindo, {form.name.data}. Obrigado pro cadastrar-se.', 'success')
        return render_template('admin/login.html', form=form)
    return render_template('admin/register.html', form=form, title='Registration page')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data 
            flash(f"Bem-vindo, '{form.email.data}' Você está conectado.", 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Senha ou e-mail errado, por favor tente novamente.', 'danger')
    return render_template('admin/login.html', form=form, title='Login Page')

@app.route('/admin/logout')
def adminLogout():
    if 'email' not in session:
        flash('Ocorreu algum erro.','danger') 
        return redirect(url_for('admin'))
    elif 'email' in session:
            session.pop('email')
            flash('Você foi desconectado.','success')
            return redirect(url_for('login'))
                