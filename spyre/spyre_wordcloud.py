from spyre import server
from wordcloud import WordCloud#, ImageColorGenerator
import matplotlib.pyplot as plt
import re
import numpy as np
from nltk.corpus import stopwords
from PIL import Image

class WCApp(server.App):
    title = "Word Cloud"

    controls = [{
        "type": "upload",
        "id": "ubutton"
    }, {
        "type": "button",
        "label": "refresh",
        "id": "update_data"       
    }]

    inputs = [{
       "type": 'slider',
       "label": 'Number of words',
       "min": 100, "max": 1000, "value": 500, "step": 100,
       "key": 'lim',
       "action_id": 'plot'
    }]

    tabs = ["Text", "WordCloud"]

    outputs = [{
        "type": "plot",
        "id": "plot",
        "control_id": "update_data",
        "tab": "WordCloud",
        "on_page_load": False
        
    }, {
        "type": "html",
        "id": "html1",
        "control_id": "update_data",
        "tab": "Text"
        
    }]

    def __init__(self):
        self.upload_data = None
        self.upload_file = None

    def html1(self, params):
        text = (
            "Upload a text file and press refresh."
        )
        if self.upload_data is not None:
            text = self.upload_data
        return text

    def storeUpload(self, file):
        self.upload_file = file
        self.upload_data = file.read()
   
    def getData(self):
        regex = re.compile(r"(\b[-']\b)|[\W_]+")
        english_stopwords = set(stopwords.words('english'))
        if self.upload_data is not None:
            txt = str(self.upload_data.decode("utf-8"))
            txt = regex.sub(" ", txt).lower()
        return txt, english_stopwords

    def getPlot(self, params):
        txt, english_stopwords = self.getData()
        wc_mask = np.array(Image.open("../data/python.png"))
        limit = int(params['lim'])

        wordcloud = WordCloud(
            max_words=limit,
            stopwords=english_stopwords,
            mask=wc_mask,
        ).generate(txt)
       
        fig = plt.figure()
        fig.set_figwidth(8)
        fig.set_figheight(8)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis('off')
        return fig       

if __name__ == '__main__':
    app = WCApp()
    app.launch()
