from shop import db
from datetime import datetime


class AddProduct(db.Model):   
    __searchable__= ['name','desc']
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), nullable=False)
    price= db.Column(db.Numeric(10,2), nullable=False) 
    discount= db.Column(db.Integer, default=0)
    stock= db.Column(db.Integer, nullable=False)
    desc= db.Column(db.Text, nullable=False)
    pub_date= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    category_id= db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category= db.relationship('Category', backref=db.backref('categories', lazy=True))

    image_1= db.Column(db.String(150),nullable=False, default='image.jpg')
    image_2= db.Column(db.String(150),nullable=False, default='image.jpg')
    image_3= db.Column(db.String(150),nullable=False, default='image.jpg')

    calorias= db.Column(db.Numeric(10,2), nullable=False) 
    proteinas= db.Column(db.Numeric(10,2), nullable=False) 
    carboidrato= db.Column(db.Numeric(10,2), nullable=False) 
    fibra= db.Column(db.Numeric(10,2), nullable=False) 
    fat= db.Column(db.Numeric(10,2), nullable=False) 
    sodio= db.Column(db.Numeric(10,2), nullable=False) 

    def __repr__(self):
        return '<AddProduct %r>' % self.title

class Category(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return '<Category %r>' % self.title

db.create_all()
