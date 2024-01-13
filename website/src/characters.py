from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import  login_required, current_user
from .. import db
from .models import DndChar

characters = Blueprint('characters', __name__)

#Module used for showing every character
@characters.route('/')
@login_required
def char_page():
    """Returns all characters and renders the character page"""
    return render_template("character/characters.html", user=current_user)

#Module used for showing a certain character
@characters.route('/<char_id>')
@login_required
def char_view(char_id):
    """
    Return the character page
    Parameter char_id: char id
    """
    current_char = DndChar.query.filter_by(id=char_id).first()

    if current_char:
        return render_template("character/char_view.html", character=current_char, user=current_user)
    else:
        return redirect(url_for("characters.char_page"))

#Module for creating a character
@characters.route("/create", methods=["GET", "POST"])
@login_required
def char_create():
    """Creates a new character"""
    if request.method == 'POST':
        charName = request.form.get('charName')
        charClass = request.form.get('charClass')
        charAllign = request.form.get('charAllign')
        charRace = request.form.get('charRace')

        if len(charName) < 1:
            flash('Character name must be greater than 1 character', category='error')
        else:
            new_char = DndChar(name=charName, charClass=charClass,
                               race=charRace, alling=charAllign,
                               exp=10, stren=0, dex=0,
                               consti=0, inteli=0,
                               wisdom=0, charisma=0, 
                               user_id=current_user.id)
            db.session.add(new_char)
            db.session.commit()
            flash('Character added succesfully!', category='success')
            return redirect(url_for("characters.char_page"))
        
    return render_template("character/char_create.html", user=current_user)

#Module for updating characters
@characters.route('/<char_id>/update', methods=["GET", "POST"])
@login_required
def char_update(char_id):
    """
    Updates a character
    Parameter char_id: char id
    """
    current_char = DndChar.query.filter_by(id=char_id).first()

    if request.method == 'POST':

        charName = request.form.get('charName')

        if len(charName) < 1:
                flash('Character name must be greater than 1 character', category='error')
        else:
            current_char.name=charName
            current_char.charClass=request.form.get('charClass')
            current_char.race=request.form.get('charAllign')
            current_char.alling=request.form.get('charRace')
            current_char.exp=request.form.get('exp')
            current_char.stren=request.form.get('stren')
            current_char.dex=request.form.get('dex')
            current_char.consti=request.form.get('consti')
            current_char.inteli=request.form.get('inteligence')
            current_char.wisdom=request.form.get('wisdom')
            current_char.charisma=request.form.get('charisma')
            current_char.user_id=current_user.id
            db.session.commit()
            flash('Character edited succesfully!', category='success')
            return redirect(url_for("characters.char_page"))
            
    return render_template("character/char_update.html", character=current_char, user=current_user)

#Module for deleting a certain character
@characters.route('/<char_id>/delete')
@login_required
def char_delete(char_id):
    """
    Deletes a character
    Parameter char_id: char id
    """
    current_char = DndChar.query.filter_by(id=char_id).first()
    db.session.delete(current_char)
    db.session.commit()
    flash("Character deleted succesfully!", "success")
    return redirect(url_for("characters.char_page"))
