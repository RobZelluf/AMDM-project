from sklearn.cluster import SpectralClustering
from utils import *

start = datetime.datetime.now()
graph = read_file('roadNet-CA.txt')

num_partitions = 50

# Spectral Clustering
sc = SpectralClustering(num_partitions, affinity='precomputed', n_init=100)
sc.fit(graph.adjacency_matrix)
sc_labels = sc.labels_
for i in range(num_partitions):
    print("Num", i, " - ", len([x for x in sc_labels if x == i]))
score = score_partitioning(graph, sc_labels)
print(score)
end = datetime.datetime.now()
print("Spectral clustering done in", (end-start).total_seconds())

write_file("CA-GrQc", graph, sc_labels)