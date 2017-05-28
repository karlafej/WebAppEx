from wtforms import Form, SelectField, SubmitField, FileField

class InputFile(Form):
    textfile = FileField()
    submit1 = SubmitField('upload')

class InputLim(Form):
    limit = SelectField(
        label='Number of words', 
        choices=[(100, "100"),
            (200, "200"),
            (300, "300"),
            (400, "400"),
            (500, "500"),
            (1000, "1000")],
        default = 500,
        )

