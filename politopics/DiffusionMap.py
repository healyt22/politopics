import yaml
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from mpl_toolkits import mplot3d
from matplotlib.pyplot import figure
from collections import Counter
from preprocess import *

class DiffusionMap():
    def __init__(self, handle, eps):
        self.eps = eps
        self.obj = Preprocess(handle)
        self.X = self.obj.td_matrix.toarray()
        self.main()

    def cos_similarity(self, x, y):
        sol = (x.dot(y)) / (np.linalg.norm(x) * np.linalg.norm(y))
        return(sol)


    def calc_distance_matrix(self):
        n = self.X.shape[0]
        self.D = np.zeros((n,n))

        i = np.nditer(self.D, flags=['multi_index'])
        while not i.finished:
            self.D[i.multi_index] = self.cos_similarity(self.X[i.multi_index[0],:],
                                                        self.X[i.multi_index[1],:])
            i.iternext()

    def laplacian_dm(self):
        M = metrics.pairwise.rbf_kernel(self.D, gamma=1./(2.*self.eps))
        self.W, self.V = np.linalg.eig(M)

    def kmeans(self, n_clusters):
        kmeans = KMeans(n_clusters=n_clusters).fit(self.V)
        self.clusters = kmeans.labels_
        cluster_summary = Counter(self.clusters)
        print(cluster_summary)
        fig = plt.figure(figsize=(12,12))
        sb.set_style('darkgrid')
        ax = fig.add_subplot(projection='3d')
        ax = plt.axes(projection='3d')
        x = self.V[:,1]; y = self.V[:,2]; z = self.V[:,3]
        ax.scatter3D(x, y, z, c=self.clusters)

    def DBSCAN(self, eps, min_samples):
        scaler = StandardScaler()
        V_3D = self.V[:,1:4]
        V_3D_scaled = scaler.fit_transform(V_3D)
        dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(V_3D_scaled)
        self.clusters = dbscan.labels_
        cluster_summary = Counter(self.clusters)
        print(cluster_summary)

        fig = plt.figure(figsize=(12,12))
        sb.set_style('darkgrid')
        ax = fig.add_subplot(projection='3d')
        ax = plt.axes(projection='3d')
        x = self.V[:,1]; y = self.V[:,2]; z = self.V[:,3]
        ax.scatter3D(x, y, z, c=self.clusters)

    def explore_clusters(self, num):
        for cluster, tweet in zip(self.clusters, self.obj.tweets):
            if cluster == num:
                print('\n\n')
                print(tweet)

    def main(self):
        self.calc_distance_matrix()
        self.laplacian_dm()
