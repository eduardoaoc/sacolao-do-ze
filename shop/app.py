from flask import Flask, render_template


app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

@app.route('/')
def index():
    return render_template('cliente/login.html')

@app.route('/i')
def teste():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    