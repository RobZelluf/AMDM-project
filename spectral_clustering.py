from sklearn.cluster import SpectralClustering
from utils import *

graph, num_partitions = read_file()

# Spectral Clustering
sc = SpectralClustering(num_partitions, affinity='precomputed', n_init=100)
sc.fit(graph.laplacian)
sc_labels = sc.labels_
for i in range(num_partitions):
    print("Num", i, " - ", len([x for x in sc_labels if x == i]))
score = score_partitioning(graph, sc_labels)
print(score)