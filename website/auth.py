from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "A"

@auth.route('/logout')
def logout():
    return "L"

@auth.route('/register')
def register():
    return "R"