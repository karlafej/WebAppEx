from wtforms import Form, StringField, RadioField, validators, SubmitField

class InputForm(Form):
    imgurl = StringField('Photo URL: ', [validators.InputRequired()])
    imageset = RadioField('Find your lookalike among: ', choices=[
        ('science', 'Scientists'),
        ('movie', 'Actors and Actresses'),
        ('porn', 'Pornstars')],
        default='movie')
