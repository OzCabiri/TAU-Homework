import math
import pandas as pd
import numpy as np

"""
assigns each vector to the closest centroid,
and returns a list of lists where each list contains
the vectors assigned to the corresponding centroid
@param vectors: list of vectors
@type vectors: list of lists
@param centroids: list of centroids
@type centroids: list of lists
@return: cluster assignment (list of lists of vectors)
@rtype: list of lists (size: k*d)
"""
def assignClusters(vectors, centroids):
    clusters = [[] for i in range(len(centroids))] # Initialize clusters as a list of lists
    
    for vector in vectors:
        min_distance = math.inf
        cluster_index = 0
        for j in range(len(centroids)):
            distance = np.linalg.norm(vector - centroids[j])
            if distance < min_distance:
                min_distance = distance
                cluster_index = j
        clusters[cluster_index].append(vector)

    return clusters

"""
updates the centroids by taking the mean of the vectors in each cluster
@param centroids: list of centroids
@type centroids: list of lists
@param clusters: list of lists where each list contains the vectors assigned to the corresponding centroid
@return: updated centroids
@rtype: list of lists
"""
def updateCentroids(centroids, clusters):
    for i in range(len(centroids)):
        if clusters[i]: # Avoid division by zero
            centroids[i] = np.mean(clusters[i], axis=0)

    return centroids

"""
checks if the centroids have converged
@param centroids: list of centroids
@type centroids: list of lists
@param clusters: list of lists where each list contains the vectors assigned to the corresponding centroid
@type clusters: list of lists
@return: True if the centroids have converged, False otherwise
"""
def updateCentroidAndConvergence(centroids, clusters):
    convergence = True
    for i in range(len(centroids)):
        if clusters[i]:
            new_centroid = np.mean(clusters[i], axis=0)
        else:
            new_centroid = np.zeros(len(centroids[0]))

        if np.linalg.norm(new_centroid - centroids[i]) >= 0.0001:
            convergence = False
        centroids[i] = new_centroid
    return convergence

"""
performs k-means clustering on the given vectors
@param vectors: list of vectors
@type vectors: list of lists
@param k: number of clusters
@type k: int
@return: list of centroids
"""
def doKmeans(vectors, k):
    centroids = vectors[:k].copy() # Choose first k vectors as initial centroids

    for i in range(300):
        # Assign each vector to the closest centroid
        clusters = assignClusters(vectors, centroids)

        # Update centroids
        if updateCentroidAndConvergence(centroids, clusters):
            break

    return centroids.tolist()
