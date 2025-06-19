import math
import sys


class Vector:
    def __init__(self, data):
        self.data = data
        self.length = len(data)

    def __add__(self, other):
        new_vector = []
        new_length = min(self.length, other.length)
        for i in range(new_length):
            new_vector.append(self.data[i] + other.data[i])
        return Vector(new_vector)

    def __repr__(self):
        helper = ["%.4f" % elem for elem in self.data]
        return ','.join(map(str, helper))

    # Function to calculate the distance between vectors, assuming equal length
    def distance(self, other):
        vec_sum = 0
        for i in range(self.length):
            vec_sum += (self.data[i] - other.data[i]) ** 2
        return math.sqrt(vec_sum)

    # Function to find the closest centroid, assuming equal length - returns index
    def find_closest_centroid(self, centroids):
        min_centroid = float('inf')
        min_index = -1
        for i in range(len(centroids)):
            curr_d = self.distance(centroids[i])
            if curr_d < min_centroid:
                min_centroid = curr_d
                min_index = i
        return min_index


# Assert correct values for k, iter
def assert_input(k, iter, N):
    ok = True
    if not ((1 < k < N) and (k % 1 == 0)):
        print("Invalid number of clusters!")
        ok = False
        return ok
    if not ((1 < iter < 1000) and (iter % 1 == 0)):
        print("Invalid maximum iteration!")
        ok = False
    return ok


def compute_centroid_from_cluster(cluster, k):
    new_centroid = Vector([0 for i in range(cluster[0].length)])
    for vector in cluster:
        new_centroid = new_centroid + vector
    for i in range(new_centroid.length):
        new_centroid.data[i] /= len(cluster)
    return new_centroid


def update_centroid_and_convergence(clusters, centroids, k):
    convergence = True
    for i in range(k):
        if len(clusters[i]) != 0:
            new_centroid = compute_centroid_from_cluster(clusters[i], k)
        else:
            new_centroid = Vector([float(0) for i in range(centroids[0].length)])
        if centroids[i].distance(new_centroid) >= 0.001:
            convergence = False
        centroids[i] = new_centroid
    return convergence


my_file = None


def main():
    try:
        # Get data from console
        input_data = sys.argv
        if len(input_data) < 4:
            k, iter, filename = float(input_data[1]), 200, input_data[2]
        else:
            k, iter, filename = float(input_data[1]), float(input_data[2]), input_data[3]

        # Read the data from the file and add all the vectors to a list
        vectors = []
        my_file = open(filename, "r")
        for line in my_file:
            vectors.append(Vector([float(x) for x in line.replace("\n", "").split(",")]))

        # Assert correct values for k, iter
        if not assert_input(k, iter, len(vectors)):
            return
        else:
            k = int(k)
            iter = int(iter)

        # Initialize the centroids, convergence and the clusters
        centroids = vectors[:k]
        clusters = [[] for i in range(k)]

        for i in range(iter):

            # Clear clusters
            clusters = [[] for i in range(k)]

            # Assign vectors into clusters
            for vec in vectors:
                j = vec.find_closest_centroid(centroids)
                clusters[j].append(vec)

            # Calculate new centroids from cluster and check convergence
            if update_centroid_and_convergence(clusters, centroids, k):
                break

        # Print centroids to screen
        print("\n".join(str(cent) for cent in centroids))

    except:
        print("An Error Has Ocurred")
    finally:
        my_file.close()


if __name__ == "__main__":
    main()