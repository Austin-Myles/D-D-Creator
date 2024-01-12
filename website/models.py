from . import db
from flask_login import UserMixin

#Usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(40))
    is_confirmed = db.Column(db.Boolean(), nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    characters = db.relationship('DndChar')


#Personaje a crear
class DndChar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    charClass = db.Column(db.String(50))
    race = db.Column(db.String(50))
    alling = db.Column(db.String(50))
    exp = db.Column(db.Integer)
    stren = db.Column(db.Integer)
    dex = db.Column(db.Integer)
    consti = db.Column(db.Integer)
    inteli = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))