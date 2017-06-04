''' 
Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve bokeh_hist.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/bokeh_hist

in your browser.

BokehUserWarning: ColumnDataSource's columns must be of the same length
  lambda: warnings.warn("ColumnDataSource's columns must be of the same length", BokehUserWarning))
because hist and hist1 data sources have different number of columns...
'''
import numpy as np
import csv

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models.widgets import Slider
from bokeh.plotting import figure

# Set up data
with open('../data/twitter_stars.csv', 'r',  encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        columns = list(zip(*reader))
stars = {c[0] : c[1:] for c in columns}
for key in stars.keys():
  stars[key] = [int(n) for n in stars[key]]
likes = [favs + rts for favs, rts in zip(stars['favs'], stars['rts'])]
hist, edges = np.histogram(likes, bins = 30)

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="histogram of @python_tip stars",
              tools="crosshair,pan,reset,save,wheel_zoom,hover")

hh = plot.quad(bottom=0, left=edges[:-1], right=edges[1:], top=hist, fill_color="#446785", line_color="#033649")

# Set up widgets
bins_slider = Slider(title="bins", value=30, start=5, end=50, step = 1)


# Set up callbacks
def update(attrname, old, new):

    # Get the current slider values
    b = bins_slider.value

    # Generate the new curve
    hist1, edges1 = np.histogram(likes, bins=b)

    hh.data_source.data["top"]  =  hist1
    hh.data_source.data["left"]  =  edges1[:-1]
    hh.data_source.data["right"]  =  edges1[1:]

bins_slider.on_change('value', update)

# Set up layouts and add to document
inputs = widgetbox(bins_slider)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Histogram"


