import math
import sys
import pandas as pd
import numpy as np
import kmeans as kmeans
import symnmf as symnmf
from sklearn.metrics import silhouette_score

"""
Find the closest centroid to a given vector.

This function calculates the Euclidean distance between the given vector and each centroid,
and returns the index of the closest centroid.

Parameters:
vector (np.ndarray): A numpy array representing the vector.
centroids (list of lists): A list of centroids where each centroid is a list.

Returns:
int: The index of the closest centroid.
"""
def findClosestCentroid(vector, centroids): 
    min_distance = math.inf
    cluster_index = 0

    for j in range(len(centroids)):
        distance = np.linalg.norm(vector - centroids[j])
        if distance < min_distance:
            min_distance = distance
            cluster_index = j

    return cluster_index

"""
Calculate K-means labels for the given vectors.

This function converts the input vectors to a numpy array, performs K-means clustering,
and assigns each vector to the closest centroid. It returns the labels indicating the
cluster assignment for each vector.

Parameters:
vectors (pd.DataFrame): A pandas DataFrame containing the input vectors.
k (int): The number of clusters to form.

Returns:
list: A list of integers where each integer represents the cluster label for the corresponding vector.
"""
def calculateKmeansLabels(vectors, k): 
    vectors = vectors.to_numpy()  # kmeans requires numpy array
    kmeansMatrix = kmeans.doKmeans(vectors, k)
    kmeansLabels = [-1 for i in range(len(vectors))]

    for i in range(len(vectors)):
        clusterIndex = findClosestCentroid(vectors[i], kmeansMatrix)
        kmeansLabels[i] = clusterIndex

    return kmeansLabels

"""
Calculate SymNMF labels for the given vectors.

This function converts the input vectors to a list of lists, performs Symmetric Non-negative Matrix Factorization (SymNMF),
and returns the cluster assignments.

Parameters:
vectors (pd.DataFrame): A pandas DataFrame containing the input vectors.
k (int): The number of clusters to form.

Returns:
list: A list representing the cluster assignment for each vector.
"""
def calculateSymnmfLabels(vectors, k):
    vectors = vectors.values.tolist() # Convert data to list of lists
    symnmfMatrix = symnmf.doSymnmf(vectors, k)

    return np.array(symnmfMatrix).argmax(axis=1)

def main():
    try:
        # Get data from console
        input_data = sys.argv
        k, input_file = int(input_data[1]), input_data[2]

        # Create Vectors dataframe from csv file
        vectors = pd.read_csv(input_file, header=None)

        # Calculate kmeans sillohuette score
        kmeansLables = calculateKmeansLabels(vectors, k)
        scoreKmeans = silhouette_score(vectors, kmeansLables)

        # Calculate symnmf sillohuette score
        symnmfLabels = calculateSymnmfLabels(vectors, k)
        scoreSymnmf = silhouette_score(vectors, symnmfLabels)

        print("nmf: " + format(scoreSymnmf, ".4f"))
        print("kmeans: " + format(scoreKmeans, ".4f"))

    except Exception:
        print("An Error Has Occurred")


if __name__ == "__main__":
    main()