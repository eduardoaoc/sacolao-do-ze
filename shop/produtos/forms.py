from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField, StringField, BooleanField, TextAreaField, Form, validators, DecimalField

class Addproducts(Form):
    name= StringField('Nome',[validators.DataRequired()])
    price= DecimalField('Preço',[validators.DataRequired()])
    discount= IntegerField('Desconto', default=0)
    stock= IntegerField('Quantidade', [validators.DataRequired()])
    discription= TextAreaField('Descrição', [validators.DataRequired()])

    image_1= FileField('Image 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_2= FileField('Image 2', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_3= FileField('Image 3', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    