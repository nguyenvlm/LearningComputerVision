import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


class KMCClassifier:
    def __init__(self, k):
        self.k = k

    def fit(self, X):
        self.X = X
        # init centroids and labels:
        self.centroids_eval = [self.X[np.random.choice(self.X.shape[0], self.k, replace=False)]]
        self.labels_eval = []
        
    def assign_labels(self):
        self.labels_eval.append(np.argmin(cdist(self.X, self.centroids_eval[-1]), axis=1))

    def update_centroids(self):
        centroids = np.zeros((self.k, self.X.shape[1]))
        for k in range(self.k):
            # collect all points assigned to the k-th cluster 
            Xk = self.X[self.labels_eval[-1] == k, :]
            # take average
            centroids[k,:] = np.mean(Xk, axis = 0)
        # Converged check:
        if set(tuple(c) for c in self.centroids_eval[-1]) == set(tuple(c) for c in centroids):
            return False
        self.centroids_eval.append(centroids)
        return True

    def evaluate(self):
        self.iter = 0
        self.assign_labels()
        while self.update_centroids():
            self.assign_labels()
            self.iter += 1
        
        return self.centroids_eval, self.labels_eval

    def visualize(self):
        colors = list('bgrcmyk')
        if self.X.shape[1] > 2 or self.k > len(colors):
            print("Can't visualize data with more than 2 dimensions or classifier with more than %d means."%len(colors))
        else:
            for i in range(self.k):
                XL = self.X[self.labels_eval[-1] == i, :]
                c = self.centroids_eval[-1][i]
                plt.plot(XL[:, 0], XL[:, 1], colors[i]+'.', markersize=5, alpha=0.5)
                plt.plot(c[0], c[1], colors[i]+'+', markersize=15)
            plt.title('K-means Clustering Visualization - iters=%d'%self.iter)
            plt.axis('equal')
            plt.show()

def generateRandomData(samples = 100, dim = 2, clusters = 0, low=0.0, high=1.0):
    if clusters <= 0:
        return np.random.uniform(low=low, high=high, size=(samples, dim))
    
    means = generateRandomData(samples=clusters)
    cov = [[high,low], [low,high]]
    return np.concatenate([
        np.random.multivariate_normal(means[i], cov, int(samples/clusters)) 
        for i in range(clusters)
    ])


if __name__ == "__main__":
    k = 4
    c = 10
    s = 600

    clf = KMCClassifier(k)
    clf.fit(generateRandomData(samples = s, clusters=c))
    clf.evaluate()
    clf.visualize()