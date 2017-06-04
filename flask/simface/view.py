from model import InputForm, ImageSet, Cycle
from flask import Flask, render_template, request, session
import simface

app = Flask(__name__)
app.secret_key = 'sosecretsolongblablabla'

@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = InputForm(request.form, prefix="form1")
    form2 = ImageSet(request.form, prefix="form2")
    form3 = Cycle(request.form, prefix="form3")
    results = dict()
    
    if form1.validate_on_submit() and form1.imgurl.data:
        session['face_id'] = simface.get_face_id(form1.imgurl.data)
        session['k'] = 0
        
    if 'face_id' in session:
        if form2.validate_on_submit() and form2.imageset.data: 
            session['k'] = 0
            session['idx'] = form2.imageset.data
            list_id = simface.imageset[session['idx']]
            session['similars'] = simface.face_similar(session['face_id'], list_id)
            results = simface.get_info(session['idx'], session['similars'][0]['persistedFaceId'])
            results['confidence'] = session['similars'][0]['confidence']
    
    if form3.validate_on_submit() and form3.cycle.data:
        if session['k'] < (len(session['similars'])-1):
            session['k'] = session['k']+1
        else:
            session['k'] = 0
        results = simface.get_info(session['idx'], session['similars'][session['k']]['persistedFaceId'])
        results['confidence'] = session['similars'][session['k']]['confidence']
  
    return render_template('view.html', form1=form1, form2 = form2, form3 = form3, results = results)

if __name__ == '__main__':
    app.run(debug=True)