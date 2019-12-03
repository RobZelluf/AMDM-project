from utils import *
from sklearn.cluster import KMeans
from scipy.sparse.linalg import eigsh
import numpy as np
import os
import pickle as p

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
max_num_eigenvectors = int(input("Maximum number of eigenvectors"))
k_means_iterations = 500
##########

laplacian = graph.laplacian
best_score = 999

print("Calculating", max_num_eigenvectors, "eigenvalues and eigenvectors...")
vals, vecs = eigsh(laplacian, max_num_eigenvectors, which="SM")

vecs = vecs[:, np.argsort(vals)]
vals = vals[np.argsort(vals)]

with open("EV/" + filename[:-4] + ".p", "wb") as f:
    p.dump([vecs, vals], f)


for num_eigenvectors in range(num_partitions, max_num_eigenvectors, int((max_num_eigenvectors - num_partitions) / 10)):
    print("Running k-means", k_means_iterations, "times for", num_eigenvectors, "eigenvectors.")
    count = 0
    for it in range(k_means_iterations):
        count += 1
        # kmeans on first three vectors with nonzero eigenvalues
        kmeans = KMeans(n_clusters=num_partitions)
        kmeans.fit(vecs[:, 1:num_eigenvectors + 1])

        labels = kmeans.labels_
        score = score_partitioning(graph, labels)

        if score < best_score:
            best_score = score
            print(count, "- New best score:", best_score)
            write_file(output_name, filename, graph, labels, num_partitions)