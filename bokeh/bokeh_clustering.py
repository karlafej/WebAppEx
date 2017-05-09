''' 
Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve bokeh_hist.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/bokeh_clustering

in your browser.
'''

import numpy as np
from sklearn.cluster import KMeans
from sklearn import datasets
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select, Slider
from bokeh.plotting import figure
import seaborn.apionly as sns


# set up data
iris = datasets.load_iris()
axis_map = {
    "sepal length (cm)": 0,
    "sepal width (cm)": 1,
    "petal length (cm)": 2,
    "petal width (cm)": 3,
}

# Create Input controls
x_axis = Select(title="X Variable", options=sorted(iris.feature_names), value="sepal length (cm)")
y_axis = Select(title="Y Variable", options=sorted(iris.feature_names), value="sepal width (cm)")
clusters = Slider(title="Cluster count", value=3, start=1, end=9, step = 1)


# Set up plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[]))
centers = ColumnDataSource(data=dict(cx=[], cy=[]))
plot = figure(width=700, height=500, title='Iris K-means clustering')
plot.circle(x="x", y="y", source=source, size=15, color="colors")
plot.x(x="cx", y="cy", source=centers, color="black", size=20)

def update():
    # Get the current slider values
    N = clusters.value
    x_var = axis_map[x_axis.value]
    y_var = axis_map[y_axis.value]

    k_means = KMeans(n_clusters=N)
    k_means.fit(iris.data) 
    centroids = k_means.cluster_centers_
    
    palette = sns.palettes.color_palette('hls', N)
    colormap = np.array(palette.as_hex())[k_means.labels_] # as hex is necessary for bokeh to render the colors properly.
    
    plot.xaxis.axis_label = x_axis.value
    plot.yaxis.axis_label = y_axis.value

    source.data = dict(
        x=iris.data[:,x_var],
        y=iris.data[:,y_var],
        colors=colormap)
    centers.data = dict(
        cx=centroids[:,x_var],
        cy=centroids[:,y_var])
   

controls = [clusters, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

# Set up layouts and add to document
inputs = widgetbox(x_axis,y_axis,clusters)

update() #initial load of data

curdoc().add_root(row(inputs, plot, width=1000))
curdoc().title = "Iris K-means clustering"


