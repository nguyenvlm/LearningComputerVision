import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


class KMCClassifier:
    def __init__(self, k):
        np.random.seed(1998)
        self.k = k

    def fit(self, X):
        self.X = X
        self.centroids = X[np.random.choice(
            self.X.shape[0], self.k, replace=False)]
        # print(self.centroids)
        self.assign_labels()
        # print(self.labels)

    def assign_labels(self):
        self.labels = np.argmin(cdist(self.X, self.centroids), axis=1)

    def evaluate(self):
        prev_loss = np.inf
        loss = np.inf
        while loss <= prev_loss*1.1:
            for x in self.X:
                np.min(np.linalg.norm(x-centroids[i])
                       for i in centroids.shape[0])

    def loss(self):
        return (np.linalg.norm(self.X[self.labels == self.centroids[i]] - self.centroids[i])
                for i in range(self.k))

    def visualize(self):
        colors = list('bgrcmykw')
        if self.X.shape[1] > 2 or self.k > len(colors):
            print("Can't visualize data with more than 2 dimensions.")
        else:
            for i in range(self.k):
                XL = X[self.labels == i, :]
                plt.plot(XL[:, 0], XL[:, 1], colors[i] +
                         'x', markersize=4, alpha=.8)
            plt.axis('equal')
            plt.plot()
            plt.show()


if __name__ == "__main__":
    clf = KMCClassifier(3)
    X = np.random.uniform(low=0.0, high=10.0, size=(100, 2))
    clf.fit(X)
    clf.visualize()
