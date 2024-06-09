from flask import Flask, render_template, flash, redirect, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY']="secret-key-goes-here"

app.config['SQLALCHEMY_DATABASE_URI']="postgresql:///adoption"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
with app.app_context():
    db.create_all()


toolbar = DebugToolbarExtension(app)


### Flask Routing ###

@app.route("/")
def display_pets():
    """List all the Pets availible"""

    pets = Pet.query.all()
    return render_template("pet_list.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Add a pet"""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        print(data)
        #new_pet = Pet(**data)
        new_pet = Pet(name= form.name.data, age=form.age.data, species= form.species.data, photo_url =form.photo_url.data, notes = form.notes.data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet} is now here!")
        return redirect(url_for('display_pets'))
    
    else:
        return render_template("pet_add_form.html", form=form)
    


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Edit pet"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} has been updated.")
        return redirect(url_for('list_pets'))
    
    else:
        #return form for editing
        return render_template("pet_edit_form.html", form=form, pet=pet)
    

@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)
    
