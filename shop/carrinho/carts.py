from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import app

from shop import db
from shop.produtos.models import AddProduct
from shop.produtos.routes import *


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

#metodo para adicionar um produto ao carrinho
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = AddProduct.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method=='POST':
            DictItems = {product_id: {'name': product.name, 'price':float(product.price), 'discount': product.discount,  
            'quantity': quantity, 'image': product.image_1}}
            if 'Shoppingcart' in session:
                if product_id in session['Shoppingcart']:
                    for key , item in session['Shoppingcart'].items():
                        print(key, item)
                        if int(key) == int(product_id):
                            session.modified = True 
                            qnt = int(item['quantity'])
                            qnt +=1
                            item['quantity'] = qnt
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

#página do carrinho de compras 
@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
         return render_template('produtos/carrinho_limpo.html')
    categories= Category.query.join(AddProduct, (Category.id==AddProduct.category_id)).all()
    subtotal=0
    total=2    
    for key , product in session['Shoppingcart'].items():
        discount= (product['discount']/100) * float(product['price'])
        subtotal+= float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax= ("%.2f" % (.06 * float(subtotal)))
        total= float("%.2f" % (1.06 * subtotal))
    return render_template('produtos/carrinho.html', categories=categories, total=total, tax=tax)    


#carrinho vázio
@app.route('/cartclear')
def empty_cart():
    return render_template('produtos/carrinho_limpo.html')
  

#atualiza os produtos do carrinho
@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('cartclear'))
    if request.method == 'POST':
        quantity= request.form.get('quantity')
        color= request.form.get('color')
        try:
            session.modified= True
            for key, item in session['Shoppingcart'].items():
                if int(key)== code:
                    item['quantity']= quantity
                    item['color']= color
                    flash('Item is updated.')
                    return redirect(url_for('getCart'))      
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))      


#remove produtos do carrinho
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('cartclear'))
    try:
        session.modified= True
        for key, item in session['Shoppingcart'].items():
            if int(key)== id:
                session['Shoppingcart'].pop(key, None)
                flash('Item removido com sucesso.')
                return redirect(url_for('getCart'))     
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))        

#limpar carrinho
@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return render_template('produtos/carrinho_limpo.html')
    except Exception as e:
        print(e)    