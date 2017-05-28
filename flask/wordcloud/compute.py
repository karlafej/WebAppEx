import numpy as np
from nltk.corpus import stopwords
from PIL import Image
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64

english_stopwords = set(stopwords.words('english')) 
wc_mask = np.array(Image.open("../../data/python.png"))
        
def get_plot(limit, txt, wc_mask=wc_mask, stop = english_stopwords):
    wordcloud = WordCloud(
        max_words=limit,
        stopwords=stop,
        mask=wc_mask
        ).generate(txt)
    fig = plt.figure()
    fig.set_figwidth(8)
    fig.set_figheight(8)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0) 
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    return figdata_png