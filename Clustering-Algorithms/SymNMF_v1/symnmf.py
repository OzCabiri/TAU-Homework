import math
import sys
import pandas as pd
import numpy as np
import mysymnmfsp as SymNMF

np.random.seed(1234)

"""
Initialize the matrix H (decomposition matrix) for Symmetric Non-negative Matrix Factorization (SymNMF).

This function initializes the matrix H with random values from the interval [0, 2*sqrt(m/k)],
where m is the mean of the entries in the input matrix w_mat and k is the number of centroids.

Parameters:
w_mat (list): A list of list of float representing the normalized similarity matrix.
N (int): The number of vectors (rows in the matrix H).
k (int): The number of centroids (columns in the matrix H).

Returns:
list: A list of list of float of shape (N, k) representing a matrix initialized with random values.
"""
def initializeH(w_mat, N, k):
    m = np.mean(w_mat) # Calculate the average of all entries in w_mat
    upper_bound = 2 * np.sqrt(m / k) # Calculate the upper bound for the random values
    H = np.random.uniform(low=0, high=upper_bound, size=(N, k)) # Initialize H with random values from the interval [0, upper_bound]
    return H.tolist()

"""
Perform Symmetric Non-negative Matrix Factorization (SymNMF) on the given vectors.

This function normalizes the input vectors to calculate the W matrix (normalized similarity matrix),
initializes the H matrix (decomposition matrix),
and then performs SymNMF to calculate the resulting matrix.

Parameters:
vectors (list of list of float): A list of lists representing the input vectors.
k (int): The number of clusters to form.

Returns:
list: A list of list of float representing the resulting matrix after performing SymNMF.
"""
def doSymnmf(vectors, k):
    w_mat = SymNMF.norm(vectors) # Calling norm function in C to calculate W matrix
    h_mat = initializeH(w_mat, len(vectors), k) # Initialize H matrix
    matrix_goal = SymNMF.symnmf(w_mat, h_mat, k) # Calling symnmf function in C to calculate the matrix
    return matrix_goal

def main():
    try:
        # Get data from console
        input_data = sys.argv
        k, goal, input_file = int(input_data[1]), input_data[2], input_data[3]

        # Create Vectors dataframe from csv file
        vectors = pd.read_csv(input_file, header=None)
        # Convert vectors to python list of lists
        vectors = vectors.values.tolist()
        
        matrix_goal = None # The matrix to calculate and return

        # Choose which matrix to calculate and return
        if goal == "sym":
            matrix_goal = SymNMF.sym(vectors) # Calling sym function in C to calculate the matrix
        elif goal == "ddg":
            matrix_goal = SymNMF.ddg(vectors) # Calling ddg function in C to calculate the matrix
        elif goal == "norm":
            matrix_goal = SymNMF.norm(vectors) # Calling norm function in C to calculate the matrix  
        elif goal == "symnmf":
            matrix_goal = doSymnmf(vectors, k)
        else:
            print("An Error Has Occurred")
            return

        # print matrix_goal until 4 decimal points
        for row in matrix_goal:
            print(','.join(format(x, ".4f") for x in row))

    except Exception:
        print("An Error Has Occurred")


if __name__ == "__main__":
    main()
