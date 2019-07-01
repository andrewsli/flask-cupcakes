"""Cupcakes application."""

from flask import Flask, request, redirect, jsonify
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "SUPER-SECRET-KEY"

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def landing_page():
    """landing page redirecting to list of all cupcakes"""
    return redirect('/cupcakes')


@app.route('/cupcakes')
def list_cupcakes():
    """returns list of all cupcakes as object through json"""
    cupcakes = Cupcake.query.all()

    serialized_cupcakes = [{
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    } for cupcake in cupcakes]

    return jsonify(response=serialized_cupcakes)


@app.route('/cupcakes', methods=["POST"])
def create_cupcake():
    """creates cupcake instance from posted data, adds cupcake to database,
    returns data on added cupcake in json form
    """
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    serialized_cupcake = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }

    return jsonify(response=serialized_cupcake)
