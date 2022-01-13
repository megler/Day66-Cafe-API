from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired


class CafeForm(FlaskForm):
    """WTForm fields to add a cafe"""

    name = StringField(label="Cafe Name", validators=[DataRequired()])
    cafe_url = StringField(label="Cafe Map URL", validators=[DataRequired()])
    img_url = StringField(label="Cafe Image URL", validators=[DataRequired()])
    location = StringField(label="Cafe Location (eg. Peckham)",
                           validators=[DataRequired()])
    has_sockets = BooleanField(label="Does Cafe Have Sockets?",
                               validators=[DataRequired()])
    has_toilet = BooleanField(label="Does Cafe Have A Bathroom?",
                              validators=[DataRequired()])
    has_wifi = BooleanField(label="Does Cafe Have Wifi?",
                            validators=[DataRequired()])
    take_calls = BooleanField(label="Does Cafe Allow You To Take Phonecalls?",
                              validators=[DataRequired()])
    seats = SelectField(
        label="How Many Seats?",
        choices=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"],
        validators=[DataRequired()],
    )
    coffee_price = FloatField(label="Price Of Coffee",
                              validators=[DataRequired()])
    submit = SubmitField("Submit")
