from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, Form, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register

class CustomerRegisterForm(FlaskForm):
    name= StringField('Nome Completo:')
    username= StringField('Usuário:')
    email= StringField('Email:', [validators.Email(), validators.DataRequired()])
    password= PasswordField('Senha:', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match.')])
    confirm= PasswordField('Confirmar Senha:', [validators.DataRequired()])
    city= StringField('Cidade:', [validators.DataRequired()])
    address= StringField('Endereço:', [validators.DataRequired()])
    contact= StringField('Telefone:', [validators.DataRequired()])

    submit= SubmitField('Cadastrar')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already in use!')

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('This email is already in use!')        


class CustomerLoginForm(FlaskForm):
    email= StringField('Email:', [validators.Email(), validators.DataRequired()])
    password= PasswordField('Senha:', [validators.DataRequired()])
    submit= SubmitField('Login')
    