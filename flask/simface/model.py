from flask_wtf import FlaskForm
from wtforms import  StringField, RadioField, validators, SubmitField


class InputForm(FlaskForm):
    imgurl = StringField('Photo URL: ', [validators.InputRequired()])

class ImageSet(FlaskForm):
    imageset = RadioField('Find your lookalike among: ', choices=[
        ('science', 'Scientists'),
        ('movie', 'Actors and Actresses'),
        ('porn', 'Pornstars')],
        default='movie')

class Cycle(FlaskForm):
    cycle = SubmitField("Don't like it? Try again!")
        