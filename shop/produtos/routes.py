from flask import redirect, render_template, url_for, flash, request, session, current_app
import secrets, os

from shop import app 
from shop import db, photos, search
from shop.admin.routes import category
from .models import Category, AddProduct
from .forms import Addproducts


#página inicial/ todos produtos
@app.route('/')
def home():
    page= request.args.get('page', 1, type=int)
    products= AddProduct.query.filter(AddProduct.stock > 0).order_by(AddProduct.id.desc()).paginate(page=page, per_page= 8)
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    return render_template('produtos/index.html', products=products, categories=categories)

#pequisa de produtos, etc.
@app.route('/result')
def result():
    searchword= request.args.get('q')
    products= AddProduct.query.msearch(searchword, fields=['name', 'desc'], limit=6)
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    return render_template('produtos/resultados.html', products=products, categories=categories)

#página individual de um produto
@app.route('/product/<int:id>')
def single_page(id):
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    product= AddProduct.query.get_or_404(id)
    return render_template('produtos/single_page.html', product=product, categories=categories)

#página de produtos por categoria
@app.route('/categories/<int:id>')
def get_category(id):
    page= request.args.get('page', 1, type=int)
    get_cat= Category.query.filter_by(id=id).first_or_404()
    get_cat_prod= AddProduct.query.filter_by(category=get_cat).paginate(page=page, per_page= 6)
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    return render_template('produtos/index.html', get_cat_prod=get_cat_prod, categories=categories, get_cat=get_cat)



'''------ADMIN COMANDS URLs------'''
#adiciona uma categoria
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    '''if 'email' not in session:
        flash(f'Por favor, conect-se primeiro.', 'danger')
        return redirect(url_for('login'))'''
        
    if request.method== 'POST':
        getcat= request.form.get('category')
        cat= Category(name=getcat)
        db.session.add(cat)
        flash(f'A categoria {getcat} foi adicionada ao banco de dados.', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('produtos/addcat.html')    

#atualiza uma categoria selecionada
@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    '''if 'email' not in session:
        flash(f'Por favor, conect-se primeiro.', 'danger')
        return redirect(url_for('login'))'''
        
    updatecat= Category.query.get_or_404(id)
    category= request.form.get('category')

    if request.method== 'POST':
        updatecat.name= category
        flash(f'A categoria foi atualizada.','success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatecat.html', title='Update category page', updatecat=updatecat)            

#remove uma categoria
@app.route('/deletecat/<int:id>')
def deletecat(id):
    '''if 'email' not in session:
        flash(f'Por favor, conect-se primeiro.', 'danger')
        return redirect(url_for('login'))'''
        
    category= Category.query.filter_by(id=id).first()
    try:
        db.session.delete(category)
        db.session.commit()
        flash(f'A categoria {category.name} foi removida do banco de dados..', 'success')
    except:
        flash(f'An error ocurred','danger')    
    return redirect(url_for('category'))
  
#adiciona um produto
@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    '''if 'email' not in session:
        flash(f'Por favor, conect-se primeiro.', 'danger')
        return redirect(url_for('login'))'''
        
    categories= Category.query.all()
    form= Addproducts(request.form)

    if request.method =='POST':
        name= form.name.data
        price= form.price.data
        discount= form.discount.data
        stock= form.stock.data
        desc= form.discription.data
        category= request.form.get('category')

        image_1=photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
        image_2=photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
        image_3=photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')

        addpro= AddProduct(name=name,price=price,discount=discount, stock=stock, 
        desc=desc, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'O produto {name} foi adicionado ao banco de dados.', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('produtos/addproduto.html' , title='Add product page', form=form, categories= categories)    

#atualiza o produto selicionado
@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    '''if 'email' not in session:
        flash(f'Por favor, conect-se primeiro.', 'danger')
        return redirect(url_for('login'))'''
        
    categories= Category.query.all()
    product= AddProduct.query.get_or_404(id)
    category= request.form.get('category')
    form= Addproducts(request.form)

    if request.method == 'POST':
        product.name= form.name.data
        product.price= form.price.data
        product.discount= form.discount.data
        product.category_id= category
        product.desc= form.discription.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))  
                product.image_1=  photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')  
            except:
                product.image_1=  photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')  
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))  
                product.image_1=  photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')  
            except:
                product.image_1=  photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')  

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))  
                product.image_1=  photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')  
            except:
                product.image_1=  photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')  

        db.session.commit()
        flash(f'O produto foi atualizado.', 'success')
        return redirect(url_for('admin'))

    form.name.data= product.name
    form.price.data= product.price
    form.discount.data= product.discount
    form.stock.data= product.stock
    form.discription.data= product.desc 
    return render_template('produtos/updateproduto.html', form=form, categories=categories, product=product)

#remove um produto
@app.route('/deleteproduct/<int:id>')
def deleteproduct(id):
    '''if 'email' not in session:
        flash(f'Por favor, conect-se primeiro.', 'danger')
        return redirect(url_for('login'))'''
        
    product= AddProduct.query.filter_by(id=id).first()
    try:
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))  
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))  
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))  
    except Exception as e:
        print(e)
        flash(f'Ocorreu algum erro.','danger')    
    db.session.delete(product)
    db.session.commit()
    flash(f'The product {product.name} was deleted from your database.', 'success')
    return redirect(url_for('admin'))
