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

    serialized_cupcakes = [cupcake.serialized() for cupcake in cupcakes]

    return jsonify(response=serialized_cupcakes)


@app.route('/cupcakes', methods=["POST"])
def create_cupcake():
    """creates cupcake instance from posted data, adds cupcake to database,
    returns data on added cupcake in json form
    """
    data = request.json
    cupcake = Cupcake(
        flavor=data["flavor"],
        size=data["size"],
        rating=data["rating"],
        image=data["image"] or None,
        )

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(response=cupcake.serialized())


@app.route("/cupcakes/<int:cupcake_id>")
def show_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(response=cupcake.serialized())


@app.route('/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """update cupcake"""
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = data["flavor"]
    cupcake.size = data["size"]
    cupcake.rating = data["rating"]
    cupcake.image = data["image"] or None
    db.session.commit()

    return jsonify(response=cupcake.serialized())


@app.route('/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """delete cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    message = {
        "message": "Deleted"
    }

    return jsonify(response=message)
