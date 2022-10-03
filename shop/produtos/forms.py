from flask_wtf.file import FileAllowed, FileField
from wtforms import IntegerField, StringField, TextAreaField, Form, validators, DecimalField

class Addproducts(Form):
    name= StringField('Nome',[validators.DataRequired()])
    price= DecimalField('Preço',[validators.DataRequired()])
    discount= IntegerField('Desconto', default=0)
    stock= IntegerField('Quantidade', [validators.DataRequired()])
    discription= TextAreaField('Descrição', [validators.DataRequired()])

    image_1= FileField('Imagem 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_2= FileField('Imagem 2', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_3= FileField('Imagem 3', validators=[FileAllowed(['jpg','png','gif','jpeg'])])

    calorias= DecimalField('Calorias (Kcal)',[validators.DataRequired()]) 
    proteinas= DecimalField('Proteínas',[validators.DataRequired()])
    carboidrato= DecimalField('Carboidratos',[validators.DataRequired()])
    fibra= DecimalField('Fibra',[validators.DataRequired()])
    fat= DecimalField('Gordura',[validators.DataRequired()])
    sodio= DecimalField('Sódio',[validators.DataRequired()])
    
