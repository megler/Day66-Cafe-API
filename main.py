# cafeAPI.py
#
# Python Bootcamp Day 66 - Cafe API
# Usage:
#      A Flask App driven RESTful API that allows the user to perform CRUD
# operations to the database.
#
# Marceia Egler January 13, 2022

from flask import Flask, jsonify, render_template, request
from sqlalchemy.sql.functions import func
from model import db
from forms import CafeForm
import secrets, random

app = Flask(__name__)

##Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
db.app = app
db.init_app(app)
with app.test_request_context():
    from model import Cafe

    db.create_all()


@app.route("/")
def home():
    """Returns Home Page"""
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def random_cafe():
    """Generate a random number between 1 and len of db and return JSON output of cafe."""
    num_rows = Cafe.query.count()
    rand_num = random.randint(1, num_rows)
    random_cafe = Cafe.query.filter_by(id=rand_num).first()
    cafe_dict = Cafe.make_dict(random_cafe)
    return jsonify(cafe=cafe_dict)


@app.route("/all", methods=["GET"])
def all():
    """Lists all cafes in database"""
    get_cafes = Cafe.query.all()
    cafes = []
    for cafe in get_cafes:
        cafes.append(Cafe.make_dict(cafe))

    return jsonify(cafes=cafes)


@app.route("/search", methods=["GET"])
def search():
    """Search for a specific cafe by location"""
    location = request.args.get("location")
    db_query = Cafe.query.filter_by(location=location).all()
    locations = []
    if db_query:
        for loc in db_query:
            locations.append(Cafe.make_dict(loc))
    else:
        return jsonify(
            error={
                "Not Found": "Sorry we don't have a cafe at that location."
            })
    return jsonify(locations=locations)


@app.route("/add", methods=["POST"])
def add_cafe():
    """Add cafe to database"""
    add_cafe_form = CafeForm()
    add_cafe_db = Cafe(
        name=add_cafe_form.name.data,
        map_url=add_cafe_form.cafe_url.data,
        img_url=add_cafe_form.img_url.data,
        location=add_cafe_form.location.data,
        has_sockets=add_cafe_form.has_sockets.data,
        has_toilet=add_cafe_form.has_toilet.data,
        has_wifi=add_cafe_form.has_wifi.data,
        can_take_calls=add_cafe_form.take_calls.data,
        seats=add_cafe_form.seats.data,
        coffee_price=add_cafe_form.coffee_price.data,
    )
    db.session.add(add_cafe_db)
    db.session.commit()

    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<id>", methods=["PATCH"])
def update_price(id):
    """Update the price of coffee for a specific location id"""
    new_price = request.args.get("location")
    db_query = Cafe.query.filter_by(id=id).first()
    if db_query:
        Cafe.coffee_price = new_price
        db.session.commit()
    else:
        return (
            jsonify({
                "Not Found":
                "Sorry a cafe with that id was not found in the database."
            }),
            404,
        )
    return (
        jsonify({"success": "Successfully updated the price."}),
        200,
    )


@app.route("/report-closed/<id>", methods=["DELETE"])
def report_closed(id):
    """Delete a cafe from the database if there is an id and api-key match"""
    api_key = request.args.get("api-key")
    db_query = Cafe.query.filter_by(id=id).first()
    if api_key == "TopSecretAPIKey":
        if db_query:
            db.session.delete(db_query)
            db.session.commit()
        else:
            return (
                jsonify(
                    error={
                        "Not Found":
                        "Sorry a cafe with that id was not found in the database."
                    }),
                404,
            )
    else:
        return (
            jsonify(
                error={
                    "Not Found":
                    "Sorry, that's not allowed. Make sure you have the correct API Key"
                }),
            403,
        )

    return jsonify(response={"success": "Successfully deleted the cafe."}), 200


if __name__ == "__main__":
    app.run(debug=True)
