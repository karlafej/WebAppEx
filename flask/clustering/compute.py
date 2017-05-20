import numpy as np
from sklearn.cluster import KMeans
from sklearn import datasets

import matplotlib.pyplot as plt
from matplotlib.cm import rainbow
import os, time,glob

iris = datasets.load_iris()
        
def get_plot(x, y, k, iris=iris):
    k_means = KMeans(n_clusters= k)
    k_means.fit(iris.data) 
    colormap = rainbow(np.linspace(0, 1, k))
  
    fig = plt.figure()
    splt = fig.add_subplot(1, 1, 1)
    splt.scatter(iris.data[:,x], iris.data[:,y], c = colormap[k_means.labels_], s=40)
    splt.scatter(k_means.cluster_centers_[:,x], k_means.cluster_centers_[:,y], c = 'black', marker='x')
    splt.set_xlabel(iris.feature_names[x])
    splt.set_ylabel(iris.feature_names[y])

    # dont do this nebo se poperou!
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
    # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    return plotfile
