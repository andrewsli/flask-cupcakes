"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = "https://tinyurl.com/truffle-cupcake"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """class corresponding to cupcake table"""

    def __repr__(self):
        x = self
        return f"<Cupcake {x.id}: {x.size} {x.flavor}. Rating: {x.rating}>"

    __tablename__ = "cupcakes"

    # create columns
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        )
    flavor = db.Column(
        db.Text,
        nullable=False,
        )
    size = db.Column(
        db.Text,
        nullable=False,
        )
    rating = db.Column(
        db.Float,
        nullable=False,
        )
    image = db.Column(
        db.Text,
        default=DEFAULT_IMAGE,
    )

    def serialized(self):
        serialized_cupcake = {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image,
        }

        return serialized_cupcake
