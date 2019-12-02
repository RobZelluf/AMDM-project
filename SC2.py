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

filename = DIRs[data]
graph, num_partitions = read_file(filename)
print("Number of partitions:", num_partitions)
##########

laplacian = graph.laplacian
vals, vecs = eigsh(laplacian, graph.num_vertices / 2, which="SM")

vecs = vecs[:, np.argsort(vals)]
vals = vals[np.argsort(vals)]

# kmeans on first three vectors with nonzero eigenvalues
kmeans = KMeans(n_clusters=num_partitions)
kmeans.fit(vecs[:, 1:10])

labels = kmeans.labels_
for i in range(num_partitions):
    print("Num", i, " - ", len([x for x in labels if x == i]))

score = score_partitioning(graph, labels)
print("Score:", score)