from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import json
import plotly

import dash.utils as utils
from dash.components import graph
from dash.components import element as el


name = 'dash-clustering'
app = Flask(name)
app.debug = True
app.config['key'] = 'secret'
socketio = SocketIO(app)

from dash_clustering_iris import Dash
dash = Dash()

# Write the HTML "includes" blocks to /templates/runtime/dash-clustering
# We're using the template "layout_single_column_and_controls" which uses the
# includes blocks: 'controls.html', main_pane.html'.
utils.write_templates(
    {
        'header': [
            el('h4', {}, 'Iris K-means clustering')
        ],
        # 'controls.html' is already written as a raw html file in
        # templates/runtime/dash-clustering
        'main_pane': [graph('iris')],
    }, name
)


@app.route('/')
def index():

    return render_template('layouts/layout_single_column_and_controls.html',
                           app_name=name)


@socketio.on('pong')
def onpong(app_state):
    messages = dash.on_pong(app_state)
    emit('postMessage', json.dumps(messages,
                                   cls=plotly.utils.PlotlyJSONEncoder))


@socketio.on('replot')
def replot(app_state):
    print(app_state)
    messages = dash.replot(app_state)
    emit('postMessage', json.dumps(messages,
                                   cls=plotly.utils.PlotlyJSONEncoder))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9999)
