import numpy as np
from sklearn.cluster import KMeans
from sklearn import datasets
import seaborn.apionly as sns

class Dash():
    def __init__(self):
        self.iris = datasets.load_iris()
        self.count = 3
        self.xaxis = 0
        self.yaxis = 1
        

    def on_page_load(self):
        pass

    def on_pong(self, message):
        print('on_pong')
        messages = []
        messages.extend(self.replot(message))
        return messages

    def replot(self, app_state):
        self.xaxis = int(app_state['xaxis'])
        self.yaxis = int(app_state['yaxis'])
        self.count = int(app_state['clusters'])

        axis_map = {
            0: "sepal length (cm)",
            1: "sepal width (cm)",
            2: "petal length (cm)",
            3: "petal width (cm)",
        }
        
        N = self.count
        k_means = KMeans(n_clusters=N)
        k_means.fit(self.iris.data) 
        centroids = k_means.cluster_centers_

        palette = sns.palettes.color_palette('hls', N)
        colormap = np.array(palette.as_hex())[k_means.labels_]

       
        fig = {
            'data': [{
                'x': self.iris.data[:,self.xaxis],
                'y': self.iris.data[:,self.yaxis],
                'mode': 'markers',
                'name': 'data',
                'marker': dict(
                    size='12',
                    color = colormap
                )
            },
            {   'x': centroids[:,self.xaxis],
                'y': centroids[:,self.yaxis],
                'mode': 'markers',
                'name': 'centroids',
                'marker': dict(
                    size='12',
                    color = 'black',
                    symbol = 'x-thin-open'
                )

            }],
            'layout': {
                'xaxis': {
                    'title': axis_map[self.xaxis],
                },
                'yaxis': {
                    'title': axis_map[self.yaxis],
                },
                'showlegend': False,
            }
        }

        messages = [
            {
                'id': 'iris',
                'task': 'newPlot',
                'data': fig['data'],
                'layout': fig['layout']
            }
        ]

        return messages
