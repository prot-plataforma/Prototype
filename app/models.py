from db import db
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin



class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True )

    nm = db.Column(db.String(50), unique=True, nullable=False)

    psswrd = db.Column(db.String())

    email = db.Column(db.String(120), unique=True)

    cred = db.Column(db.String(11), unique=True)


# class Fazendas(db.Model):
  #  __tablename__ = 'fazendas'

   # id = db.Column(db.Integer, primary_key=True)
