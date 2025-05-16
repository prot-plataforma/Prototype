from db import db
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
import mongoengine as me
from itsdangerous import TimedSerializer, URLSafeTimedSerializer 
from flask import app



class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True )

    nm = db.Column(db.String(50), unique=True, nullable=False)

    psswrd = db.Column(db.String())

    email = db.Column(db.String(120), unique=True)

    cred = db.Column(db.String(11), unique=True)

    
    #def get_reset_token(self, expired_sec=1800):
    #   s=TimedSerializer(app.config['SECRET_KEY'], expired_sec)
    #    return s.dump({'id': self.id}).decode('utf-8')
    
    #@staticmethod
    #def verify_reset_token(token):
    #    s=TimedSerializer(app.config['SECRET_KEY'])
    #    try:
    #        id = s.loads(token)['id']
    #    except:
    #        return None
    #    return User.query.get(id) 
       

#class User(me.Document):
 #   id = me.IntField(required=True)
    
    