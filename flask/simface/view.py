from model import InputForm
from flask import Flask, render_template, request, session
import simface

app = Flask(__name__)
app.secret_key = 'sosecretsolongblablabla'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    results = dict()
    
    if form.imgurl.data:
        session['face_id'] = simface.get_face_id(form.imgurl.data)
    if 'face_id' in session:
        if form.imageset.data: 
            idx = form.imageset.data
            list_id = simface.imageset[idx]
            similars = simface.face_similar(session['face_id'], list_id)
            results = simface.get_info(idx, similars[0]['persistedFaceId'])
            results['confidence'] = similars[0]['confidence']
     
    return render_template('view.html', form=form, results = results)

if __name__ == '__main__':
    app.run(debug=True)