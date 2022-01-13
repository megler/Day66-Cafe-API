from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cafe(db.Model):
    """Fields for table in db."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def make_dict(self):
        """Organize table data and return dict for later JSONification."""
        cafe_data = {
            "id":
            self.id,
            "cafe_name":
            self.name,
            "map_url":
            self.map_url,
            "img_url":
            self.img_url,
            "cafe_location":
            self.location,
            "options": [{
                "seats": self.seats,
                "toilet": self.has_toilet,
                "wifi": self.has_wifi,
                "sockets": self.has_sockets,
                "calls": self.can_take_calls,
            }],
            "coffee_price":
            self.coffee_price,
        }
        return cafe_data
