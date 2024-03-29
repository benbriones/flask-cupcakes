"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    """Cupcake Class"""

    __tablename__ = 'cupcakes'


    id = db.Column(
        db.Integer,
        primary_key = True
    )

    flavor = db.Column(
        db.String(50),
        nullable = False
    )

    size = db.Column(
        db.String(15),
        nullable = False
    )

    rating = db.Column(
        db.Integer,
        nullable = False
    )

    image_url = db.Column(
        db.String(500),
        nullable = False,
        default = DEFAULT_IMAGE_URL
    )

    def serialize(self):
        """Serialize info to dictionary"""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image_url": self.image_url
            }