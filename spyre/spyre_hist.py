from spyre import server
import matplotlib.pyplot as plt
#import numpy as np
import seaborn as sns
import csv


class Hist(server.App):
    title = "Histogram of @python_tip likes"


    inputs = [{
       "type": 'slider',
       "label": 'Number of bins',
       "min": 10, "max": 50, "value": 30, "step": 1,
       "key": 'bins',
       "action_id": 'plot'
    }]


    outputs = [{
        "type": "plot",
        "id": "plot",
    }]

    def __init__(self):
        with open('../data/twitter_stars.csv', 'r',  encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            columns = list(zip(*reader))
        stars = {c[0] : c[1:] for c in columns}
        for key in stars.keys():
           stars[key] = [int(n) for n in stars[key]]
        self.likes = [favs + rts for favs, rts in zip(stars['favs'], stars['rts'])]

   
    def getPlot(self, params):
        n = int(params['bins'])
        fig = sns.distplot(self.likes, bins=n, rug = False, kde = False, hist_kws=dict(alpha=0.75, edgecolor="k", linewidth=1))
        fig.set_xlabel('Number of likes')
        fig.set_ylabel('Count')
        return fig
     

if __name__ == '__main__':
    app = Hist()
    app.launch()
