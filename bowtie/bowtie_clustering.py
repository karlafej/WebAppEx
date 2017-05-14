#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bowtie.control import Dropdown, Slider
from bowtie.visual import Plotly, SmartGrid, SVG

import numpy as np
from sklearn.cluster import KMeans
from sklearn import datasets
import plotlywrapper as pw
import seaborn.apionly as sns
import plotly.graph_objs as go

iris = datasets.load_iris()

attrs = iris.feature_names

axis_map = {
    "sepal length (cm)": 0,
    "sepal width (cm)": 1,
    "petal length (cm)": 2,
    "petal width (cm)": 3,
}

xdown = Dropdown(caption='X variable', labels=attrs, values=attrs)
ydown = Dropdown(caption='Y variable', labels=attrs, values=attrs)
clslider = Slider(caption='Cluster count', start=3, minimum=1, maximum=9)

kplot = Plotly()


def Kplot(x, y, N):
    if x is None or y is None or N is None:
        return
    x_var = xdown.get()['value']
    y_var = ydown.get()['value']
    x = axis_map[x_var]
    y = axis_map[y_var]
    N = clslider.get()
    k_means = KMeans(n_clusters= N)
    k_means.fit(iris.data)
    palette = sns.palettes.color_palette('hls', N)
    colormap = np.array(palette.as_hex())[k_means.labels_]
    data = go.Scatter(
        x = iris.data[:,x],
        y = iris.data[:,y],
        mode = 'markers',
        name = 'data',
        marker = dict(
                    size='12',
                    color = colormap
                )
    )
    centroids = go.Scatter(
        x = k_means.cluster_centers_[:,x],
        y = k_means.cluster_centers_[:,y],
        mode = 'markers',
        name = 'centroids',
        marker = dict(
                    size='14',
                    color = 'black',
                    symbol = 'x-thin-open'
                )
    )
    traces = [data, centroids]
    plot = pw.Chart()
    plot.data = traces
    #plot+= pw.scatter(iris.data[:,x], iris.data[:,y])
    #plot+= pw.scatter(k_means.cluster_centers_[:,x], k_means.cluster_centers_[:,y], color = 'black')
    plot.xlabel(x_var)
    plot.ylabel(y_var)
    plot.legend(visible = False)

    kplot.do_all(plot.to_json())


from bowtie import command

@command
def construct(path):
    from bowtie import Layout
    description = """
Iris K-means clustering
===========
 

"""
    layout = Layout(description=description, background_color='LightGrey', debug=False)
    layout.add_sidebar(clslider)
    layout.add_sidebar(xdown)
    layout.add_sidebar(ydown)
    
    layout.add(kplot)

    layout.subscribe(Kplot, xdown.on_change, ydown.on_change, clslider.on_change)
   
    layout.build()
