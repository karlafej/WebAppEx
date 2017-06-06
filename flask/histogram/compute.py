import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def get_likes():
    with open('../../data/twitter_stars.csv', 'r',  encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        columns = list(zip(*reader))
    stars = {c[0] : c[1:] for c in columns}
    for key in stars.keys():
        stars[key] = [int(n) for n in stars[key]]
    likes = [favs + rts for favs, rts in zip(stars['favs'], stars['rts'])]
    return likes
likes = get_likes()
        
def get_plot(nbins, likes = likes):
    
    fig = plt.figure()
    splt = fig.add_subplot(1, 1, 1)
    splt.hist(likes, bins=nbins, edgecolor="k")
    splt.set_xlabel('Number of likes')
    splt.set_ylabel('Count')
        
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0) 
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    return figdata_png


    