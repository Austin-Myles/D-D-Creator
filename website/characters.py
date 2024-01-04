from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import  login_required, current_user
from . import db
from .models import DndChar

characters = Blueprint('characters', __name__)

#Module used for showing every character
@characters.route('/')
@login_required
def char_page():
    """Returns all characters and renders the character page"""
    return render_template("characters.html", user=current_user)

#Module used for showing a certain character
@characters.route('/<char_id>')
@login_required
def char_show(char_id):
    """
    Return the character page
    Parameter char_id: char id
    """
    character = "null"
    return render_template("char_view.html", character=character)

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
        exp = 10

        charDnd = DndChar.query.filter_by(name=charName).first()

        if charDnd:
            flash('Character name already exists', category='error')
        elif len(charName) < 1:
            flash('Character name must be greater than 1 character', category='error')
        else:
            new_char = DndChar(name=charName, charClass=charClass,
                               race=charRace, allingment=charAllign,
                               exp=exp, fuerza=0, destreza=0,
                               constitucion=0, inteligencia=0,
                               sabiduria=0, carisma=0, 
                               user_id=current_user.id)
            db.session.add(new_char)
            db.session.commit()
            flash('Character added succesfully!', category='success')
            return redirect(url_for("characters.char_page"))
        
    return render_template("char_create.html", user=current_user)

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
        charExists = True
        charName = request.form.get('charName')
        charDnd = DndChar.query.filter_by(name=charName).first()

        if charDnd:
            if (int(char_id) != charDnd.id):
                flash("The name entered is not available", category='error')
            else: 
                charExists = False

        elif len(charName) < 1:
                flash('Character name must be greater than 1 character', category='error')

        else:
            charExists = False

        if (charExists == False):
            current_char.name=charName
            current_char.charClass=request.form.get('charClass')
            current_char.race=request.form.get('charAllign')
            current_char.allingment=request.form.get('charRace')
            current_char.exp=request.form.get('exp')
            current_char.fuerza=request.form.get('strenght')
            current_char.destreza=request.form.get('dex')
            current_char.constitution=request.form.get('constitution')
            current_char.inteligencia=request.form.get('inteligence')
            current_char.sabiduria=request.form.get('wisdom')
            current_char.carisma=request.form.get('charisma')
            current_char.user_id=current_user.id
            db.session.commit()
            flash('Character edited succesfully!', category='success')
            return redirect(url_for("characters.char_page"))
            
    return render_template("char_update.html", user=current_user, character=current_char)

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
