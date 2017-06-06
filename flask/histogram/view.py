from model import InputBins
from flask import Flask, render_template, request, session
from compute import get_plot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form = InputBins(request.form)
    if request.method == 'POST' and form.nbins.data:
        nbins = int(form.nbins.data)
    else:
        nbins = 30

    result = get_plot(nbins=nbins)       
        
    return render_template('view.html', form=form,result=result)

if __name__ == '__main__':
    app.run(debug=True)