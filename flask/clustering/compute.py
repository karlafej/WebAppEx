import numpy as np
from sklearn.cluster import KMeans
from sklearn import datasets

import matplotlib.pyplot as plt
from matplotlib.cm import rainbow
from io import BytesIO
import base64

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
    
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0) 
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    return figdata_png
