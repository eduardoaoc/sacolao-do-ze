from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField

class RegistrationForm(Form):
    username= StringField('Username', [validators.Length(min=4, max=25)])
    name= StringField('Nome', [validators.Length(min=4, max=25)])
    email= StringField('Email', [validators.Length(min=9, max=35), validators.Email()])
    password= PasswordField('Senha',[
        validators.Length(min=6, max=30),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='As senhas devem corresponder.')
    ])
    confirm= PasswordField('Confirme sua senha')
    submit= SubmitField('Cadastrar')


class LoginForm(Form):
    email= StringField('Email:',[validators.Length(min=6, max=35), validators.Email()])
    password= PasswordField('Senha:', [ validators.Length(min=6, max=30), validators.DataRequired()])
    