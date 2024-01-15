from flask import Blueprint, render_template
from flask_login import  login_required, current_user

from website.src.accounts.auth import check_is_confirmed

views = Blueprint('views', __name__)

@views.route('/')
@login_required
@check_is_confirmed
def home_page():
    return render_template("home.html", user=current_user)







