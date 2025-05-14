from flask import Flask, render_template, request, url_for, redirect, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import werkzeug
import werkzeug.exceptions
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User
from werkzeug.exceptions import HTTPException, NotFound
import hashlib
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import *



app = Flask(__name__)
app.secret_key = 'geofarm'
lm = LoginManager(app)
lm.login_view = 'login'

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
#db.init_app(app)





def Hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()


# filtra o user pelo id no bd
@lm.user_loader
def user_loader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user



# landing page
@app.route('/')
def index():
    return render_template('index.html')

# pagina de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        email = request.form['emailF']
        psswrd = request.form['psswdF']

        user = db.session.query(User).filter_by(email=email, psswrd=hash(psswrd)).first()

        
        if not user:
           return werkzeug.exceptions.NotFound(description='Email ou Senha Invalidos', response=None)
        
        
        login_user(user)
        return redirect(url_for('home'))


# pagina inicial da plataforma
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


# botão de logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# rota para vizualizar o geotiff
@app.route('/geotiff', methods=['GET'])
def geotiff():
    if request.method == 'GET':
        return render_template('geotiff.html')


# rota para se cadastrar na plataforma
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nm = request.form['nomeF']
        email = request.form['emailF']
        psswrd = request.form['psswdF']
        cred = request.form['credF']
        
        new_user = User(nm=nm, email=email, psswrd=hash(psswrd), cred=cred)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('home'))


# main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

