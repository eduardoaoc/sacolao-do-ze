from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username= StringField('Username', [validators.Length(min=4, max=25)])
    name= StringField('Nome', [validators.Length(min=4, max=25)])
    email= StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    password= PasswordField('Senha',[
        validators.DataRequired(),
        validators.EqualTo('Confirme', message='As senhas devem corresponder.')
    ])
    confirm= PasswordField('Confirme sua senha.')

class LoginForm(Form):
    email= StringField('Email:',[validators.Length(min=6, max=35), validators.Email()])
    password= PasswordField('Senha:', [validators.DataRequired()])
    