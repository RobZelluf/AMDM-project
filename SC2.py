from utils import *
from sklearn.cluster import KMeans
import numpy as np

filename = "Oregon-1.txt"
graph, num_partitions = read_file(filename)
laplacian = graph.laplacian


min_score = 1

while min_score > 0.61:
    vals, vecs = np.linalg.eigh(graph.laplacian)
    vecs = vecs[:, np.argsort(vals)]
    vals = vals[np.argsort(vals)]
    # kmeans on first three vectors with nonzero eigenvalues
    kmeans = KMeans(n_clusters=num_partitions)
    kmeans.fit(vecs[:, 1:10])
    labels = kmeans.labels_
    for i in range(num_partitions):
        print("Num", i, " - ", len([x for x in labels if x == i]))

    score = score_partitioning(graph, labels)

    if score < min_score:
        min_score = score
        final_partitioning = labels.copy()

    print("Score:", score)
    print("Min Score: ", min_score)
    #
    # partitioning = reassign_partitions(graph, labels, num_partitions, score)
    # print("Score after reassignment: ", score_partitioning(graph, partitioning))

write_file(filename, graph, final_partitioning, num_partitions)
