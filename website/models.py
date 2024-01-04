from . import db
from flask_login import UserMixin

#Usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(40))
    characters = db.relationship('DndChar')


#Personaje a crear
class DndChar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    charClass = db.Column(db.String(50))
    race = db.Column(db.String(50))
    allingment = db.Column(db.String(50))
    exp = db.Column(db.Integer)
    fuerza = db.Column(db.Integer)
    destreza = db.Column(db.Integer)
    constitucion = db.Column(db.Integer)
    inteligencia = db.Column(db.Integer)
    sabiduria = db.Column(db.Integer)
    carisma = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))