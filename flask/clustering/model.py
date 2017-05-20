from wtforms import Form, SelectField

class InputForm(Form):
    x = SelectField(
        label='X value', 
        choices=[(0, "sepal length (cm)"),
            (1, "sepal width (cm)"),
            (2, "petal length (cm)"),
            (3, "petal width (cm)")],
        default = 0,
        )
    y = SelectField(
        label='Y value', 
        choices=[(0, "sepal length (cm)"),
            (1, "sepal width (cm)"),
            (2, "petal length (cm)"),
            (3, "petal width (cm)")],
        default = 2,
        )
    k = SelectField(
        label='Cluster count', 
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9')],
        default = 3,
        )

