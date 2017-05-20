from model import InputForm
from flask import Flask, render_template, request
from compute import get_plot

app = Flask(__name__)


@app.route('/iris', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST':
        result = get_plot(int(form.x.data), int(form.y.data),
                        int(form.k.data))
    else:
        result = get_plot(0, 2, 3)
        
    return render_template('view.html', form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)