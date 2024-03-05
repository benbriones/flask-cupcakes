"""Flask app for Cupcakes"""
import os
from models import Cupcake, db, connect_db, DEFAULT_IMAGE_URL
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret'


connect_db(app)

@app.get('/')
def display_homepage():
    """displays homepage"""
    return render_template('homepage.html')


@app.get('/api/cupcakes')
def get_all_cupcakes():
    """Get data about all cupcakes and return JSON
    {cupcakes: [{id, flavor, size, rating, image_url}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake and return JSON
    {cupcake: {id, flavor, size, rating, image_url}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def create_cupcake():
    """Create a cupcake and return JSON
    {cupcake: {id, flavor, size, rating, image_url}}"""

    new_cupcake = Cupcake(
        flavor=request.json['flavor'],
        size=request.json['size'],
        rating=request.json['rating'],
        image_url=request.json['image_url'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Update a cupcake and return JSON
    {cupcake: {id, flavor, size, rating, image_url}}"""
# TODO: more specific with what we can update
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor') or cupcake.flavor
    cupcake.size = request.json.get('size') or cupcake.size
    cupcake.rating = request.json.get('rating') or cupcake.rating
    if "image_url" in request.json:
        cupcake.image_url = request.json.get('image_url') or DEFAULT_IMAGE_URL

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """ Return JSON {deleted: [cupcake-id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=[cupcake_id])
