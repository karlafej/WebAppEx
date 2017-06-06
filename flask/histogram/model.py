from wtforms import Form 
from wtforms.fields.html5 import IntegerRangeField


class InputBins(Form):
    nbins = IntegerRangeField('Number of bins', default = 30)
    
  
        
        
