from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import json
import plotly
import plotly.graph_objs as go

import dash.utils as utils
from dash.components import graph
from dash.components import element as el

import numpy as np
import csv

'''

PLOTLY HISTOGRAM IS WEIRD! 


'''

name = 'dash-hist'
app = Flask(name)
app.debug = True
app.config['key'] = 'secret'
socketio = SocketIO(app)

class Dash():
    def __init__(self):
        self.bins = 30

        with open('../data/twitter_stars.csv', 'r',  encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            columns = list(zip(*reader))
        stars = {c[0] : c[1:] for c in columns}
        for key in stars.keys():
            stars[key] = [int(n) for n in stars[key]]
        self.likes = [favs + rts for favs, rts in zip(stars['favs'], stars['rts'])]

    def on_page_load(self):
        pass

    def on_pong(self, message):
        print('on_pong')
        messages = []
        messages.extend(self.replot(message))
        return messages

    def replot(self, app_state):
        self.bins = int(app_state['bins'])

        hist_data = np.histogram(self.likes, bins = self.bins)
        binsize = hist_data[1][1] - hist_data[1][0]

        trace = go.Histogram(
            x=self.likes,
            autobinx=False,
            xbins=dict(
                start=hist_data[1][0],
                end=hist_data[1][-1],
                size=binsize
           )
        )
        data = [trace]
       
        fig = {
            'data': data, 
                

            'layout': {
                'xaxis': {
                    'title': 'Number of likes',
                },
                'yaxis': {
                    'title': 'Count',
                },
                'bargroupgap' :0.05,
            }
        }

        messages = [
            {
                'id': 'hist',
                'task': 'newPlot',
                'data': fig['data'],
                'layout': fig['layout']
            }
        ]

        return messages

dash = Dash()

# Write the HTML "includes" blocks to /templates/runtime/dash-clustering
# We're using the template "layout_single_column_and_controls" which uses the
# includes blocks: 'controls.html', main_pane.html'.
utils.write_templates(
    {
        'header': [
            el('h4', {}, 'Histogram of @python_tip likes')
        ],
        # 'controls.html' is already written as a raw html file in
        # templates/runtime/dash-clustering
        'main_pane': [graph('hist')],
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
