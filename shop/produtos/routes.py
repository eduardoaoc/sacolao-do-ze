from flask import redirect, render_template, url_for, flash, request, current_app
import secrets, os

from shop import  db, app, photos, produtos, search
from shop.admin.routes import category
from .models import Category, AddProduct
from .forms import Addproducts

def categories():
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    return categories

@app.route('/')
def home():
    page= request.args.get('page', 1, type=int)
    products= AddProduct.query.filter(AddProduct.stock > 0).order_by(AddProduct.id.desc()).paginate(page=page, per_page=10)
    return render_template('produtos/index.html', products=products, categories=categories())

@app.route('/result')
def result():
    searchword= request.args.get('q')
    products= AddProduct.query.msearch(searchword, fields=['name', 'desc'], limit=6)
    return render_template('produtos/resultados.html', products=products, categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product= AddProduct.query.get_or_404(id)
    return render_template('produtos/single_page.html', product=product, categories=categories())

@app.route('/categories/<int:id>')
def get_category(id):
    page= request.args.get('page', 1, type=int)
    get_cat= Category.query.filter_by(id=id).first_or_404()
    get_cat_prod= AddProduct.query.filter_by(category=get_cat).paginate(page=page, per_page= 6)
    return render_template('produtos/categorias.html', get_cat_prod=get_cat_prod, categories=categories(),  get_cat=get_cat)



'''------ADMIN -  COMANDS URLs------'''
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    '''if 'email' not in session:
        flash(f'Por favor, conect-se primeiro.', 'danger')
        return redirect(url_for('login'))'''
        
    if request.method== 'POST':
        getcat= request.form.get('category')
        cat= Category(name=getcat)
        db.session.add(cat)
        flash(f"A categoria '{getcat}' foi adicionada ao banco de dados.", 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('produtos/addcat.html')    

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
    return render_template('produtos/updatecategory.html', title='Update category page', updatecat=updatecat)            

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
        flash(f"A categoria '{category.name}' foi removida do banco de dados.", 'success')
    except:
        flash(f'Ocorreu algum erro.','danger')    
    return redirect(url_for('category'))
  
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

        calorias= form.calorias.data
        proteinas= form.proteinas.data
        carboidrato= form.carboidrato.data
        fibra= form.fibra.data
        fat= form.fat.data
        sodio= form.sodio.data

        addpro= AddProduct(name=name,price=price,discount=discount, stock=stock, 
        desc=desc, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3, calorias=calorias,
        proteinas=proteinas, carboidrato=carboidrato, fibra=fibra, fat=fat, sodio=sodio)
        db.session.add(addpro)
        flash(f"O produto '{name}' foi adicionado ao banco de dados.", 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('produtos/addproduto.html' , title='Add product page', form=form, categories=categories)    

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
        
        product.calorias= form.calorias.data
        product.proteinas= form.proteinas.data
        product.carboidrato= form.carboidrato.data
        product.fibra= form.fibra.data

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
    
    form.calorias.data= product.calorias
    form.proteinas.data= product.proteinas
    form.carboidrato.data= product.carboidrato
    form.fibra.data= product.fibra 

    return render_template('produtos/updateproduto.html', form=form, categories=categories, product=product)

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
    flash(f"O produto '{product.name}' foi removido do banco de dados.", 'success')
    return redirect(url_for('admin'))
 

''''teste consumo de api externa'''
import requests

url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"

querystring = {"ingr":"apple" }

res= {"hints":"nutrients"}

'''label:''Apple', 'nutrients': {'ENERC_KCAL': 52.0, 'PROCNT': 0.26, 'FAT': 0.17, 'CHOCDF': 13.81, 'FIBTG': 2.4}'''

headers = {
	"X-RapidAPI-Key": "f4906a3716mshc557dfb66b7a3e0p1acf2cjsn6ededaaf0dec",
	"X-RapidAPI-Host": "edamam-food-and-grocery-database.p.rapidapi.com"
}

responses = requests.request("GET", url, headers=headers, params=querystring)
r= responses.json()


@app.route('/response')
def response():
    return r['food']


