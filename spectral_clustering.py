from sklearn.cluster import SpectralClustering
from utils import *

graph = read_file('roadNet-CA.txt')

# Spectral Clustering
sc = SpectralClustering(2, affinity='precomputed', n_init=100)
sc.fit(graph.adjacency_matrix)
sc_labels = sc.labels_
for i in range(5):
    print("Num", i, " - ", len([x for x in sc_labels if x == i]))
score = score_partitioning(graph, sc_labels)
print(score)

write_file("CA-GrQc", graph, sc_labels)