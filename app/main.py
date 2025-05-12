from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nm = request.form['nomeF']
        email = request.form['emailF']
        psswrd = request.form['psswdF']
        cred = request.form['credF']
        
        new_user = User(nm=nm, email=email, psswrd=psswrd, cred=cred)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

