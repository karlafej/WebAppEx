from wtforms import Form, SelectField

class InputForm(Form):
    x = SelectField(
        label='X value', 
        choices=[(0, "Sepal length"),
            (1, "Sepal width"),
            (2, "Petal length"),
            (3, "Petal width")],
        default = 0,
        )
    y = SelectField(
        label='Y value', 
        choices=[(0, "Sepal length"),
            (1, "Sepal width"),
            (2, "Petal length"),
            (3, "Petal width")],
        default = 2,
        )
    k = SelectField(
        label='Cluster count', 
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9')],
        default = 3,
        )

