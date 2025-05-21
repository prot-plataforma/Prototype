from db import db
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
import mongoengine as me
from itsdangerous import TimedSerializer, URLSafeTimedSerializer, BadSignature, SignatureExpired 
from flask import current_app



class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True )

    nm = db.Column(db.String(50), unique=True, nullable=False)

    psswrd = db.Column(db.String())

    email = db.Column(db.String(120), unique=True)

    cred = db.Column(db.String(11), unique=True)

    def generate_reset_password_token(self, expires_sec=1800):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps({'user_id': self.id, 'email':self.email})
    
    @staticmethod
    def validate_reset_password_token(token: str, user_id:int):
        user = db.session.get(User, user_id)

        if user is None:
            return None
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token, max_age=1800)
        except (BadSignature, SignatureExpired):
            return None

        if data.get('user_id') != user_id:

            return None
        
        user = db.session.get(User, user_id)
        if user and user.email == data.get('email'):
            return user

        return None 

    

    