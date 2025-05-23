from flask import Flask, render_template, request, url_for, redirect, abort, flash, render_template_string
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from sqlalchemy import select
from models import User
from werkzeug.exceptions import HTTPException, NotFound
import hashlib
from flask_mail import Message, Mail
#from flask_mailman import EmailMessage
from flask_login import current_user, confirm_login, login_user
from forms import ResetPsswrdRequestForm, ResetPasswordForm
from templates.auth.reset_password_email_content import (
    reset_password_email_html_content
)
from dotenv import load_dotenv
import os





app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
lm = LoginManager(app)
lm.login_view = 'login'


load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

# email config - verificar o numero de telefone na conta 
mail_settings = {
    "MAIL_SERVER": os.getenv('MAIL_SERVER'),
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.getenv('MAIL_PASSWORD')

}

app.config.update(mail_settings)
mail = Mail(app)

# envia email de recuperação de senha
def send_mail(user):
    reset_psswrd_url = url_for("reset_password",
                               token=user.generate_reset_password_token(),
                               user_id=user.id,
                               _external=True,
                               )
    email_body=render_template_string(
        reset_password_email_html_content, reset_psswrd_url=reset_psswrd_url
    ) 
    message = Message(
        subject="Reset your Password",
        recipients=[user.email],
        html=email_body
    )
    message.content_subtype = "html"
    mail.send(message)

# transforma a senha em hash
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

        user = db.session.query(User).filter_by(email=email, psswrd=Hash(psswrd)).first()
        error = 'Invalid credentials'     
        
        if not user:
           return error
                
        
        
        login_user(user)
        return redirect(url_for('home'))


# rota para recuperar a senha 
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_psswrd_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = ResetPsswrdRequestForm()

    if form.validate_on_submit():
        user_select = select(User).where(User.email == form.email.data)
        user = db.session.scalar(user_select)

        if user:
            send_mail(user)

            flash(
                "Instructions to reset your password were sent to your email address,"
            " if it exists in our system."
            )

            return redirect(url_for("login"))
        
        else:
           flash("You are not register, go back and create an account!")
           
        
    return render_template(
        "auth/reset_password_request.html", title="Reset Password", form=form
    )   
          
# rota de token para recuperar senha            
@app.route('/reset_password/<token>/<int:user_id>', methods=['GET', 'POST'])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.validate_reset_password_token(token, user_id)
    if not user:
        return render_template(
            "auth/reset_password_error.html", title="Reset Password Error"
        )
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()

        return render_template(
            "auth/reset_password_success.html", title="Reset Password Succes"
        )
    return render_template(
        "auth/reset_password.html", title="Reset Password", form=form
    )


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
        psswrd2 = request.form['psswdF2'] 
        cred = request.form['credF']

        if psswrd2 != psswrd:
            flash("senhas diferentes")
            return redirect(url_for('register'))
            
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email já cadastrado. Faça Login.")
            return redirect(url_for('register'))
            
        
        new_user = User(nm=nm, email=email, psswrd=Hash(psswrd), cred=cred)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('home'))


# rota para perfil
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html')
    
    profile = request.args.get('personal_info')
    return render_template('profile.html', profile=profile)

      
            

# main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

