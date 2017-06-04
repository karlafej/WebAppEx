from model import InputLim, InputFile
from flask import Flask, render_template, request, session
from compute import get_plot
import re
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'sosecretsolongblablabla'
regex = re.compile(r"(\b[-']\b)|[\W_]+")

SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
PERMANENT_SESSION_LIFETIME = 300
app.config.from_object(__name__)
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = InputFile(request.form)
    form2 = InputLim(request.form)

    if form2.limit.data:
        session['limit'] = int(form2.limit.data)
    else: session['limit'] = 500

    if form1.submit1.data :
        txt = request.files[form1.textfile.name].read()
        txt=str(txt.decode("utf-8"))
        txt=regex.sub(" ", txt).lower() 
        if len(txt)>0 :
            session['text'] = txt
        	
    if 'text' in session:
        result = get_plot(session['limit'], session['text'])       
    else:
        result = None
        
    return render_template('view.html', form1=form1, form2 = form2, result=result)

if __name__ == '__main__':
    app.run(debug=True)