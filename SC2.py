from utils import *
from sklearn.cluster import KMeans
from scipy.sparse.linalg import eigsh
import numpy as np
import os

# Input prompt for filename
DIRs = [x for x in os.listdir("data/")]
i = 0
for DIR in DIRs:
    print(i, DIR)
    i += 1

data = int(input("Model number:"))
output_name = input("Output name:")

filename = DIRs[data]
graph, num_partitions = read_file(filename)
print("Number of partitions:", num_partitions)
##########

laplacian = graph.laplacian

print("Calculating eigenvalues and eigenvectors..")
vals, vecs = eigsh(laplacian, num_partitions * 2, which="SM")

vecs = vecs[:, np.argsort(vals)]
vals = vals[np.argsort(vals)]

count = 0
best_score = 999
while True:
    count += 1
    # kmeans on first three vectors with nonzero eigenvalues
    kmeans = KMeans(n_clusters=num_partitions)
    kmeans.fit(vecs[:, 1:])

    labels = kmeans.labels_
    score = score_partitioning(graph, labels)

    if score < best_score:
        best_score = score
        print(count, "- New best score:", best_score)
        write_file(output_name, graph, labels, num_partitions)