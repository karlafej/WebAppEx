'''
The only working example in bowtie so far. ¯\(°_o)/¯
python 2.7
bowtie==0.3.2
'''
from bowtie.visual import Plotly
from bowtie.control import Nouislider
import numpy as np
import plotlywrapper as pw

sine_plot = Plotly()
freq_slider = Nouislider(caption='frequency', minimum=1, maximum=10, start=5)

def listener(freq):
    freq = float(freq[0])
    t = np.linspace(0, 10, 100)
    sine_plot.do_all(pw.line(t, np.sin(freq * t)).to_json())

from bowtie import command
@command
def construct(path):
    from bowtie import Layout
    layout = Layout(directory=path)
    layout.add_sidebar(freq_slider)
    layout.add(sine_plot)
    layout.subscribe(listener, freq_slider.on_change)
    layout.build()
