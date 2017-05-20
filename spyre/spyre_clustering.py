from spyre import server

import numpy as np
from sklearn.cluster import KMeans
from sklearn import datasets
import matplotlib.pyplot as plt
from matplotlib.cm import rainbow

class IrissApp(server.App):
    title = "Iris K-means clustering"

    inputs = [{
        "type": 'dropdown',
        "label": 'X Variable',
        "options": [
            {"label": "sepal length", "value": 0},
            {"label": "sepal width", "value": 1},
            {"label": "petal length", "value": 2},
            {"label": "petal length", "value": 3}],
        "value": 0,
        "key": 'x_axis',
        "action_id": "plot"
        }, {
        "type": 'dropdown',
        "label": 'Y Variable',
        "options": [
            {"label": "sepal length", "value": 0},
            {"label": "sepal width", "value": 1},
            {"label": "petal length", "value": 2},
            {"label": "petal length", "value": 3}],
        "value": 1,
        "key": 'y_axis',
        "action_id": "plot"
        }, {
            "type": 'slider',
            "label": 'Cluster count',
            "min": 1, "max": 9, "value": 3, "step": 1,
            "key": 'cluster',
            "action_id": 'plot'
        }
    ]

    outputs = [{
        "type": "plot",
        "id": "plot"
    }]

    def __init__(self):
    	self.iris = datasets.load_iris()

    def getPlot(self, params):
        k = int(params['cluster'])
        x = int(params['x_axis'])
        y = int(params['y_axis'])
        k_means = KMeans(n_clusters= k )
        k_means.fit(self.iris.data) 
        colormap = rainbow(np.linspace(0, 1, k))
        fig = plt.figure()
        splt = fig.add_subplot(1, 1, 1)
        splt.scatter(self.iris.data[:,x], self.iris.data[:,y], c = colormap[k_means.labels_], s=40)
        splt.scatter(k_means.cluster_centers_[:,x], k_means.cluster_centers_[:,y], c = 'black', marker='x')
        splt.set_xlabel(self.iris.feature_names[x])
        splt.set_ylabel(self.iris.feature_names[y])
        return fig
        
if __name__ == '__main__':
    app = IrissApp()
    app.launch()