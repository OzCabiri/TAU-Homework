import math
import sys
import pandas as pd
import numpy as np
import mykmeanssp as kmc
np.random.seed(1234)

def is_k_iter_eps_numbers(k, iter, eps):
    try:
        float(k)
    except ValueError:
        print("Invalid number of clusters!")
        exit(1)
        
    try:
        float(iter)
    except ValueError:
        print("Invalid maximum iteration!")
        exit(1)
        
    try:
        float(eps)
    except ValueError:
        print("Invalid epsilon!")
        exit(1)

# Assert correct values for k, iter, epsilon
def assert_inputs(k, iter, eps, N):
    ok = True
    if not ((1 < k < N)  and (k % 1 == 0)):
        print("Invalid number of clusters!")
        return not ok
    if not ((1 <= iter <= 1000) and (iter % 1 == 0)):
        print("Invalid maximum iteration!")
        return not ok
    if not (0 <= eps):
        print("Invalid epsilon!")
        return not ok
    return ok

"""
This function calculates the distance of each point to the nearest centroid
Return value will be a list where in the i index will
store the distance of the i-th point to the nearest centroid
"""
def find_min_distance_from_centroids(vectors, centroids, N):
    distances = [-1 for i in range(N)]
    for i in range(len(vectors)):
        min_distance = math.inf
        for centroid in centroids:
            distance = np.linalg.norm(np.array(centroid) - np.array(vectors.iloc[i]))
            if distance < min_distance:
                min_distance = distance
        distances[vectors.iloc[i].name] = min_distance
    return distances

def kmeans_pp(vectors, k, N, iter, eps):

    # Init list to save all indexes of vectors in vectors that are already chosen
    ignore = []

    # Choose the first centroid uniformly at random from the data points
    centroids = [vectors.iloc[np.random.choice(N)]]

    # add the index of the first centroid to the chosen list
    ignore.append(centroids[0].name)

    # Filter out rows where the original index is in the ignore list
    vectors = vectors[~vectors.index.isin(ignore)]

    # Choose the next k - 1 centroids
    for _ in range(k - 1):

        # Calculate the distance of each point to the nearest centroid
        distances = find_min_distance_from_centroids(vectors, centroids, N)
        
        # Save sum of distances excluding -1 values
        sum_distances = sum(filter(lambda x: x != -1, distances))

        # Calculate the probability of each point to be chosen as the next centroid for all N data points
        # Notice some data points are already non existential (distance = -1)
        probabilities_all = [distance / sum_distances for distance in distances]

        # Calculate the probability of each point to be chosen as the next centroid for the real data points
        probabilities_real = [0 for i in range(len(vectors))]

        # Set negative probabilities to 0 (this vectors are already chosen)
        for i in range(len(vectors)):
            curr_vec_name = vectors.iloc[i].name
            probabilities_real[i] = probabilities_all[curr_vec_name]

        # Choose the next centroid with probability proportional to the distance
        next_centroid = vectors.iloc[np.random.choice(len(vectors), p=probabilities_real)]

        # Add the next centroid to the list of centroids
        centroids.append(next_centroid)

        # add the index of the next centroid to the chosen list
        ignore.append(next_centroid.name)

        # Filter out rows where the original index is in the ignore list
        vectors = vectors[~vectors.index.isin(ignore)]

    return [centroids,ignore]


def main():

    try:
        # Get data from console
        input_data = sys.argv
        if len(input_data) < 6:
            is_k_iter_eps_numbers(input_data[1],300,input_data[2]) # Check if k, iter, eps are numbers
            k, iter, eps, file_name1, file_name2 = float(input_data[1]), 300, float(input_data[2]), input_data[3], input_data[4]
        else:
            is_k_iter_eps_numbers(input_data[1],input_data[2],input_data[3]) # Check if k, iter, eps are numbers
            k, iter, eps, file_name1, file_name2 = float(input_data[1]), float(input_data[2]), float(input_data[3]), input_data[4], input_data[5]

        # Combine both input files into one dataframe using inner-join with the first column as key
        df1 = pd.read_csv(file_name1, header=None)
        df2 = pd.read_csv(file_name2, header=None)
        vectors = pd.merge(df1, df2, on=0, how='inner')

        # Sort result by the first column
        vectors = vectors.sort_values(by=[0])

        # Save dictionary that maps index to first column value
        name_to_cloumn_zero = {}
        for i in range(len(vectors)):
            name_to_cloumn_zero[vectors.iloc[i].name] = vectors.iloc[i][0]

        # Delete the first column
        vectors = vectors.drop(columns=[0])

        N = int(len(vectors))

        # Assert inputs
        if not assert_inputs(k, iter, eps, N):
            exit(1)

        # Parse k, iter to int
        k = int(k)
        iter = int(iter)
        
        # Choose k centroids using kmeans++
        centroids,ignore = kmeans_pp(vectors, k, N, iter, eps)

        choesn_vectors = []
        for i in range(len(ignore)):
            choesn_vectors.append(int(name_to_cloumn_zero[ignore[i]]))

        # Save number of vector columns
        vecdim = len(vectors.columns)

        # Convert vectors to python list of lists
        vectors = vectors.values.tolist()

        # Convert centroids to python list of lists with only the values
        # Init a python list of lists sized k x vecdim
        centroids_as_pylist = [[0 for i in range(vecdim)] for j in range(k)]
        for i in range(k):
            for j in range(vecdim):
                centroids_as_pylist[i][j] = centroids[i].iloc[j]

        # Run kmeans algorithm
        final_centroids = kmc.fit(k,N,vecdim,iter,eps,vectors,centroids_as_pylist)

        # Print the chosen vectors
        print(','.join(str(x) for x in choesn_vectors))
        # print final centroids until 4 decimal points
        for centroid in final_centroids:
            print(','.join(format(x, ".4f") for x in centroid))

    except Exception:
        print("An Error Has Occurred")

if __name__ == "__main__":
    main()
