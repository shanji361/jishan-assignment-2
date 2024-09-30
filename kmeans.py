import numpy as np
import random



class KMeans:
    def __init__(self, n_clusters=3, max_iter=100, init_method="random"):
        self.n_clusters = int(n_clusters)
        self.max_iter = max_iter
        self.init_method = init_method
        self.centroids = None


    def fit(self, X, initial_centroids=None):
        if self.init_method == "random":
            self.centroids = self.initialize_random(X)
        elif self.init_method == "farthest_first":
            self.centroids = self.initialize_farthest_first(X)
        elif self.init_method == "kmeans++":
            self.centroids = self.initialize_kmeans_plus(X)
        elif self.init_method == "manual" and initial_centroids is not None:
            self.centroids = initial_centroids
        else:
            raise ValueError("Unknown initialization method")


        print(f"Initial centroids using {self.init_method}: {self.centroids}")

        if self.centroids is None or len(self.centroids) == 0:
            raise ValueError("Centroids have not been initialized correctly.")

        for _ in range(self.max_iter):
            self.labels = self.assign_clusters(X)
            new_centroids = self.update_centroids(X)
            if np.all(new_centroids == self.centroids):
                break
            self.centroids = new_centroids
        return self.centroids, self.labels


    def initialize_random(self, X):
        return X[random.sample(range(X.shape[0]), self.n_clusters)]


    def initialize_farthest_first(self, X):
        centroids = [X[random.randint(0, X.shape[0] - 1)]]
        for _ in range(1, self.n_clusters):
            distances = np.min(np.linalg.norm(X[:, np.newaxis] - centroids, axis=2), axis=1)
            next_centroid = X[np.argmax(distances)]
            centroids.append(next_centroid)
        return np.array(centroids)


    def initialize_kmeans_plus(self, X):
        centroids = [X[random.randint(0, X.shape[0] - 1)]]
        for _ in range(1, self.n_clusters):
            distances = np.min(np.linalg.norm(X[:, np.newaxis] - centroids, axis=2), axis=1)
            probabilities = distances / distances.sum()
            next_centroid = X[np.random.choice(range(X.shape[0]), p=probabilities)]
            centroids.append(next_centroid)
        return np.array(centroids)


    def assign_clusters(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)


    def update_centroids(self, X):
        centroids = []
        for i in range(self.n_clusters):
            if len(X[self.labels == i]) > 0:
                centroids.append(X[self.labels == i].mean(axis=0))
            else:
                centroids.append(self.centroids[i])  
        return np.array(centroids)