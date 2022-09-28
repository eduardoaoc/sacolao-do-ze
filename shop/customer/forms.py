from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm
from .models import Register

class CustomerRegisterForm(FlaskForm):
    name= StringField('Nome Completo:', [validators.Length(min=5, max=35)])
    username= StringField('Usuário:', [validators.Length(min=5, max=35)])
    email= StringField('Email:', [validators.Email(), validators.DataRequired(), validators.Length(min=9, max=35)])
    password= PasswordField('Senha:', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match.'), validators.Length(min=6, max=30)])
    confirm= PasswordField('Confirmar Senha:', [validators.DataRequired(), validators.Length(min=6, max=30)])
    city= StringField('Cidade:', [validators.DataRequired(), validators.Length(max=30)])
    address= StringField('Endereço:', [validators.DataRequired(), validators.Length(max=30)])
    contact= StringField('Telefone:', [validators.DataRequired(), validators.Length(max=30)])
    submit= SubmitField('Cadastrar')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('Esse nome de usuário já está em uso.')

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('Esse e-mail já está em uso')        


class CustomerLoginForm(FlaskForm):
    email= StringField('Email:', [validators.Email(), validators.DataRequired(), validators.Length(max=35)])
    password= PasswordField('Senha:', [validators.DataRequired(), validators.Length(max=35)])
    submit= SubmitField('Login')
    