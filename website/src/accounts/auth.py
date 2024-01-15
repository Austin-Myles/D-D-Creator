from datetime import datetime
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask_mail import Message, Mail

from website.src.accounts.token import generate_token, confirm_token
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ... import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)
mail = Mail()

#Useful decorators

def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already authenticated.", "info")
            return redirect(url_for("views.home_page"))
        return func(*args, **kwargs)

    return decorated_function


def check_is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_confirmed is False:
            flash("Please confirm your account!", "warning")
            return redirect(url_for("auth.inactive"))
        return func(*args, **kwargs)

    return decorated_function

@auth.route('/login', methods=['GET','POST'])
@logout_required
def login():
    """
        Logs in a registered user
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if not user.is_confirmed:
                    flash('User is not active, confirm your email', category='error')
                    return redirect(url_for('auth.login'))
                else:
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home_page'))
            
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("auth/login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
        Self explanatory, it logs off the user
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET','POST'])
@logout_required
def register():
    """
        Creates a new user and sends a confirmation mail to the user's email address
    """

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
    
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(username) < 1:
            flash('Username must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, username=username
            , password=generate_password_hash(password1, method='pbkdf2:sha256')
            , is_confirmed=False)
            db.session.add(new_user)
            db.session.commit()

            token = generate_token(new_user.email)
            confirm_url = url_for("auth.confirm_email", token=token, _external=True)
            html = f"Welcome! Thanks for signing up. Please click link to confirm your account!{confirm_url}"
            subject = "Please confirm your email"
            msg = Message(subject, recipients=[new_user.email], body=html, sender=current_app.config["MAIL_DEFAULT_SENDER"],)
            mail.send(msg)

            login_user(new_user)

            flash("A confirmation email has been sent via email.", "success")
            return redirect(url_for('auth.inactive'))

    return render_template("auth/register.html", user=current_user)


@auth.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("views.home_page"))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("views.home_page"))


@auth.route("/inactive")
@login_required
def inactive():
    if current_user.is_confirmed:
        return redirect(url_for("views.home_page"))
    return render_template("auth/inactive.html", user=current_user)


@auth.route("/resend")
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for("views.home_page"))
    token = generate_token(current_user.email)
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    html = f"Welcome! Thanks for signing up. Please click link to confirm your account!{confirm_url}"
    subject = "Please confirm your email"
    msg = Message(subject, recipients=[current_user.email], body=html, sender=current_app.config["MAIL_DEFAULT_SENDER"],)
    mail.send(msg)

    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("auth.inactive"))


@auth.route('/profile', methods=['GET','POST'])
@login_required
@check_is_confirmed
def profile():
    
    if request.method == 'POST':    

        actpass = request.form.get('actpass')
        newpass1 = request.form.get('newpass1')
        newpass2 = request.form.get('newpass2')
        newpassaux = generate_password_hash(newpass1, method='pbkdf2:sha256')

        if check_password_hash(current_user.password, actpass):
            if newpass1 != newpass2:
                flash('Passwords don\'t match, try again.', category='error')
            elif len(newpass1) < 7:
                flash('Password must be at least 7 characters', category='error')
            else:
                user = User.query.filter_by(email=current_user.email).first_or_404()
                user.password = newpassaux
                db.session.add(user)
                db.session.commit()
                flash("You have changed your password!", "success")
        else:
            flash('Incorrect password, try again.', category='error')

    return render_template("profile.html", user=current_user)


@auth.route('/delete')
@login_required
def delete_profile():
    """
    Deletes the account
    """
    db.session.delete(current_user)
    db.session.commit()
    flash("Account deleted successfully!", "success")
    return redirect(url_for("auth.register"))

