''' 
Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve bokeh_hist.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/bokeh_hist

in your browser.

BokehUserWarning: ColumnDataSource's columns must be of the same length
  lambda: warnings.warn("ColumnDataSource's columns must be of the same length", BokehUserWarning))
'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models.widgets import Slider
from bokeh.plotting import figure

# Set up data
x = np.random.normal(0, 1, 5000)
hist, edges = np.histogram(x, bins = 30)
hmax = max(hist)*1.1

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="histogram of x",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-4, 4],  y_range=(0, hmax))

hh = plot.quad(bottom=0, left=edges[:-1], right=edges[1:], top=hist, color="white", line_color="#3A5785")

# Set up widgets
bins_slider = Slider(title="bins", value=30, start=5, end=50, step = 1)


# Set up callbacks
def update(attrname, old, new):

    # Get the current slider values
    b = bins_slider.value

    # Generate the new curve
    hist1, edges1 = np.histogram(x, bins=b)
    hmax1 = max(hist1)*1.1

    hh.data_source.data["top"]  =  hist1
    hh.data_source.data["left"]  =  edges1[:-1]
    hh.data_source.data["right"]  =  edges1[1:]
    plot.y_range.end = hmax1 


bins_slider.on_change('value', update)

# Set up layouts and add to document
inputs = widgetbox(bins_slider)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Histogram"


