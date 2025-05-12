from db import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True )

    nm = db.Column(db.String(50), unique=True)
    psswrd = db.Column(db.String())

    email = db.Column(db.String(120), unique=True)

    cred = db.Column(db.String(11), unique=True)